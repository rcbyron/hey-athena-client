"""
Finds and stores APIs in the 'api_lib' global variable
"""

import pkgutil
import inspect
import traceback

from athena import settings, log

api_lib = None


def find_apis():
    """ Find APIs """
    global api_lib
    api_lib = {}
    log.debug('Looking for APIs in: '+str(settings.API_DIRS))
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
            log.error('Error loading \''+name+'\' '+str(e))


def verify_apis(user):
    """ Verify APIs """
    global api_lib
    api_lib = dict(api for api in api_lib.items() if api[1].verify_data(user))


def list_apis():
    """ List APIs """
    global api_lib
    log.debug('APIs: '+str(list(api_lib.keys()))[1:-1])
