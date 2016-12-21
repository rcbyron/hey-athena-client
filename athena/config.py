"""
Helpful methods for generating a user .yml config file
"""

import os
import yaml

from athena import settings
from athena.apis import api_lib

def block_print(title):
    """ Prints a pretty title block """
    if not title:
        title = '(empty)'
    length = len(title)+10
    print('#'*length)
    print('#' + ' '*(length-2) + '#')
    print('#    ' + title + '    #')
    print('#' + ' '*(length-2) + '#')
    print('#'*length + '\n')


def generate():
    """ Generates a user .yml config file """
    block_print('USER CONFIG FILE GENERATOR')
    print('~ Please let me learn some things about you :)\n')
    print('~ Required fields are denoted with a \'*\'\n')
    config_info = {}

    for key, api in api_lib.items():
        if hasattr(api, 'save_data'):
            block_print(key.replace('_', ' ').title())
            api_info = {}
            for field in api.save_data:
                api_info[field.key] = field.get_input()
            if api_info:
                config_info[key] = api_info

    file_loc = os.path.join(settings.USERS_DIR, config_info['user_api']['username']+'.yml')
    print('~ Writing to:', file_loc)
    with open(file_loc, 'w') as f:
        yaml.dump(config_info, f, default_flow_style=False)
    print('~ Success! You can now log in with this user.\n')
