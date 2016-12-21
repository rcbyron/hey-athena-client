"""
A simple test script to see if the brain is responding to input
"""
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
