'''
Created on Jul 19, 2015

@author: Connor
'''
from client.classes.module import Module
from client.classes.task import ActiveTask
from client.modules.api_library import bitcoin_api

class GetValueTask(ActiveTask):
    
    def __init__(self):
        patterns = [r'.*\b(bitcoin)\b.*']
        super().__init__(patterns)
    
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
        self.speak(str(bitcoin_api.get_data('last')), print_phrase=False)


class Bitcoin(Module):

    def __init__(self):
        tasks = [GetValueTask()]
        super().__init__(mod_name='bitcoin', mod_tasks=tasks, mod_priority=2)