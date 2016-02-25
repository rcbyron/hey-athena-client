"""
Finds and stores APIs in the 'api_lib' global variable
"""

import pkgutil, inspect, traceback

from athena import api_library

api_lib = None

def find_apis():
    """ Find APIs """
    global api_lib
    api_lib = {}
    print('~ Looking for APIs in: '+str(api_library.__path__).replace('\\\\', '\\').replace('//', '/')[1:-1])
    for finder, name, _ in pkgutil.iter_modules(api_library.__path__):
        try:
            file = finder.find_module(name).load_module(name)
            for member in dir(file):
                obj = getattr(file, member)
                if inspect.isclass(obj):
                    for parent in obj.__bases__:
                        if 'Api' is parent.__name__:
                            api = obj()
                            api_lib[api.key] = api
        except Exception as e:
            print(traceback.format_exc())
            print('\n~ Error loading \''+name+'\' '+str(e))        

def verify_apis(user):
    """ Verify APIs """
    global api_lib
    api_lib = dict(item for item in api_lib.items() if item[1].verify_data(user))

def list_apis():
    """ List APIs """
    global api_lib
    print('\n~ APIs: ', end='')
    print(str(list(api_lib.keys()))[1:-1]+'\n')
    