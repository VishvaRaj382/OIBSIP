import pyjokes
from modules.speech import speak
from modules.logger import setup_logger

logger = setup_logger("Jokes")


def tell() -> None:
    """Fetches a random joke and speaks it."""
    try:
        joke = pyjokes.get_joke()
        logger.info(f"Telling joke: {joke}")
        speak(joke)
    except Exception as e:
        logger.error(f"Error fetching joke: {e}")
        speak("Why did the computer go to the doctor? Because it had a virus!")