'''
Created on Jan 9, 2016

@author: Connor
'''
import os, yaml

def ensure_dir(d):
    if not os.path.exists(d):
        os.mkdir(d)

CLIENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CLIENT_DIR)
KEYS_DIR = os.path.join(CLIENT_DIR, '.credentials')
MODEL_DIR = os.path.join(CLIENT_DIR, 'models')
LOGS_DIR = os.path.join(CLIENT_DIR, 'logs')
MEDIA_DIR = os.path.join(CLIENT_DIR, 'media')
USERS_DIR = os.path.join(CLIENT_DIR, 'users')

DIRS = [KEYS_DIR, MODEL_DIR, LOGS_DIR, MEDIA_DIR, USERS_DIR]
for folder in DIRS:
    ensure_dir(folder)

# Set these to False while debugging
USE_STT = True
USE_TTS = True

inst = None
def init():
    global inst
    inst = Settings()

class Settings():
    def __init__(self):
        self.login()
        #self.load_keys()
        
    def find_users(self):
        """ Returns a list of available user strings """
        self.users = []
        for file in os.listdir(USERS_DIR):
            if file.endswith('.yml'):
                with open(os.path.join(USERS_DIR, file)) as f:
                    user = yaml.load(f)
                    self.users.append(user['user_api']['username'])
        return self.users
        
    def verify_users(self):
        """ Verify that at least 1 user exists """
        self.find_users()
        if not self.users:
            print('~ No users found. Please create a new user.\n')
            import athena.config as cfg
            cfg.generate()
            self.find_users()

    def load_user(self, username):
        with open(os.path.join(USERS_DIR, username+'.yml'), 'r') as f:
            self.user = yaml.load(f)
            print('\n~ Logged in as: '+self.user['user_api']['username'])
            
    def login(self):
        self.verify_users()
        if len(self.users) == 1:
            self.load_user(self.users[0])
            return
        
        print('~ Users: ', str(self.users)[1:-1])
        username = ''
        while username not in self.users:
            username = input('\n~ Username: ')
            if username not in self.users:
                print('\n~ Please enter a valid username')
                continue
        self.load_user(username)
        
    def load_keys(self):
        self.keys = None
        with open(os.path.join(KEYS_DIR, 'keys.yml'), 'r') as f:
            self.keys = yaml.load(f)
