"""
A simple test script to see if the brain is responding to input
"""
print('---- Running Input Test ----')

import traceback
import time

from athena import settings
from athena.brain import Brain

settings.USE_STT = False
settings.USE_TTS = False
my_brain = Brain(greet_user=False)

inputs = [
    "What's up?",
    "How's it going?",
    "Lol!"
]

passed = True

try:
    for text in inputs:
        my_brain.match_mods(text)
        my_brain.execute_mods(text)
    print('---- TEST PASSED ----\n')
except:
    passed = False
    print(traceback.format_exc())

time.sleep(1)