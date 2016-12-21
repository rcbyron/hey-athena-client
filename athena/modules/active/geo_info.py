"""
Uses the external IP to find geographical info

Usage Examples:
    - "What time is it?"
    - "Where am I?"
"""

from athena.classes.module import Module
from athena.classes.task import ActiveTask
from athena.api_library import geo_info_api


class GetIPInfoTask(ActiveTask):

    def __init__(self):
        match_words = ['ip', 'country', 'region', 'city', 'latitude',
                       'longitude', 'isp', 'internet service provider',
                       'timezone', 'time', 'where am I', 'where are we',
                       'location']
        super(GetIPInfoTask, self).__init__(words=match_words)

        # geo_info_api.update_data()
        self.groups = {1: 'query'}

    def match(self, text):
        return self.match_and_save_groups(text, self.groups)

    def action(self, text):
        if 'time' in self.query:
            self.speak('It\'s currently'+geo_info_api.time())
            return

        geo_info_api.update_data()
        self.speak(str(geo_info_api.get_data(self.query)))


class GeoInfo(Module):

    def __init__(self):
        tasks = [GetIPInfoTask()]
        super(GeoInfo, self).__init__('geo_info', tasks, priority=3)
