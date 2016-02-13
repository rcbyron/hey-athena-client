'''
Created on Feb 11, 2016

@author: Connor
'''

class Api(object):
    
    def __init__(self, key, save_data=None, enabled=True):
        """ Make a unique api key name (e.g. 'spotify_api') """
        self.key = key
        self.save_data = save_data
        self.enabled = enabled
        
    def verify_data(self, user):
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