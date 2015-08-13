'''
Created on Aug 12, 2015

@author: Connor
'''
from gtts import gTTS
import pyglet, tempfile, os

LANGS = ['af', 'sq', 'ar', 'hy', 'ca', 'zh-CN', 'zh-TW', 'hr', 'cs',
         'da', 'nl', 'en', 'eo', 'fi', 'fr', 'de', 'el', 'ht', 'hi',
         'hu', 'is', 'id', 'it', 'ja', 'ko', 'la', 'lv', 'mk', 'no',
         'pl', 'pt', 'ro', 'ru', 'sr', 'sk', 'es', 'sw', 'sv', 'ta',
         'th', 'tr', 'vi', 'cy']

MAX_CHAR = 140

def init():
    #pyglet.options['audio'] = ('openal', 'directsound', 'silent')
    pyglet.lib.load_library('avbin')
    pyglet.have_avbin=True

def filter_phrase(phrase):
    return phrase[:MAX_CHAR]

def speak(phrase):
    tts = gTTS(text=filter_phrase(phrase), lang='en')
      
    with tempfile.NamedTemporaryFile(mode='wb', suffix='.mp3', delete=False) as f:
        (temp_path, temp_name) = os.path.split(f.name)
        tts.write_to_fp(f)
    
    #print(temp_path, " --- ", temp_name)
    pyglet.resource.path.append(temp_path)
    #pyglet.resource.reindex()
    #print(pyglet.resource.path)
    
    sound = pyglet.resource.media(temp_name, streaming=False)
    sound.play()
    
    def exit_callback(dt):
        pyglet.app.exit()
        
    pyglet.clock.schedule_once(exit_callback, sound.duration)
    pyglet.app.run()
    
    os.remove(os.path.join(temp_path, temp_name))