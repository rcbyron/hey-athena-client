"""
Handles most general questions (including math!)

Requires:
    - WolframAlpha API key

Usage Examples:
    - "How tall is Mount Everest?"
    - "What is the derivative of y = 2x?"
"""

import wolframalpha

from athena.classes.module import Module
from athena.classes.task import ActiveTask
from athena import settings

wolfram_client = wolframalpha.Client(settings.WOLFRAM_KEY)


class AnswerTask(ActiveTask):

    def match(self, text):
        return True

    def action(self, text):
        try:
            query = wolfram_client.query(text)
            self.speak(next(query.results).text)
        except:
            self.speak(settings.NO_MODULES)


class Wolfram(Module):

    def __init__(self):
        tasks = [AnswerTask()]
        super(Wolfram, self).__init__('wolfram', tasks, priority=0)
