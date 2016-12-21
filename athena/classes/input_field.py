"""

The "InputField" class is used for required user configuration data

"""
from __future__ import print_function

try:
    input = raw_input  # Python 2 fix
except NameError:
    pass


class InputField(object):

    def __init__(self, key, help_msg='', prompt='', require=False, val=None):
        self.key = key
        self.help_msg = help_msg

        if not prompt:
            self.prompt = key.replace('_', ' ').title()+': '
        else:
            self.prompt = prompt

        self.require = require
        self.val = val

    def get_input(self):
        """ Prompts the user for input and saves the value """
        answer = ''
        if self.require:
            confirm = 'N'
            while len(confirm) < 1 or confirm.upper()[0] is not 'Y':
                if self.help_msg:
                    print(self.help_msg)
                answer = input('* '+self.prompt)
                if not answer:
                    print('\n~ Please enter a valid value')
                    continue
                print('\n~ Input:', answer)
                confirm = input('~ Confirm (Y / N): ')
        else:
            answer = input(self.prompt)
        print()
        return answer
