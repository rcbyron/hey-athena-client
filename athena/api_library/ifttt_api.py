"""

A simple IFTTT trigger tool
| API Documentation: https://ifttt.com/maker

"""

import urllib

from urllib import request

from athena import settings

BASE_URL = 'https://maker.ifttt.com/trigger/'

def trigger(event, val1=None, val2=None, val3=None):
    params = {}
    if val1:
        params['value1'] = val1
    if val2:
        params['value2'] = val2
    if val3:
        params['value3'] = val3
        
    req_url = BASE_URL+event+'/with/key/'+settings.IFTTT_KEY+'?'+urllib.parse.urlencode(params)
    print('\n~ Making GET request at:')
    print(req_url+'\n')
    request.urlopen(req_url)
