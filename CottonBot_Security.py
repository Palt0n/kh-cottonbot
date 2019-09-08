
import sys
import os
from CottonBot.Utilities import get_EnvironmentVariable

# if os.path.isfile('set_env.sh'):
#     os.system('bash -c echo $PWD')
#     os.system('bash -c source set_env.sh')
# else:
#     print("The script set_env.sh file not found!")
#     print("It contains private required environment variables.")
#     print("Please refer to set_env.template.sh to create your own file.")
#     print("ERROR: The script set_env.sh file not found!")
#     sys.exit()

PATH_PHOTO = get_EnvironmentVariable('PATH_PHOTO')
PATH_STORE = get_EnvironmentVariable('PATH_STORE')
CHAT_ID_GROUP = get_EnvironmentVariable('CHAT_ID_GROUP')
CHATBOT_KEY = get_EnvironmentVariable('CHATBOT_KEY')

print("PATH_PHOTO={}".format(PATH_PHOTO))
print("PATH_STORE={}".format(PATH_STORE))
print("CHAT_ID_GROUP={}".format(CHAT_ID_GROUP))
print("CHAT_ID_GROUP={}".format(CHAT_ID_GROUP))

if None in [PATH_PHOTO, PATH_STORE, CHAT_ID_GROUP]:
    #raise IOError("Required environment variables not set!")
    print("ERROR: Some required environment variables are missing!")
    print("Did you forget to:")
    print("source set_env.sh")
    sys.exit()

TIME_MIN = 5
STATUS_SENDIMAGE = False
STATUS_POWER = True
STATUS_MOVEIMAGE = True
STATUS_BATTERY = '100'

def main():
    pass

main()
