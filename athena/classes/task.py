'''
Created on Jun 4, 2015

@author: Connor
'''
import re

from athena.tts import speak

class Task(object):
    def action(self, text):
        """ Execute the task action """
        return
    
    def speak(self, phrase, show_text=True):
        if show_text:
            print('\n~ '+phrase+'\n')
        speak(phrase)

class ActiveTask(Task):
    def __init__(self,
                 patterns=[],
                 priority=0,
                 api=None,
                 greedy=True,
                 regex_precompile=True,
                 regex_ignore_case=True):
        
        if regex_precompile:
            if regex_ignore_case:
                self.patterns = [re.compile(p, re.IGNORECASE) for p in patterns]
            else:
                self.patterns = [re.compile(p) for p in patterns]
        else:
            self.patterns = patterns
        
        """ Tasks are matched/sorted with priority in modules """
        self.priority = priority
        
        """ Optional API object to use """
        self.api = api
        
        """ If task is matched, stop module from matching the proceeding tasks """
        self.greedy = greedy
        
    def match(self, text):
        """ Check if the task input criteria is met """
        return False
