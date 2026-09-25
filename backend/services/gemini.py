import os
import google.genai

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable is required")

client = google.genai.Client(api_key=api_key)

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

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    return response.text
