import time
import sys
import json
import os
import datetime
import twitter
import logging

from twitbotreminder.model import ReminderList, Properties, InputBot


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
        self.oauth = twitter.OAuth(self.properties.token,  \
                                   self.properties.token_secret, \
                                   self.properties.consumer_key,  \
                                   self.properties.consumer_secret)
        self.twitter = twitter.Twitter(auth=self.oauth)
        self.connected = True

    def disconnect(self):
           self.connected = False

    def execute(self, reminders):
        if self.connected:
            for reminder in reminders:
                text = self.properties.greeting + " @" + self.properties.me + "! " + reminder.text
                self._try_post_tweet(text)

    def _twit(self, text):
        self.twitter.statuses.update(status=text)
        self._logger.info("New twit posted: %s" % text)

    def _try_post_tweet(self, new_tweet):
        try:
            self._twit(new_tweet)

        except:
            self.connect()
            # Try to post again.
            try:
                self._twit(new_tweet)

            except Exception as e:
                self._logger.error("Error posting twit due to: %s" % (e))
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
                self.logger.error("ERROR: Twitbot could NOT read expected config from file :: %s" % str(e))
                self.load_files = False
        else:
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
            while True:

                now = datetime.datetime.now()
                self.logger.info("Processing reminders for date %s" % now)
                reminders = self.load_reminders()
                current_reminders = reminders.search_by_date(now.day, now.month)
                connector.execute(current_reminders)

                # Sleep iteration
                secondsPerDay = 24 * 60 * 60
                time.sleep(secondsPerDay)

        except Exception as e:
            self.logger.error("An exception happened caused by: %s" % e)
            connector.disconnect()
            sys.exit(-1)


class TwibotLogger:

    @staticmethod
    def getLogger(filename):
        logger = logging.getLogger("twitbot-reminder")
        hdlr = logging.FileHandler(filename)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr)
        logger.setLevel(logging.DEBUG)
        return logger





