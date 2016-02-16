"""
    A simple API to retrieve user info
"""

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
        