from typing import Optional

INTENTS: dict[str, list[str]] = {
    "greeting": [
        "hello",
        "hi",
        "hey",
        "good morning",
        "good afternoon",
        "good evening"
    ],

    "how_are_you": [
        "how are you",
        "how r u",
        "how r ya",
        "how's it going",
        "how do you do",
        "how are you doing",
        "what's up",
        "whats up",
        "what are you doing"
    ],

    "who_are_you": [
        "who are you",
        "who r u",
        "hu r u",
        "hu r ya",
        "who r ya",
        "hu are u",
        "who ru",
        "hu ru",
        "who u",
        "hu u",
        "who are u",
        "what is your name",
        "what's your name",
        "whats your name",
        "who created you",
        "who made you",
        "who built you",
        "who is your creator",
        "who is your developer",
        "tell me about yourself",
        "introduce yourself"
    ],

    "what_can_you_do": [
        "what can you do",
        "what can u do",
        "wat can u do",
        "what are your capabilities",
        "what features do you have",
        "how can you help me",
        "help me",
        "help"
    ],

    "thank_you": [
        "thank you",
        "thanks",
        "thx",
        "thank u",
        "thank you jarvis",
        "thanks jarvis",
        "good job",
        "well done",
        "nice job",
        "awesome"
    ],

    "temperature": [
        "temperature",
        "current temperature",
        "how hot",
        "how cold",
        "degrees",
        "temperature outside"
    ],

    "weather": [
        "weather",
        "weather today",
        "forecast",
        "rain",
        "humidity",
        "wind",
        "outside weather"
    ],

    "time": [
        "time",
        "clock",
        "current time"
    ],

    "date": [
        "date",
        "today's date",
        "day today"
    ],

    "youtube": [
        "youtube",
        "play youtube",
        "open youtube"
    ],

    "gmail": [
        "gmail",
        "email inbox",
        "open gmail"
    ],

    "send_email": [
        "send email",
        "send an email",
        "compose email",
        "write an email",
        "email to"
    ],

    "google_search": [
        "search google",
        "search google for",
        "search on google"
    ],

    "google": [
        "google",
        "open google"
    ],

    "joke": [
        "joke",
        "make me laugh",
        "funny"
    ],

    "ip": [
        "ip",
        "ip address",
        "my ip",
        "what is my ip address"
    ],

    "wikipedia": [
        "tell me about",
        "wikipedia"
    ],

    "question": [
        "what",
        "who",
        "why",
        "when",
        "where",
        "how",
        "which",
        "whose",
        "whom",
        "explain",
        "define",
        "tell me about"
    ],

    "open_app": [
        "open chrome",
        "open safari",
        "open finder",
        "open terminal",
        "open vscode",
        "open spotify",
        "open calculator",
        "open notes",
        "open calendar",
        "open mail",
        "open photos",
        "open music",
        "open facetime",
        "open settings",
        "open app",
        "open application",
        "launch"
    ],

    "reminder": [
        "remind me",
        "set reminder",
        "set a reminder",
        "alarm for",
        "timer for"
    ],

    "add_custom_command": [
        "add custom command",
        "add a custom command",
        "create custom command",
        "create a custom command",
        "new custom command",
        "add new custom command",
        "create new custom command",
        "make custom command",
        "make a custom command",
        "add custom",
        "add command",
        "add a command",
        "set custom command"
    ],

    "exit": [
        "exit",
        "bye",
        "goodbye",
        "quit",
        "stop",
        "close jarvis"
    ]
}


WORD_NORMALIZATIONS: dict[str, str] = {
    "hu": "who",
    "hoo": "who",
    "whu": "who",
    "r": "are",
    "ar": "are",
    "u": "you",
    "yu": "you",
    "ya": "you",
    "ur": "your",
    "yr": "your",
    "wat": "what",
    "wut": "what",
    "pls": "please",
    "thx": "thanks",
}


def normalize_query(query: str) -> str:
    """Normalizes phonetic speech recognition contractions and common STT mishearings."""
    if not query:
        return ""
    words = query.lower().strip().split()
    normalized_words = [WORD_NORMALIZATIONS.get(w, w) for w in words]
    return " ".join(normalized_words)


def detect_intent(query: str) -> Optional[str]:
    """Scores user query against known intent phrase rules and returns best matching intent."""
    if not query:
        return None

    # Process raw query and normalized phonetic query
    raw_query = query.lower().strip()
    norm_query = normalize_query(raw_query)

    best_intent: Optional[str] = None
    best_score: int = 0

    for q in set([raw_query, norm_query]):
        words = q.split()

        for intent, phrases in INTENTS.items():
            score = 0

            for phrase in phrases:
                phrase = phrase.lower()

                if " " in phrase:
                    if phrase in q:
                        score += len(phrase.split()) + 1
                else:
                    if phrase in words:
                        score += 1

            if score > best_score:
                best_score = score
                best_intent = intent

    return best_intent if best_score > 0 else None