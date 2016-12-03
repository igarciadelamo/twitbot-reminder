import os
import sys
import getopt

from twitbotreminder import TwitbotReminder

HELP_TEXT = "bot.py -c <config_file> -r <reminder_file>"

class ConfigFiles(object):

  def __init__(self, properties, reminders):
     self.properties_file = properties
     self.reminders_file = reminders


def read_configuration(argv):
    try:
        opts, args = getopt.getopt(argv,"hp:r:",["properties=","reminders="])
        properties_file = "sample/properties-sample.json"
        reminders_file = "sample/reminders-sample.json"
    except getopt.GetoptError:
      print (HELP_TEXT)
      sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print (HELP_TEXT)
            sys.exit(0)
        elif opt in ("-p", "--properties"):
            properties_file = arg
        elif opt in ("-r", "--reminder"):
            reminders_file = arg
    return ConfigFiles(properties_file, reminders_file)


if __name__ == "__main__":
    conf = read_configuration(sys.argv[1:])
    reminder = TwitbotReminder(conf.properties_file, conf.reminders_file)
    reminder.run()
