'''
Created on Jun 4, 2015

@author: Connor
'''

if __name__ == '__main__':
    pass

import client.modules.active as active_modules
import pkgutil, re, traceback

def find_mods():
    """ Find modules """
    global modules
    modules = []
    print('~ Looking for modules in: '+str(active_modules.__path__).replace('\\\\', '\\')[1:-1])
    for finder, name, _ in pkgutil.iter_modules(active_modules.__path__):
        try:
            mod = finder.find_module(name).load_module(name)
            modules.append(mod)
        except Exception as e:
            print('\n~ Error loading \''+name+'\' '+str(e))        
    modules.sort(key=lambda mod: mod.MOD_PRIORITY if hasattr(mod, 'MOD_PRIORITY') else 0, reverse=True)

def init_mods():
    """ Initialize modules """
    print('\n~ Initializing modules...')
    for mod in modules:
        try:
            if not hasattr(mod, 'init'):
                raise Exception('(missing \'init\' method)')
            mod.init()
            if not hasattr(mod, 'tasks'):
                raise Exception('(missing \'tasks\' list)')
        except Exception as e:
            print('\n~ Error intializing \''+mod.__name__+'\' '+str(e))
            modules.remove(mod)

def list_mods():
    """ List module order """
    print('\n~ Prioritized Module Order: ', end='')
    print(str([mod.__name__ for mod in modules])[1:-1]+'\n')

def greet():
    """ Greet the user """
    print('  _      _     __      _    ')
    print(' / `    / )    )_)    /_)   ')
    print('(_.  o (_/  o / \  o / /  o ')
    print('\n~ Hello, what can I do for you today?\n')

def execute_tasks(mod):
    """ Executes a module's task queue """
    for task in mod.task_queue:
        task.action(text)
        if task.task_greedy:
            break
    return task.mod_greedy

def mod_select(matched_mods):
    """ Prompt user to specify which module to use to respond """
    print('\n~ Which module would you like me to use to respond?')
    print('~ Choices: '+str([mod.__name__ for mod in matched_mods])[1:-1]+'\n')
    mod_select = input('> ')
    
    found_mod = False
    for mod in matched_mods:
        if re.search('^.*\\b'+mod.__name__+'\\b.*$',  mod_select, re.IGNORECASE):
            found_mod = True
            if execute_tasks(mod):
                break
    if not found_mod:
        print('\n~ No module name found.\n')

find_mods()
init_mods()
list_mods()
greet()

import client.stt as stt
import winsound, time
stt.init()
while True:
    try:
        text = input('> ')
#         print("~ Passive listening... ")
#         stt.listen_keyword()
        winsound.Beep(900, 150)
        time.sleep(0.01)
        winsound.Beep(900, 150)
#         print("\n~ Active listening... ")
#         text = stt.active_listen()
#         print("\n~ \""+text+"\"")
    
        matched_mods = []
        for mod in modules:
            """ Find matched tasks and add to module's task queue """
            mod.task_queue = []
            for task in mod.tasks:
                if task.match(text):
                    mod.task_queue.append(task)
                    if task.task_greedy:
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
    except:
        print(traceback.format_exc())
