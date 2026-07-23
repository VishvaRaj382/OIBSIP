import webbrowser
from urllib.parse import quote_plus
from typing import Optional
from modules.speech import speak, listen
from modules.logger import setup_logger

logger = setup_logger("Browser")


def youtube() -> None:
    """Opens YouTube in the default browser."""
    speak("Opening YouTube")
    logger.info("Opening YouTube")
    webbrowser.open("https://youtube.com")


def gmail() -> None:
    """Opens Gmail in the default browser."""
    speak("Opening Gmail")
    logger.info("Opening Gmail")
    webbrowser.open("https://mail.google.com")


def google_search(search_query: Optional[str] = None) -> None:
    """Performs a Google Search in default browser."""
    if not search_query:
        speak("What should I search on Google?")
        search_query = listen()
        if not search_query:
            speak("No search query provided. Action cancelled.")
            return

    encoded_query = quote_plus(search_query.strip())
    search_url = f"https://www.google.com/search?q={encoded_query}"

    logger.info(f"Opening Google Search for: '{search_query}'")
    speak(f"Searching Google for {search_query}")
    webbrowser.open(search_url)