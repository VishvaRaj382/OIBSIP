from modules.speech import speak
from modules.logger import setup_logger

logger = setup_logger("Greeting")


def greet(query: str) -> None:
    """Responds to user greetings based on query content."""
    query_clean = query.lower()

    if "good morning" in query_clean:
        response = "Good morning, sir."
    elif "good afternoon" in query_clean:
        response = "Good afternoon, sir."
    elif "good evening" in query_clean:
        response = "Good evening, sir."
    elif "hello" in query_clean:
        response = "Hello, sir."
    elif "hi" in query_clean:
        response = "Hi, sir."
    elif "hey" in query_clean:
        response = "Hey, sir."
    else:
        response = "Hello, sir."

    logger.info(f"Greeting response: '{response}'")
    speak(response)
