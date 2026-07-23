import platform
import subprocess
from modules.speech import speak
from modules.logger import setup_logger

logger = setup_logger("Launcher")
system = platform.system()


def open_app(app_name: str) -> None:
    """Launches target desktop application by name cross-platform."""
    if not app_name:
        speak("Which application would you like to open?")
        return

    app_clean = app_name.lower().strip()

    try:
        if system == "Darwin":  # macOS
            apps = {
                "chrome": "Google Chrome",
                "google chrome": "Google Chrome",
                "safari": "Safari",
                "finder": "Finder",
                "terminal": "Terminal",
                "vscode": "Visual Studio Code",
                "visual studio code": "Visual Studio Code",
                "code": "Visual Studio Code",
                "spotify": "Spotify",
                "calculator": "Calculator",
                "notes": "Notes",
                "calendar": "Calendar",
                "mail": "Mail",
                "photos": "Photos",
                "music": "Music",
                "facetime": "FaceTime",
                "system settings": "System Settings",
                "settings": "System Settings",
            }

            if app_clean in apps:
                target_app = apps[app_clean]
                subprocess.run(["open", "-a", target_app], check=False)
                logger.info(f"Launched macOS app: {target_app}")
                speak(f"Opening {app_name}")
            else:
                # Direct launch attempt
                subprocess.run(["open", "-a", app_clean], check=False)
                speak(f"Opening {app_name}")

        elif system == "Windows":
            apps = {
                "calculator": "calc",
                "notepad": "notepad",
                "paint": "mspaint",
                "cmd": "cmd",
                "command prompt": "cmd",
            }

            target = apps.get(app_clean, app_clean)
            subprocess.Popen([target], shell=True)
            logger.info(f"Launched Windows app: {target}")
            speak(f"Opening {app_name}")

        elif system == "Linux":
            subprocess.Popen([app_clean])
            logger.info(f"Launched Linux process: {app_clean}")
            speak(f"Opening {app_name}")

    except Exception as e:
        logger.error(f"Error launching application '{app_name}': {e}")
        speak("Sorry, I couldn't open that application.")