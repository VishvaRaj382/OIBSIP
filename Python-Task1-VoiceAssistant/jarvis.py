#!/usr/bin/env python3
import sys
import signal
import argparse
from config import APP_NAME, APP_VERSION
from modules.logger import setup_logger
from modules.assistant import wish
from modules.speech import listen, speak, set_text_mode
from modules.wikipedia_search import search
from modules.browser import youtube, gmail, google_search
from modules.weather import temperature, weather
from modules.system import tell_date, tell_time, ip
from modules.jokes import tell
from modules.intents import detect_intent
from modules.greeting import greet
from modules.email_service import send_email
from modules.qa import answer_question
from modules.launcher import open_app
from modules.reminder import set_reminder
from modules.custom_commands import execute_custom_command, add_custom_command_prompt
from modules.identity import tell_who_am_i, tell_what_can_do, respond_how_are_you, respond_thank_you

logger = setup_logger("JarvisCore")

QUESTION_TRIGGERS = (
    "what",
    "who",
    "where",
    "when",
    "why",
    "how",
    "which",
    "whose",
    "whom",
    "explain",
    "define",
    "tell me about",
)


def handle_signal(sig, frame):
    """Graceful signal handling for Ctrl+C or termination signals."""
    print("\n")
    logger.info("Shutdown signal received.")
    speak("Goodbye.")
    sys.exit(0)


def parse_cli_args():
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(description=f"{APP_NAME} - Production AI Voice Assistant")
    parser.add_argument(
        "-t", "--text",
        action="store_true",
        help="Run in text-only mode (ideal for CLI/headless environments)"
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"{APP_NAME} v{APP_VERSION}"
    )
    return parser.parse_args()


def main():
    args = parse_cli_args()
    if args.text:
        set_text_mode(True)

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    logger.info(f"Starting {APP_NAME} v{APP_VERSION}")
    wish()

    while True:
        try:
            query = listen()

            if not query:
                continue

            query = query.lower().strip()
            logger.info(f"Input received: '{query}'")

            intent = detect_intent(query)
            logger.info(f"Detected intent: '{intent}'")

            if intent == "add_custom_command":
                add_custom_command_prompt(query)

            elif intent == "exit":
                speak("Goodbye.")
                break

            elif intent == "greeting":
                greet(query)

            elif intent == "who_are_you":
                tell_who_am_i()

            elif intent == "what_can_you_do":
                tell_what_can_do()

            elif intent == "how_are_you":
                respond_how_are_you()

            elif intent == "thank_you":
                respond_thank_you()

            elif "i am fine" in query or "i am also fine" in query or "i am good" in query:
                speak("That's great to hear, sir!")

            elif intent == "temperature":
                temperature(query)

            elif intent == "weather":
                weather(query)

            elif intent == "date":
                tell_date()

            elif intent == "time":
                tell_time()

            elif intent == "youtube":
                youtube()

            elif intent == "gmail":
                gmail()

            elif intent == "google":
                google_search()

            elif intent == "google_search":
                search_query = query
                phrases = [
                    "search google for",
                    "search on google",
                    "google search",
                    "search for",
                    "google"
                ]
                for phrase in phrases:
                    search_query = search_query.replace(phrase, "")
                search_query = search_query.strip()

                if search_query:
                    google_search(search_query)
                else:
                    google_search()

            elif intent == "open_app":
                app_name = query
                for prefix in ("open application ", "open app ", "open ", "launch "):
                    if app_name.startswith(prefix):
                        app_name = app_name[len(prefix):].strip()
                        break
                open_app(app_name)

            elif intent == "reminder":
                set_reminder(query)

            elif intent == "ip":
                ip()

            elif intent == "joke":
                tell()

            elif intent == "send_email":
                send_email()

            elif intent == "wikipedia":
                search(query)

            elif intent == "question":
                answer_question(query)

            elif execute_custom_command(query):
                continue

            else:
                logger.info("No matching intent found.")

                if query.startswith(QUESTION_TRIGGERS) or query.endswith("?"):
                    logger.info("Routing query to AI Q&A engine...")
                    answer_question(query)
                else:
                    speak("Sorry, I don't understand that command.")

        except (KeyboardInterrupt, EOFError):
            speak("Goodbye.")
            break
        except Exception as e:
            logger.error(f"Main loop exception: {e}", exc_info=True)
            speak("Sorry, an unexpected error occurred.")


if __name__ == "__main__":
    main()