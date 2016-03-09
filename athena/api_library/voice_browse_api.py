"""

Tools to automate browsing (requires Firefox)
    
"""
import urllib.parse as up

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from athena.classes.api import Api
from athena import settings

GOOGLE_URL = 'https://www.google.com/search?gs_ivs=1&q='
OS_KEY = Keys.CONTROL # Mac users must change to Keys.COMMAND

class VoiceBrowseApi(Api):
    
    def __init__(self):
        self.key = 'voice_browse_api'
        self.driver = None
        
    def open(self, url=None, new_tab=True):
        if not self.driver:
            try:
                self.driver = webdriver.Chrome(settings.CHROME_PATH)
            except:
                self.driver = webdriver.Firefox()
        else:
            if new_tab:
                print('\n~ Opening new tab...')
                self.driver.find_element_by_tag_name('body').send_keys(OS_KEY+'t')
        if url:
            if not url[0:4] == 'http':
                url = 'https://'+url.replace(' ', '')
            self.driver.get(url)
        
    def close(self):
        if self.driver:
            self.driver.quit()
            self.driver = None
            
    def close_tab(self):
        if self.driver:
            self.driver.find_element_by_tag_name('body').send_keys(OS_KEY+'w')
            try:
                self.driver.current_url()
            except:
                self.driver = None
                print('\n~ Browser closed.')
    
    def switch_tab(self):
        if self.driver:
            self.driver.find_element_by_tag_name('body').send_keys(OS_KEY+Keys.TAB)
    
    def maximize(self):
        if self.driver:
            self.driver.maximize_window()
            
    def search(self, q):
        self.open(GOOGLE_URL+up.quote_plus(q), new_tab=False)
    
    def clear(self):
        if self.driver:
            self.driver.switch_to_active_element().clear()
    
    def type(self, text):
        if self.driver:
            self.driver.switch_to_active_element().send_keys(text+Keys.RETURN)
    
    def click(self):
        if self.driver:
            self.driver.switch_to_active_element().click()