"""
The "Api" class is used when an instance
of an API is required in the athena.apis.api_lib

Use "from athena.apis import api_lib" & "api_lib['(api_name_key)']"
to access instances of APIs.
"""
import traceback


class Api(object):

    def __init__(self, key, save_data=None, enabled=True):
        """ Make a unique api key name (e.g. 'spotify_api') """
        self.key = key
        if save_data is not None:
            self.save_data = save_data
        self.enabled = enabled

    def verify_data(self, user):
        """ Verify that the current user .yml file
        has required save_data attributes
        """
        try:
            if hasattr(self, 'save_data'):
                # print()
                for field in self.save_data:
                    """ If data is required and not there, throw error """
                    if field.key in user[self.key]:
                        setattr(self, field.key, user[self.key][field.key])
                        # print('API: '+self.key+', Loading data: '+field.key)
                    elif field.require:
                        raise Exception
            return True
        except:
            print(traceback.format_exc())
            return False
