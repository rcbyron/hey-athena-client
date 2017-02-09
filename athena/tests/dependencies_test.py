"""
A simple test script to check if all dependencies are installed
"""
print('---- Running Dependencies Test ----')

import time
import traceback

dep = ['PyAudio', 'pocketsphinx', 'SpeechRecognition', 'gTTS',
        'pygame', 'WolframAlpha', 'HeyAthena']

passed = True


def test_case(case):
    global passed
    try:
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
            import pygame
        elif case is 6:
            import wolframalpha
        elif case is 7:
            import athena
            import athena.brain
    except:
        print(traceback.format_exc())
        print('~ Import failed for:', dep[case])
        passed = False

for i in range(len(dep)):
    test_case(i)

if passed:
    print('---- TEST PASSED ---- \n')
else:
    print('\n~ Requires: ' + str(dep)[1:-1] + '\n')
    print('---- TEST FAILED :( ---- \n')

time.sleep(1)