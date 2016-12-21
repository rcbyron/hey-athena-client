"""
A simple module for playing music

Usage Examples:
    - "Play some music"
    - "Turn up!"
"""

from athena.classes.module import Module
from athena.classes.task import ActiveTask
from athena.tts import play_mp3

# Checks 'media' folder by default
TURN_UP_SONG = 'godj.mp3'


class PlaySongTask(ActiveTask):

    def __init__(self):
        super(PlaySongTask, self).__init__(patterns=[r'.*\b(get turnt|turn up|play.*music)\b.*'])

    def action(self, text):
        self.speak('Turning up...')
        play_mp3(TURN_UP_SONG)


class Music(Module):

    def __init__(self):
        tasks = [PlaySongTask()]
        super(Music, self).__init__('music', tasks, priority=2)
