"""
    A simple API to retrieve user info
"""

from athena.classes.api import Api
from athena.classes.input_field import InputField


class UserApi(Api):

    def __init__(self):
        self.save_data = [
            InputField('username', require=True),
            InputField('full_name'),
            InputField('nickname'),
            InputField('phone'),
            InputField('email'),
        ]
        super(UserApi, self).__init__('user_api')

    def name(self):
        name = None
        if hasattr(self, 'nickname'):
            name = self.nickname
        elif hasattr(self, 'full_name'):
            name = self.full_name
        return name
