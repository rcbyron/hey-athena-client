'''
Created on Aug 14, 2015

@author: Connor
'''

import abc

class Module(object):
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, mod_name='unnamed', mod_tasks=[], mod_priority=0, mod_greedy=True, enabled=True):
        self.name = mod_name
        self.tasks = mod_tasks
        self.priority = mod_priority
        self.greedy = mod_greedy
        self.enabled = enabled