'''
Created on Jan 28, 2016

@author: Connor
'''
import traceback

print('---- Running Microphone Test ----')

try:
    print('\n~ Importing stt.py...')
    import athena.stt as stt
    print('~ Initializing stt.py...')
    stt.init()
    
    text = ''
    while 'q' not in text.lower():
        print('\n~ Type \'q\' at any time to quit')
        text = input('~ Test Active or Passive Listening? (A/P): ')
        if 'p' in text.lower():
            print('\n~ Wake Up Word: \''+stt.WAKE_UP_WORD+'\'')
            stt.listen_keyword()
            print('~ Wake Up Word Detected!')
        elif 'a' in text.lower():
            stt.active_listen()
    
    print('\nMicrophone Test PASSED! :)\n')
except Exception as e:
    print(traceback.format_exc())
    if 'invalid input device' in str(e).lower():
        print('\n~ PyAudio could not detect a microphone!')
        print('~ Try using a USB microphone and connecting it to different ports.')
        print('~ The test must be started with the microphone ALREADY plugged in.\n')
    else:
        print('\n~ Microphone Test failed :(\n')