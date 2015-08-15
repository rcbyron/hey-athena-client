'''
Created on Jun 5, 2015

@author: Connor
'''
from client.classes.module import Module
from client.classes.task import ActiveTask
from client.modules.api_library import geo_info_api

class GetIPInfoTask(ActiveTask):
    
    def __init__(self):
        p_list = [r'.*(?:\b)+(ip|country|region|city|latitude|longitude|asn|isp|timezone)(?:\b)+.*']
        super().__init__(patterns=p_list)
    
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
        
class GeoInfo(Module):

    def __init__(self):
        tasks = [GetIPInfoTask()]
        super().__init__(mod_name='geo_info', mod_tasks=tasks, mod_priority=2)

    