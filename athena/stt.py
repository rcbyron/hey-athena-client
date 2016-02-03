'''
Created on Aug 6, 2015

@author: Connor
'''
import os, pyaudio, speech_recognition
import athena.tts as tts
import athena.settings as settings

from sphinxbase.sphinxbase import Config, Config_swigregister
from pocketsphinx.pocketsphinx import Decoder

"""
    Word(s) must be in the sphinx dict file
    Change to 'hey athena' if background noise triggering occurs
"""
WAKE_UP_WORD = 'athena'
ERROR_MESSAGE = 'Sorry, I could not understand that.'

def init():
    # Be wary of an OSError due to a race condition
    if not os.path.exists(settings.LOGS_DIR):
        os.makedirs(settings.LOGS_DIR)
    
    # Create a decoder with certain model
    config = Decoder.default_config()
    config.set_string('-logfn', os.path.join(settings.LOGS_DIR, 'passive-listen.log'))
    config.set_string('-hmm', os.path.join(settings.MODEL_DIR, 'en-us\en-us'))
    config.set_string('-lm', os.path.join(settings.MODEL_DIR, 'en-us\en-us.lm.dmp'))
    config.set_string('-dict', os.path.join(settings.MODEL_DIR, 'en-us\cmudict-en-us.dict'))
    config.set_string('-kws_threshold', '1e-50')
    
    # Decode streaming data
    global decoder, p
    decoder = Decoder(config)
    decoder.set_keyphrase('wakeup', WAKE_UP_WORD)
    decoder.set_search('wakeup')
    
    p = pyaudio.PyAudio()

def listen_keyword():
    global decoder, p
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
    stream.start_stream()
    p.get_default_input_device_info()
    
    print('~ Passive listening... ')
    decoder.start_utt()
    while True:
        buf = stream.read(1024)
        decoder.process_raw(buf, False, False)
        if decoder.hyp() != None and decoder.hyp().hypstr == WAKE_UP_WORD:
            decoder.end_utt()
            return
        else:
            continue
    decoder.end_utt()
    
def active_listen():
    r = speech_recognition.Recognizer()

    with speech_recognition.Microphone() as src:    # use the default microphone as the audio source
        r.adjust_for_ambient_noise(src)             # listen for 1 second to calibrate the energy threshold for ambient noise levels
        print('\n~ Active listening... ')
        tts.play_mp3('double-beep.mp3')
        audio = r.listen(src)                       # listen for the first phrase and extract it into audio data
    
    msg = ''
    try:
        msg = r.recognize_google(audio)             # recognize speech using Google Speech Recognition
        print('\n~ \''+msg+'\'')
    except LookupError:                             # speech is unintelligible
        msg = ''
        print('\n~ '+ERROR_MESSAGE+'\n')
        tts.speak(ERROR_MESSAGE)
    finally:
        return msg
