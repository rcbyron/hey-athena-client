'''
Created on Jan 9, 2016

@author: Connor
'''
from client.classes.module import Module
from client.classes.task import ActiveTask
import client.tts as tts
import random as r

EMOTION_CHANCE = 0.5

# Relative emotion weights (should add to 1)
EMOTIONS = {
    0: 0.15, # HUMOR
    1: 0.1,  # SASS
    2: 0.35, # OPTIMISM
    3: 0.4,  # ADMIRATION
}
RESPONSES = {
    0: ["Self destructing in 3... 2... 1... (kidding... calm down)"],
    1: ["I'll answer that when I please.", "I don't feel like answering that right now."],
    2: ["I'll answer that, but first let me say, today is a great day."],
    3: ["By the way, have I told you that you're the coolest person I've met?"],
}

class BuildEmotionTask(ActiveTask):
    
    def match(self, text):
        return r.random() < EMOTION_CHANCE
    
    def action(self, text):
        rand = r.random()
        chance = 0
        for k, v in EMOTIONS.items():
            chance += v
            if (rand < chance):
                tts.speak(r.choice(RESPONSES[k]))
                break
        
class Emotion(Module):

    def __init__(self):
        tasks = [BuildEmotionTask()]
        super().__init__(mod_name='emotion', mod_tasks=tasks, mod_priority=2, mod_greedy=False)

    