import platform
import subprocess
import speech_recognition as sr
from typing import Optional
from config import VOICE_RATE
from modules.logger import setup_logger

logger = setup_logger("Speech")
system = platform.system()

# Flag to enable text-only mode for CLI / server environments
TEXT_MODE: bool = False


def set_text_mode(enabled: bool = True) -> None:
    """Toggle text-only mode for command-line usage without speech synthesis or microphone."""
    global TEXT_MODE
    TEXT_MODE = enabled
    logger.info(f"Text mode set to: {enabled}")


def speak(text: str, rate: int = VOICE_RATE, voice: Optional[str] = None) -> None:
    """Outputs text to stdout and synthesizes speech using system TTS engines."""
    if not text:
        return

    print(f"Jarvis: {text}")

    if TEXT_MODE:
        return

    try:
        if system == "Darwin":
            command = ["say", "-r", str(rate)]
            if voice:
                command.extend(["-v", voice])
            command.append(text)
            subprocess.run(command, check=False)

        elif system == "Windows":
            command = [
                "powershell",
                "-Command",
                f'''
                Add-Type -AssemblyName System.Speech;
                $speaker = New-Object System.Speech.Synthesis.SpeechSynthesizer;
                $speaker.Rate = 0;
                $speaker.Speak("{text}");
                '''
            ]
            subprocess.run(command, check=False)

        elif system == "Linux":
            subprocess.run(
                ["espeak", "-s", str(rate), text],
                check=False
            )
    except Exception as e:
        logger.error(f"Text-to-Speech Error: {e}")


def listen(max_attempts: int = 3) -> str:
    """Listens for audio input via microphone or prompts for keyboard text input in text mode."""
    if TEXT_MODE:
        try:
            user_input = input("You: ").strip()
            return user_input.lower()
        except (KeyboardInterrupt, EOFError):
            return ""

    recognizer = sr.Recognizer()

    for attempt in range(max_attempts):
        try:
            with sr.Microphone() as source:
                print("Listening...")
                recognizer.adjust_for_ambient_noise(source, duration=0.8)

                try:
                    audio = recognizer.listen(source, timeout=5)
                except sr.WaitTimeoutError:
                    if attempt < max_attempts - 1:
                        print("No speech detected.")
                        speak("I didn't hear anything. Please repeat.")
                        continue
                    else:
                        speak("No voice detected.")
                        return ""

        except Exception as mic_err:
            logger.warning(f"Microphone error/unavailable: {mic_err}. Falling back to keyboard input.")
            try:
                user_input = input("You (type command): ").strip()
                return user_input.lower()
            except (KeyboardInterrupt, EOFError):
                return ""

        try:
            print("Recognizing...")
            query = recognizer.recognize_google(audio)
            print(f"You: {query}")
            return query.lower().strip()

        except sr.UnknownValueError:
            if attempt < max_attempts - 1:
                print("Speech not understood.")
                speak("Sorry, I didn't understand that. Please repeat.")
            else:
                speak("Sorry, I still couldn't understand you.")
                return ""

        except sr.RequestError as req_err:
            logger.error(f"Speech recognition service error: {req_err}")
            speak("Speech recognition service is unavailable.")
            return ""

    return ""