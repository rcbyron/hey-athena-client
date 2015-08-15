'''
Created on Jun 5, 2015

@author: Connor
'''
from client.classes.module import Module
from client.classes.task import ActiveTask
import wolframalpha

API_KEY = '4QR84U-VY7T7AVA34'
ERROR_MESSAGE = 'Sorry, could you re-word the question?'

MOD_PRIORITY = 1
tasks = []

class AnswerTask(ActiveTask):
    def __init__(self):
        p_list = [r'.*\b(who|what|when|where|why|how|(can|are) you)\b.*']
        super().__init__(patterns=p_list)
    
    def match(self, text):
        for p in self.patterns:
            if p.match(text):
                return True
        return False
    
    def action(self, text):
        query = wolframalpha.Client(API_KEY).query(text)
        if len(query.pods) > 1:
            pod = query.pods[1]
            if pod.text:
                texts = pod.text
            else:
                texts = ERROR_MESSAGE

            self.speak(texts.replace('|',''))
        else:
            self.speak(ERROR_MESSAGE)
        
class Wolfram(Module):

    def __init__(self):
        tasks = [AnswerTask()]
        super().__init__(mod_name='wolfram', mod_tasks=tasks, mod_priority=1)

