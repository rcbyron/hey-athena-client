from __future__ import print_function

from athena.tests import dependencies_test
from athena.tests import input_test
from athena.tests import audio_test
from athena.tests import mic_test

print("---- Tests Passed? ----")
print("~ Dependencies:", dependencies_test.passed)
print("~ Basic Input:", input_test.passed)
print("~ Play Audio:", audio_test.passed)
print("~ Microphone:", mic_test.passed)
