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


class AnswerTask(ActiveTask):
    
    def __init__(self):
        p_list = [r'.*\b((who|what|when|where|why|how)(\')?(s)?|(can|are|is|will))\b.*']
        super().__init__(patterns=p_list)
    
    def action(self, text):
        query = wolframalpha.Client(settings.WOLFRAM_KEY).query(text)
        
        if len(query.pods) > 1 and query.pods[1].text:
            answer = query.pods[1].text.replace('|', '')
            self.speak(answer, show_text=True)
        else:
            self.speak(settings.ERROR)
        
        
class Wolfram(Module):

    def __init__(self):
        tasks = [AnswerTask()]
        super().__init__('wolfram', tasks, priority=1)

