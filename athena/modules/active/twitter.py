"""
    Allows users to send tweets via voice command

    Requires:
        - IFTTT configuration

    Usage Examples:
        - "Tweet What's up guys?"
        - "Post What's up everyone? to twitter"
"""

from athena.classes.module import Module
from athena.classes.task import ActiveTask
from athena.api_library import ifttt_api as ifttt


class SendTweetTask(ActiveTask):

    def __init__(self):
        super(SendTweetTask, self).__init__(patterns=[r'.*?\btweet (.+)',
                                   r'.*\bpost (.+)\bto twitter\b',
                                   r'.*\bpost to twitter\b(.+)'])

    def match(self, text):
        return self.match_and_save_groups(text, {1: 'tweet'})

    def action(self, text):
        self.tweet += ' - from Athena'
        print('\n~ Tweet: '+self.tweet)
        self.speak('Sending tweet... ', show_text=True)
        ifttt.trigger('voice_tweet', self.tweet)


class Twitter(Module):

    def __init__(self):
        tasks = [SendTweetTask()]
        super(Twitter, self).__init__('twitter', tasks, priority=3)
