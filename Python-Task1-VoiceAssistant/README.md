# Jarvis AI Voice Assistant

Jarvis is a Python-based voice assistant that can listen to voice commands, understand what the user wants, and perform different tasks.

It can tell the time and date, search the web, check weather, send emails, set reminders, open applications, answer questions, and run custom commands.

The project also supports a text mode, so Jarvis can be used without a microphone.

---

## Features

### Voice Commands

Jarvis listens to the user's voice using Python's Speech Recognition library and converts speech into text.

If a microphone is not available, Jarvis can also work in text mode.

### Smart Command Detection

Jarvis tries to understand what the user wants instead of depending only on exact commands.

For example:

* "What is the weather?"
* "Tell me the weather in London"
* "What is the temperature in Delhi?"

Jarvis recognizes these as weather-related commands.

### Date and Time

Jarvis can tell the current:

* Time
* Date

Example:

```text
What time is it?
What is today's date?
```

### Weather Information

Jarvis uses the OpenWeatherMap API to provide current weather information.

Example:

```text
What is the weather?
What is the temperature in London?
```

The default city can also be configured in the `.env` file.

### AI Question Answering

Jarvis can answer general knowledge questions using Google Gemini AI.

Wikipedia is also used for information and topic searches.

Example:

```text
What is quantum computing?
Tell me about Albert Einstein.
```

### Email

Jarvis can send emails using voice commands.

Example:

```text
Send email to Vishu.
or you can add more contact with email and name from email_service.py file by adding more id with specific name in CONTACTS dictonary.
```

The email is sent using Python's `smtplib` and Gmail SMTP with TLS encryption.

### Reminders

Jarvis can create timed reminders.

Example:

```text
Remind me in 10 seconds to drink water.
Set a reminder for 5 minutes.
```

When the timer finishes, Jarvis gives an audible reminder.

### Open Applications

Jarvis can open supported applications installed on the computer.

Example:

```text
Open Chrome.
Launch Terminal.
Open VS Code.
```

### Web Commands

Jarvis can also open websites and perform web searches.

For example:

```text
Open YouTube.
Open Gmail.
Search Google for artificial intelligence.
```

### Custom Commands

Users can create their own Jarvis commands.

Example:

```text
Add custom command
```

Jarvis will ask for the command and what it should do.

A command can also be added directly:

```text
Add custom command open google url https://google.com
```

Custom commands are saved locally inside:

```text
custom_commands.json
```

### Error Handling

Jarvis handles common problems such as:

* Voice not understood
* Microphone timeout
* Internet connection problems
* API errors
* Invalid commands
* Missing configuration

Instead of crashing, Jarvis displays or speaks an appropriate message.

---

# Project Structure

```text
OIBSIP/
├── jarvis.py
├── config.py
├── custom_commands.json
├── requirements.txt
├── test_suite.py
├── .env.example
│
└── modules/
    ├── assistant.py
    ├── browser.py
    ├── custom_commands.py
    ├── email_service.py
    ├── greeting.py
    ├── identity.py
    ├── intents.py
    ├── jokes.py
    ├── launcher.py
    ├── logger.py
    ├── qa.py
    ├── reminder.py
    ├── speech.py
    ├── system.py
    ├── weather.py
    └── wikipedia_search.py
```

Each module handles a different part of Jarvis, which makes the project easier to understand, maintain, and improve.

---

# Installation

## Requirements

Before running Jarvis, make sure you have:

* Python 3.10 or newer
* Internet connection
* Microphone for voice mode

## 1. Create Virtual Environment

```bash
python3 -m venv venv
```

Activate it on macOS/Linux:

```bash
source venv/bin/activate
```

On Windows:

```bash
venv\Scripts\activate
```

## 2. Install Required Libraries

```bash
pip install -r requirements.txt
```

## 3. Configure API Keys

Copy:

```text
.env.example
```

and create:

```text
.env
```

Add your configuration:

```env
GEMINI_API_KEY=your_gemini_api_key_here
OPENWEATHER_API_KEY=your_openweather_api_key_here
JARVIS_DEFAULT_CITY=Jaipur
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password_here
```

Never upload your real `.env` file or API keys to GitHub.

---

# Running Jarvis

## Voice Mode

Run:

```bash
python jarvis.py
```

Jarvis will start listening for voice commands.

## Text Mode

If you want to use Jarvis without a microphone:

```bash
python jarvis.py --text
```

You can then type commands directly into the terminal.

## Help

```bash
python jarvis.py --help
```

## Version

```bash
python jarvis.py --version
```

---

# Example Commands

```text
Hello Jarvis

Who are you?

What can you do?

What time is it?

What is today's date?

What is the weather?

What is the temperature in London?

Remind me in 10 seconds to drink water.

Send email to Vishu.

Open Chrome.

Launch Terminal.

Open VS Code.

Search Google for robotics.

What is quantum computing?

Tell me about Albert Einstein.
```

---

# Testing

The project contains an automated test suite.

Run:

```bash
python test_suite.py
```

The tests check important parts of Jarvis while using mock services where possible so that testing does not depend on real external API requests.

---

# Privacy

Jarvis uses some external services, but it tries to keep information local whenever possible.

### Voice

Microphone audio is captured when Jarvis is listening and is used for speech recognition.

Audio is not intentionally stored as an audio file by Jarvis.

### AI Questions

When a question needs AI assistance, the text of the question may be sent to the configured Google Gemini API.

### Weather

For weather requests, the requested city name is sent to the weather service.

Jarvis does not require GPS location.

### Email

Email information is sent through the configured SMTP server when the user asks Jarvis to send an email.

### API Keys

API keys and email credentials are stored in the local `.env` file.

The `.env` file should never be uploaded to GitHub.

### Custom Commands

Custom commands are stored locally inside:

```text
custom_commands.json
```

### Text-to-Speech

Jarvis uses the operating system's available speech tools for voice output.

Supported implementations include:

* macOS `say`
* Windows PowerShell Speech Synthesizer
* Linux `espeak`

---

# Technologies Used

* Python
* SpeechRecognition
* Google Gemini API
* Wikipedia API
* OpenWeatherMap API
* SMTP
* Python threading
* JSON
* Python logging
* Environment variables
* text-to-speech

---

# Purpose of the Project

The purpose of this project is to demonstrate how Python can be used to create an intelligent voice assistant that combines speech recognition, natural-language command handling, APIs, automation, and text-to-speech.

This project was developed as **Task 1 - Voice Assistant** for the **Oasis Infobyte Python Programming Internship**.

---

# Future Improvements

Future versions of Jarvis could include:

* Graphical user interface
* Better natural language understanding
* More application integrations
* Calendar integration
* More customizable commands
* Offline speech recognition
* Smart home device support
* Conversation history

---

# Author

**Vishva**

Python Programming Internship Project
Oasis Infobyte
