"""
A simple test script for passive/active listening
"""
print('---- Running Audio Test ----')

try:
    input = raw_input  # Python 2 fix
except NameError:
    pass

import pygame
import time

from pygame import mixer

passed = True

mixer.pre_init(16000, -16, 2, 1024)
mixer.init()
mixer.music.load("../data/media/responses/test.mp3")

print("~ Attempting to play audio...")
mixer.music.play()
while mixer.music.get_busy():
    pygame.time.delay(100)
resp = "something"
while True:
    resp = input("~ Audio test complete! Did you hear Athena speaking? (Y/N): ")
    if resp[0].lower() == "y":
        print("---- TEST PASSED ----\n")
        break
    elif resp[0].lower() == "n":
        passed = False
        print("---- TEST FAILED :( ----\n")
        break
time.sleep(1)