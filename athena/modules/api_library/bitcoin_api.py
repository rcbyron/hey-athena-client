'''
Created on Jun 18, 2015

@author: Connor

API Documentation:
https://bitcoinaverage.com/api

'''
import urllib.request, json

'''
CURRENCY_CODES = ['AUD', 'BRL', 'CAD', 'CHF', 'CNY', 'EUR', 'GBP', 'IDR',
'ILS', 'MXN', 'NOK', 'NZD', 'PLN', 'RON', 'RUB', 'SEK', 'SGD', 'USD', 'ZAR']
'''

CURRENCY_CODE = 'USD'
URL = 'https://api.bitcoinaverage.com/ticker/'+CURRENCY_CODE+'/'

def update_data():
    return json.loads(urllib.request.urlopen(URL).read().decode('utf-8'))

def get_data(key):
    """
        Keys:
        - 24h_avg: average of weighted averages for last 24 hours
        - ask: weighted average of ask prices
        - bid: weighted average of bid prices
        - last: weighted average of last prices
        - total_vol: total trading volume across all exchanges in last 24 hours
    """
    
    response = update_data()
    if key not in response:
        return None
    return response[key]
