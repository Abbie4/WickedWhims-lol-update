'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from sims.occult.occult_tracker import OccultTracker
from sims.sim_info import SimInfo
from turbolib.events.events_handler import TurboEventsHandler
from turbolib.injector_util import inject
from turbolib.native.enum import TurboEnum
from turbolib.special.custom_exception_watcher import log_custom_exception
SIM_EVENTS_HANDLER = TurboEventsHandler()

class SimEventType(TurboEnum):
    __qualname__ = 'SimEventType'
    SIM_EARLY_INIT = 1
    SIM_LATE_INIT = 2
    SIM_OCCULT_CHANGE = 3

def register_sim_info_instance_init_event_method(unique_id=None, priority=0, early=False, late=False):

    def _method_wrapper(event_method):
        if early is True:
            SIM_EVENTS_HANDLER.register_event_method(priority, unique_id, event_method, event_type=SimEventType.SIM_EARLY_INIT)
        if late is True:
            SIM_EVENTS_HANDLER.register_event_method(priority, unique_id, event_method, event_type=SimEventType.SIM_LATE_INIT)
        return event_method

    return _method_wrapper

@inject(SimInfo, '__init__')
def _turbolib_sim_info_init(original, self, *args, **kwargs):
    result = original(self, *args, **kwargs)
    try:
        SIM_EVENTS_HANDLER.execute_event_methods(self, event_type=SimEventType.SIM_EARLY_INIT)
    except Exception as ex:
        log_custom_exception("[TurboLib] Failed to run internal method '_turbolib_sim_info_init' at 'SimInfo.__init__'.", ex)
    return result

@inject(SimInfo, 'load_sim_info')
def _turbolib_sim_info_load(original, self, *args, **kwargs):
    result = original(self, *args, **kwargs)
    try:
        SIM_EVENTS_HANDLER.execute_event_methods(self, event_type=SimEventType.SIM_LATE_INIT)
    except Exception as ex:
        log_custom_exception("[TurboLib] Failed to run internal method '_turbolib_sim_info_load' at 'SimInfo.load_sim_info'.", ex)
    return result

def register_sim_occult_type_change_event_method(unique_id=None, priority=0):

    def _method_wrapper(event_method):
        SIM_EVENTS_HANDLER.register_event_method(priority, unique_id, event_method, event_type=SimEventType.SIM_OCCULT_CHANGE)
        return event_method

    return _method_wrapper

@inject(OccultTracker, 'switch_to_occult_type')
def _turbolib_on_switch_to_occult_type(original, self, *args, **kwargs):
    result = original(self, *args, **kwargs)
    try:
        sim_info = self._sim_info
        occult_type = args[0]
        SIM_EVENTS_HANDLER.execute_event_methods(sim_info, occult_type, event_type=SimEventType.SIM_OCCULT_CHANGE)
    except Exception as ex:
        log_custom_exception("[TurboLib] Failed to run internal method '_turbolib_on_switch_to_occult_type' at 'OccultTracker.switch_to_occult_type'.", ex)
    return result

