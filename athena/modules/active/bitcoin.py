'''
Created on Jul 19, 2015

@author: Connor
'''
from athena.classes.module import Module
from athena.classes.task import ActiveTask
from athena.modules.api_library import bitcoin_api

MOD_PARAMS = {
    'name': 'bitcoin',
    'priority': 2,
}

class GetValueTask(ActiveTask):
    
    def __init__(self):
        super().__init__(patterns=[r'.*\b(bitcoin)\b.*'])
    
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
        self.speak(str(bitcoin_api.get_data('last')))


class Bitcoin(Module):
    
    def __init__(self):
        tasks = [GetValueTask()]
        super().__init__(MOD_PARAMS, tasks)