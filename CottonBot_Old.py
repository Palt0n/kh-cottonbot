
"""

source set_env.sh

"""
import sys
import os
from CottonBot.Utilities import get_EnvironmentVariable
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import os
import shutil
import re
from glob import glob
import datetime
import psutil

PATH_SENSOR = get_EnvironmentVariable('PATH_SENSOR')
PATH_SENSOR_STORE = get_EnvironmentVariable('PATH_SENSOR_STORE')
PATH_PHOTO = get_EnvironmentVariable('PATH_PHOTO')
PATH_PHOTO_STORE = get_EnvironmentVariable('PATH_PHOTO_STORE')
CHAT_ID_GROUP = get_EnvironmentVariable('CHAT_ID_GROUP')
CHATBOT_KEY = get_EnvironmentVariable('CHATBOT_KEY')

STATUS_SENDIMAGE = False
STATUS_POWER = True
STATUS_MOVEIMAGE = True
STATUS_BATTERY = '100'

print("PATH_SENSOR={}".format(PATH_SENSOR))
print("PATH_SENSOR_STORE={}".format(PATH_SENSOR_STORE))
print("PATH_PHOTO={}".format(PATH_PHOTO))
print("PATH_PHOTO_STORE={}".format(PATH_PHOTO_STORE))
print("CHAT_ID_GROUP={}".format(CHAT_ID_GROUP))
print("CHAT_ID_GROUP={}".format(CHAT_ID_GROUP))

if None in [PATH_PHOTO, PATH_PHOTO_STORE, CHAT_ID_GROUP, CHATBOT_KEY]:
    #raise IOError("Required environment variables not set!")
    print("ERROR: Some required environment variables are missing!")
    print("Did you forget to:")
    print("source set_env.sh")
    sys.exit()


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')
    update.message.reply_text('CHAT ID: {}'.format(update.message.chat.id))


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def test(bot, update):
    """Send a message when the command /test is issued."""
    update.message.reply_text('Test!')
    bot.sendMessage(chat_id=CHAT_ID_GROUP,text='TEST!')

def power(bot, update):
    """Send a message when the command /test is issued."""
    battery = psutil.sensors_battery()
    plugged = battery.power_plugged
    percent = str(battery.percent)
    if plugged is False:
        plugged = "Not Plugged In"
    else: 
        plugged="Plugged In"
    update.message.reply_text(percent+'% | '+plugged)

def echo(bot, update):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

def checkPower(bot, job):
    """Send a message when the command /test is issued."""
    global STATUS_POWER
    global STATUS_BATTERY
    battery = psutil.sensors_battery()
    plugged = battery.power_plugged
    percent = str(battery.percent)
    if plugged is False:
        plugged_string = "Not Plugged In"
    else: 
        plugged_string="Plugged In"
    message = percent+'% | '+plugged_string

    if plugged != STATUS_POWER:
        bot.sendMessage(chat_id=CHAT_ID_GROUP,text=message)
    elif plugged is False and percent != STATUS_BATTERY:
        bot.sendMessage(chat_id=CHAT_ID_GROUP,text=message)

    STATUS_BATTERY = percent
    STATUS_POWER = plugged

def sendImage(bot, job):
    global STATUS_MOVEIMAGE
    if STATUS_MOVEIMAGE is True:
        print("read STATUS_MOVEIMAGE to True")
        STATUS_MOVEIMAGE = False
        print("set STATUS_MOVEIMAGE to False")
        try:
            filepath_list = [y for x in os.walk(PATH_PHOTO) for y in glob(os.path.join(x[0], '*.jpg'))]
            if len(filepath_list) == 0:
                logging.info("No files to move")
            else:
                logging.info("{} files to move".format(len(filepath_list)))

            for filepath in filepath_list:
                filename = os.path.basename(filepath)
                filepath_new = filepath.replace(PATH_PHOTO,PATH_PHOTO_STORE)
                filedir_new = os.path.dirname(filepath_new)
                #filepath_new = os.path.join(PATH_PHOTO_STORE,filename)
                cam, caption = parse_filename(filename)
                if cam is not None:
                    if not os.path.exists(filedir_new):
                        os.makedirs(filedir_new)
                    logging.info('Moving {} to {}'.format(filepath, filepath_new))
                    if os.path.isfile(filepath):
                        shutil.move(filepath, filepath_new)
                        logging.info('Move Complete {}'.format(filename))
                    else:
                        logging.error('Move Unable {}'.format(filename))
                        
                    if STATUS_SENDIMAGE is True:
                        logging.info('Sending {}'.format(filename))
                        bot.send_photo(chat_id=CHAT_ID_GROUP, photo=open(filepath_new, 'rb'), caption=caption)
                        logging.info('Send Complete {}'.format(filename))
        finally:
            STATUS_MOVEIMAGE = True
        print("set STATUS_MOVEIMAGE to True")
    else:
        logging.warning("read STATUS_MOVEIMAGE is False")


