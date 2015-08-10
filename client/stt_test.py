'''
Created on Aug 7, 2015

@author: Connor
'''
from os import path

from pocketsphinx.pocketsphinx import Decoder
from sphinxbase.sphinxbase import *

MODELDIR = "C:\\Workspace\\c-cpp\\pocketsphinx\\model"
DATADIR = "C:\\Workspace\\c-cpp\\pocketsphinx\\test\\data"

# Create a decoder with certain model
config = Decoder.default_config()
config.set_string('-logfn', 'null')
config.set_string('-hmm', path.join(MODELDIR, 'en-us/en-us'))
config.set_string('-lm', path.join(MODELDIR, 'en-us/en-us.lm.dmp'))
config.set_string('-dict', path.join(MODELDIR, 'en-us/cmudict-en-us.dict'))
decoder = Decoder(config)

# Decode streaming data.
decoder = Decoder(config)

import pyaudio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
stream.start_stream()

decoder.start_utt()
#stream = open(path.join(DATADIR, 'goforward.raw'), 'rb')
while True:
    buf = stream.read(1024)
    decoder.process_raw(buf, False, False)
    if decoder.hyp() != None:
        print(decoder.hyp().hypstr)
    else:
        #break
        continue
decoder.end_utt()
#print ('Best hypothesis segments: ', [seg.word for seg in decoder.seg()])