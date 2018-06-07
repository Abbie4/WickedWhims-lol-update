'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''from zone import Zonefrom turbolib.events.events_handler import TurboEventsHandlerfrom turbolib.injector_util import injectfrom turbolib.native.enum import TurboEnumfrom turbolib.special.custom_exception_watcher import log_custom_exceptionHAS_GAME_LOADED = FalseIS_GAME_LOADING = TrueCORE_EVENTS_HANDLER = TurboEventsHandler()
class CoreEventType(TurboEnum):
    __qualname__ = 'CoreEventType'
    ZONE_EARLY_LOAD = 1
    ZONE_LATE_LOAD = 2
    ZONE_SAVE = 3
    ZONE_TEARDOWN = 4

def has_game_loaded():
    '''
    :return: bool -> returns if the game has loaded for the first time
    '''
    return HAS_GAME_LOADED

def is_game_loading():
    '''
    :return: bool -> returns if the game is loading a zone
    '''
    return IS_GAME_LOADING

def register_zone_load_event_method(unique_id=None, priority=0, early=False, late=False):
    '''
    Registers method for the Zone Load Event.
    Use as a decorator on any method without arguments to register it.
    Methods registered for the Zone Load Event will trigger when any game zone loads.
    :param unique_id: str -> unique modification identifier for the modification that uses this function
    :param priority: int -> order at which this method will run at, lower value means higher priority
    :param early: bool -> if should be register as early load method (early load happens before any game objects are ready, use to load external data or check save id)
    :param late: bool -> if should be register as late load method (late load happens after all game objects are ready, use to add and edit tuning or affect sims)
    '''

    def _method_wrapper(event_method):
        if early is True:
            CORE_EVENTS_HANDLER.register_event_method(priority, unique_id, event_method, event_type=CoreEventType.ZONE_EARLY_LOAD)
        if late is True:
            CORE_EVENTS_HANDLER.register_event_method(priority, unique_id, event_method, event_type=CoreEventType.ZONE_LATE_LOAD)
        return event_method

    return _method_wrapper

@inject(Zone, 'load_zone')
def _turbolib_on_early_zone_load(original, self, *args, **kwargs):
    result = original(self, *args, **kwargs)
    try:
        CORE_EVENTS_HANDLER.execute_event_methods(event_type=CoreEventType.ZONE_EARLY_LOAD)
    except Exception as ex:
        log_custom_exception("[TurboLib] Failed to run internal method '_turbolib_on_early_zone_load' at 'Zone.load_zone'.", ex)
    return result

@inject(Zone, 'do_zone_spin_up')
def _turbolib_on_late_zone_load(original, self, *args, **kwargs):
    global HAS_GAME_LOADED, IS_GAME_LOADING
    result = original(self, *args, **kwargs)
    try:
        CORE_EVENTS_HANDLER.execute_event_methods(event_type=CoreEventType.ZONE_LATE_LOAD)
        HAS_GAME_LOADED = True
        IS_GAME_LOADING = False
    except Exception as ex:
        log_custom_exception("[TurboLib] Failed to run internal method '_turbolib_on_late_zone_load' at 'Zone.do_zone_spin_up'.", ex)
    return result

def register_zone_teardown_event(unique_id=None, priority=0):
    '''
    Registers method for the Zone Teardown Event.
    Use as a decorator on any method without arguments to register it.
    Methods registered for the Zone Teardown Event will trigger when any game zone teardowns.
    :param unique_id: str -> unique modification identifier for the modification that uses this function
    :param priority: int -> order at which this method will run at, lower value means higher priority
    '''

    def _method_wrapper(event_method):
        CORE_EVENTS_HANDLER.register_event_method(priority, unique_id, event_method, event_type=CoreEventType.ZONE_TEARDOWN)
        return event_method

    return _method_wrapper

@inject(Zone, 'on_teardown')
def _turbolib_on_zone_teardown(original, self, *args, **kwargs):
    global IS_GAME_LOADING
    result = original(self, *args, **kwargs)
    try:
        CORE_EVENTS_HANDLER.execute_event_methods(event_type=CoreEventType.ZONE_TEARDOWN)
        IS_GAME_LOADING = True
    except Exception as ex:
        log_custom_exception("[TurboLib] Failed to run internal method '_turbolib_on_zone_teardown' at 'Zone.on_teardown'.", ex)
    return result

def register_zone_save_event(unique_id=None, priority=0):
    '''
    Registers method for the Zone Save Event.
    Use as a decorator on any method without arguments to register it.
    Methods registered for the Zone Save Event will trigger when any game zone saves.
    The game triggers a save with id 0 every time a zone is unloaded.
    :param unique_id: str -> unique modification identifier for the modification that uses this function
    :param priority: int -> order at which this method will run at, lower value means higher priority
    '''

    def _method_wrapper(event_method):
        CORE_EVENTS_HANDLER.register_event_method(priority, unique_id, event_method, event_type=CoreEventType.ZONE_SAVE)
        return event_method

    return _method_wrapper

@inject(Zone, 'save_zone')
def _turbolib_on_zone_save(original, self, *args, **kwargs):
    result = original(self, *args, **kwargs)
    try:
        CORE_EVENTS_HANDLER.execute_event_methods(event_type=CoreEventType.ZONE_SAVE)
    except Exception as ex:
        log_custom_exception("[TurboLib] Failed to run internal method '_turbolib_on_zone_save' at 'Zone.save_zone'.", ex)
    return result
