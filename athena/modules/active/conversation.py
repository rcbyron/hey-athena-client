"""
    Responds to general conversation questions

    Usage Examples:
        - "What's up?"
        - "Tell me a joke"
"""

import re, random

from athena.classes.module import Module
from athena.classes.task import ActiveTask

""" Place the most specific regex keys first """
RESPONSES = {
    r'.*\b(joke(s)?)\b.*':
        ['I don\'t like country music, but I don\'t mean to denigrate those who do. And for the people who like country music, denigrate means \'put down\'.',
         'I want to die peacefully in my sleep, like my grandfather... Not screaming and yelling like the passengers in his car.',
         'I bought the world\'s worst thesaurus yesterday. Not only is it terrible, it\'s terrible.',
         'I have an EpiPen. My friend gave it to me when he was dying, it seemed very important to him that I have it.',
         'A termite walks into the bar and asks, "Is the bar tender here?"',
         '"I\'m sorry" and "I apologize" mean the same thing... except when you\'re at a funeral.',
         'Joke? Try looking in a mirror.'],
             
    r'.*\b(hey|hi|hello|(w(h)?(a|o|u)t(\')?s?(\s)+up(\?)?|s+u+p+))\b.*':
        ['Hey there! I\'m just computing numbers and such. You?',
         'Oh hey, I\'m just hanging out right now.',
         'Oh hey, I\'m just trying to solve p=np',
         'Hey, how\'s it going?'],
             
    r'.*\b(how(\')?s? (it going?|are you))\b.*':
        ['I\'m doing well. How about you?'],
    
    r'.*\b(lol|lmao|laugh out loud|rofl)\b.*':
        ['Haha what\'s so funny?'],
    
    r'.*\b(thanks)\b.*':
        ['You\'re welcome.'],
    
    r'.*\b(why not)\b.*':
        ['Because.'],
        
    r'.*\b(because why)\b.*':
        ['Just because okay?'],
        
    r'.*\b(ok(ay)?)\b.*':
        ['Yep.'],
    
    r'.*\b(yo+)\b.*':
        ['Sup holmes.',
         'Ayyyyy hombre.',
         'How\'s it goin\' ese???'],
             
    r'.*\b(no(pe)?|wrong)\b.*':
        ['Sorry, I am not perfect.'],
             
    r'.*\b(sweet|cool|awesome|neat|interesting|(s)?well|good|great)\b.*':
        ['\\1? good to hear.', '\\1? awesome.'],
        
    r'.*\b(nothin(g)?|nvm|nevermind)\b.*':
        ['\\1? okay then.', '\\1? okay.'],
        
    r'.*\b(aliens.*(exist|universe|space)|(believe|universe|space).*aliens)\b.*':
        ['Science has not confirmed that aliens exist, but the universe is expansive and full of mysteries.'],
}


class ConversationTask(ActiveTask):
    
    def match(self, text):
        for p, responses in RESPONSES.items():
            if re.search(p, text, re.IGNORECASE):
                self.response = re.sub(p, random.choice(responses), text)
                return True
        return False
    
    def action(self, text):
        self.speak(self.response)


class Conversation(Module):
    
    def __init__(self):
        tasks = [ConversationTask()]
        super().__init__('conversation', tasks, priority=2)
