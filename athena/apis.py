"""
Finds and stores APIs in the 'api_lib' global variable
"""

import pkgutil
import inspect
import traceback

from athena import settings

api_lib = None


def find_apis():
    """ Find APIs """
    global api_lib
    api_lib = {}
    print('~ Looking for APIs in:', settings.API_DIRS)
    for finder, name, _ in pkgutil.iter_modules(settings.API_DIRS):
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
    api_lib = dict(api for api in api_lib.items() if api[1].verify_data(user))


def list_apis():
    """ List APIs """
    global api_lib
    print('\n~ APIs:', str(list(api_lib.keys()))[1:-1]+'\n')
