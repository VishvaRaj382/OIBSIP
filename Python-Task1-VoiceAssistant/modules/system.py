import datetime
import requests
from modules.speech import speak
from modules.logger import setup_logger

logger = setup_logger("System")


def tell_date() -> None:
    """Announces today's date."""
    today = datetime.datetime.now().strftime("%d/%m/%Y")
    logger.info(f"Date requested: {today}")
    speak(f"Today's date is {today}")


def tell_time() -> None:
    """Announces current local time."""
    current = datetime.datetime.now().strftime("%I:%M %p")
    logger.info(f"Time requested: {current}")
    speak(f"The time is {current}")


def ip() -> None:
    """Fetches public IP address using ipify service."""
    try:
        response = requests.get("https://api.ipify.org", timeout=5)
        if response.status_code == 200:
            address = response.text.strip()
            logger.info(f"Public IP: {address}")
            speak(f"Your IP address is {address}")
        else:
            speak("Unable to fetch IP address.")
    except requests.RequestException as req_err:
        logger.error(f"IP fetch error: {req_err}")
        speak("Unable to fetch IP address due to connection failure.")
    except Exception as e:
        logger.error(f"System IP error: {e}")
        speak("Unable to fetch IP address.")