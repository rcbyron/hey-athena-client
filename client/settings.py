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
USERS_DIR = os.path.join(BASE_DIR, "users")

# Set these to False while debugging
USE_STT = True
USE_TTS = False

# Obtained from Wunderground
WEATHER_API_KEY = 'd647ca403a0ac94b'

user_info = None

def load_user():
    global user_info
    users = []
    for file in os.listdir(USERS_DIR):
        if file.endswith(".yml"):
            with open(os.path.join(USERS_DIR, file)) as f:
                user_info = yaml.load(f)
                users.append(user_info['username'])
    print("~ Users: ", str(users)[1:-1])
    
    valid_user = False
    while not valid_user:
        user = input("\n~ Username: ")
        if user not in users:
            print("\n~ Please enter a valid username")
            continue
        with open(os.path.join(USERS_DIR, user+'.yml'), 'r') as f:
            user_info = yaml.load(f)
            print("\n~ Logged in as: "+user_info['username'])
            break