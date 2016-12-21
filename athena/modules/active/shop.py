"""
File Name: hello_world.py
Shop with your voice
Usage Examples:
- "Order me some pizza"
"""

from athena.classes.module import Module
from athena.classes.task import ActiveTask


class OrderSomething(ActiveTask):

    def __init__(self):
        # Matches any statement with these words
        super(OrderSomething, self).__init__(patterns=[r'^\b(order|buy)(?: me)?\b(.*)'])

    def match(self, text):
        return self.match_and_save_groups(text, {1: 'verb', 2: 'thing'})

    def action(self, text):
        self.thing = self.thing.replace('my', 'your')
        self.thing = self.thing.replace('favor', 'Favor')
        if self.verb.lower() == "order":
            return ('shop', 'Ordering you '+self.thing+'.')
        return ('shop', 'Buying you '+self.thing+'.')


class CancelOrder(ActiveTask):

    def __init__(self):
        # Matches any statement with these words
        super(CancelOrder, self).__init__(patterns=[r'.*\b(cancel.*order)\b.*'])

    def action(self, text):
        return ('shop', 'Canceling previous order.')


# This is a bare-minimum module
class HelloWorld(Module):

    def __init__(self):
        tasks = [OrderSomething(), CancelOrder()]
        super(HelloWorld, self).__init__('shop', tasks, priority=2)
