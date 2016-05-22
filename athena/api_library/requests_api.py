"""

A simple API for HTTP Requests (GET and POST)

"""

import json
import traceback

try:
    from urllib.request import urlopen, Request
    from urllib.parse import urlencode     # Python 3
except ImportError:
    from urllib2 import Request
    from urllib import urlopen, urlencode  # Python 2


def get(url, params=None, post=False, key=None):
    if params:
        data = urlencode(params).encode('utf-8')
    if post:
        req = Request(url, data)
    else:
        url += '?'+data
        req = Request(url)

    try:
        response = json.loads(urlopen(req).read().decode('utf-8'))
        if key:
            if key not in response:
                print('('+key+' key not found)')
                return None
            return response[key]
    except:
        print(traceback.format_exc())
        print('Error occurred fetching: '+url)
