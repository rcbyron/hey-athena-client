'''
Created on Jan 9, 2016

@author: Connor
'''
import os, yaml

CLIENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CLIENT_DIR)
MODEL_DIR = os.path.join(BASE_DIR, "models")
LOGS_DIR = os.path.join(BASE_DIR, "logs")
MEDIA_DIR = os.path.join(BASE_DIR, "media")
USERS_DIR = os.path.join(CLIENT_DIR, "users")

# Set these to False while debugging
USE_STT = True
USE_TTS = False

# Obtained from Wunderground
WEATHER_API_KEY = 'd647ca403a0ac94b'

def load_user():
    with open(os.path.join(USERS_DIR, 'conzor.yml'), 'r') as f:
        doc = yaml.load(f)
        print(doc)