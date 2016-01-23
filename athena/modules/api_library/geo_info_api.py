'''
Created on Jun 18, 2015

@author: Connor

API Documentation:
http://www.telize.com/
'''
import urllib.request, json

URL = 'http://www.telize.com/geoip'

def update_data():
    return json.loads(urllib.request.urlopen(URL).read().decode('utf-8'))
    
def get_data(key):
    """
        Keys:
        - ip (Visitor IP address, or IP address specified as parameter)
        - country_code (Two-letter ISO 3166-1 alpha-2 country code)
        - country_code3 (Three-letter ISO 3166-1 alpha-3 country code)
        - country (Name of the country)
        - region_code (Two-letter ISO-3166-2 state / region code)
        - region (Name of the region)
        - city (Name of the city)
        - postal_code (Postal code / Zip code)
        - continent_code (Two-letter continent code)
        - latitude (Latitude)
        - longitude (Longitude)
        - dma_code (DMA Code)
        - area_code (Area Code)
        - asn (Autonomous System Number)
        - isp (Internet service provider)
        - timezone (Time Zone)
    """

    response = update_data()
    if key not in response:
        return None
    return response[key]
