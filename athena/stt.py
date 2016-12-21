"""
Basic Speech-To-Text tools are stored here
"""

import pyaudio
import speech_recognition

from athena import settings, tts, log

from sphinxbase.sphinxbase import Config, Config_swigregister
from pocketsphinx.pocketsphinx import Decoder


def init():
    # Create a decoder with certain model
    config = Decoder.default_config()
    config.set_string('-logfn', settings.POCKETSPHINX_LOG)
    config.set_string('-hmm',   settings.ACOUSTIC_MODEL)
    config.set_string('-lm',    settings.LANGUAGE_MODEL)
    config.set_string('-dict',  settings.POCKET_DICT)

    # Decode streaming data
    global decoder, p
    decoder = Decoder(config)
    decoder.set_keyphrase('wakeup', settings.WAKE_UP_WORD)
    decoder.set_search('wakeup')
    p = pyaudio.PyAudio()

    global r
    r = speech_recognition.Recognizer()
    # r.recognize_google(settings.LANG_4CODE)


def listen_keyword():
    """ Passively listens for the WAKE_UP_WORD string """
    with tts.ignore_stderr():
        global decoder, p
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000,
                        input=True, frames_per_buffer=1024)
        stream.start_stream()
        p.get_default_input_device_info()

    log.info("Waiting to be woken up... ")
    decoder.start_utt()
    while True:
        buf = stream.read(1024)
        decoder.process_raw(buf, False, False)
        if decoder.hyp() and decoder.hyp().hypstr == settings.WAKE_UP_WORD:
            decoder.end_utt()
            return
    decoder.end_utt()


def active_listen():
    """
    Actively listens for speech to translate into text
    :return: speech input as a text string
    """
    global r
    # use the default microphone as the audio source
    with tts.ignore_stderr():
        with speech_recognition.Microphone() as src:
            # listen for 1 second to adjust energy threshold for ambient noise
            # r.adjust_for_ambient_noise(src)
            log.info("Active listening... ")
            tts.play_mp3('double-beep.mp3')

            # listen for the first phrase and extract it into audio data
            audio = r.listen(src)

    msg = ''
    try:
        msg = r.recognize_google(audio)  # recognize speech using Google STT
    except speech_recognition.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except speech_recognition.RequestError as e:
        print("Could not request results from Google STT; {0}".format(e))
    except:
        print("Unknown exception occurred!")
    finally:
        return msg
