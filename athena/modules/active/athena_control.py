"""
A module for controlling Athena

Usage Examples:
    - "Athena stop"
    - "Enable Google"
"""

from athena.classes.module import Module
from athena.classes.task import ActiveTask
from athena import brain, log


class QuitTask(ActiveTask):

    def __init__(self):
        super(QuitTask, self).__init__(patterns=[r'\b(athena )?(quit|stop)\b.*'])

    def action(self, text):
        brain.inst.quit()


class ListModulesTask(ActiveTask):

    def __init__(self):
        super(ListModulesTask, self).__init__(words=['list modules', 'list mods'])

    def action(self, text):
        brain.inst.list_mods()


class ToggleModuleTask(ActiveTask):

    def __init__(self):
        super(ToggleModuleTask, self).__init__(patterns=[r'.*\b(enable|add|disable|remove) (.*)'])
        self.groups = {1: 'enable', 2: 'module'}

    def match(self, text):
        return self.match_and_save_groups(text, self.groups)

    def action(self, text):
        mod_name = self.module.lower().strip().replace(' ', '')
        if 'disable' in self.enable.lower() or 'remove' in self.enable.lower():
            log.info("Attempting to disable '"+mod_name+"'")
            brain.inst.disable_mod(mod_name)
        else:
            log.info("Attempting to enable '"+mod_name+"'")
            brain.inst.enable_mod(mod_name)


class AthenaControl(Module):

    def __init__(self):
        tasks = [QuitTask(), ListModulesTask(), ToggleModuleTask()]
        super(AthenaControl, self).__init__('athena_control', tasks, priority=3)
