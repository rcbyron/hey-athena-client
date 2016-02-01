'''
Created on Aug 13, 2015

@author: Connor
'''
from athena.classes.module import Module
from athena.classes.task import ActiveTask
from athena.tts import play_mp3

MOD_PARAMS = {
    'name': 'music',
    'priority': 2,
}

# Checks 'media' folder by default
TURN_UP_SONG = 'godj.mp3'

class PlaySongTask(ActiveTask):
    
    def __init__(self):
        super().__init__(patterns=[r'.*(\b)+turn(\s)+up(\b)+.*'])
         
    def match(self, text):
        return self.patterns[0].match(text) is not None
    
    def action(self, text):
        self.speak('Turning up...')
        play_mp3(TURN_UP_SONG)
        
        
class Music(Module):

    def __init__(self):
        tasks = [PlaySongTask()]
        super().__init__(MOD_PARAMS, tasks)
