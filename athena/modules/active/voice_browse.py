'''
Created on Jan 30, 2016

@author: Connor
'''
from athena.classes.module import Module
from athena.classes.task import ActiveTask
from athena.modules.api_library import voice_browse_api

MOD_PARAMS = {
    'name': 'voice_browse',
    'priority': 2,
}

class VoiceBrowseTask(ActiveTask):
    
    def __init__(self, vb_api):
        super().__init__(patterns=[r'.*\b(?:search|look up|tell me about)\b(.*)',
                                   r'.*\b(?:go to|open)(.*\.(com|org|net|edu|gov|io|html))\b',
                                   r'.*\b(?:close(?: the| this)? (browser|tab|page))\b.*',
                                   r'.*\b(?:type)\b(.*)',
                                   r'.*\b(delete|clear the)\b.*',
                                   r'.*\b(maximize)\b.*',
                                   r'.*\b(click)\b.*',
                                   r'.*\b(?:next|switch the) (tab|page)\b.*'], api=vb_api)
    
    def match(self, text):
        for case, p in enumerate(self.patterns):            
            m = p.match(text)
            if m is not None:
                self.case = case
                self.q = m.group(1).strip()
                return True
        return False
    
    def action(self, text):
        if self.case is 0:       
            print('\n~ Searching '+self.q+'...')
            self.api.search(self.q)
        elif self.case is 1:
            if self.q[0:4] is not 'http':
                self.q = 'https://'+self.q.replace(' ', '')
            print('\n~ Opening '+self.q+'...')
            self.api.open(self.q)
        elif self.case is 2:
            print('\n~ Closing the '+self.q+'...')
            if 'browser' in self.q:
                self.api.close()
            else:
                self.api.close_tab()
        elif self.case is 3:
            print('\n~ Typing: '+self.q)
            self.api.type(self.q)
        elif self.case is 4:
            print('\n~ Maximizing...')
            self.api.maximize()
        elif self.case is 5:
            print('\n~ Clearing text...')
            self.api.clear()
        elif self.case is 6:
            print('\n~ Clicking...')
            self.api.click()
        elif self.case is 7:
            print('\n~ Switching the'+self.q+'...')
            self.api.switch_tab()


class VoiceBrowse(Module):
    
    def __init__(self):
        tasks = [VoiceBrowseTask(voice_browse_api.VoiceBrowseApi())]
        super().__init__(MOD_PARAMS, tasks)