"""
    Finds and returns the latest bitcoin price

    Usage Examples:
        - "What is the price of bitcoin?"
        - "How much is a bitcoin worth?"
"""

from athena.classes.module import Module
from athena.classes.task import ActiveTask
from athena import brain


class QuitTask(ActiveTask):
    
    def __init__(self):
        super().__init__(words=['quit', 'stop'])

    def action(self, text):
        brain.inst.quit()

class ListModulesTask(ActiveTask):
    
    def __init__(self):
        super().__init__(words=['list modules', 'list mods'])

    def action(self, text):
        brain.inst.list_mods()
        
class ToggleModuleTask(ActiveTask):
    
    def __init__(self):
        super().__init__(patterns=[r'.*\b(enable|add|disable|remove) (.*)'])
        self.groups = {1: 'enable', 2: 'module'}

    def match(self, text):
        return self.match_and_save_groups(text, self.groups)

    def action(self, text):
        mod_name = self.module.lower().strip().replace(' ', '_')
        if 'disable' in self.enable.lower() or 'remove' in self.enable.lower():
            brain.inst.disable_mod(mod_name)
        else:
            brain.inst.enable_mod(mod_name)
        

class AthenaControl(Module):
    
    def __init__(self):
        tasks = [QuitTask(), ListModulesTask(), ToggleModuleTask()]
        super().__init__('athena_control', tasks, priority=3)