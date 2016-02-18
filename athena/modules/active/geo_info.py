"""
    Uses the external IP to find geographical info

    Usage Examples:
        - "What time is it?"
        - "Where am I?"
"""

from athena.classes.module import Module
from athena.classes.task import ActiveTask
from athena.api_library import geo_info_api

MOD_PARAMS = {
    'name': 'geo_info',
    'priority': 2,
}

class GetIPInfoTask(ActiveTask):
    
    def __init__(self):
        patterns = [r'.*\b(ip|country|region|city|latitude|longitude|isp|internet service provider|timezone|time|where (am I|are we)|location)\b.*']
        super().__init__(patterns)
        
        geo_info_api.update_data()
        self.groups = {1: 'query'}
    
    def match(self, text):
        return self.match_and_save_groups(text, self.groups)
    
    def action(self, text):
        if 'time' in self.query:
            self.speak('The time is '+geo_info_api.time())
            return
        
        self.speak(str(geo_info_api.get_data(self.query)))
        
        
class GeoInfo(Module):

    def __init__(self):
        tasks = [GetIPInfoTask()]
        super().__init__(MOD_PARAMS, tasks)

    