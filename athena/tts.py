'''
Created on Aug 12, 2015

@author: Connor
'''
import pyglet, tempfile, os
import athena.settings as settings

from requests.exceptions import HTTPError
from gtts import gTTS

"""
LANGS = ['af', 'sq', 'ar', 'hy', 'ca', 'zh-CN', 'zh-TW', 'hr', 'cs',
         'da', 'nl', 'en', 'eo', 'fi', 'fr', 'de', 'el', 'ht', 'hi',
         'hu', 'is', 'id', 'it', 'ja', 'ko', 'la', 'lv', 'mk', 'no',
         'pl', 'pt', 'ro', 'ru', 'sr', 'sk', 'es', 'sw', 'sv', 'ta',
         'th', 'tr', 'vi', 'cy']
"""

MAX_CHAR = 140
speaking = False

def init():
    #pyglet.options['audio'] = ('openal', 'directsound', 'silent')
    pyglet.lib.load_library('avbin')
    pyglet.have_avbin=True
    
def play_mp3(file_name, file_path=settings.MEDIA_DIR):
    pyglet.resource.path.clear()
    pyglet.resource.path.append(file_path)
    pyglet.resource.reindex()
    
    sound = pyglet.resource.media(file_name, streaming=False)
    sound.play()
    
    def exit_callback(dt):
        pyglet.app.exit()
        
    pyglet.clock.schedule_once(exit_callback, sound.duration)
    pyglet.app.run()

def filter_phrase(phrase):
    return phrase[:MAX_CHAR]

def speak(phrase):
    if not settings.USE_TTS:
        print('SPOKEN:', phrase)
        return
    global speaking
    if speaking:
        print('Warning: Speak was called multiple times too quickly')
        return
    speaking = True
    try:
        tts = gTTS(text=filter_phrase(phrase), lang='en')
        
        with tempfile.NamedTemporaryFile(mode='wb', suffix='.mp3', delete=False) as f:
            (temp_path, temp_name) = os.path.split(f.name)
            tts.write_to_fp(f)
        
        play_mp3(temp_name, temp_path)
        os.remove(os.path.join(temp_path, temp_name))
        speaking = False
    except HTTPError as e:
        print('Google TTS not working:', e)
    except Exception as e:
        print('Unknown Google TTS issue:', e)
