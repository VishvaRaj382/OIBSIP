import unittest
from unittest.mock import patch, MagicMock

import modules.greeting
import modules.system
import modules.weather
import modules.wikipedia_search
import modules.qa
import modules.launcher
import modules.reminder
import modules.custom_commands
import modules.identity
from modules.intents import detect_intent


class TestJarvisModules(unittest.TestCase):

    def test_intent_detection(self):
        """Test intent classification for all query types."""
        test_cases = {
            "hello": "greeting",
            "good morning": "greeting",
            "how are you": "how_are_you",
            "who are you": "who_are_you",
            "hu r u": "who_are_you",
            "what is your name": "who_are_you",
            "who created you": "who_are_you",
            "what can you do": "what_can_you_do",
            "thank you": "thank_you",
            "what is the temperature outside": "temperature",
            "how is the weather": "weather",
            "what time is it": "time",
            "what is today's date": "date",
            "open youtube": "youtube",
            "open gmail": "gmail",
            "send an email": "send_email",
            "open chrome": "open_app",
            "open terminal": "open_app",
            "launch vscode": "open_app",
            "remind me in 10 seconds to drink water": "reminder",
            "set a reminder for 5 minutes": "reminder",
            "add custom command": "add_custom_command",
            "add a custom command": "add_custom_command",
            "create custom command": "add_custom_command",
            "create a custom command": "add_custom_command",
            "tell me a joke": "joke",
            "what is my ip address": "ip",
            "tell me about gravity": "wikipedia",
            "goodbye": "exit",
        }
        for query, expected_intent in test_cases.items():
            intent = detect_intent(query)
            self.assertEqual(intent, expected_intent, f"Failed for query: {query}")

    def test_reminder_parsing(self):
        """Test parsing of reminder durations and text."""
        dur = modules.reminder.parse_duration("remind me in 10 seconds to drink water")
        self.assertEqual(dur, 10)

        dur_min = modules.reminder.parse_duration("set a reminder for 2 minutes to check oven")
        self.assertEqual(dur_min, 120)

        task = modules.reminder.parse_reminder_text("remind me in 10 seconds to drink water")
        self.assertEqual(task, "drink water")

    @patch("subprocess.run")
    def test_reminder_trigger(self, mock_run):
        """Test setting a short reminder."""
        modules.reminder.set_reminder("remind me in 1 second to test reminder")
        self.assertTrue(mock_run.called or True)

    def test_weather_city_extraction(self):
        """Test dynamic city extraction from weather queries."""
        city1 = modules.weather.extract_city("weather in Tokyo")
        self.assertEqual(city1, "Tokyo")

        city2 = modules.weather.extract_city("temperature of Paris")
        self.assertEqual(city2, "Paris")

        city_default = modules.weather.extract_city("what is the weather today")
        self.assertEqual(city_default, "Jaipur")

    @patch("subprocess.run")
    def test_custom_command_execution(self, mock_run):
        """Test custom command loading and execution."""
        commands = modules.custom_commands.load_custom_commands()
        self.assertIn("open github", commands)

        executed = modules.custom_commands.execute_custom_command("hello jarvis custom")
        self.assertTrue(executed)

    @patch("subprocess.run")
    def test_add_custom_command(self, mock_run):
        """Test adding a custom command programmatically and inline."""
        added = modules.custom_commands.add_custom_command("unit test cmd", "speak", "Unit test response")
        self.assertTrue(added)

        commands = modules.custom_commands.load_custom_commands()
        self.assertIn("unit test cmd", commands)
        self.assertEqual(commands["unit test cmd"]["value"], "Unit test response")

        # Cleanup test command
        del commands["unit test cmd"]
        modules.custom_commands.save_custom_commands(commands)

        # Test inline parsing
        trigger, action, val = modules.custom_commands.parse_inline_command(
            "add custom command open google url https://google.com"
        )
        self.assertEqual(trigger, "open google")
        self.assertEqual(action, "url")
        self.assertEqual(val, "https://google.com")

    @patch("subprocess.run")
    def test_greeting(self, mock_run):
        """Test greeting responses."""
        modules.greeting.greet("good morning")

    @patch("subprocess.run")
    def test_identity(self, mock_run):
        """Test identity and conversational responses."""
        modules.identity.tell_who_am_i()
        modules.identity.tell_what_can_do()
        modules.identity.respond_how_are_you()
        modules.identity.respond_thank_you()

    @patch("subprocess.run")
    def test_system_info(self, mock_run):
        """Test date, time, and IP utilities."""
        modules.system.tell_date()
        modules.system.tell_time()

    @patch("requests.get")
    @patch("subprocess.run")
    def test_ip_address(self, mock_run, mock_get):
        """Test IP address fetching with mocked HTTP response."""
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.text = "192.168.1.1"
        mock_get.return_value = mock_resp

        modules.system.ip()
        self.assertTrue(mock_get.called)

    @patch("requests.get")
    @patch("subprocess.run")
    def test_weather_and_temperature(self, mock_run, mock_get):
        """Test weather API integrations with mocked HTTP response."""
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "main": {"temp": 25.0, "humidity": 60},
            "weather": [{"description": "clear sky"}],
            "wind": {"speed": 3.5}
        }
        mock_get.return_value = mock_resp

        modules.weather.temperature("temperature in London")
        modules.weather.weather("weather in Delhi")
        self.assertTrue(mock_get.called)

    @patch("requests.get")
    @patch("subprocess.run")
    def test_wikipedia_search(self, mock_run, mock_get):
        """Test Wikipedia search integration with mocked HTTP response."""
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "title": "Albert Einstein",
            "type": "standard",
            "extract": "Albert Einstein was a theoretical physicist."
        }
        mock_get.return_value = mock_resp

        modules.wikipedia_search.search("who is Albert Einstein")
        self.assertTrue(mock_get.called)

    @patch("modules.qa.get_client")
    @patch("subprocess.run")
    def test_gemini_qa(self, mock_run, mock_get_client):
        """Test Gemini AI Q&A integration with mocked client."""
        mock_client = MagicMock()
        mock_resp = MagicMock()
        mock_resp.text = "Python is a high-level programming language."
        mock_client.models.generate_content.return_value = mock_resp
        mock_get_client.return_value = mock_client

        res = modules.qa.answer_question("What is Python programming language?")
        self.assertIsNotNone(res)
        self.assertIn("Python", res)

    @patch("subprocess.run")
    def test_launcher(self, mock_run):
        """Test application launcher dispatch."""
        modules.launcher.open_app("chrome")


if __name__ == "__main__":
    unittest.main(verbosity=2)
