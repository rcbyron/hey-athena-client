'''
Created on Jan 12, 2016

@author: Connor
'''
from athena.classes.api import Api

SAVE_DATA = [
    ('username' , 'Username: '      , True ),
    ('full_name', 'Full Name: '     , False),
    ('nickname' , 'Nickname: '      , False),
    ('phone'    , 'Phone Number: '  , False),
    ('email'    , 'Email: '         , False),
]

class UserApi(Api):
    
    def __init__(self):
        super().__init__('user_api', SAVE_DATA)
        