import logging
import unittest
from unittest.mock import Mock

from twitbotreminder.model import InputBot
from twitbotreminder.twitbotreminder import TwitbotReminder, TwitterConnector

FAKE_FILE = "does_not_exist.json"
PROPERTIES_FILE = "sample/properties.json"
REMINDERS_FILE = "sample/reminders.json"
LOG_FILE = "twitbot-reminder.log"


class TwitbotReminderCase(unittest.TestCase):

    def test_load_properties(self):
        reminder = self.create_twitbot_reminder(PROPERTIES_FILE, REMINDERS_FILE)
        properties = reminder.load_properties();
        self.assertEqual(reminder.load_files, True)
        self.assertEqual(properties.consumer_key, "test-consumer-key")
        self.assertEqual(properties.consumer_secret, "test-consumer-secret")
        self.assertEqual(properties.greeting, "Hi")
        self.assertEqual(properties.me, "my_twitter_username")
        self.assertEqual(properties.token, "test-access-token")
        self.assertEqual(properties.token_secret, "test-access-token-secret")
        self.assertEqual(properties.welcome_text, "This is my first message")

    def test_load_properties_with_wrong_file(self):
        reminder = self.create_twitbot_reminder(FAKE_FILE, REMINDERS_FILE)
        properties = reminder.load_properties();
        self.assertEqual(reminder.load_files, False)

    def test_load_reminders(self):
        reminder = self.create_twitbot_reminder(PROPERTIES_FILE, REMINDERS_FILE)
        reminders = reminder.load_reminders();
        self.assertEqual(reminder.load_files, True)
        self.assertEqual(len(reminders.list), 2)

    def test_load_reminders_with_wrong_file(self):
        reminder = self.create_twitbot_reminder(PROPERTIES_FILE, FAKE_FILE)
        reminders = reminder.load_reminders();
        self.assertEqual(reminder.load_files, False)

    def create_twitbot_reminder(self, properties_file, reminders_file):
        input_bot = self.create_input_bot(properties_file=properties_file, reminders_file=reminders_file)
        reminder = TwitbotReminder(input_bot)
        reminder.logger = create_logger()
        return reminder

    def create_input_bot(self, properties_file, reminders_file):
        return InputBot(properties_file, reminders_file, LOG_FILE)


class TwitterConnectorCase(unittest.TestCase):

    def test_disconnect(self):
        properties = Mock()
        connector = self.create_twitter_connector(properties)
        connector.disconnect()
        self.assertEqual(connector.connected, False)

    def test_connect(self):
        properties = Mock()
        connector = self.create_twitter_connector(properties)
        connector.connect()
        self.assertEqual(connector.connected, True)

    def create_twitter_connector(self, properties):
        return TwitterConnector(properties)


def create_logger():
    logger = logging.getLogger("twitbot-reminder")
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger


def main():
    unittest.main()


if __name__ == "__main__":
    main()
