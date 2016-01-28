'''
Created on Jan 28, 2016

@author: Connor
'''
import traceback

print('---- Running Dependencies Test ----')

dep = ['PyAudio', 'pocketsphinx', 'SpeechRecognition', 'gTTS',
        'pyglet', 'PyYAML', 'WolframAlpha', 'AthenaVoice']

print('\n~ Requires: '+str(dep)[1:-1]+'\n')

passed = True

def test_case(case):
    try:
        print('~ Checking dependency:', dep[case])
        if case is 0:
            import pyaudio
        elif case is 1:
            from sphinxbase.sphinxbase import Config, Config_swigregister
            from pocketsphinx.pocketsphinx import Decoder
        elif case is 2:
            import speech_recognition
        elif case is 3:
            from requests.exceptions import HTTPError
            from gtts import gTTS
        elif case is 4:
            import pyglet
        elif case is 5:
            import yaml
        elif case is 6:
            import wolframalpha
        elif case is 7:
            import athena
            import athena.brain
        print('~ Import successful.')
    except Exception as e:
        print(traceback.format_exc())
        print('~ Import failed!')
        passed = False

for i, _ in enumerate(dep):
    test_case(i)
if passed:
    print('\nDependencies Test PASSED! :)\n')
else:
    print('\n~ Dependencies Test failed :(\n')