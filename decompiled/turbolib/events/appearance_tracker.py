'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from buffs.appearance_modifier.appearance_tracker import AppearanceTracker
from sims.sim_info_base_wrapper import SimInfoBaseWrapper
from sims4.callback_utils import CallableList
from turbolib.injector_util import inject
from turbolib.special.custom_exception_watcher import log_custom_exception

@inject(SimInfoBaseWrapper, '__init__')
def _turbolib_on_sim_info_base_wrapper_init(original, self, *args, **kwargs):
    try:
        self.appearance_tracker_changed = CallableList()
    except Exception as ex:
        log_custom_exception("[TurboLib] Failed to inject 'appearance_tracker_changed' variable at 'SimInfoBaseWrapper.__init__'.", ex)
    return original(self, *args, **kwargs)

@inject(AppearanceTracker, 'apply_appearance_modifiers')
def _turbolib_on_apply_appearance_modifiers(original, self, *args, **kwargs):
    result = original(self, *args, **kwargs)
    try:
        while self is self._sim_info.appearance_tracker:
            self._sim_info.appearance_tracker_changed(self._sim_info)
    except Exception as ex:
        log_custom_exception("[TurboLib] Failed to run injected method 'appearance_tracker_changed' CallableList at 'AppearanceTracker.apply_appearance_modifiers'.", ex)
    return result

