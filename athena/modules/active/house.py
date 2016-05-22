"""
        File Name: hello_world.py
        Shop with your voice
        Usage Examples:
        - "Order me some pizza"
"""

from athena.classes.module import Module
from athena.classes.task import ActiveTask


class ControlHouseTask(ActiveTask):

    def __init__(self):
        # Matches any statement with these words
        super().__init__(patterns=[r'.*\b(?:turn (off|on))\b (.*)'])

    def match(self, text):
        return self.match_and_save_groups(text, {1: 'verb', 2: 'thing'})

    def action(self, text):
        if self.verb.lower() == "on":
            return ('shop', 'Turning on '+self.thing+'.')
        return ('shop', 'Turning off '+self.thing+'.')


# This is a bare-minimum module
class ControlHouse(Module):

    def __init__(self):
        tasks = [ControlHouseTask()]
        super().__init__('house', tasks, priority=2)
