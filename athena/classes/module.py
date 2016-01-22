'''
Created on Aug 14, 2015

@author: Connor
'''

class Module(object):
    def __init__(self, mod_params, mod_tasks=[]):
        """ Make a unique mod name """
        self.name = mod_params['name']
        
        """ Modules match and execute in prioritized order """
        self.priority = mod_params['priority']
        
        """ Greedy mods stop future mods from being matched """
        self.greedy = mod_params['greedy']
        
        """ True if the mod is enabled """
        self.enabled = mod_params['enabled']

        """ Tasks find input text patterns and perform an action """
        self.tasks = mod_tasks