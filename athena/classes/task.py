"""

The "Task" class represents an action to be performed

The "ActiveTask" class uses the "match" method to trigger an action.
Generally regex patterns are supplied to do the input matching.
The "match" method can be overriden with "return match_any(text)" to
trigger an action upon matching any given regex pattern.

"""

import re

from athena import tts

class Task(object):
    speak = staticmethod(tts.speak)
    
    def action(self, text):
        """ Execute the task action """
        return

class ActiveTask(Task):
    def __init__(self,
                 patterns=None,
                 words=None,
                 priority=0,
                 greedy=True,
                 regex_precompile=True,
                 regex_ignore_case=True):
        if patterns is None:
            patterns = []
        if words is None:
            words = []
        
        if words:
            p =  r'.*\b('
            p += str(words)[1:-1].replace('\'', '').replace(', ', '|')
            p += r')\b.*'
            patterns.append(p)
        
        if regex_precompile:
            if regex_ignore_case:
                self.patterns = [re.compile(p, re.IGNORECASE) for p in patterns]
            else:
                self.patterns = [re.compile(p) for p in patterns]
        else:
            self.patterns = patterns
        
        """ Tasks are matched/sorted with priority in modules """
        self.priority = priority
        
        """ If task is matched, stop module from matching the proceeding tasks """
        self.greedy = greedy
        
    def match(self, text):
        """ Check if the task input criteria is met """
        return self.match_any(text)

    def match_any(self, text):
        """ Check if any patterns match """
        for p in self.patterns:
            if p.match(text):
                return True
        return False

    def match_and_save_groups(self, text, group_key_dict):
        """
            Check if any patterns match,
            If so, save the match groups to self.(key name)
        """
        for case, p in enumerate(self.patterns):
            m = p.match(text)
            if m is not None:
                self.case = case
                for group_num, attribute_name in group_key_dict.items():
                    setattr(self, attribute_name, m.group(group_num).strip())
                return True
        return False
    