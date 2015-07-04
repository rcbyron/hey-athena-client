'''
Created on Jun 1, 2015

@author: Connor
'''
from client.task import Task
import random, urllib.request, json, html

MOD_PRIORITY = 1
RESPONSES = {
    r'.*(\b)+(hey|hi|hello|(w(h)?(a|o|u)t(\'s)?(\s)+up(\?)?|s+up))(\b)+.*':
        ['Hey there! I\'m just computing numbers and such. You?',
         'Oh hey, I\'m just hanging out right now.'],
    
    r'.*(\b)+yo+(\b)+':
        ['Sup holmes.',
         'Ayyyyy hombre.',
         'How\'s it goin\' ese???']
}

class ConversationTask(Task):
    def match(self, text):
        for p, responses in RESPONSES.items():
            if p.match(text):
                self.response = random.choice(responses)
                return True
        return False
    
    def action(self):
        print('\n~ '+self.response+'\n')
        
class JokeTask(Task):
    URL = 'http://api.icndb.com/jokes/random'
    
    def match(self, text):
        for p in self.patterns:
            if p.match(text):
                return True
        return False
    
    def action(self):
        joke_json = json.loads(urllib.request.urlopen(self.URL).read().decode('utf-8'))
        print('\n~ '+html.unescape(joke_json['value']['joke'])+'\n')

def init():
    global tasks
    tasks = [ConversationTask(priority=1), JokeTask([r'.*(\b)+joke(s)?(\b)+.*'])]
