"""
    Finds and returns the latest bitcoin price

    Usage Examples:
        - "What is the price of bitcoin?"
        - "How much is a bitcoin worth?"
"""

from athena.classes.module import Module
from athena.classes.task import ActiveTask
from athena.api_library import bitcoin_api


class GetValueTask(ActiveTask):
    
    def __init__(self):
        super().__init__(words=['bitcoin'])

    def action(self, text):
        bitcoin_price = str(bitcoin_api.get_data('last'))
        self.speak(bitcoin_price)


class Bitcoin(Module):
    
    def __init__(self):
        tasks = [GetValueTask()]
        super().__init__('bitcoin', tasks, priority=2)