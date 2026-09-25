import os
import google.genai as genai

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable is required")

genai.configure(api_key=api_key)

SYSTEM_PROMPT = """You are PharmaAssist AI.

You are a pharmaceutical product information assistant.

Answer questions using the provided product information.

Do not:
- diagnose diseases
- prescribe medicines
- recommend changing medication
- provide patient-specific medical advice
- invent product information

If information is not available in the provided data,
say that the information is not available.

Keep responses concise and helpful."""

async def query_gemini(user_question: str, product_data: str) -> str:
    prompt = f"""{SYSTEM_PROMPT}

Product information:
{product_data}

User question:
{user_question}"""

    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)
    return response.text
