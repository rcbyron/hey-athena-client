'''
Created on Feb 11, 2016

@author: Connor
'''
from athena import tts
    
print('~ Enter \'q\' at any time to quit')
while True:
    
    fname = input('\n~ Unique Filename: ')
    if len(fname) is 0 or 'q' in fname[0].lower():
        break
    
    phrase = input('~ Phrase: ')
    if len(phrase) is 0 or 'q' in phrase[0].lower(): 
        break
    
    tts.speak(phrase, cache=True, filename=fname)