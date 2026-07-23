import re
import requests
from typing import Optional
from config import OPENWEATHER_API_KEY, CITY as DEFAULT_CITY
from modules.speech import speak
from modules.logger import setup_logger

logger = setup_logger("Weather")


def extract_city(query: Optional[str], default: str = DEFAULT_CITY) -> str:
    """Extracts target city name from natural language query."""
    if not query:
        return default

    match = re.search(r"\b(in|of|at|for)\s+([a-zA-Z\s]+)$", query.lower().strip())
    if match:
        city_candidate = match.group(2).strip()
        noise_words = {"today", "now", "outside", "degree", "degrees", "weather", "temperature"}
        if city_candidate not in noise_words:
            return city_candidate.title()

    return default


def temperature(query: Optional[str] = None) -> None:
    """Fetches and announces current temperature for specified city."""
    if not OPENWEATHER_API_KEY:
        speak("OpenWeather API key is not configured.")
        logger.warning("OPENWEATHER_API_KEY missing.")
        return

    city = extract_city(query)
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"

    try:
        response = requests.get(url, timeout=8)
        if response.status_code != 200:
            speak(f"Unable to fetch the temperature for {city}.")
            logger.warning(f"OpenWeather returned status code {response.status_code}")
            return

        data = response.json()
        temp = data["main"]["temp"]
        logger.info(f"Temperature in {city}: {temp}°C")
        speak(f"The current temperature in {city} is {temp} degrees Celsius.")

    except requests.RequestException as req_err:
        logger.error(f"Temperature request failed: {req_err}")
        speak("Unable to connect to the weather service.")
    except Exception as e:
        logger.error(f"Temperature error: {e}")
        speak("Unable to fetch the temperature.")


def weather(query: Optional[str] = None) -> None:
    """Fetches and announces comprehensive weather forecast for specified city."""
    if not OPENWEATHER_API_KEY:
        speak("OpenWeather API key is not configured.")
        logger.warning("OPENWEATHER_API_KEY missing.")
        return

    city = extract_city(query)
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"

    try:
        response = requests.get(url, timeout=8)
        if response.status_code != 200:
            speak(f"Unable to fetch the weather for {city}.")
            logger.warning(f"OpenWeather returned status code {response.status_code}")
            return

        data = response.json()
        description = data["weather"][0]["description"]
        temp_val = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        logger.info(f"Weather for {city}: {description}, {temp_val}°C, {humidity}%, {wind_speed} m/s")
        speak(
            f"The weather in {city} is {description}. "
            f"The temperature is {temp_val} degrees Celsius, "
            f"humidity is {humidity} percent, "
            f"and wind speed is {wind_speed} meters per second."
        )

    except requests.RequestException as req_err:
        logger.error(f"Weather request failed: {req_err}")
        speak("Unable to connect to the weather service.")
    except Exception as e:
        logger.error(f"Weather error: {e}")
        speak("Unable to fetch the weather.")