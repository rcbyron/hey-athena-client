"""

A simple API for HTTP Requests (GET and POST)

"""

import json, traceback

from urllib import parse, request

def get(url, params=None, post=False, key=None):
    if params:
        data = parse.urlencode(params).encode('utf-8')
    if post:
        req = request.Request(url, data)
    else:
        url += '?'+data
        req = request.Request(url)
        
    try:
        response = json.loads(request.urlopen(req).read().decode('utf-8'))
        if key:
            if key not in response:
                print('('+key+' key not found)')
                return None
            return response[key]
    except:
        print(traceback.format_exc())
        print('Error occurred fetching: '+url)
