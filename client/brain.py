'''
Created on Jun 4, 2015

@author: Connor
'''
import client.stt as stt

if __name__ == '__main__':
    pass

import client.tts as tts
import pkgutil, re, traceback

import client.modules.active as active_mods
from inspect import isclass

def find_mods():
    """ Find modules """
    global modules
    modules = []
    print('~ Looking for modules in: '+str(active_mods.__path__).replace('\\\\', '\\')[1:-1])
    for finder, name, _ in pkgutil.iter_modules(active_mods.__path__):
        try:
            mod = finder.find_module(name).load_module(name)
            for member in dir(mod):
                obj = getattr(mod, member)
                if isclass(obj):
                    for parent in obj.__bases__:
                        if 'Module' is parent.__name__:
                            modules.append(obj())
        except Exception as e:
            print('\n~ Error loading \''+name+'\' '+str(e))        
    modules.sort(key=lambda mod: mod.priority if hasattr(mod, 'priority') else 0, reverse=True)

def list_mods():
    """ List module order """
    print('\n~ Prioritized Module Order: ', end='')
    print(str([mod.name for mod in modules])[1:-1]+'\n')

def greet():
    """ Greet the user """
    print('     _   _   _                      ')
    print('    / \ | |_| |__   ___ _ __   __ _ ')
    print('   / _ \| __| \'_ \ / _ \ \'_ \ / _` |')
    print('  / ___ \ |_| | | |  __/ | | | (_| |')
    print(' /_/   \_\__|_| |_|\___|_| |_|\__,_|')
    print('      __     __    _                ')
    print('      \ \   / /__ (_) ___ ___       ')
    print('       \ \ / / _ \| |/ __/ _ \      ')
    print('        \ V / (_) | | (_|  __/      ')
    print('         \_/ \___/|_|\___\___|      ')
    print('\n~ Hello, what can I do for you today?\n')

def execute_tasks(mod):
    """ Executes a module's task queue """
    for task in mod.task_queue:
        task.action(text)
        if task.greedy:
            break

def get_most_important(matched_mods):
    """ Return a list of modules with the highest priority """
    max_priority = -1
    max_mods = []
    for mod in matched_mods:
        if max_priority < mod.priority:
            max_mods.clear()
            max_priority = mod.priority
        if max_priority <= mod.priority:
            max_mods.append(mod)
    return max_mods

def mod_select(matched_mods):
    matched_mods = get_most_important(matched_mods)
    if len(matched_mods) == 1:
        execute_tasks(matched_mods[0])
        return
    """ Prompt user to specify which module to use to respond """
    print('\n~ Which module would you like me to use to respond?')
    print('~ Choices: '+str([mod.name for mod in matched_mods])[1:-1]+'\n')
    mod_select = input('> ')
    
    for mod in matched_mods:
        if re.search('^.*\\b'+mod.name+'\\b.*$',  mod_select, re.IGNORECASE):
            execute_tasks(mod)
            return
    print('\n~ No module name found.\n')

find_mods()
list_mods()
greet()
stt.init()

while True:
    try:
        text = input('> ')
        #stt.listen_keyword()
        #text = stt.active_listen()
        #if not text:
        #    continue

        matched_mods = []
        for mod in modules:
            """ Find matched tasks and add to module's task queue """
            mod.task_queue = []
            for task in mod.tasks:
                if task.match(text):
                    mod.task_queue.append(task)
                    if task.greedy:
                        break
                    
            """ Add modules with matched tasks to list """
            if len(mod.task_queue):
                matched_mods.append(mod)
                 
        if len(matched_mods) == 0:
            print('\n~ No modules matched.\n')
        elif len(matched_mods) == 1:
            """ Execute module's queued tasks """
            execute_tasks(matched_mods[0])
        elif len(matched_mods) > 1:
            mod_select(matched_mods)
    except EOFError:
        print('\n\n~ Shutting down.\n')
        break
    except:
        print(traceback.format_exc())
        tts.speak("Error occurred. Would you still like to continue?")
        print("Error occurred. Would you still like to continue?\n")
        response = input('> ')
        #response = stt.active_listen()
        
        if "yes" not in response.lower():
            break
print('~ Arrivederci.')