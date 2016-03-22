"""
Basic Text-To-Speech tools are stored here
"""

import pyglet, tempfile, os

from requests.exceptions import HTTPError
from gtts import gTTS

from athena import settings

def init():
    #pyglet.options['audio'] = ('openal', 'directsound', 'silent')
    pyglet.lib.load_library('avbin')
    pyglet.have_avbin=True
    
def play_mp3(file_name, file_path=settings.MEDIA_DIR):
    """
    Plays a local MP3 file
    
    :param file_name: top-level file name (e.g. hello.mp3)
    :param file_path: directory containing file ('media' folder by default)
    """
    pyglet.resource.path.clear()
    pyglet.resource.path.append(file_path)
    pyglet.resource.reindex()
    
    sound = pyglet.resource.media(file_name, streaming=False)
    sound.play()
    
    def exit_callback(dt):
        pyglet.app.exit()
        
    pyglet.clock.schedule_once(exit_callback, sound.duration)
    pyglet.app.run()

def speak(phrase, cache=False, filename='default', show_text=True):
    """
    Speaks a given text phrase
    
    :param phrase: text string to speak
    :param cache: if True, store .mp3 in 'media/responses'
    :raises HTTPError: if Google TTS fails to respond
    """
    if show_text:
        print('\n~ '+phrase+'\n')
    if not settings.USE_TTS:
        print('SPOKEN:', phrase)
        return
    
    try:
        phrase = phrase[:settings.MAX_CHAR]
        tts = gTTS(text=phrase, lang=settings.LANG)
        
        if not cache:
            with tempfile.NamedTemporaryFile(mode='wb', suffix='.mp3', delete=False) as f:
                (temp_path, temp_name) = os.path.split(f.name)
                tts.write_to_fp(f)
            
            play_mp3(temp_name, temp_path)
            os.remove(os.path.join(temp_path, temp_name))
        else:
            filename = os.path.join(settings.RESPONSES_DIR, filename+'.mp3')
            tts.save(filename)
            print('\n~ Saved to:', filename)
            
    except HTTPError as e:
        print('Google TTS might not be updated:', e)
    except Exception as e:
        print('Unknown Google TTS issue:', e)