def sendImage_arm(bot, update):
    global STATUS_SENDIMAGE
    STATUS_SENDIMAGE = True
    logging.info('STATUS_SENDIMAGE is True')
    update.message.reply_text('SendImage - ARMED')

def sendImage_disarm(bot, update):
    global STATUS_SENDIMAGE
    STATUS_SENDIMAGE = False
    logging.info('STATUS_SENDIMAGE is False')
    update.message.reply_text('SendImage - DISARMED')

def sendSensorImage(bot, job):
    filepath_list = [y for x in os.walk(PATH_SENSOR) for y in glob(os.path.join(x[0], '*.jpg'))]
    if len(filepath_list) == 0:
        logging.info("No files to move")
    else:
        logging.info("{} files to move".format(len(filepath_list)))
    
    if len(filepath_list) > 0:
        filepath = filepath_list[0]
        filename = os.path.basename(filepath)
        filepath_new = filepath.replace(PATH_SENSOR,PATH_SENSOR_STORE)
        filedir_new = os.path.dirname(filepath_new)

        if not os.path.exists(filedir_new):
            os.makedirs(filedir_new)
        logging.info('Moving {} to {}'.format(filepath, filepath_new))
        if os.path.isfile(filepath):
            shutil.move(filepath, filepath_new)
            logging.info('Move Complete {}'.format(filename))
        else:
            logging.error('Move Unable {}'.format(filename))
            
        logging.info('Sending {}'.format(filename))
        bot.send_photo(chat_id=CHAT_ID_GROUP, photo=open(filepath_new, 'rb'), caption='Sensor Triggered')
        logging.info('Send Complete {}'.format(filename))

class CamClass:
    def __init__(self, Name):
        self.Name = Name
        self.Time_Sent = datetime.datetime.now()
    
    def state_send(self):
        Time_Now = datetime.datetime.now()
        if Time_Now - self.Time_Sent > datetime.timedelta(seconds=TIME_MIN):
            self.Time_Sent = Time_Now
            return True
        else:
            return False

    def __str__(self):
        return self.Name

DICT_CAM = {
    '100' : CamClass('Living Room'),
    '110' : CamClass('Kitchen'),
    '120' : CamClass('Van'),
    '160' : CamClass('LeftSide'),
    #'130' : CamClass('Gate'),
}


DICT_EVENT = {
    'FACE_DETECTION' : 'A Face',
    'INTRUSION_DETECTION' : 'An Intrusion',
    'MOTION_DETECTION' : 'A Motion',
    'LINE_CROSSING_DETECTION' : 'An Entry',
    'PIR' : 'A PIR Motion',
    'LIGHT_GATE' : 'A Crossing'
}

def parse_filename(filename):
    REGEX_NAME = re.match(r'192\.168\.4\.(\d+)_01_(\d+)_([A-Z_]+).jpg',filename)
    if REGEX_NAME:
        cam = REGEX_NAME.group(1)
        event = REGEX_NAME.group(3)
        assert event in DICT_EVENT
        if cam in DICT_CAM:
            return DICT_CAM[cam], '{} was detected at the {}'.format(DICT_EVENT[event],DICT_CAM[cam])
        else:
            return None, 'No Camera: {}'.format(filename)
    else:
        return None, 'No Match: {}'.format(filename)

def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(CHATBOT_KEY)
    jobqueue = updater.job_queue
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("test", test))
    dp.add_handler(CommandHandler("power", power))
    dp.add_handler(CommandHandler("arm", sendImage_arm))
    dp.add_handler(CommandHandler("disarm", sendImage_disarm))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    jobqueue.run_repeating(sendImage, interval=5, first=0)
    jobqueue.run_repeating(checkPower, interval=5, first=0)
    jobqueue.run_repeating(sendSensorImage, interval=5, first=0)
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()