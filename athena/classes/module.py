"""
The "Module" class represents a collection of tasks
"""

DEFAULT_PRIORITY = 0
DEFAULT_GREEDY = True
DEFAULT_ENABLED = True


class Module(object):

    def __init__(self,
                 name,
                 mod_tasks=[],
                 priority=DEFAULT_PRIORITY,
                 greedy=DEFAULT_GREEDY,
                 enabled=DEFAULT_ENABLED):

        # Make a unique mod name
        self.name = name

        # Tasks find input text patterns and perform an action
        self.tasks = mod_tasks
        self.tasks.sort(key=lambda task: task.priority, reverse=True)

        # Modules match and execute in prioritized order
        self.priority = priority

        # Greedy mods stop future mods from being matched
        self.greedy = greedy

        # True if the mod is enabled
        self.enabled = enabled

    def disable(self):
        self.enabled = False

    def enable(self):
        self.enabled = True
