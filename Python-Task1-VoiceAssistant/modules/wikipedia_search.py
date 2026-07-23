import requests
from urllib.parse import quote_plus
from config import USER_AGENT
from modules.speech import speak
from modules.logger import setup_logger

logger = setup_logger("Wikipedia")

REMOVE_WORDS = [
    "wikipedia",
    "who is",
    "what is",
    "tell me about",
    "search",
    "please",
]


def search(query: str) -> None:
    """Searches Wikipedia API for summary of given query."""
    if not query:
        speak("Please tell me what you want to search.")
        return

    text = query.lower()
    for word in REMOVE_WORDS:
        text = text.replace(word, "")
    text = text.strip()

    if not text:
        speak("Please tell me what you want to search on Wikipedia.")
        return

    try:
        title = quote_plus(text)
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}"
        logger.info(f"Fetching Wikipedia summary for '{text}' via {url}")

        response = requests.get(
            url,
            headers={"User-Agent": USER_AGENT},
            timeout=8
        )

        if response.status_code != 200:
            speak("Sorry, I could not find anything on Wikipedia.")
            logger.info(f"Wikipedia API returned status code {response.status_code}")
            return

        data = response.json()
        summary = data.get("extract", "")
        title_str = data.get("title", "")
        page_type = data.get("type", "")

        if page_type == "disambiguation":
            speak(f"{title_str} has multiple meanings. Please be more specific.")
            return

        if not summary:
            speak("Sorry, I could not find a summary for that topic.")
            return

        logger.info(f"Wikipedia result found: {title_str}")
        speak(summary)

    except requests.RequestException as req_err:
        logger.error(f"Wikipedia connection failed: {req_err}")
        speak("Unable to connect to Wikipedia service.")
    except Exception as e:
        logger.error(f"Wikipedia processing error: {e}")
        speak("An error occurred while fetching Wikipedia information.")