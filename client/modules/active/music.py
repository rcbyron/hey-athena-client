'''
Created on Aug 13, 2015

@author: Connor
'''
from client.classes.module import Module
from client.classes.task import ActiveTask
from client.tts import play_mp3

class PlaySongTask(ActiveTask):
    
    def __init__(self):
        super().__init__(patterns=[r'.*(\b)+turn(\s)+up(\b)+.*'])
         
    def match(self, text):
        for p in self.patterns:
            if p.match(text):
                return True
        return False
    
    def action(self, text):
        self.speak("Turning up...")
        play_mp3("limbo.mp3")
        
        
class Music(Module):

    def __init__(self):
        tasks = [PlaySongTask()]
        super().__init__(mod_name='music', mod_tasks=tasks, mod_priority=2)
