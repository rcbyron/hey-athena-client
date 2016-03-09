"""

A wrapper API for Spotify Web Player (requires Firefox)

"""
import traceback

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from athena.classes.api import Api
from athena.classes.input_field import InputField

BASE_URL = 'https://play.spotify.com/browse'

class SpotifyApi(Api):
    
    def __init__(self):
        self.save_data = [
            InputField('username', require=True),
            InputField('password', require=True),
        ]
        super().__init__('spotify_api')
        self.frame = None
        self.driver = None
    
    def login(self):
        self.driver = webdriver.Firefox()
        self.driver.get(BASE_URL)
    
        self.driver.find_element_by_id('has-account').click()
    
        self.driver.find_element_by_id('login-usr').clear()
        self.driver.find_element_by_id('login-usr').send_keys(self.username)
    
        self.driver.find_element_by_id('login-pass').clear()
        self.driver.find_element_by_id('login-pass').send_keys(self.password)
        self.driver.find_element_by_id('login-pass').submit()
        
        main_frame = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@id="section-browse"]/descendant::iframe'))
        )
        self.ensure_frame(main_frame)
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'nav'))
        )
        self.driver.switch_to_default_content()
    
    def ensure_frame(self, frame):
        if self.frame is not frame:
            self.driver.switch_to_default_content()
            self.driver.switch_to_frame(frame)
            self.frame = frame
            
    def ensure_login(self):
        if not self.driver or 'play.spotify' not in self.driver.current_url:
            self.login()
    
    def play_pause_track(self):
        self.ensure_login()
        self.ensure_frame('app-player')
        self.driver.find_element_by_id('play-pause').click()
    
    def prev_track(self):
        self.ensure_login()
        self.ensure_frame('app-player')
        self.driver.find_element_by_id('previous').click()
    
    def next_track(self):
        self.ensure_login()
        self.ensure_frame('app-player')
        self.driver.find_element_by_id('next').click()

    def search(self, query):
        self.ensure_login()
        self.driver.switch_to_default_content()
        try:
            nav_search = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, 'nav-search'))
            )
            nav_search.click()
            self.ensure_frame('suggest')
            form = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, 'form'))
            )
            search_bar = form.find_element_by_tag_name('input')
            search_bar.send_keys(query)
            show_results = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@class="results"]/descendant::a'))
            )
            show_results.click()
            self.driver.switch_to_default_content()
            wrapper = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'front'))
            )
            iframe = wrapper.find_element_by_tag_name('iframe')
            self.driver.switch_to_frame(iframe)
            songs = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, 'tbody'))
            )
            first_song = songs.find_element_by_tag_name('tr')
            first_song.click()
            first_song.send_keys(Keys.RETURN)
        except:
            print('Can\'t find element...')
            print(traceback.format_exc())
