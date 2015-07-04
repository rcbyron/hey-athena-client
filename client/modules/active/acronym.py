'''
Created on Jun 5, 2015

@author: Connor
'''
from client.task import Task
import urllib.request, json

MOD_PRIORITY = 1

class AnswerTask(Task):
    URL = 'http://www.nactem.ac.uk/software/acromine/dictionary.py?sf='
    
    def match(self, text):
        for p in self.patterns:
            m = p.match(text)
            if m is not None:
                self.acronym = m.group(1)
                return True
        return False
    
    def action(self):
        print('\n~ Top acronym results for '+self.acronym+': ')
        acronyms = json.loads(urllib.request.urlopen(self.URL+self.acronym).read().decode('utf-8'))
        if not any(acronyms):
            print('~ No results.\n')
            return
        for meaning in acronyms[0]['lfs'][:10]:
            print('~ '+meaning['lf'])
        print('')
        
def init():
    global tasks
    tasks = [AnswerTask([r'.*(?:\b)+(\w+)\s(acronym\s)?(stand(s)?\sfor|mean|abbr(eviation)?)(?:\b)+.*'])]
