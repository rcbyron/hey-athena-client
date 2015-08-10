'''
Created on Jun 1, 2015

@author: Connor
'''
import re, random

from client.task import Task


MOD_PRIORITY = 2

""" Place the most specific regex keys first """
RESPONSES = {
    r'.*(\b)+joke(s)?(\b)+.*':
        ['I don\'t like country music, but I don\'t mean to denigrate those who do. And for the people who like country music, denigrate means \'put down\'.',
         'I want to die peacefully in my sleep, like my grandfather... Not screaming and yelling like the passengers in his car.',
         'War does not determine who is right - only who is left.',
         'I bought the world\'s worst thesaurus yesterday. Not only is it terrible, it\'s terrible.',
         'I have an EpiPen. My friend gave it to me when he was dying, it seemed very important to him that I have it.',
         'A termite walks into the bar and asks, "Is the bar tender here?"',
         '"I\'m sorry" and "I apologize" mean the same thing... except when you\'re at a funeral.'],
             
    r'.*(\b)+(hey|hi|hello|(w(h)?(a|o|u)t(\'s)?(\s)+up(\?)?|s+u+p+))(\b)+.*':
        ['Hey there! I\'m just computing numbers and such. You?',
         'Oh hey, I\'m just hanging out right now.'],
    
    r'.*(\b)+y+o+(\b)+':
        ['Sup holmes.',
         'Ayyyyy hombre.',
         'How\'s it goin\' ese???'],
}

class ConversationTask(Task):
    def match(self, text):
        for p, responses in RESPONSES.items():
            if re.search(p, text, re.IGNORECASE):
                self.response = random.choice(responses)
                return True
        return False
    
    def action(self, text):
        print('\n~ '+self.response+'\n')

def init():
    global tasks
    tasks = [ConversationTask()]
