import re
import threading
from modules.speech import speak, listen
from modules.logger import setup_logger

logger = setup_logger("Reminder")


def parse_duration(query: str) -> int:
    """
    Extract duration in seconds from natural text.
    Examples: 'in 10 seconds', 'for 2 minutes', 'in 1 hour', '30 seconds'
    """
    if not query:
        return 0

    total_seconds = 0

    hours = re.search(r"(\d+)\s*(hours|hour|hrs|hr)\b", query, re.IGNORECASE)
    if hours:
        total_seconds += int(hours.group(1)) * 3600

    minutes = re.search(r"(\d+)\s*(minutes|minute|mins|min)\b", query, re.IGNORECASE)
    if minutes:
        total_seconds += int(minutes.group(1)) * 60

    seconds = re.search(r"(\d+)\s*(seconds|second|secs|sec)\b", query, re.IGNORECASE)
    if seconds:
        total_seconds += int(seconds.group(1))

    return total_seconds


def parse_reminder_text(query: str) -> str:
    """Extract task description from query."""
    if not query:
        return "check your task"

    clean = query.lower()
    time_pattern = r"\b(in|for)?\s*\d+\s*(seconds|second|secs|sec|minutes|minute|mins|min|hours|hour|hrs|hr)\b"
    clean = re.sub(time_pattern, "", clean)

    prefixes = [
        "remind me to ",
        "remind me ",
        "set a reminder to ",
        "set a reminder for ",
        "set reminder to ",
        "set reminder ",
        "timer to ",
        "alarm to "
    ]
    for prefix in prefixes:
        clean = clean.replace(prefix, "")

    clean = clean.strip()
    if clean.startswith("to "):
        clean = clean[3:].strip()

    return clean if clean else "check your task"


def _trigger_alert(task: str) -> None:
    """Audible alert triggered when timer expires."""
    logger.info(f"Reminder Alert triggered: {task}")
    speak(f"Reminder Alert! It is time to {task}.")


def set_reminder(query: str = "") -> None:
    """Schedules a non-blocking background reminder thread."""
    seconds = parse_duration(query)
    task = parse_reminder_text(query)

    if seconds <= 0:
        speak("What should I remind you about?")
        task_input = listen()
        if task_input:
            task = task_input

        speak("In how many seconds or minutes should I set the reminder?")
        time_input = listen()
        seconds = parse_duration(time_input)

    if seconds <= 0:
        speak("Sorry, I could not understand the duration for the reminder.")
        return

    logger.info(f"Setting reminder '{task}' for {seconds} seconds.")

    timer = threading.Timer(seconds, _trigger_alert, args=[task])
    timer.daemon = True
    timer.start()

    speak(f"Reminder set for {task} in {seconds} seconds.")
