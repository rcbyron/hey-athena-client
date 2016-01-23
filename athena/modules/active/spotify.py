'''
Created on Jan 10, 2016

@author: Connor
'''
from athena.classes.module import Module
from athena.classes.task import ActiveTask
from athena.modules.api_library import spotify_api

MOD_PARAMS = {
    'name': 'spotify',
    'priority': 2,
}

class PlaySongTask(ActiveTask):
    
    def __init__(self, s_api):
        super().__init__(patterns=[r'.*\bplay\s(.+)\b.*'], api=s_api)
         
    def match(self, text):
        m = self.patterns[0].match(text)
        if m is not None:
            self.song = m.group(1)
            return True
        return False
    
    def action(self, text):
        self.speak('Attempting to play song...')
        self.api.search(self.song)
        
        
class PauseSongTask(ActiveTask):
    
    def __init__(self, s_api):
        p_list = [r'.*\b(play|(un)?pause|stop|start)(\sth(e|is))?\ssong\b.*']
        super().__init__(patterns=p_list, priority=1, api=s_api)
         
    def match(self, text):
        return self.patterns[0].match(text) is not None

    def action(self, text):
        self.speak('Toggling song...')
        self.api.play_pause_track()
        
        
class NextSongTask(ActiveTask):
    
    def __init__(self, s_api):
        super().__init__(patterns=[r'.*\b(next)\ssong\b.*'], priority=1, api=s_api)
         
    def match(self, text):
        return self.patterns[0].match(text) is not None

    def action(self, text):
        self.speak('Next song...')
        self.api.next_track()
        
        
class Music(Module):

    def __init__(self):
        s_api = spotify_api.SpotifyApi()
        tasks = [PlaySongTask(s_api), PauseSongTask(s_api), NextSongTask(s_api)]
        super().__init__(MOD_PARAMS, tasks)
