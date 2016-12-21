"""
A simple test script to check if all dependencies are installed
"""
import traceback

print('---- Running Dependencies Test ----')

dep = ['PyAudio', 'pocketsphinx', 'SpeechRecognition', 'gTTS',
        'pyglet', 'WolframAlpha', 'HeyAthena']

print('\n~ Requires: '+str(dep)[1:-1]+'\n')

passed = True


def test_case(case):
    global passed
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
        elif case is 6:
            import wolframalpha
        elif case is 7:
            import athena
            import athena.brain
        print('~ Import successful.')
    except:
        print(traceback.format_exc())
        print('~ Import failed!')
        passed = False

for i in range(len(dep)):
    test_case(i)

if passed:
    print('\nDependencies Test PASSED! :)\n')
else:
    print('\n~ Dependencies Test failed :(\n')