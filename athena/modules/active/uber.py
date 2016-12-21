"""
File Name: uber.py

This module demonstrates how you could call an uber

Usage Examples:
- "Order me an uber"
"""

from athena.classes.module import Module
from athena.classes.task import ActiveTask

UBER_REGEX = r"^\b(order|call|request)(?: me)? "
UBER_REGEX += r"((an |a )?(lyft|uber|taxi|limo)).*"

CANCEL_REGEX = r".*\b(cancel.*(order|request|uber|lyft))\b.*"


class CallUberTask(ActiveTask):

    def __init__(self):
        # Matches any statement with these words
        super(CallUberTask, self).__init__(patterns=[UBER_REGEX])

    def match(self, text):
        # Matches the 1 & 2 regex capture groups and stores them in variables
        return self.match_and_save_groups(text, {1: 'verb', 2: 'thing'})

    def action(self, text):
        return self.speak('Requesting '+self.thing+' for you.')


class CancelUberTask(ActiveTask):

    def __init__(self):
        # Matches any statement with these words
        super(CancelUberTask, self).__init__(patterns=[CANCEL_REGEX])

    def action(self, text):
        return self.speak('Canceling ride sharing request.')


# This is a bare-minimum module
class CallUber(Module):

    def __init__(self):
        tasks = [CallUberTask(), CancelUberTask()]
        super(CallUber, self).__init__('uber', tasks, priority=2)
