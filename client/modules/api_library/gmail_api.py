'''
Created on Jun 18, 2015

@author: Connor

API Documentation:
https://developers.google.com/gmail/api/

PyDoc:
https://google-api-client-libraries.appspot.com/documentation/gmail/v1/python/latest/
'''
import httplib2
import os
import oauth2client

from oauth2client import client
from oauth2client import tools
from apiclient import discovery
from apiclient.http import BatchHttpRequest

SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = './secrets/client_secrets.json'
APPLICATION_NAME = 'Athena Voice Gmail API'
MAX_EMAILS = 50
def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """

    credential_dir = '.credentials'
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'gmail-credentials.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        
        try:
            import argparse
            flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
        except ImportError:
            flags = None
        credentials = tools.run_flow(flow, store, flags)
        print('Storing credentials to ' + credential_path)
    return credentials

class GmailApi():
    def __init__(self):
        self.credentials = get_credentials()
        http = self.credentials.authorize(httplib2.Http())
        self.service = discovery.build('gmail', 'v1', http=http)

    def bulk_fetch(self, service, search_primary):
        params = 'is:unread '
        if search_primary:
            params += 'category:primary'
        results = service.users().messages().list(userId='me', maxResults=MAX_EMAILS, q=params).execute()
        return results.get('messages')
    
    def has_categories(self, service):
        ''' Checks if the user has categories enabled '''
        results = service.users().messages().list(userId='me', maxResults=1, q='category:primary').execute()
        return results.get('messages') is not None
    
    def unread_ids(self):
        search_primary = self.has_categories(self.service)
        messages = self.bulk_fetch(self.service, search_primary)
        return messages

    def subject_callback(self, request_id, response, exception):
        if exception:
            raise('Error: Could not list email subjects.')
        
        for name in response['payload']['headers']:
            if name['name'] == 'Subject':
                self.subjects.append(name['value'])
                return

    def unread_subjects(self):
        batch = BatchHttpRequest()
        messages = self.unread_ids()
        self.subjects = []
        for msg in messages:
            batch.add(self.service.users().messages().get(userId='me', id=msg['id']), callback=self.subject_callback)
        batch.execute()
        return self.subjects