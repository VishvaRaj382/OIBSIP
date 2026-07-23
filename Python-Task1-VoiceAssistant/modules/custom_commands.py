import json
import os
import re
import webbrowser
from config import BASE_DIR
from modules.speech import speak, listen

CUSTOM_COMMANDS_FILE = os.path.join(BASE_DIR, "custom_commands.json")


def load_custom_commands():
    if not os.path.exists(CUSTOM_COMMANDS_FILE):
        return {}
    try:
        with open(CUSTOM_COMMANDS_FILE, "r") as f:
            data = json.load(f)
            return data.get("commands", {})
    except Exception as e:
        print(f"Error loading custom commands: {e}")
        return {}


def save_custom_commands(commands):
    try:
        with open(CUSTOM_COMMANDS_FILE, "w") as f:
            json.dump({"commands": commands}, f, indent=2)
    except Exception as e:
        print(f"Error saving custom commands: {e}")


def add_custom_command(trigger, action, value):
    if not trigger or not action or not value:
        return False
    trigger = trigger.lower().strip()
    action = action.lower().strip()
    value = value.strip()
    if action == "url" and not value.startswith("http"):
        value = f"https://{value}"

    commands = load_custom_commands()
    commands[trigger] = {"action": action, "value": value}
    save_custom_commands(commands)
    return True


def execute_custom_command(query):
    commands = load_custom_commands()
    query = query.lower().strip()

    for trigger, config in commands.items():
        trigger_clean = trigger.lower().strip()
        pattern = r'\b' + re.escape(trigger_clean) + r'\b'
        if re.search(pattern, query):
            action = config.get("action")
            value = config.get("value")

            if action == "speak":
                speak(value)
                return True

            elif action == "url":
                speak(f"Opening custom link for {trigger}")
                webbrowser.open(value)
                return True

    return False


def parse_inline_command(query):
    """
    Attempt to extract trigger, action, value from inline phrases like:
    'add custom command google url https://google.com'
    'add custom command hello speak Hello world'
    """
    if not query:
        return None, None, None

    prefixes = [
        "add custom command ",
        "add a custom command ",
        "create custom command ",
        "create a custom command ",
        "new custom command ",
        "add command "
    ]
    cleaned = query.lower().strip()
    matched_prefix = None
    for p in prefixes:
        if cleaned.startswith(p):
            matched_prefix = p
            break

    if not matched_prefix:
        return None, None, None

    remainder = query[len(matched_prefix):].strip()

    # Look for action keywords ' url ' or ' speak '
    match_url = re.search(r'^(.*?)\s+(url|website|link)\s+(https?://\S+|\S+)$', remainder, re.IGNORECASE)
    if match_url:
        return match_url.group(1).strip(), "url", match_url.group(3).strip()

    match_speak = re.search(r'^(.*?)\s+(speak|say)\s+(.+)$', remainder, re.IGNORECASE)
    if match_speak:
        return match_speak.group(1).strip(), "speak", match_speak.group(3).strip()

    return None, None, None


def add_custom_command_prompt(query=None):
    if query:
        trigger, action, value = parse_inline_command(query)
        if trigger and action and value:
            success = add_custom_command(trigger, action, value)
            if success:
                if action == "url":
                    speak(f"Custom command added! Saying '{trigger}' will now open {value}.")
                else:
                    speak(f"Custom command added! Saying '{trigger}' will now respond with '{value}'.")
                return

    speak("What phrase would you like to set as the custom trigger?")
    trigger = listen()

    if not trigger:
        speak("I didn't hear a trigger phrase. Action cancelled.")
        return

    speak("Should this command speak a response, or open a website URL? Say speak or URL.")
    command_type = listen()
    if command_type:
        command_type = command_type.lower().strip()
    else:
        command_type = ""

    if not command_type:
        speak("I didn't hear a command type. Action cancelled.")
        return

    if "url" in command_type or "link" in command_type or "website" in command_type:
        speak("Please say or type the website URL.")
        url = listen()
        if not url:
            speak("No URL provided. Action cancelled.")
            return

        add_custom_command(trigger, "url", url)
        if not url.startswith("http"):
            url = f"https://{url}"
        speak(f"Custom command added! Saying '{trigger}' will now open {url}.")

    elif "speak" in command_type or "say" in command_type or "text" in command_type or "response" in command_type:
        speak("What response should I speak?")
        response_text = listen()
        if not response_text:
            speak("No response text provided. Action cancelled.")
            return

        add_custom_command(trigger, "speak", response_text)
        speak(f"Custom command added! Saying '{trigger}' will now respond with '{response_text}'.")
    else:
        speak("Unrecognized command type. Please specify speak or URL. Action cancelled.")

