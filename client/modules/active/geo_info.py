'''
Created on Jun 5, 2015

@author: Connor
'''
from client.task import Task
from client.modules.api_library import geo_info_api

MOD_PRIORITY = 1

class GetIPInfoTask(Task):
    def match(self, text):
        for p in self.patterns:
            m = p.match(text)
            if m is not None:
                self.query = m.group(1)
                return True
        return False
    
    def action(self, text):
        geo_info_api.update_data()
        
        title = self.query.title()
        if len(title) <= 3:
            title = title.upper()
            
        print('\n~ '+title+':',  geo_info_api.get_data(self.query), '\n')
        
def init():
    global tasks
    tasks = [GetIPInfoTask([r'.*(?:\b)+(ip|country|region|city|latitude|longitude|asn|isp|timezone)(?:\b)+.*'])]
    