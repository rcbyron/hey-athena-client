'''
Created on Jun 18, 2015

@author: Connor
'''
import urllib.request, json

NUM_RANDOM_NUMBERS = 1
URL = 'http://qrng.anu.edu.au/API/jsonI.php?length='+NUM_RANDOM_NUMBERS+'&type=uint8'
response = '(undefined)'

def update():
    global response
    response = json.loads(urllib.request.urlopen(URL).read().decode('utf-8'))

def flip_coin():
    update()
    if int(response['data'][0]) < 128:
        return 'HEADS!'
    else:
        return 'TAILS!'