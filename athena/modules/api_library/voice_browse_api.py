'''
Created on Jan 30, 2016

@author: Connor
'''
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

#FOLDER_PATH = os.path.dirname(os.path.abspath(__file__))
#CHROME_PATH = os.path.join(FOLDER_PATH, 'chromedriver')
GOOGLE_URL = 'https://www.google.com'
SEARCH_XPATH = '//input[@name="q"]'
OS_KEY = Keys.CONTROL # Mac users must change to Keys.COMMAND

class VoiceBrowseApi():
    
    def __init__(self):
        self.driver = None
        
    def open(self, url=None):
        if not self.driver:
            #self.driver = webdriver.Chrome(CHROME_PATH)
            self.driver = webdriver.Firefox()
        else:
            print('\n~ Opening new tab...')
            self.driver.find_element_by_tag_name('body').send_keys(OS_KEY+'t')
        if url:
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
        self.open(GOOGLE_URL)
        search_bar = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, SEARCH_XPATH))
        )
        search_bar.send_keys(q+Keys.RETURN)
    
    def clear(self):
        if self.driver:
            self.driver.switch_to_active_element().clear()
    
    def type(self, text):
        if self.driver:
            self.driver.switch_to_active_element().send_keys(text+Keys.RETURN)
    
    def click(self):
        if self.driver:
            self.driver.switch_to_active_element().click()