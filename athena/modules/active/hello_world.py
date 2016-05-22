"""
        File Name: hello_world.py
        Tells you what to eat
        Usage Examples:
        - "What type of food should I eat tonight"
"""

from athena.classes.module import Module
from athena.classes.task import ActiveTask


class SpeakPhrase(ActiveTask):

    def __init__(self):
        # Matches any statement with these words
        super(SpeakPhrase, self).__init__(words=['eat', 'food', 'type'])

    def action(self, text):
        self.speak('You should eat Mexican food tonight')


# This is a bare-minimum module
class HelloWorld(Module):

    def __init__(self):
        tasks = [SpeakPhrase()]
        super(HelloWorld, self).__init__('hello_world', tasks, priority=2)
