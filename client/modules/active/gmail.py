'''
Created on Jul 19, 2015

@author: Connor
'''
from client.classes.module import Module
from client.classes.task import ActiveTask
from client.modules.api_library import gmail_api

class GetUnreadMail(ActiveTask):
    
    def __init__(self):
        patterns = [r'.*\b(mail)\b.*']
        super().__init__(patterns)
    
    def match(self, text):
        for p in self.patterns:
            if p.match(text):
                return True
        return False
    
    def action(self, text):
        gmailapi = gmail_api.GmailApi()
        subjects = gmailapi.unread_subjects()
        
        if subjects is None:
            self.speak('No important unread messages.')
            return
        elif len(subjects) is 1:
            self.speak('You have 1 unread message:')
        elif gmail_api.MAX_EMAILS <= len(subjects):
            self.speak('You have over'+str(gmail_api.MAX_EMAILS)+' unread messages:')
        else:
            self.speak('You have '+str(len(subjects))+' unread messages:')
        for subject in subjects[:10]:
            print('---- '+subject)
        print('')
        if 10 < len(subjects):
            print('top 10 displayed)\n')


class Gmail(Module):

    def __init__(self):
        tasks = [GetUnreadMail()]
        super().__init__(mod_name='gmail', mod_tasks=tasks, mod_priority=2)