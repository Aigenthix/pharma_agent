import os
import logging
import google.genai

logger = logging.getLogger(__name__)

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable is required")

try:
    client = google.genai.Client(api_key=api_key)
except Exception as e:
    logger.error(f"Failed to initialize Gemini client: {e}")
    raise ValueError(f"Invalid API key: {e}")

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
    try:
        prompt = f"""{SYSTEM_PROMPT}

Product information:
{product_data}

User question:
{user_question}"""

        response = client.models.generate_content(
            model="gemini-3.0-flash-lite",
            contents=prompt
        )

        if not response or not hasattr(response, 'text'):
            logger.error("Invalid response from Gemini API")
            return "Unable to process your question. Please try again."

        return response.text

    except Exception as e:
        logger.error(f"Gemini API error: {e}")
        if "401" in str(e) or "unauthorized" in str(e).lower():
            raise ValueError("Invalid API key")
        elif "429" in str(e):
            raise ValueError("Rate limit exceeded. Please try again later.")
        else:
            logger.warning(f"Returning fallback response due to: {e}")
            return f"I encountered an issue processing your request: {str(e)[:100]}. Please try again."
