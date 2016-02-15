""" Helpful methods for generating a user .yml config file """
import os, yaml

import athena.settings as settings
from athena.apis import api_lib

def safe_input(prompt, require=False):
    """ Prompts the user for input """
    answer = ''
    if require:
        confirm = 'N'
        while (len(confirm) < 1 or confirm.upper()[0] is not 'Y'):
            answer = input('* '+prompt)
            if not answer:
                print('\n~ Please enter a valid value')
                continue
            print('\n~ Input:', answer)
            confirm = input('~ Confirm (Y / N): ')
            print()
    else:
        answer = input(prompt)
        print()
    return answer

def block_print(title):
    """ Prints a title block """
    if not title:
        title = '(empty)'
    length = len(title)+10
    print('#'*length                )
    print('#' + ' '*(length-2) + '#')
    print('#    '  + title + '    #')
    print('#' + ' '*(length-2) + '#')
    print('#'*length           +'\n')

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
            for tup in api.save_data:
                api_info[tup[0]] = safe_input(tup[1], tup[2])
            if api_info:
                config_info[key] = api_info

    file_loc = os.path.join(settings.USERS_DIR, config_info['user_api']['username']+'.yml')
    print('~ Writing to:', file_loc)
    with open(file_loc, 'w') as f:
        yaml.dump(config_info, f, default_flow_style=False)
    print('~ Success! You can now log in with this user.\n')
