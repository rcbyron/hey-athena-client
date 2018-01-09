"""
Basic Speech-To-Text tools are stored here
"""

import contextlib
import sys
import os
import pyaudio
import traceback
import speech_recognition

from athena import settings, tts, log

from pocketsphinx import DefaultConfig, Decoder, get_model_path, get_data_path

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
    # Create a decoder with certain model
    config = DefaultConfig()
    config.set_string('-logfn', settings.POCKETSPHINX_LOG)
    #config.set_string('-hmm',   settings.ACOUSTIC_MODEL)
    config.set_string('-hmm', os.path.join(get_model_path(), 'en-us'))
    config.set_string('-dict', os.path.join(get_model_path(), 'cmudict-en-us.dict'))
    #config.set_string('-lm',    settings.LANGUAGE_MODEL)
    config.set_string('-kws',   settings.KEYPHRASES)
    #config.set_string('-dict',  settings.POCKET_DICT)

    # Decode streaming data
    global decoder, p
    decoder = Decoder(config)
    p = pyaudio.PyAudio()

    global r
    r = speech_recognition.Recognizer()


def listen_keyword():
    """ Passively listens for the WAKE_UP_WORD string """
    with ignore_stderr():
        global decoder, p
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000,
                        input=True, frames_per_buffer=1024)
        stream.start_stream()

        log.info("Waiting to be woken up... ")
        # Process audio chunk by chunk. On keyword detected perform action and restart search
        decoder.start_utt()
        waiting = False
        wait_count = 0
        while True:
            buf = stream.read(1024, exception_on_overflow=False)
            decoder.process_raw(buf, False, False)
            if decoder.hyp():
                if decoder.hyp().hypstr[:13] == "athena cancel" or decoder.hyp().hypstr[:11] == "athena stop":
                    decoder.end_utt()
                    return "athena stop"
                else:
                    if waiting:
                        if wait_count >= 8:
                            decoder.end_utt()
                            return "athena"
                        else:
                            wait_count += 1
                    else:
                        waiting = True


def active_listen():
    """
    Actively listens for speech to translate into text
    :return: speech input as a text string
    """
    global r
    # use the default microphone as the audio source
    with ignore_stderr():
        with speech_recognition.Microphone() as src:
            # listen for 1 second to adjust energy threshold for ambient noise
            # r.adjust_for_ambient_noise(src)
            log.info("Active listening... ")
            tts.play_mp3('double-beep.wav')

            # listen for the first phrase and extract it into audio data
            audio = r.listen(src)

    msg = ''
    try:
        if settings.ACTIVE_ENGINE == "google":
            msg = r.recognize_google(audio, language=settings.LANG_4CODE)  # recognize speech using Google STT
        elif settings.ACTIVE_ENGINE == "sphinx":
            msg = r.recognize_sphinx(audio)
    except speech_recognition.UnknownValueError:
        log.info("Google Speech Recognition could not understand audio")
    except speech_recognition.RequestError as e:
        log.info("Could not request results from Google STT; {0}".format(e))
        log.info("Perhaps you need to update the 'SpeechRecognition' python package")
    except:
        log.info("Unknown exception occurred!")
        log.info(traceback.format_exc())
    finally:
        return msg

