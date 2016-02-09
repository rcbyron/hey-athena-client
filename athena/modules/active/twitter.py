'''
Created on Feb 6, 2016

@author: Connor
'''
from athena.classes.module import Module
from athena.classes.task import ActiveTask
from athena.modules.api_library import ifttt_api as ifttt

MOD_PARAMS = {
    'name': 'twitter',
    'priority': 2,
}

class SendTweetTask(ActiveTask):
    
    def __init__(self):
        super().__init__(patterns=[r'.*\btweet (.*)', r'.*\bpost (.*)\bto twitter\b.*'])
         
    def match(self, text):
        for p in self.patterns:
            m = p.match(text)
            if m is not None:
                self.tweet = m.group(1)
                return True
        return False
    
    def action(self, text):
        self.speak('Sending tweet...')
        ifttt.trigger('voice_tweet', self.tweet)
        
        
class Twitter(Module):

    def __init__(self):
        tasks = [SendTweetTask()]
        super().__init__(MOD_PARAMS, tasks)
