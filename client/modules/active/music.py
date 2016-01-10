'''
Created on Aug 13, 2015

@author: Connor
'''
from os import listdir
from os.path import isfile, join
import random
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
        response = input('Do you want to specify a directory? Y/N: ')
        if response == 'Y':
            music_dir = input('What is your music directory: ')
            shuffle = input('Do you want a specific song? Y/N: ')
            if shuffle == 'Y':
                song = input('What song do you want to be played?: ')
                play_mp3(song, music_dir) 
            else:
                songs = [f for f in listdir(music_dir) if isfile(join(music_dir, f))]
                while 1:
                    song = random.choice(songs)
                    while song.endswith(".mp3"):
                        play_mp3(song, music_dir)
                        song = random.choice(songs)
        else:
            play_mp3("limbo.mp3")
        
        
class Music(Module):

    def __init__(self):
        tasks = [PlaySongTask()]
        super().__init__(mod_name='music', mod_tasks=tasks, mod_priority=2)
