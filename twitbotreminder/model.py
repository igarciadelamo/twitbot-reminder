class Properties:
    def __init__(self, json):
        self.consumer_key = json["connection"]["consumer-key"]
        self.consumer_secret = json["connection"]["consumer-secret"]
        self.token = json["connection"]["access-token"]
        self.token_secret = json["connection"]["access-token-secret"]
        self.me = json["me"]
        self.greeting = json["greeting"]
        self.welcome_text = json["welcome-text"]

class Reminder:
    def __init__(self, json):
        self.month = json["month"]
        self.dayOfMonth = json["dayOfMonth"]
        self.text = json["text"]

class ReminderList:
    def __init__(self, json):
        self.list = [Reminder(each) for each in json]

    def search_by_date(self, dayOfMonth, month):
        for item in self.list:
            if item.month == month and item.dayOfMonth == dayOfMonth: yield item

class InputBot:
  def __init__(self, properties, reminders, logs):
     self.properties_file = properties
     self.reminders_file = reminders
     self.logs_file = logs