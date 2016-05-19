"""
Finds and stores APIs in the 'api_lib' global variable
"""

import pkgutil
import inspect
import traceback

from athena import settings

mod_lib = None


def find_mods():
    """ Find and import modules from the module directories """
    global mod_lib
    mod_lib = []
    print('~ Looking for modules in:', settings.MOD_DIRS)
    for finder, name, _ in pkgutil.iter_modules(settings.MOD_DIRS):
        try:
            mod = finder.find_module(name).load_module(name)
            for member in dir(mod):
                obj = getattr(mod, member)
                if inspect.isclass(obj):
                    for parent in obj.__bases__:
                        if 'Module' is parent.__name__:
                            mod_lib.append(obj())
        except Exception as e:
            print(traceback.format_exc())
            print('\n~ Error loading \''+name+'\' '+str(e))
    mod_lib.sort(key=lambda mod: mod.priority, reverse=True)


def list_mods():
    """ Print modules in order """
    global mod_lib
    print('\n~ Module Order: ', end='')
    print(str([mod.name for mod in mod_lib])[1:-1]+'\n')


def disable_mod(name):
    global mod_lib
    for mod in mod_lib:
        if name in mod.name:
            print('\n~ Disabling: '+name+'\n')
            mod.enabled = False


def enable_mod(name):
    global mod_lib
    for mod in mod_lib:
        if name in mod.name:
            print('\n~ Enabling: '+name+'\n')
            mod.enabled = True
