'''
Created on Jun 1, 2015

@author: Connor
'''

from client.task import Task
from client.modules.api_library import weather_api
import re

MOD_PRIORITY = 2
DEFAULT_ZIP_IATA_CITY = 'plano'
DEFAULT_STATE_COUNTRY = 'tx'

class CurrentDayTask(Task):    
    def match(self, text):
        text = weather_api.replace_day_aliases(text)
        
        """ Invalid if text contains a non-current day """
        invalid_days = list(weather_api.DAYS)
        invalid_days.remove(weather_api.get_day(0))
        if any(day in text.lower() for day in invalid_days):
            return False
        
        """ Find matched weather information cases (e.g. - temperature, humidity) """
        self.cases = []
        for i, p in enumerate(self.patterns):
            if p.match(text):
                self.cases.append(i)
        return len(self.cases) > 0
    
    def action(self, text):
        weather_api.load_conditions()
        """ Outputs the desired current weather conditions """
        print('\n~ Location:', weather_api.location(), '\n')
        for case in self.cases:
            if case is 0:
                print('~ Temperature:', weather_api.temperature())
                print('~ Feels Like:', weather_api.feels_like())
            elif case is 1:
                print('~ Humidity:', weather_api.humidity())
            elif case is 2:
                print('~ Wind Speed:', weather_api.wind_speed())
            elif case is 3:
                print('~ UV Index:', weather_api.uv_index())
            elif case is 4:
                print('~ Precipitation:', weather_api.precip_today(), 'today,', end='')
                print(weather_api.precip_1_hr(), 'past hour')
            elif case is 5:
                print('~ Visibility:', weather_api.visibility())
            elif case is 6:
                print('~ Pressure:', weather_api.pressure())
            elif case is 7:
                print('~ Conditions:', weather_api.conditions())
        print('')

class ForecastTask(Task):    
    def match(self, text):
        text = weather_api.replace_day_aliases(text)
        
        """ See if it matches any weather input patterns """
        for p in self.patterns:
            if p.match(text):
                return True
        return False
        
    def find_periods(self, text):
        """ Finds time periods to forecast
            Periods are half of a day in length """
        matched_periods = []
        for day in weather_api.DAYS:
            if re.search('^.*\\b'+day+'\\b.*$', text, re.IGNORECASE):
                day_num = weather_api.DAYS.index(day)
                if day_num < weather_api.today_num():
                    day_num += 7
                day_num -= weather_api.today_num()
                period = day_num*2
                if re.search('^.*\\b'+day+'\\s+night\\b.*$', text, re.IGNORECASE):
                    period += 1
                matched_periods.append(period)
        """ If no matched periods, forecast today """
        if len(matched_periods) <= 0:
            matched_periods.append(0)
        self.matched_periods.sort()
    
    def action(self, text):
        weather_api.load_forecast()
        matched_periods = self.find_periods(text)
        print('')
        for period in matched_periods.sort():
            fc = weather_api.fc_day(period)
            if fc[1]:
                print('~ '+fc[0]+': '+fc[1])
            else:
                print('~ '+fc[0])
        print('')
        
class UpdateLocationTask(Task):
    ZIP_IATA_PATTERN = r'.*\b(in|at|near|around|close to)\s(\d{5}|[A-Z]{3})\b.*'
    CITY_PATTERN = r'.*\b(in|at|near|around|close to)\s([a-zA-Z_]+),?(\s([a-zA-Z_]+))?\b.*'

    def match(self, text):
        """ Look for a weather location """
        self.task_greedy = False
        self.zip_iata_city = ''
        self.state_country = ''
        m = self.patterns[0].match(text)
        if m is not None:
            self.zip_iata_city = m.group(2)
            return True
        else:
            m = self.patterns[1].match(text)
            if m is not None:
                self.zip_iata_city = m.group(2)
                self.state_country = m.group(4)
                return True
        return False

    def action(self, text):
        """ Try to update location """
        if not weather_api.update_loc(self.zip_iata_city, self.state_country):
            print('\n~ Location not found using:')
            if self.state_country:
                print('~ City:', self.zip_iata_city)
                print('~ State/Country:', self.state_country+'\n')
            else:
                print('~ Zip/Airport Code:', self.zip_iata_city+'\n')
            print('~ TIP: use underscores for spaces within names (e.g. "new_york_city")\n')
            
            """ Make task greedy if matched location but could not update """
            self.task_greedy = True

def init():
    """ If the default location is invalid, don't load the module """
    if not weather_api.update_loc(DEFAULT_ZIP_IATA_CITY, DEFAULT_STATE_COUNTRY):
        raise Exception
    
    weather_input_patterns = [r'^.*\b(temp(erature)?|high(s)?|low(s)?|heat|hot(ter|test)?|(cold|cool)(er|est)?)\b.*$',
                              r'^.*\bhumid(ity)?\b.*$',
                              r'^.*\bwind(s|y|ier)?\b.*$',
                              r'^.*\b((u(\.)?v(\.)?|ultra\sviolet)(\sindex)?)\b.*$',
                              r'^.*\b((rain|snow)(ing|s|y|fall)?|precip(itation|itating)?)\b.*$',
                              r'^.*\b(visibility|fog(gy)?)\b.*$',
                              r'^.*\b(pressure)\b.*$',
                              r'^.*\b(weather|forecast(s)?|condition(s)?)\b.*$']
    
    global tasks
    tasks = [UpdateLocationTask([UpdateLocationTask.ZIP_IATA_PATTERN,
                                 UpdateLocationTask.CITY_PATTERN], priority=5),
             ForecastTask(weather_input_patterns),
             CurrentDayTask(weather_input_patterns)]
