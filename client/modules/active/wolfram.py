'''
Created on Jun 5, 2015

@author: Connor
'''
from client.task import Task
import wolframalpha

API_KEY = '4QR84U-VY7T7AVA34'
ERROR_MESSAGE = '\n~ Sorry, could you re-word the question?\n'

MOD_PRIORITY = 0
tasks = []

class AnswerTask(Task):
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
            print('\n~ '+texts.replace('|','')+'\n')
        else:
            print(ERROR_MESSAGE)
        
def init():
    global tasks
    tasks = [AnswerTask([r'.*\b(who|what|when|where|why|how)\b.*\?'])]
