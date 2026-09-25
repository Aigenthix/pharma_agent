import json
import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from services.gemini import query_gemini

load_dotenv()

app = FastAPI(title="PharmaAssist AI")

# Load medicines database (test or real)
def load_medicines():
    import os
    db_path = "data/medicines_test.json" if os.path.exists("data/medicines_test.json") else "data/medicines.json"
    with open(db_path) as f:
        return json.load(f)

medicines_db = load_medicines()

class ChatRequest(BaseModel):
    message: str

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/api/medicines")
def get_medicines():
    return medicines_db

@app.get("/api/medicines/search")
def search_medicines(q: str):
    q_lower = q.lower()
    results = [
        med for med in medicines_db
        if q_lower in med["name"].lower()
        or q_lower in med.get("generic_name", "").lower()
        or q_lower in med.get("category", "").lower()
    ]
    return results

@app.post("/api/chat")
async def chat(request: ChatRequest):
    relevant_medicines = []
    for med in medicines_db:
        if (request.message.lower().find(med["name"].lower()) != -1 or
            request.message.lower().find(med.get("generic_name", "").lower()) != -1):
            relevant_medicines.append(med)

    if not relevant_medicines:
        relevant_medicines = medicines_db[:3]

    sources = [med["name"] for med in relevant_medicines]

    product_data = json.dumps(relevant_medicines, indent=2)

    response = await query_gemini(request.message, product_data)

    return {
        "answer": response,
        "sources": sources
    }

# Serve frontend
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
async def root():
    return FileResponse("frontend/index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
