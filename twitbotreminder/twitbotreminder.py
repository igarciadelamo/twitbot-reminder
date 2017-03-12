import time
import sys
import json
import os
import datetime
from urllib.error import URLError

import tweepy
import logging

from twitbotreminder.model import ReminderList, Properties, InputBot

MAX_ATTEMPTS = 5
EXECUTION_TIME = 24 * 60 * 60
RECONNECTION_TIME = 10 * 60


class TwitterConnector:
    def __init__(self, properties):
        self.properties = properties
        self.twitter = None
        self.connected = False
        self._logger = None

    @property
    def logger(self):
        return self._logger

    @logger.setter
    def logger(self, value):
        self._logger = value

    def connect(self):
        auth = tweepy.OAuthHandler(self.properties.consumer_key, self.properties.consumer_secret)
        auth.set_access_token(self.properties.token,  self.properties.token_secret)
        self.twitter = tweepy.API(auth)
        self.connected = True

    def disconnect(self):
        self.connected = False

    def check_previous_tweets(self):
        self._logger.info("Checking last published tweet... ")
        timeline = self.twitter.user_timeline(count=1)
        tweet = next(iter(timeline or []), None)
        if(tweet is not None):
            self._logger.info("Last published tweet at %s with text %s" % (tweet.created_at,tweet.text))
        else:
            self._tweet(self, self._compose_text(self.properties.welcome_text))

    def execute(self, reminders):
        if self.connected:
            for reminder in reminders:
                text = self.compose_text(reminder.text)
                self._try_post_tweet(text, 1)

    def _compose_text(self, text):
        return  self.properties.greeting + " @" + self.properties.me + "! " + text

    def _tweet(self, text):
        self.twitter.statuses.update(status=text)
        self._logger.info("New tweet posted: %s" % text)

    def _try_post_tweet(self, new_tweet, attempt):
        try:
            self._tweet(new_tweet)

        except URLError as e:
            self._logger.error("Error in the http connection: %s" % (e))
            if attempt == MAX_ATTEMPTS:
                self._logger.error("Maximum number of attempts reached.")
                sys.exit(-1)

            # Sleep until next reconnection
            time.sleep(RECONNECTION_TIME)
            # Try to post again.
            self.connect()
            self._try_post_tweet(new_tweet, attempt+1)

        except Exception as e:
            self._logger.error("Unexpected error posting tweet: %s" % (e))
            sys.exit(-1)


class TwitbotReminder:
    def __init__(self, input_bot: InputBot):
        self.logger = TwibotLogger.getLogger(input_bot.logs_file)
        self.properties_file = input_bot.properties_file
        self.reminders_file = input_bot.reminders_file
        self.load_files = True

    def load_properties(self):
        properties = None
        self.logger.info("Twitbot loading config from file %s" % self.properties_file)
        if os.path.isfile(self.properties_file):
            try:
                with open(self.properties_file) as json_data:
                    data = json.load(json_data)
                    properties = Properties(data)
                    self.logger.info("Twitbot has loaded config successfully")

            except KeyError as e:
                self.logger.error("Twitbot could NOT read expected config from file :: %s" % str(e))
                self.load_files = False
        else:
            self.logger.error("Twitbot could NOT find property file : %s" % self.properties_file)
            self.load_files = False

        return properties

    def load_reminders(self):
        reminders = None

        if os.path.isfile(self.reminders_file):
            with open(self.reminders_file) as json_data:
                data = json.load(json_data)
                reminders = ReminderList(data)
                self.logger.info("Twitbot file with reminders #%d" % len(reminders.list))
        else:
            self.logger.error("Twitbot could NOT find reminder file : %s" % self.reminders_file)
            self.load_files = False

        return reminders

    def execute(self):

        if not self.load_files:
            self.logger.error("The config files are not correct. Check paths and format")
            sys.exit(-1)

        try:
            properties = self.load_properties()
            connector = TwitterConnector(properties)
            connector.logger = self.logger
            connector.connect()
            time.sleep(5)

            connector.check_previous_tweets()

            while True:

                now = datetime.datetime.now()
                self.logger.info("Processing reminders for date %s" % now)
                reminders = self.load_reminders()
                current_reminders = reminders.search_by_date(now.day, now.month)
                connector.execute(current_reminders)

                # Sleep iteration
                time.sleep(EXECUTION_TIME)

        except Exception as e:
            self.logger.error("An exception happened caused by: %s" % e)
            connector.disconnect()
            sys.exit(-1)


class TwibotLogger:

    @staticmethod
    def getLogger(filename):
        logger = logging.getLogger("twitbot-reminder")
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        handler = logging.FileHandler(filename)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
        return logger





