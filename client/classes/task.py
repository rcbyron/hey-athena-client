'''
Created on Jun 4, 2015

@author: Connor
'''

import abc, re
from client.tts import speak

class Task(object):
    @abc.abstractmethod
    def action(self, text):
        """Execute the task action."""
        return
    
    def speak(self, phrase, print_phrase=True):
        if print_phrase:
            print("\n~ "+phrase+"\n")
        speak(phrase)

class ActiveTask(Task):
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, patterns=[], priority=0, greedy=True,
                 regex_precompile=True, regex_ignore_case=True):
        if regex_precompile:
            if regex_ignore_case:
                self.patterns = [re.compile(p, re.IGNORECASE) for p in patterns]
            else:
                self.patterns = [re.compile(p) for p in patterns]
        else:
            self.patterns = patterns
        
        # Tasks are matched/sorted with priority in modules
        self.priority = priority
        
        # If task is matched, stop module from matching the proceeding tasks
        self.greedy = greedy
        
    @abc.abstractmethod
    def match(self, text):
        """Check if the task input criteria is met."""
        return
