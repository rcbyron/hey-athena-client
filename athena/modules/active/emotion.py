"""
    Randomly generates responses based on "emotion" chances
"""

import random as r

from athena.classes.module import Module
from athena.classes.task import ActiveTask
from athena import brain

EMOTION_CHANCE = 0.1

# Relative emotion weights (should add to 1)
EMOTIONS = {
    0: 0.15, # HUMOR
    1: 0.1,  # SASS
    2: 0.35, # OPTIMISM
    3: 0.4,  # ADMIRATION
}

RESPONSES = {
    0: ["Beep boop. Computing a response...",
        "I actually have no idea how to respond... Psych!",
        "Self destructing in 3... 2... 1... (kidding... calm down)"],
    1: ["I'll respond when I please. Okay?",
        "I don't feel like responding to that right now. But I will."],
    2: ["First let me say, today is a great day."],
    3: ["You are a fascinating human.", 
        "By the way, you're pretty cool.",
        "By the way, have I told you that you're the coolest person I've met?"],
}


class BuildEmotionTask(ActiveTask):
    
    def match(self, text):
        return r.random() < EMOTION_CHANCE
    
    def action(self, text):
        if len(brain.inst.matched_mods) > 1:
            rand = r.random()
            chance = 0
            for k, v in EMOTIONS.items():
                chance += v
                if (rand < chance):
                    self.speak(r.choice(RESPONSES[k]))
                    break
        
        
class Emotion(Module):

    def __init__(self):
        tasks = [BuildEmotionTask()]
        super().__init__('emotion', tasks, priority=3, greedy=False)

    