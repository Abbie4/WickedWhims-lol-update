'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from zone import Zone
from turbolib.events.events_handler import TurboEventsHandler
from turbolib.injector_util import inject
from turbolib.native.enum import TurboEnum
from turbolib.special.custom_exception_watcher import log_custom_exception
BUILDBUY_EVENTS_HANDLER = TurboEventsHandler()

class BuildBuyEventType(TurboEnum):
    __qualname__ = 'BuildBuyEventType'
    BUILD_BUY_ENTER = 1
    BUILD_BUY_EXIT = 2

def register_buildbuy_state_change_event_method(unique_id=None, priority=0, on_enter=False, on_exit=False):

    def _method_wrapper(event_method):
        if on_enter is True:
            BUILDBUY_EVENTS_HANDLER.register_event_method(priority, unique_id, event_method, event_type=BuildBuyEventType.BUILD_BUY_ENTER)
        if on_exit is True:
            BUILDBUY_EVENTS_HANDLER.register_event_method(priority, unique_id, event_method, event_type=BuildBuyEventType.BUILD_BUY_EXIT)
        return event_method

    return _method_wrapper

@inject(Zone, 'on_build_buy_enter')
def _turbolib_build_buy_enter(original, self, *args, **kwargs):
    result = original(self, *args, **kwargs)
    try:
        BUILDBUY_EVENTS_HANDLER.execute_event_methods(event_type=BuildBuyEventType.BUILD_BUY_ENTER)
    except Exception as ex:
        log_custom_exception("[TurboLib] Failed to run internal method '_turbolib_build_buy_enter' at 'Zone.on_build_buy_enter'.", ex)
    return result

@inject(Zone, 'on_build_buy_exit')
def _turbolib_build_buy_exit(original, self, *args, **kwargs):
    result = original(self, *args, **kwargs)
    try:
        BUILDBUY_EVENTS_HANDLER.execute_event_methods(event_type=BuildBuyEventType.BUILD_BUY_EXIT)
    except Exception as ex:
        log_custom_exception("[TurboLib] Failed to run internal method '_turbolib_build_buy_exit' at 'Zone.on_build_buy_exit'.", ex)
    return result

