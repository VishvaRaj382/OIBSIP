import datetime
from modules.speech import speak
from modules.logger import setup_logger

logger = setup_logger("Assistant")


def wish() -> None:
    """Welcomes the user with a time-appropriate greeting."""
    hour = datetime.datetime.now().hour

    if hour < 12:
        greeting = "Good Morning"
    elif hour < 18:
        greeting = "Good Afternoon"
    else:
        greeting = "Good Evening"

    logger.info(f"Initial greeting: {greeting}")
    speak(greeting)
    speak("I am Jarvis. How can I help you?")