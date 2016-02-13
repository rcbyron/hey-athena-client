'''
Created on Feb 6, 2016

@author: Connor
'''
from athena.classes.module import Module
from athena.classes.task import ActiveTask
from athena.api_library import ifttt_api as ifttt

MOD_PARAMS = {
    'name': 'twitter',
    'priority': 2,
}

class SendTweetTask(ActiveTask):
    
    def __init__(self):
        super().__init__(patterns=[r'.*\btweet (.*)',
                                   r'.*\bpost (.*)\bto twitter\b.*'])
        
        self.groups = {1: 'tweet'}
         
    def match(self, text):
        return self.match_and_save_groups(text, self.groups)
    
    def action(self, text):
        self.speak('Sending tweet...', show_text=True)
        ifttt.trigger('voice_tweet', self.tweet)
        
        
class Twitter(Module):

    def __init__(self):
        tasks = [SendTweetTask()]
        super().__init__(MOD_PARAMS, tasks)
