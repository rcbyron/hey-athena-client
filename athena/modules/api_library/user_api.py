'''
Created on Jan 12, 2016

@author: Connor
'''
import athena.config as cfg

def config():
    user_info = {}
    print('** Username will be used as the .yml file name\n')
    user_info['username'] = cfg.safe_input('Username: ', require=True)
    user_info['full-name'] = cfg.safe_input('Full Name: ')
    user_info['nickname'] = cfg.safe_input('Nickname: ')
    user_info['phone'] = cfg.safe_input('Phone Number: ')
    user_info['email'] = cfg.safe_input('Email: ')
    return user_info
