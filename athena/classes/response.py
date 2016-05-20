"""
The "Response" class represents a cached audio response
"""

import os.path as path

from athena import settings


class Response():

    def __init__(self, key, text):
        self.key = key
        self.file = path.join(settings.RESPONSES_DIR, self.key+'.mp3')
        self.text = text

        if not path.isfile(self.file):
            pass
