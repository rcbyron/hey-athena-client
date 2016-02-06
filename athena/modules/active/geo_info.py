'''
Created on Jun 5, 2015

@author: Connor
'''
from athena.classes.module import Module
from athena.classes.task import ActiveTask
from athena.modules.api_library import geo_info_api

MOD_PARAMS = {
    'name': 'geo_info',
    'priority': 2,
}

class GetIPInfoTask(ActiveTask):
    
    def __init__(self):
        patterns = [r'.*\b(ip|country|region|city|latitude|longitude|isp|internet service provider|timezone|time|where (am I|are we)|location)\b.*']
        super().__init__(patterns)
        
        geo_info_api.update_data()
    
    def match(self, text):
        for p in self.patterns:
            m = p.match(text)
            if m is not None:
                self.query = m.group(1)
                return True
        return False
    
    def action(self, text):
        if 'time' in self.query:
            print('\n~ The time is '+geo_info_api.time()+'\n')
            return
        
        title = self.query.title()
        if len(title) <= 3:
            title = title.upper()

        print('\n~ '+title+': '+str(geo_info_api.get_data(self.query))+'\n')
        
        
class GeoInfo(Module):

    def __init__(self):
        tasks = [GetIPInfoTask()]
        super().__init__(MOD_PARAMS, tasks)

    