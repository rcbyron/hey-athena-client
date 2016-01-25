'''
Created on Jan 10, 2016

@author: Connor
'''
import traceback

import athena.config as cfg
import athena.settings as settings

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = 'https://play.spotify.com/browse'

def config():
    spotify_info = {}
    spotify_info['username'] = cfg.safe_input('Spotify Username: ')
    spotify_info['password'] = cfg.safe_input('Spotify Password: ')
    return spotify_info

class SpotifyApi():
    
    def __init__(self):
        self.frame = None
        self.driver = None
        if 'spotify_api' in settings.inst.user:
            self.username = settings.inst.user['spotify_api']['username']
            self.password = settings.inst.user['spotify_api']['password']
        else:
            print('~ Please add spotify configuration to your user.')
    
    def login(self):
        if not self.password or not self.username:
            self.username = input('Username: ')
            self.password = input('Password: ')
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
