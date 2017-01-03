import time
import sys
import json
import os
import datetime
import twitter

from twitbotreminder.model import ReminderList, Properties, InputBot


class TwitterConnector:
    def __init__(self, properties):
        self.properties = properties

        self.twitter = None
        # Create locks for these instances, so they won't be accessed at the
        # same time by different threads.
        #self._tlock = Lock()

        # Create a Boolean that indicates whether the bot is logged in
        self.loggedin = False

    #def start(self):
    #    self.thread = Thread(target=self._execute)
    #    self.thread.daemon = True
    #    self.thread.name = 'TwitbotThread'
    #    self.thread.start()

    def connect(self):

        # Log in to a Twitter account
        self.oauth = twitter.OAuth(self.properties.access_token, self.properties.access_token_secret, \
                                    self.properties.consumer_key, self.properties.consumer_secret)
        self.twitter = twitter.Twitter(auth=self.oauth)
        self.loggedin = True

    def disconnect(self):
           self.loggedin = False
           #self.thread._stop()

    def execute(self, reminders):
        if self.loggedin:

            now = datetime.datetime.now()
            for reminder in self.reminders:
                text = self.properties.greeting + " @" + self.properties.me + "! " + reminder.text
                self._try_post_tweet(text)

    def _twit(self, text):
        self.twitter.statuses.update(status=text)
        print("INFO: New twit posted: %s" % text)

    def _try_post_tweet(self, new_tweet):
        try:
            self._twit(new_tweet)

        except:
            self.connect()
            # Try to post again.
            try:
                self._twit(new_tweet)

            except Exception as e:
                print("ERROR: Error posting twit due to: %s" % (e))
                sys.exit(-1)



class TwitbotReminder:
    def __init__(self, input_bot: InputBot):
        self.properties_file = input_bot.properties_file
        self.reminders_file = input_bot.reminders_file
        self.load_files = True

    def load_properties(self):
        properties = None
        print("INFO: Twitbot loading config from file %s" % self.properties_file)
        if os.path.isfile(self.properties_file):
            try:
                with open(self.properties_file) as json_data:
                    data = json.load(json_data)
                    properties = Properties(data)
                    print("INFO: Twitbot has loaded config successfully")

            except KeyError as e:
                print("ERROR: Twitbot could NOT read expected config from file :: %s" % str(e))
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
                print("INFO: Twitbot file with reminders #%d" % len(reminders.list))
        else:
            self.load_files = False

        return reminders

    def execute(self) -> object:
        if not self.load_files:
            print("ERROR: The config files are not correct. Check paths and format")
            sys.exit(-1)

        try:
            properties = self.load_properties()
            connector = TwitterConnector(properties)
            connector.connect()
            time.sleep(5)
            while True:

                reminders = self.load_reminders();
                now = datetime.datetime.now()
                print("INFO: Processing reminders for date %s" % now)
                reminders = self.load_reminders()
                print("INFO: Filtering reminders #%d" % len(reminders))
                if len(reminders) == 0:
                    connector.execute(reminders.search_by_date(now.day, now.month))

                # Sleep iteration
                time.sleep(20)

        except:
            print("ERROR: The twitter connection properties are not correct. Review the config files'")
            connector.disconnect()
            sys.exit(-1)





