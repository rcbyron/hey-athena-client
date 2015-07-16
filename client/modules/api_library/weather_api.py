'''
Created on Jun 1, 2015

@author: Connor
'''

import urllib.request, json, datetime, re

API_KEY = 'd647ca403a0ac94b'
DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
URL_DATA_TYPES = {
    'conditions': '/conditions/q/',
    'forecast':   '/forecast/q/',
    'geolookup':  '/geolookup/q/'
}
        
def get_json_data(data_type):
    """ Returns the desired JSON weather data """
    url = 'http://api.wunderground.com/api/'+API_KEY+URL_DATA_TYPES[data_type]+loc_extension
    return json.loads(urllib.request.urlopen(url).read().decode('utf-8'))

def load_conditions():
    """ Load current weather conditions in c_data """
    global c_data
    c_data = get_json_data('conditions')['current_observation']

def load_forecast():
    """ Load 3-day forecast in fc_list """
    global fc_list 
    fc_list = get_json_data('forecast')['forecast']['txt_forecast']['forecastday']
    
def update_loc(new_zip_iata_city, new_state_country=''):
    """ Updates the location, if valid
    
    Returns:
        True if successful, False if failed
    """
    test_ext = new_zip_iata_city+'.json'
    if new_state_country:
        test_ext = new_state_country+'/'+test_ext
    url = 'http://api.wunderground.com/api/'+API_KEY+'/geolookup/q/'+test_ext
    location = urllib.request.urlopen(url).read().decode('utf-8')
    
    if 'location' in json.loads(location):
        global loc_extension, zip_iata_city, state_country
        loc_extension = test_ext
        zip_iata_city = new_zip_iata_city
        state_country = new_state_country
        return True
    return False

def location():
    return c_data['display_location']['full']

def temperature():
    return c_data['temperature_string']

def feels_like():
    return c_data['feelslike_string']

def humidity():
    return c_data['relative_humidity']

def wind_speed():
    return c_data['wind_string']

def uv_index():
    return c_data['UV']

def precip_today():
    return c_data['precip_today_string']

def precip_1_hr():
    return c_data['precip_1hr_string'].replace('( ', '(')

def visibility():
    return c_data['visibility_mi']

def pressure():
    return c_data['pressure_in']

def conditions():
    return c_data['weather']

def fc_day(period):
    """ Gets the forecast given a list of period numbers 0-7 """
    if period > 7:
        return ('I don\'t have any further forecasts beyond 3 days.', '')
    return (fc_list[period]['title'], fc_list[period]['fcttext'])

def get_day(offset):
    """ Get the day string relative to today """
    return DAYS[(today_num()+offset)%7]

def today_num():
    """ Get the weekday number of today """
    #load_forecast()
    return datetime.datetime.today().weekday()

def replace_day_aliases(text):
    """ Replaces day aliases with usable day names """
    text = re.sub(r'(.*)\b(day after tomorrow|next day)\b(.*)',             '\\1'+get_day(2)+'\\3', text, re.IGNORECASE)
    text = re.sub(r'(.*)\b(tomorrow)\b(.*)',                                '\\1'+get_day(1)+'\\3', text, re.IGNORECASE)
    text = re.sub(r'(.*)\b(today|now|current(?:ly)?|present(?:ly)?)\b(.*)', '\\1'+get_day(0)+'\\3', text, re.IGNORECASE)
    text = re.sub(r'(.*)\b(yesterday)\b(.*)',                               '\\1'+get_day(6)+'\\3', text, re.IGNORECASE)
    return text
