'''
Created on Jun 18, 2015

@author: Connor

API Documentation:
https://qrng.anu.edu.au/API/api-demo.php
'''
import urllib.request, json

DEFAULT_CACHE_SIZE = 1024
URL = 'http://qrng.anu.edu.au/API/jsonI.php?length='

EXTENSIONS = {
    0: '&type=uint8',
    1: '&type=uint16',
    2: '&type=hex16&size=1'
}

MAX_SIZES = {
    0: 256,
    1: 65536,
    2: 0xFF
}

class TrueRandomNumCache():
    def __init__(self, cache_type, cache_size=DEFAULT_CACHE_SIZE):
        self.max_size = MAX_SIZES[cache_type]
        self.cache_size = cache_size
        self.url = URL+str(cache_size)+EXTENSIONS[cache_type]
        self.update_cache()
        self.index = 0

    def update_cache(self):
        self.num_cache = json.loads(urllib.request.urlopen(self.url).read().decode('utf-8'))['data']

    def random(self):
        num = self.num_cache[self.index]
        self.index += 1
        self.index %= self.cache_size
        if not self.index:
            self.update_cache()
        return num
    
    def random_range(self, offset=0, num_range=2):
        return int((self.random() / self.max_size) * num_range) + offset
