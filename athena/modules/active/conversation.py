'''
Created on Jun 1, 2015

@author: Connor
'''
import re, random

from athena.classes.module import Module
from athena.classes.task import ActiveTask

MOD_PARAMS = {
    'name': 'conversation',
    'priority': 2,
}

""" Place the most specific regex keys first """
RESPONSES = {
    r'.*\b(joke(s)?)\b.*':
        ['I don\'t like country music, but I don\'t mean to denigrate those who do. And for the people who like country music, denigrate means \'put down\'.',
         'I want to die peacefully in my sleep, like my grandfather... Not screaming and yelling like the passengers in his car.',
         'War does not determine who is right - only who is left.',
         'I bought the world\'s worst thesaurus yesterday. Not only is it terrible, it\'s terrible.',
         'I have an EpiPen. My friend gave it to me when he was dying, it seemed very important to him that I have it.',
         'A termite walks into the bar and asks, "Is the bar tender here?"',
         '"I\'m sorry" and "I apologize" mean the same thing... except when you\'re at a funeral.',
         'Joke? Try looking in a mirror.'],
             
    r'.*\b(hey|hi|hello|(w(h)?(a|o|u)t(\'s)?(\s)+up(\?)?|s+u+p+))\b.*':
        ['Hey there! I\'m just computing numbers and such. You?',
         'Oh hey, I\'m just hanging out right now.',
         'Oh hey, I\'m just trying to solve p=np',
         'Hey, how\'s it goin\' yo?'],
    
    r'.*\b(y+o+)\b.*':
        ['Sup holmes.',
         'Ayyyyy hombre.',
         'How\'s it goin\' ese???'],
             
    r'.*\b(sweet|cool)\b.*':
        ['Cool? Sweet? indeed.'],
    
    r'.*\b(movie(s)?)\b.*':
        ['My master hasn\'t created a "movies" module for me yet. Maybe you could help me?'],
}

class ConversationTask(ActiveTask):
    
    def match(self, text):
        for p, responses in RESPONSES.items():
            if re.search(p, text, re.IGNORECASE):
                self.response = random.choice(responses)
                return True
        return False
    
    def action(self, text):
        self.speak(self.response)


class Conversation(Module):
    
    def __init__(self):
        tasks = [ConversationTask()]
        super().__init__(MOD_PARAMS, tasks)
