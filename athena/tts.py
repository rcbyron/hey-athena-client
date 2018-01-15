"""
Basic Text-To-Speech tools are stored here
"""

import tempfile
import os
import pygame

from requests.exceptions import HTTPError
from gtts import gTTS
from pygame import mixer
from athena import settings, log


def init():
    """ Initialize the pygame mixer """
    mixer.init()

def play_mp3(file_name, file_path=settings.MEDIA_DIR, blocking=False):
    """Plays a local MP3 file

    :param file_name: top-level file name (e.g. hello.mp3)
    :param file_path: directory containing file ('media' folder by default)
    :param blocking: if false, play mp3 in background
    """
    if ".mp3" in file_name:
        mixer.music.load(os.path.join(file_path, file_name))
        mixer.music.play()
    else:
        sound = pygame.mixer.Sound(os.path.join(file_path, file_name))
        chan = pygame.mixer.find_channel()
        chan.queue(sound)

    if blocking:
        while mixer.music.get_busy():
            pygame.time.delay(100)


def speak(phrase, cache=False, filename='default', show_text=True, log_text=True):
    """Speaks a given text phrase

    :param phrase: text string to speak
    :param cache: if True, store .mp3 in 'media/responses'
    :param filename: filename if cached
    :param show_text: if True, store .mp3 in 'media/responses'
    :param cache: if True, store .mp3 in 'media/responses'
    """
    if show_text:
        log.info(phrase)
    if not settings.USE_TTS:
        log.info('SPOKEN: '+phrase)
        return

    try:
        phrase = phrase[:settings.MAX_CHAR]
        tts = gTTS(text=phrase, lang=settings.LANG_CODE)

        if not cache:
            with tempfile.NamedTemporaryFile(mode='wb', suffix='.mp3',
                                             delete=False) as f:
                (temp_path, temp_name) = os.path.split(f.name)
                tts.write_to_fp(f)

            play_mp3(temp_name, temp_path)
            os.remove(os.path.join(temp_path, temp_name))
        else:
            filename = os.path.join(settings.RESPONSES_DIR, filename+'.wav')
            tts.save(filename)
            log.info('Saved to: '+filename)

    except HTTPError as e:
        log.error('Google TTS might not be updated: '+str(e))
    except Exception as e:
        log.error('Unknown Google TTS issue: '+str(e))


