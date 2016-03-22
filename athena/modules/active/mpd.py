from athena.classes.module import Module
from athena.classes.task import ActiveTask

from mpd import MPDClient

client = MPDClient()
client.connect("192.168.0.150", 6600)

class PauseSongTask(ActiveTask):
    def __init__(self):
        p_list = [r'.*\b(play|(un)?pause|stop|start)(\sth(e|is))?\ssong\b.*']
        super().__init__(patterns=p_list, priority=1)

    def action(self, text):
        self.speak('Toggling song...')
        client.pause()
    
class PlaySongTask(ActiveTask):
    def __init__(self):
        super().__init__(patterns=[r'.*\bplay\s(.+)\b.*'])
        self.groups = {1: 'song'}
        
    def match(self, text):
        return self.match_and_save_groups(text, self.groups)
    
    def action(self, text):
        self.speak('Attempting to play song...')
        playlist_results = client.playlistsearch('title', self.song)
        if not playlist_results:
            #search_results = client.search('title', self.song)
            playlist_results = client.searchadd('title', self.song)
        if playlist_results:
            client.playid(playlist_results[0]['id'])
            
class NextSongTask(ActiveTask):
    def __init__(self):
        super().__init__(patterns=[r'.*\b(next)\ssong\b.*'], priority=1)
        
    def action(self, text):
        self.speak('Next song...')
        client.next()

class VolumeUpTask(ActiveTask):
    def __init__(self):
        super().__init__(patterns=[r'.*\b(increase)\svolume\b.*'], priority=1)
        
    def action(self, text):
        self.speak('increasing volume...')
        vol_inc = 5
        if (int(client.status()['volume']) + vol_inc) < 100:
            new_vol = int(client.status()['volume']) + vol_inc 
        else:
            new_vol = 100
        client.setvol(new_vol)

class VolumeDownTask(ActiveTask):
    def __init__(self):
        super().__init__(patterns=[r'.*\b(decrease)\svolume\b.*'], priority=1)

    def action(self, text):
        self.speak('decreasing volume...')
        vol_inc = -5
        if (int(client.status()['volume']) + vol_inc) < 100:
            new_vol = int(client.status()['volume']) + vol_inc 
        else:
            new_vol = 100
        client.setvol(new_vol)

class Music(Module):
    def __init__(self):
        tasks = [PlaySongTask(), PauseSongTask(), NextSongTask(), VolumeUpTask(), VolumeDownTask()]
        super().__init__('music', tasks, priority=2)