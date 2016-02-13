'''
Created on Jul 19, 2015

@author: Connor
'''
from athena.classes.module import Module
from athena.classes.task import ActiveTask
from athena.api_library import bitcoin_api

MOD_PARAMS = {
    'name': 'bitcoin',
    'priority': 2,
}

class GetValueTask(ActiveTask):
    
    def __init__(self):
        super().__init__(patterns=[r'.*\b(bitcoin)\b.*'])
    
    def match(self, text):
        return self.match_any(text)
    
    def action(self, text):
        val = str(bitcoin_api.get_data('last'))
        self.speak(val)


class Bitcoin(Module):
    
    def __init__(self):
        tasks = [GetValueTask()]
        super().__init__(MOD_PARAMS, tasks)