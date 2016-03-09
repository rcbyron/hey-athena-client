"""

Global settings are stored here

"""

from os import mkdir, path

# Wake-up Word(s) must be in the sphinx dict file
# Change to 'hey athena' if background noise triggering occurs
WAKE_UP_WORD = 'athena'

# Set these to False while debugging
USE_STT = True
USE_TTS = True

# Max gTTS (speaking) string length
MAX_CHAR = 140

"""
LANGS = ['af', 'sq', 'ar', 'hy', 'ca', 'zh-CN', 'zh-TW', 'hr', 'cs',
         'da', 'nl', 'en', 'eo', 'fi', 'fr', 'de', 'el', 'ht', 'hi',
         'hu', 'is', 'id', 'it', 'ja', 'ko', 'la', 'lv', 'mk', 'no',
         'pl', 'pt', 'ro', 'ru', 'sr', 'sk', 'es', 'sw', 'sv', 'ta',
         'th', 'tr', 'vi', 'cy']
"""
LANG = 'en'
LANG_4CODE = 'en-US'

#####################
#    DIRECTORIES    #
#####################
CLIENT_DIR =    path.dirname(path.abspath(__file__))
BASE_DIR =      path.dirname(CLIENT_DIR)
CHROME_PATH =   path.join(CLIENT_DIR, 'chrome/chromedriver'     )
DATA_DIR =      path.join(CLIENT_DIR, 'data'                    )
LOGS_DIR =      path.join(DATA_DIR,   'logs'                    )
MEDIA_DIR =     path.join(DATA_DIR,   'media'                   )
INPUTS_DIR =    path.join(MEDIA_DIR,  'example_inputs'          )
RESPONSES_DIR = path.join(MEDIA_DIR,  'responses'               )
USERS_DIR =     path.join(DATA_DIR,   'users'                   )

# Get speech_recognition pocketsphinx models
import speech_recognition as sr
MODEL_DIR = path.join(path.dirname(path.abspath(sr.__file__)), 'pocketsphinx-data')

DIRS = [LOGS_DIR, MEDIA_DIR, INPUTS_DIR, RESPONSES_DIR, USERS_DIR]

for d in DIRS:
    if not path.exists(d):
        mkdir(d)

#####################
#     RESPONSES     #
#####################
ERROR = "Something went wrong. Would you like to see the error message?"
NO_MODULES = "I'm not sure how to respond to that."
NO_MIC = "I couldn't connect to a microphone."

#####################
#     FREE KEYS     #
#####################
WOLFRAM_KEY = '4QR84U-VY7T7AVA34'
WUNDERGROUND_KEY = 'd647ca403a0ac94b'
IFTTT_KEY = ''
