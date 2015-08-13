'''
Created on Aug 13, 2015

@author: Connor
'''
from client.task import Task

MOD_PRIORITY = 2

class GetValueTask(Task):
    URL = 'http://www.nactem.ac.uk/software/acromine/dictionary.py?sf='
    
    def match(self, text):
        for p in self.patterns:
            if p.match(text):
                return True
        return False
    
    def action(self, text):
        self.speak("Turning up...")
        open(r"C:\Workspace\py\CORA\client\turnup.mp3")
        
def init():
    global tasks
    tasks = [GetValueTask([r'.*(\b)+turn(\s)+up(\b)+.*'])]
