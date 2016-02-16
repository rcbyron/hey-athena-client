""" 
    The "Api" class is used when an instance
    of an API is required in the athena.apis.api_lib
    
    Use "from athena.apis import api_lib" & "api_lib['(api_name_key)']"
    to access instances of APIs.
"""

class Api(object):
    
    def __init__(self, key, save_data=None, enabled=True):
        """ Make a unique api key name (e.g. 'spotify_api') """
        self.key = key
        self.save_data = save_data
        self.enabled = enabled
        
    def verify_data(self, user):
        """ Verify that the current user .yml file has required save_data attributes """
        try:
            if hasattr(self, 'save_data'):
                for tup in self.save_data:
                    """ If data is required and not there, throw error """
                    if tup[0] in user[self.key]:
                        setattr(self, tup[0], user[self.key][tup[0]])
                    elif tup[2]:
                        raise Exception
            return True
        except Exception as e:
            print(e)
            return False