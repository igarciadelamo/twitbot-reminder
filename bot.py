import sys
import getopt

from twitbotreminder import TwitbotReminder
from twitbotreminder.model import InputBot

HELP_TEXT = "bot.py -c <config_path>"
PROPERTIES_FILE = "/properties.json"
REMINDERS_FILE = "/reminders.json"
FOLDER = "sample"

def read_configuration(argv):
    try:
        opts, args = getopt.getopt(argv,"hc:",["config="])
        folder = FOLDER

    except getopt.GetoptError:
        print (HELP_TEXT)
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print (HELP_TEXT)
            sys.exit(0)
        elif opt in ['-c', '--config']:
            folder = arg

    return InputBot(folder + PROPERTIES_FILE, folder + REMINDERS_FILE)


if __name__ == "__main__":
    input_bot = read_configuration(sys.argv[1:])
    reminder = TwitbotReminder(input_bot)
    reminder.execute()
