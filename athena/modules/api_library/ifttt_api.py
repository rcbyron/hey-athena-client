'''
Created on Feb 6, 2016

@author: Connor
'''
import urllib

from urllib import request

BASE_URL = 'https://maker.ifttt.com/trigger/'
KEY = ''

def trigger(event, val1=None, val2=None, val3=None):
    params = {}
    if val1:
        params['value1'] = val1
    if val2:
        params['value2'] = val2
    if val3:
        params['value3'] = val3
        
    req_url = BASE_URL+event+'/with/key/'+KEY+'?'+urllib.parse.urlencode(params)
    print('\n~ Making GET request at:')
    print(req_url+'\n')
    request.urlopen(req_url)
