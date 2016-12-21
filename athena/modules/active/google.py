"""
DISABLED by default (since this module can be buggy)

Handles most general questions (including math!)

Usage Examples:
    - "How tall is Mount Everest?"
"""

from athena.classes.module import Module
from athena.classes.task import ActiveTask
from athena.apis import api_lib
from athena import log


class AnswerTask(ActiveTask):

    def __init__(self):
        p_list = [r".*\b((who|what|when|where|why|how)(\')?(s)?|" +
                  r"(can|are|is|will|define|show me|say))\b.*"]
        super(AnswerTask, self).__init__(patterns=p_list)

    def action(self, text):
        log.info('\n~ Searching Google...\n')
        api_lib['voice_browse_api'].search(text)


class Google(Module):

    def __init__(self):
        tasks = [AnswerTask()]
        super(Google, self).__init__('google', tasks, priority=1, enabled=False)
