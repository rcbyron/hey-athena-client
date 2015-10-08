'''
Created on Jul 19, 2015

@author: Connor
'''
from client.classes.module import Module
from client.classes.task import ActiveTask
from client.modules.api_library import gmail_api

class GetUnreadMail(ActiveTask):
    def match(self, text):
        for p in self.patterns:
            if p.match(text):
                return True
        return False
    
    def action(self, text):
        
        subjects = self.api.unread_subjects()
        if len(subjects) < 1:
            self.speak('You have no important unread messages.')
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
            print('(top 10 displayed)\n')


class Gmail(Module):
    def __init__(self):
        g_api = gmail_api.GmailApi()
        tasks = [GetUnreadMail([r'.*\b(mail)\b.*'], api=g_api)]
        super().__init__(mod_name='gmail', mod_tasks=tasks, mod_priority=2) 