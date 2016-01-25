'''
Created on Jun 1, 2015

@author: Connor

API Documentation:
http://www.wunderground.com/weather/api/d/docs
'''

import urllib.request, json, time, re

import athena.settings as settings
import athena.config as cfg
import athena.tts as tts

DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
BASE_URL = 'http://api.wunderground.com/api/'
URL_DATA_TYPES = {
    'conditions': '/conditions/q/',
    'forecast':   '/forecast/q/',
    'geolookup':  '/geolookup/q/'
}
API_KEY = 'd647ca403a0ac94b'

def config():
    weather_info = {}
    prompt1 = 'Default Zip Code or City or Airport Code: '
    prompt2 = 'Default State or Country: '
    weather_info['zip-iata-city'] = cfg.safe_input(prompt1, require=True)
    weather_info['state-country'] = cfg.safe_input(prompt2)
    return weather_info

# Number of seconds to wait before a call will update the data
UPDATE_CONDITIONS_INT = 120
UPDATE_FORECAST_INT   = 120

class WeatherApi():
    def __init__(self):
        self.c_update_time  = -UPDATE_CONDITIONS_INT
        self.fc_update_time = -UPDATE_FORECAST_INT
        self.restore_flag = False
        
        if not 'weather_api' in settings.inst.user:
            raise Exception
        self.default_zip_iata_city = settings.inst.user['weather_api']['zip-iata-city']
        self.default_state_country = settings.inst.user['weather_api']['state-country']
        self.key = API_KEY
        if not self.update_loc(self.default_zip_iata_city, self.default_state_country):
            raise Exception
    
    def get_json_data(self, data_type, loc_extension=None):
        """ Returns the desired JSON weather data """
        url = BASE_URL+self.key+URL_DATA_TYPES[data_type]
        if not loc_extension:
            url += self.loc_extension
        else:
            url += loc_extension
        return json.loads(urllib.request.urlopen(url).read().decode('utf-8'))

    def load_conditions(self):
        if time.time() - self.c_update_time > UPDATE_CONDITIONS_INT:
            """ Load current weather conditions in c_data """
            self.c_data = self.get_json_data('conditions')['current_observation']
            self.c_update_time = time.time()

    def load_forecast(self):
        if time.time() - self.fc_update_time > UPDATE_FORECAST_INT:
            """ Load 3-day forecast in fc_list """
            self.fc_list = self.get_json_data('forecast')['forecast']['txt_forecast']['forecastday']
            self.fc_update_time = time.time()
    
    def try_set_loc(self, zip_iata_city, state_country=None):
        if not self.update_loc(zip_iata_city, state_country):
            print('\n~ Location not found using:')
            if state_country:
                print('~ City:', zip_iata_city)
                print('~ State/Country:', state_country+'\n')
            else:
                print('~ Zip/Airport Code:', zip_iata_city+'\n')
            print('~ TIP: use underscores for spaces within names (e.g. "new_york_city")\n')
            tts.speak('Location not found.')
            return False
        return True
    
    def update_loc(self, new_zip_iata_city, new_state_country=''):
        """ Updates the location, if valid
        
        Returns:
            True if successful, False if failed
        """
        test_ext = new_zip_iata_city+'.json'
        if new_state_country:
            test_ext = new_state_country+'/'+test_ext
        
        loc_data = self.get_json_data('geolookup', test_ext)
        if 'location' in loc_data:
            self.loc_extension = test_ext
            self.zip_iata_city = new_zip_iata_city
            self.state_country = new_state_country
            
            """ Force weather data to update """
            self.c_update_time  = -UPDATE_CONDITIONS_INT
            self.fc_update_time = -UPDATE_FORECAST_INT
                
            return True
        return False
    
    def restore_loc(self):
        if self.restore_flag:
            self.update_loc(self.default_zip_iata_city, self.default_state_country)
            self.restore_flag = False
            
    def location(self):
        if self.state_country:
            return self.zip_iata_city.replace('_', ' ').title()+', '+self.state_country.replace('_', ' ').upper()
        if len(self.zip_iata_city) is 3:
            return self.zip_iata_city.upper()
        return self.zip_iata_city.replace('_', ' ').title()

    def temperature(self):
        return self.c_data['temperature_string']
    
    def feels_like(self):
        return self.c_data['feelslike_string']
    
    def humidity(self):
        return self.c_data['relative_humidity']
    
    def wind_speed(self):
        return self.c_data['wind_string']
    
    def uv_index(self):
        return self.c_data['UV']
    
    def precip_today(self):
        return self.c_data['precip_today_string']
    
    def precip_1_hr(self):
        return self.c_data['precip_1hr_string'].replace('( ', '(')
    
    def visibility(self):
        return self.c_data['visibility_mi']
    
    def pressure(self):
        return self.c_data['pressure_in']
    
    def conditions(self):
        return self.c_data['weather']

    def fc_day(self, period):
        """ Gets the forecast given a list of period numbers 0-7 """
        if period > 7:
            return ('I don\'t have any further forecasts beyond 3 days.', '')
        return (self.fc_list[period]['title'], self.fc_list[period]['fcttext'])

    def get_day(self, offset):
        """ Get the day string relative to today """
        return DAYS[(self.today_num()+offset)%7]
    
    def today_num(self):
        """ Get the weekday number of today """
        self.load_forecast()
        return DAYS.index(self.fc_day(0)[0].lower().replace(' night', ''))

    def replace_day_aliases(self, text):
        """ Replaces day aliases with usable day names """
        text = re.sub(r'(.*)\b(day after tomorrow|next day)\b(.*)',             '\\1'+self.get_day(2)+'\\3', text, re.IGNORECASE)
        text = re.sub(r'(.*)\b(tomorrow)\b(.*)',                                '\\1'+self.get_day(1)+'\\3', text, re.IGNORECASE)
        text = re.sub(r'(.*)\b(today|now|current(?:ly)?|present(?:ly)?)\b(.*)', '\\1'+self.get_day(0)+'\\3', text, re.IGNORECASE)
        text = re.sub(r'(.*)\b(yesterday)\b(.*)',                               '\\1'+self.get_day(6)+'\\3', text, re.IGNORECASE)
        return text
