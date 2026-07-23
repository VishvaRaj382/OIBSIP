import random
from modules.speech import speak
from modules.logger import setup_logger

logger = setup_logger("Identity")


def tell_who_am_i() -> None:
    """Responds to 'who are you', identity, and creator queries."""
    responses = [
        "I am Jarvis, your intelligent AI voice assistant built to help you automate tasks, check weather, set reminders, answer questions, and manage your workflow.",
        "I am Jarvis, an advanced AI desktop assistant designed to make your daily tasks effortless and efficient."
    ]
    response = random.choice(responses)
    logger.info("Answered identity query.")
    speak(response)


def tell_what_can_do() -> None:
    """Responds to 'what can you do' and capability queries."""
    capabilities = (
        "I can check weather forecasts, set background reminders, open applications and websites, "
        "send emails, answer questions using Gemini AI, search Wikipedia, and execute your custom commands!"
    )
    logger.info("Answered capabilities query.")
    speak(capabilities)


def respond_how_are_you() -> None:
    """Responds to 'how are you' queries."""
    responses = [
        "I am doing fantastic, thank you! How can I assist you today?",
        "I'm operating at peak efficiency! How are you doing?",
        "I am doing great! Ready to help you with anything you need."
    ]
    response = random.choice(responses)
    logger.info("Answered 'how are you' query.")
    speak(response)


def respond_thank_you() -> None:
    """Responds to thank you / gratitude queries."""
    responses = [
        "You're very welcome! Let me know if you need anything else.",
        "Happy to help, sir!",
        "My pleasure! Always here to assist you."
    ]
    response = random.choice(responses)
    logger.info("Answered thank you query.")
    speak(response)
