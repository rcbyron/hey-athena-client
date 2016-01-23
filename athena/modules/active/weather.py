'''
Created on Jun 1, 2015

@author: Connor
'''
import re

from athena.classes.module import Module
from athena.classes.task import ActiveTask
from athena.modules.api_library import weather_api

MOD_PARAMS = {
    'name': 'weather',
    'priority': 2,
}

ZIP_IATA_PATTERN = r'.*\b(in|at|near|around|close to)\s(\d{5}|[A-Z]{3})\b.*'
CITY_PATTERN = r'.*\b(in|at|near|around|close to)\s([a-zA-Z_]+),?(\s([a-zA-Z_]+))?\b.*'
WEATHER_INPUT_PATTERNS = [r'^.*\b(temp(erature)?|high(s)?|low(s)?|heat|hot(ter|test)?|(cold|cool)(er|est)?)\b.*$',
                          r'^.*\bhumid(ity)?\b.*$',
                          r'^.*\bwind(s|y|ier)?\b.*$',
                          r'^.*\b((u(\.)?v(\.)?|ultra\sviolet)(\sindex)?)\b.*$',
                          r'^.*\b((rain|snow)(ing|s|y|fall)?|precip(itation|itating)?)\b.*$',
                          r'^.*\b(visibility|fog(gy)?)\b.*$',
                          r'^.*\b(pressure)\b.*$',
                          r'^.*\b(weather|forecast(s)?|condition(s)?)\b.*$']


class CurrentDayTask(ActiveTask):
    
    def match(self, text):
        text = self.api.replace_day_aliases(text)
        
        """ Invalid if text contains a non-current day """
        invalid_days = list(weather_api.DAYS)
        invalid_days.remove(self.api.get_day(0))
        if any(day in text.lower() for day in invalid_days):
            return False
        
        """ Find matched weather information cases (e.g. - temperature, humidity) """
        self.cases = set()
        for i, p in enumerate(self.patterns):
            if p.match(text):
                self.cases.add(i)
        return len(self.cases) > 0
    
    def action(self, text):
        self.api.load_conditions()
        self.api.load_forecast()
        
        """ Outputs the desired current weather conditions """
        print('\n~ Location: '+self.api.location()+'\n')
        self.spoke_once = False
        if 0 in self.cases:
            self.list_weather('Temperature',     self.api.temperature())
            self.list_weather('Feels Like',      self.api.feels_like())
        if 1 in self.cases:
            self.list_weather('Humidity',        self.api.humidity())
        if 2 in self.cases:
            self.list_weather('Wind Speed',      self.api.wind_speed())
        if 3 in self.cases:
            self.list_weather('UV Index',        self.api.uv_index())
        if 4 in self.cases:
            self.list_weather('Precipitation',   self.api.precip_today())
            self.list_weather('Past Hour',       self.api.precip_1_hr())
        if 5 in self.cases:
            self.list_weather('Visibility',      self.api.visibility())
        if 6 in self.cases:
            self.list_weather('Pressure',        self.api.pressure())
        if 7 in self.cases:
            self.list_weather('Condition',       self.api.fc_day(0)[1])
        print('')
        self.api.restore_loc()
        
    def list_weather(self, output, value):
        print('~ '+output+':', value)
        if not self.spoke_once:
            self.speak('The '+output.lower()+' in '+self.api.location()+' is '+value)
            self.spoke_once = True

class ForecastTask(ActiveTask): 
       
    def match(self, text):
        """ See if it matches any weather input patterns """
        for p in self.patterns:
            if p.match(text):
                return True
        return False
        
    def find_periods(self, text):
        """ Finds time periods to forecast
            Periods are half of a day in length """
        matched_periods = set()
        for day in weather_api.DAYS:
            if re.search(r'^.*\btonight\b.*$', text, re.IGNORECASE):
                if 'Night' not in self.api.fc_day(0)[0]:
                    matched_periods.add(1)
            if re.search(r'^.*\b'+day+r'\b.*$', text, re.IGNORECASE):
                day_num = weather_api.DAYS.index(day)
                if day_num < self.api.today_num():
                    day_num += 7
                day_num -= self.api.today_num()
                period = day_num*2
                if re.search(r'^.*\b'+day+r'\s+night\b.*$', text, re.IGNORECASE):
                    period += 1
                matched_periods.add(period)
        """ If no matched periods, forecast today """
        if len(matched_periods) <= 0:
            matched_periods.add(0)
        return matched_periods
    
    def action(self, text):
        text = self.api.replace_day_aliases(text)
        self.api.load_forecast()
        
        matched_periods = self.find_periods(text)
        print('\n~ Location: '+self.api.location()+'\n')
        for period in sorted(matched_periods):
            fc = self.api.fc_day(period)
            if fc[1]:
                print('~ '+fc[0]+': '+fc[1])
            else:
                print('~ '+fc[0])
        print('')
        self.api.restore_loc()
        
class UpdateLocationTask(ActiveTask):
    
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
        """ Make task greedy if matched location in text but could not update """
        if not self.api.try_set_loc(self.zip_iata_city, self.state_country):
            self.task_greedy = True
        else:
            self.api.restore_flag = True

class Weather(Module):
    
    def __init__(self):
        w_api = None
        mod_enabled = True
        try:
            w_api = weather_api.WeatherApi()
        except:
            mod_enabled = False
            print('~ Please properly configure the weather API')
            return
        
        tasks = [UpdateLocationTask(patterns=[ZIP_IATA_PATTERN,CITY_PATTERN],
                                    priority=5, api=w_api, greedy=False),
                 CurrentDayTask(WEATHER_INPUT_PATTERNS, priority=2, api=w_api),
                 ForecastTask(WEATHER_INPUT_PATTERNS, priority=1, api=w_api)]
        super().__init__(MOD_PARAMS, tasks)