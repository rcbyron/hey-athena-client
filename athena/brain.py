"""
The "Brain" class handles most of Hey Athena's processing.
To listen for input, use ``brain.inst.run()``
"""
from __future__ import print_function

import traceback
import os
import re
import yaml

from athena import settings, stt, tts, apis, mods, log

inst = None

try:
    input = raw_input  # Python 2 fix
except NameError:
    pass


def init():
    global inst
    inst = Brain()


class Brain():
    def __init__(self):
        """
        First look for and initialize APIs in the "api_library" folder.
        Then prompt the user to log in.
        Next verify that the user's .yml file is configured for each API.
        If an API's required configuration variables are not found,
        then the API is disabled.
        Next it finds and loads modules in the "modules" folder.
        Lastly, it initializes the STT engine.

        Use "from athena.apis import api_lib" & "api_lib['(api_name_key)']"
        to access instances of APIs.
        """

        apis.find_apis()
        self.login()

        apis.verify_apis(self.user)
        apis.list_apis()

        mods.find_mods()
        mods.list_mods()

        self.greet()
        stt.init()

        self.quit_flag = False

    def find_users(self):
        """ Returns a list of available user strings """
        self.users = []
        for file in os.listdir(settings.USERS_DIR):
            if file.endswith('.yml'):
                with open(os.path.join(settings.USERS_DIR, file)) as f:
                    user = yaml.load(f)
                    self.users.append(user['user_api']['username'])
        return self.users

    def verify_user_exists(self):
        """ Verify that at least 1 user exists """
        self.find_users()
        if not self.users:
            print('~ No users found. Please create a new user.\n')
            import athena.config as cfg
            cfg.generate()
            self.find_users()

    def load_user(self, username):
        """ Load (username).yml data into the user """
        with open(os.path.join(settings.USERS_DIR, username+'.yml'), 'r') as f:
            self.user = yaml.load(f)
            log.debug('Logged in as: '+self.user['user_api']['username'])

    def login(self):
        self.verify_user_exists()
        if len(self.users) == 1:
            self.load_user(self.users[0])
            return

        print('~ Users: ', str(self.users)[1:-1])
        username = ''
        while username not in self.users:
            username = input('\n~ Username: ')
            if username not in self.users:
                print('\n~ Please enter a valid username')
                continue
        self.load_user(username)

    def greet(self):
        """ Greet the user """
        print(r"  _    _                      _   _                      ")
        print(r" | |  | |                /\  | | | |                     ")
        print(r" | |__| | ___ _   _     /  \ | |_| |__   ___ _ __   __ _ ")
        print(r" |  __  |/ _ \ | | |   / /\ \| __| '_ \ / _ \ '_ \ / _` |")
        print(r" | |  | |  __/ |_| |  / ____ \ |_| | | |  __/ | | | (_| |")
        print(r" |_|  |_|\___|\__, | /_/    \_\__|_| |_|\___|_| |_|\__,_|")
        print(r"               __/ |                                     ")
        print(r"              |___/                                      ")
        if apis.api_lib['user_api'].name():
            print('\n~ Hey there, '+apis.api_lib['user_api'].name()+'!\n')
        else:
            print('\n~ Hello, what can I do for you today?\n')
        print('~ Try asking:')
        print('  - "Athena (double beep) what\'s the weather like in DFW?"')
        print('  - "Athena (double beep) what is the capital of Tanzania?"')
        print('  - "Athena (double beep) open facebook.com"\n')

    def execute_tasks(self, mod, text):
        """ Executes a module's task queue """
        for task in mod.task_queue:
            task.action(text)
            if task.greedy:
                break

    def execute_mods(self, text):
        """ Executes the modules in prioritized order """
        if len(self.matched_mods) <= 0:
            tts.speak(settings.NO_MODULES)
            return

        self.matched_mods.sort(key=lambda mod: mod.priority, reverse=True)

        normal_mods = []
        greedy_mods = []
        greedy_flag = False
        priority = 0
        for mod in self.matched_mods:
            if greedy_flag and mod.priority < priority:
                break
            if mod.greedy:
                greedy_mods.append(mod)
                greedy_flag = True
                priority = mod.priority
            else:
                normal_mods.append(mod)

        if len(greedy_mods) is 1:
            normal_mods.append(greedy_mods[0])
        elif len(greedy_mods) > 1:
            if 0 < len(normal_mods):
                print('\n~ Matched mods (non-greedy): '+str([mod.name for mod in normal_mods])[1:-1]+'\n')
            m = self.mod_select(greedy_mods)
            if not m:
                return
            normal_mods.append(m)
        for mod in normal_mods:
            self.execute_tasks(mod, text)

    def mod_select(self, mods):
        """ Prompt user to specify which module to use to respond """
        print('\n~ Which module (greedy) would you like me to use to respond?')
        print('~ Choices: '+str([mod.name for mod in mods])[1:-1]+'\n')
        mod_select = input('> ')

        for mod in mods:
            if re.search('^.*\\b'+mod.name+'\\b.*$',  mod_select, re.IGNORECASE):
                return mod
        log.info('No module name found.')

    def match_mods(self, text):
        """ Attempts to match a modules and their tasks """
        self.matched_mods = []
        for mod in mods.mod_lib:
            if not mod.enabled:
                continue
            """ Find matched tasks and add to module's task queue """
            mod.task_queue = []
            for task in mod.tasks:
                if task.match(text):
                    mod.task_queue.append(task)
                    if task.greedy:
                        break

            """ Add modules with matched tasks to list """
            if len(mod.task_queue):
                self.matched_mods.append(mod)

    def list_mods(self):
        print("~ Modules (highest priority first): ")
        for mod in mods.mod_lib:
            print("  - "+mod.name)

    def enable_mod(self, name):
        for mod in mods.mod_lib:
            if mod.name == name:
                mod.enabled = True
                log.info(mod.name+" enabled.")


    def disable_mod(self, name):
        for mod in mods.mod_lib:
            if mod.name == name:
                mod.enabled = False
                log.info(mod.name + " disabled.")

    def error(self):
        """ Inform the user that an error occurred """
        tts.speak(settings.ERROR)
        text = input('Continue? (Y/N) ')
        # response = stt.active_listen()
        if 'y' in text.lower():
            log.error(traceback.format_exc())

    def quit(self):
        self.quit_flag = True

    def run(self):
        """ Listen for input, match the modules and respond """
        while True:
            if self.quit_flag:
                break
            try:
                if settings.USE_STT:
                    stt.listen_keyword()
                    text = stt.active_listen()
                else:
                    text = input('> ')
                if not text:
                    log.info('No text input received.')
                    continue

                self.match_mods(text)
                self.execute_mods(text)
            except OSError as e:
                if 'Invalid input device' in str(e):
                    log.error(settings.NO_MIC+'\n')
                    settings.USE_STT = False
                    continue
                else:
                    raise Exception
            except (EOFError, KeyboardInterrupt):
                log.info('Shutting down...')
                break
            except:
                log.error("(runtime error)")
                self.error()

        log.info('Arrivederci.')
