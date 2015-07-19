'''
Created on Jul 19, 2015

@author: Connor
'''
from client.task import Task
from client.modules.api_library import bitcoin_api

MOD_PRIORITY = 1

class GetValueTask(Task):
    URL = 'http://www.nactem.ac.uk/software/acromine/dictionary.py?sf='
    
    def match(self, text):
        for p in self.patterns:
            if p.match(text):
                return True
        return False
    
    def action(self, text):
        print('')
        print('~ 24 Hour Average: $'    + str(bitcoin_api.get_data('24h_avg')))
        print('~ Last Price: $'         + str(bitcoin_api.get_data('last')))
        print('')
        
def init():
    global tasks
    tasks = [GetValueTask([r'.*(\b)+bitcoin(\b)+.*'])]
