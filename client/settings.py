'''
Created on Jan 9, 2016

@author: Connor
'''
import os, yaml

BASE_DIR = ".."
USERS_DIR = os.path.join(BASE_DIR, "users")

# Set these to False while debugging
USE_STT = True
USE_TTS = False

def load_user():
    with open(os.path.join(USERS_DIR, 'conzor.yml'), 'r') as f:
        doc = yaml.load(f)
        print(doc)