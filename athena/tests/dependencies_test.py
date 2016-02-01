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
            import pyaudio  # @UnusedImport
        elif case is 1:
            from sphinxbase.sphinxbase import Config, Config_swigregister  # @UnusedImport
            from pocketsphinx.pocketsphinx import Decoder  # @UnusedImport
        elif case is 2:
            import speech_recognition  # @UnusedImport
        elif case is 3:
            from requests.exceptions import HTTPError  # @UnusedImport
            from gtts import gTTS  # @UnusedImport
        elif case is 4:
            import pyglet  # @UnusedImport
        elif case is 5:
            import yaml  # @UnusedImport
        elif case is 6:
            import wolframalpha  # @UnusedImport
        elif case is 7:
            import athena  # @UnusedImport
            import athena.brain  # @UnusedImport
        print('~ Import successful.')
    except:
        print(traceback.format_exc())
        print('~ Import failed!')
        passed = False

for i, _ in enumerate(dep):
    test_case(i)
if passed:
    print('\nDependencies Test PASSED! :)\n')
else:
    print('\n~ Dependencies Test failed :(\n')