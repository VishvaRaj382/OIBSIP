import re
import time
from typing import Optional
from google import genai
from config import GEMINI_API_KEY
from modules.speech import speak
from modules.logger import setup_logger

logger = setup_logger("GeminiQA")

MODEL: str = "gemini-3.6-flash"
_client: Optional[genai.Client] = None


def get_client() -> Optional[genai.Client]:
    """Lazy initializer for Gemini client to prevent crashes if key is missing at startup."""
    global _client
    if _client is None:
        if not GEMINI_API_KEY:
            logger.warning("GEMINI_API_KEY is not set in environment.")
            return None
        try:
            _client = genai.Client(api_key=GEMINI_API_KEY)
        except Exception as e:
            logger.error(f"Failed to initialize Gemini client: {e}")
            return None
    return _client


def clean_text(text: str) -> str:
    """Remove markdown and normalize whitespace for clean voice synthesis."""
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"#+", "", text)
    text = text.replace("*", "")
    text = re.sub(r"\n+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def shorten_answer(text: str, max_sentences: int = 2) -> str:
    """Keep only the first few sentences for voice responses."""
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return " ".join(sentences[:max_sentences]).strip()


def answer_question(question: str) -> str:
    """Queries Gemini model and synthesizes spoken answer."""
    client = get_client()
    if not client:
        error_msg = "Gemini AI is not configured with an API key."
        logger.error(error_msg)
        speak(error_msg)
        return error_msg

    try:
        start_time = time.time()

        prompt = f"""
You are Jarvis, an intelligent voice assistant.

Rules:
- Answer in 2 or 3 short sentences.
- Maximum 40 words.
- Be conversational.
- No headings, bullet points, or markdown.
- If the answer can be given in one sentence, do so.

Question:
{question}
"""
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )

        elapsed = time.time() - start_time
        logger.info(f"Gemini Response Time: {elapsed:.2f} seconds")

        raw_answer = response.text or "Sorry, I couldn't find an answer."
        cleaned_answer = clean_text(raw_answer)
        final_answer = shorten_answer(cleaned_answer)

        logger.info(f"Answer: {final_answer}")
        speak(final_answer)
        return final_answer

    except Exception as e:
        logger.error(f"QA Error: {e}")
        error_msg = "Sorry, I couldn't answer that question right now."
        speak(error_msg)
        return error_msg