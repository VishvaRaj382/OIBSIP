import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))

MUSIC_FOLDER: str = os.path.join(BASE_DIR, "Music")
MOVIE_FOLDER: str = os.path.join(BASE_DIR, "Movies")
SCREENSHOT_FOLDER: str = os.path.join(BASE_DIR, "Screenshots")

for folder in [MUSIC_FOLDER, MOVIE_FOLDER, SCREENSHOT_FOLDER]:
    os.makedirs(folder, exist_ok=True)

CITY: str = os.getenv("JARVIS_DEFAULT_CITY", "Jaipur")

EMAIL_ADDRESS: str | None = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD: str | None = os.getenv("EMAIL_PASSWORD")
GEMINI_API_KEY: str | None = os.getenv("GEMINI_API_KEY")
OPENWEATHER_API_KEY: str | None = os.getenv("OPENWEATHER_API_KEY")

APP_NAME: str = "Jarvis AI"
APP_VERSION: str = "2.1.0"
USER_AGENT: str = f"{APP_NAME}/{APP_VERSION}"

# Voice Settings
VOICE_RATE: int = int(os.getenv("VOICE_RATE", "180"))
VOICE_VOLUME: float = float(os.getenv("VOICE_VOLUME", "1.0"))