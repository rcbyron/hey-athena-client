'''
Created on Aug 6, 2015

@author: Connor
'''
from os import path

from sphinxbase.sphinxbase import Config, Config_swigregister #@UnusedImport
from pocketsphinx.pocketsphinx import Decoder
import pyaudio

# NOTE: this requires PyAudio because it uses the Microphone class
import speech_recognition as sr

MODELDIR = "C:\\Workspace\\c-cpp\\pocketsphinx\\model"
DATADIR = "C:\\Workspace\\c-cpp\\pocketsphinx\\test\\data"

# Must be in the sphinx dict file
WAKE_UP_WORD = "icarus"

def init():
    # Create a decoder with certain model
    config = Decoder.default_config()
    config.set_string('-logfn', 'null')
    config.set_string('-hmm', path.join(MODELDIR, 'en-us/en-us'))
    config.set_string('-lm', path.join(MODELDIR, 'en-us/en-us.lm.dmp'))
    config.set_string('-dict', path.join(MODELDIR, 'en-us/cmudict-en-us.dict'))
    
    global decoder, p
    # Decode streaming data.
    decoder = Decoder(config)
    decoder.set_keyphrase("wakeup", WAKE_UP_WORD)
    decoder.set_search("wakeup")
    
    p = pyaudio.PyAudio()

def listen_keyword():
    global decoder, p
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
    stream.start_stream()
    
    decoder.start_utt()
    while True:
        buf = stream.read(1024)
        decoder.process_raw(buf, False, False)
        if decoder.hyp() != None and decoder.hyp().hypstr == WAKE_UP_WORD:
            decoder.end_utt()
            #print(decoder.hyp().hypstr)
            return
        else:
            continue
    decoder.end_utt()
    
def active_listen():
    p = pyaudio.PyAudio()
    r = sr.Recognizer()
    
    with sr.Microphone() as source:                 # use the default microphone as the audio source
        r.adjust_for_ambient_noise(source)          # listen for 1 second to calibrate the energy threshold for ambient noise levels
        audio = r.listen(source)                    # listen for the first phrase and extract it into audio data
    
    try:
        return r.recognize(audio)                   # recognize speech using Google Speech Recognition
    except LookupError:                             # speech is unintelligible
        print("Could not understand audio.")
