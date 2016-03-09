"""
    Wraps the Spotify Web Player to play music
    
    Requires:
        - Spotify username/password configuration

    Usage Examples:
        - "Play (song name XOR artist name)"
        - "Stop this song"
        - "Next song please"
"""

from athena.classes.module import Module
from athena.classes.task import ActiveTask
from athena.apis import api_lib

class PlaySongTask(ActiveTask):
    
    def __init__(self):
        super().__init__(patterns=[r'.*\bplay\s(.+)\b.*'])
        self.groups = {1: 'song'}
         
    def match(self, text):
        return self.match_and_save_groups(text, self.groups)
    
    def action(self, text):
        self.speak('Attempting to play song...')
        api_lib['spotify_api'].search(self.song)
        
        
class PauseSongTask(ActiveTask):
    
    def __init__(self):
        p_list = [r'.*\b(play|(un)?pause|stop|start)(\sth(e|is))?\ssong\b.*']
        super().__init__(patterns=p_list, priority=1)

    def action(self, text):
        self.speak('Toggling song...')
        api_lib['spotify_api'].play_pause_track()
        
        
class NextSongTask(ActiveTask):
    
    def __init__(self):
        super().__init__(patterns=[r'.*\b(next)\ssong\b.*'], priority=1)

    def action(self, text):
        self.speak('Next song...')
        api_lib['spotify_api'].next_track()
        
        
class Music(Module):

    def __init__(self):
        tasks = [PlaySongTask(), PauseSongTask(), NextSongTask()]
        super().__init__('spotify', tasks, priority=2)
