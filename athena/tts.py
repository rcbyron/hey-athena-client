"""
Basic Text-To-Speech tools are stored here
"""

import contextlib
import sys
import pyglet
import tempfile
import os

from requests.exceptions import HTTPError
from gtts import gTTS

from athena import settings, log


@contextlib.contextmanager
def ignore_stderr():
    """ Ignore unwanted 'error' output from pyglet/pyaudio """
    devnull = os.open(os.devnull, os.O_WRONLY)
    old_stderr = os.dup(2)
    sys.stderr.flush()
    os.dup2(devnull, 2)
    os.close(devnull)
    try:
        yield
    finally:
        os.dup2(old_stderr, 2)
        os.close(old_stderr)


def init():
    # pyglet.options['audio'] = ('openal', 'directsound', 'silent')
    pyglet.lib.load_library('avbin')
    pyglet.have_avbin = True


def play_mp3(file_name, file_path=settings.MEDIA_DIR):
    """Plays a local MP3 file

    :param file_name: top-level file name (e.g. hello.mp3)
    :param file_path: directory containing file ('media' folder by default)
    """
    # Clear path list
    del pyglet.resource.path[:]
    pyglet.resource.path.append(file_path)
    pyglet.resource.reindex()

    with ignore_stderr():
        sound = pyglet.resource.media(file_name, streaming=False)
        sound.play()

        def exit_callback(dt):
            pyglet.app.exit()

        pyglet.clock.schedule_once(exit_callback, sound.duration)
        pyglet.app.run()


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
        tts = gTTS(text=phrase, lang=settings.LANG)

        if not cache:
            with tempfile.NamedTemporaryFile(mode='wb', suffix='.mp3',
                                             delete=False) as f:
                (temp_path, temp_name) = os.path.split(f.name)
                tts.write_to_fp(f)

            play_mp3(temp_name, temp_path)
            os.remove(os.path.join(temp_path, temp_name))
        else:
            filename = os.path.join(settings.RESPONSES_DIR, filename+'.mp3')
            tts.save(filename)
            log.info('Saved to: '+filename)

    except HTTPError as e:
        log.error('Google TTS might not be updated: '+str(e))
    except Exception as e:
        log.error('Unknown Google TTS issue: '+str(e))


