'''
Created on Jun 18, 2015

@author: Connor
'''
import urllib.request, json

URL = 'https://api.bitcoinaverage.com/ticker/global/USD/'
response = '(undefined)'

def update():
    global response
    response = json.loads(urllib.request.urlopen(URL).read().decode('utf-8'))

def get_value():
    print(response)