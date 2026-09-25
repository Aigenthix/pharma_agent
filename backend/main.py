import json
import os
import logging
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from .services.gemini import query_gemini

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="PharmaAssist AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load medicines database (test or real)
def load_medicines():
    try:
        db_path = "data/medicines_test.json" if os.path.exists("data/medicines_test.json") else "data/medicines.json"
        with open(db_path) as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"Database file not found: {db_path}")
        return []
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in database: {e}")
        return []

medicines_db = load_medicines()

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=500)

@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    logger.error(f"Validation error: {exc}")
    return HTTPException(status_code=400, detail=str(exc))

@app.get("/health")
def health_check():
    return {"status": "ok", "database": "connected" if medicines_db else "empty"}

@app.get("/api/medicines")
def get_medicines():
    try:
        return medicines_db
    except Exception as e:
        logger.error(f"Error fetching medicines: {e}")
        raise HTTPException(status_code=500, detail="Error fetching medicines")

@app.get("/api/medicines/search")
def search_medicines(q: str = None):
    try:
        if not q:
            raise HTTPException(status_code=400, detail="Search query 'q' is required")

        q_lower = q.lower()
        results = [
            med for med in medicines_db
            if q_lower in med["name"].lower()
            or q_lower in med.get("generic_name", "").lower()
            or q_lower in med.get("category", "").lower()
        ]
        return results
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error searching medicines: {e}")
        raise HTTPException(status_code=500, detail="Error searching medicines")

@app.post("/api/chat")
async def chat(request: ChatRequest):
    try:
        if not request.message or not request.message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")

        relevant_medicines = []
        msg_lower = request.message.lower()

        for med in medicines_db:
            if (msg_lower.find(med["name"].lower()) != -1 or
                msg_lower.find(med.get("generic_name", "").lower()) != -1):
                relevant_medicines.append(med)

        if not relevant_medicines:
            relevant_medicines = medicines_db[:3] if medicines_db else []

        sources = [med["name"] for med in relevant_medicines]
        product_data = json.dumps(relevant_medicines, indent=2)

        response = await query_gemini(request.message, product_data)

        return {
            "answer": response,
            "sources": sources
        }
    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"API key error: {e}")
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail="Error processing chat request")

# Serve frontend
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
async def root():
    try:
        return FileResponse("frontend/index.html")
    except FileNotFoundError:
        logger.error("Frontend index.html not found")
        raise HTTPException(status_code=404, detail="Frontend not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
