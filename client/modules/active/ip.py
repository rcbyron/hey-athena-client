'''
Created on Jun 5, 2015

@author: Connor
'''
from client.task import Task
from client.modules.api_library import geo_ip_api

MOD_PRIORITY = 1

class GetIPTask(Task):
    def match(self, text):
        for p in self.patterns:
            if p.search(text):
                return True
        return False
    
    def action(self):
        geo_ip_api.update()
        print('\n~ External IP:', geo_ip_api.get_ip(), '\n')
        
def init():
    global tasks
    tasks = [GetIPTask([r'.*(\b)+ip(\b)+.*'])]
    