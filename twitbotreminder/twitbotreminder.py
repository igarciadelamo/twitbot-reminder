import time
import sys
import json
import os

module_exists = False

try:
    import twitter

    module_exists = True
except:
    print("ERROR: The 'twitter' library can not be loaded. It could be installed using 'pip install twitter'")


class TwitbotProperties:
    def __init__(self, json):
        self.consumer_key = json["consumer-key"]
        self.consumer_secret = json["consumer-secret"]
        self.access_token = json["access-token"]
        self.access_token_secret = json["access-token-secret"]

class TwitbotReminder:
    def __init__(self, properties_file, reminders_file):
        self.properties = None
        self.reminders = None
        self.load_files = True

        self.load_properties(properties_file)
        self.load_reminders(reminders_file)


    def load_properties(self, properties):
        print("Twitbot loading config from file %s" % properties)
        if os.path.isfile(properties):
            try:
                with open(properties) as json_data:
                    data = json.load(json_data)
                    self.properties = TwitbotProperties(data)
                    print("Twitbot has loaded config successfully")
            except KeyError as e:
                print("Twitbot could NOT read expected config from file :: %s" % str(e))
                self.load_files = False
        else:
            self.load_files = False

    def load_reminders(self, reminders):
        if os.path.isfile(reminders):
            with open(reminders) as json_data:
                data = json.load(json_data)
                self.reminders = data
                print("Twitbot file with reminders %s" % reminders)
        else:
            self.load_files = False

    def run(self) -> object:
        if not module_exists:
            sys.exit(-1)

        if not self.load_files:
            print("ERROR: The config files are not correct. Check paths and format")
            sys.exit(-1)

        while True:
            time.sleep(2)
            self._do_something()

    def _do_something(self):
        print("The time is now %s" % time.ctime())
