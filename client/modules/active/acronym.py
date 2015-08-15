'''
Created on Jun 5, 2015

@author: Connor
'''
from client.classes.module import Module
from client.classes.task import ActiveTask
import urllib.request, json

class AcronymTask(ActiveTask):
    URL = 'http://www.nactem.ac.uk/software/acromine/dictionary.py?sf='
    
    def __init__(self):
        p_list = [r'.*(?:\b)+(\w+)\s(acronym\s)?(stand(s)?\sfor|mean|abbr(eviation)?)(?:\b)+.*']
        super().__init__(patterns=p_list)
    
    def match(self, text):
        for p in self.patterns:
            m = p.match(text)
            if m is not None:
                self.acronym = m.group(1)
                return True
        return False
    
    def action(self, text):
        print('\n~ Top acronym results for '+self.acronym+': ')
        acronyms = json.loads(urllib.request.urlopen(self.URL+self.acronym).read().decode('utf-8'))
        if not any(acronyms):
            print('~ No results.\n')
            return
        for meaning in acronyms[0]['lfs'][:10]:
            print('~ '+meaning['lf'])
        print('')
   
        
class Acronym(Module):

    def __init__(self):
        tasks = [AcronymTask()]
        super().__init__(mod_name='acronym', mod_tasks=tasks, mod_priority=2)

