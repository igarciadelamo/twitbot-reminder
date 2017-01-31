import sys
import getopt

from twitbotreminder.twitbotreminder import TwitbotReminder
from twitbotreminder.model import InputBot

HELP_TEXT = "bot.py -c <config_path> -l <log_dir>"
PROPERTIES_FILE = "/properties.json"
REMINDERS_FILE = "/reminders.json"
LOG_FILE = "/twitbot-reminder.log"
CONFIG_DIRECTORY = "sample"
LOG_DIRECTORY = "./"


def read_configuration(argv):
    try:
        opts, args = getopt.getopt(argv,"hc:l:",["config=", "logdir="])
        config = CONFIG_DIRECTORY
        logs = LOG_DIRECTORY

    except getopt.GetoptError:
        print (HELP_TEXT)
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print (HELP_TEXT)
            sys.exit(0)
        elif opt in ['-c', '--config']:
            config = arg
        elif opt in ['-l', '--logdir']:
            logs = arg

    return InputBot(config + PROPERTIES_FILE, config + REMINDERS_FILE, logs + LOG_FILE )


if __name__ == "__main__":
    input_bot = read_configuration(sys.argv[1:])
    reminder = TwitbotReminder(input_bot)
    reminder.execute()
