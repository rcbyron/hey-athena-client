'''
Created on Jan 28, 2016

@author: Connor
'''
import traceback

from athena import brain
brain.init()

print('---- Running Input Test ----')

inputs = [
    "What's up?",
    "How's it going?",
    "Lol!"
]

try:
    for text in inputs:
        brain.inst.match_mods(text)
        brain.inst.execute_mods(text)
    print('~ Input Test passed! :)')
except:
    print(traceback.format_exc())
