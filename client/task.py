'''
Created on Jun 4, 2015

@author: Connor
'''

import abc, re

class Task(object):
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, patterns=[], priority=0, task_greedy=True, mod_greedy=False,
                 regex_precompile=True, regex_ignore_case=True):
        if regex_precompile:
            if regex_ignore_case:
                self.patterns = [re.compile(p, re.IGNORECASE) for p in patterns]
            else:
                self.patterns = [re.compile(p) for p in patterns]
        else:
            self.patterns = patterns
        self.priority = priority
        self.task_greedy = task_greedy
        self.mod_greedy = mod_greedy
        
    @abc.abstractmethod
    def match(self, text):
        """Check if the task input criteria is met."""
        return
    
    @abc.abstractmethod
    def action(self, text):
        """Execute the task action."""
        return