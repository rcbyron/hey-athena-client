'''
Created on Jun 18, 2015

@author: Connor
'''
import urllib.request, json

URL = 'http://www.telize.com/geoip'
response = '(undefined)'

def update():
    global response
    response = json.loads(urllib.request.urlopen(URL).read().decode('utf-8'))
    
def get_ip():
    return response