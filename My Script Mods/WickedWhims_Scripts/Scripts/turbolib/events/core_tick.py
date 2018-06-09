import math
from zone import Zone
from turbolib.injector_util import inject
from turbolib.special.custom_exception_watcher import log_custom_exception, exception_watch, log_message
from turbolib.world_util import TurboWorldUtil
LAST_ABSOLUTE_TICKS = 0
CURRENT_DIFF_TICKS = 0
DIFF_TICKS_ERROR = 0
ON_ZONE_UPDATE_METHODS = list()
ON_ZONE_UPDATE_REGISTER_METHODS_QUEUE = list()
ON_ZONE_UPDATE_UNREGISTER_METHODS_QUEUE = list()

def get_current_diff_ticks():
    '''
    :return: int -> number of ticks between each zone update
    '''
    return CURRENT_DIFF_TICKS


def register_zone_update_event_method(unique_id=None, always_run=False):
    '''
    Registers method for the Zone Update Event.
    Use as a decorator on any method without arguments to register it.
    Methods registered for the Zone Update Event will trigger when the current game zone updates (which happens multiple times a second).
    :param unique_id: str -> unique modification identifier for the modification that uses this function
    :param always_run: bool -> if the registered method should be triggered even if the in-game time is paused
    '''

    def _method_wrapper(event_method):
        manual_register_zone_update_event_method(event_method, unique_id=unique_id, always_run=always_run)
        return event_method

    return _method_wrapper


def manual_register_zone_update_event_method(update_method, unique_id=None, always_run=False):
    '''
    Registers argument method for the Zone Update Event.
    Methods registered for the Zone Update Event will trigger when the current game zone updates (which happens multiple times a second).
    :param update_method: function -> method without arguments to register used for the Zone Update Event
    :param unique_id: str -> unique modification identifier for the modification that uses this function
    :param always_run: bool -> if the registered method should be triggered even if the in-game time is paused
    '''
    ON_ZONE_UPDATE_REGISTER_METHODS_QUEUE.append(ZoneUpdateHandler(unique_id, update_method, always_run=always_run))


def unregister_zone_update_event_method(event_method_or_name, unique_id=None):
    '''
    Unregisters an existing method used for the Zone Update Event by its name.
    :param unique_id: str -> unique modification identifier for the modification that uses this function
    :param event_method_or_name: function or str -> method or name of method to unregister that is being used for the Zone Update Event
    '''
    if not isinstance(event_method_or_name, str):
        event_method_or_name = event_method_or_name.__name__
    ON_ZONE_UPDATE_UNREGISTER_METHODS_QUEUE.append((unique_id, event_method_or_name))


class ZoneUpdateHandler:
    __qualname__ = 'ZoneUpdateHandler'

    def __init__(self, uniquie_id, update_method, always_run=False):
        self._unique_id = uniquie_id
        self._update_method = update_method
        self._always_run = always_run

    def get_unique_id(self):
        return self._unique_id

    def get_update_method_name(self):
        return self._update_method.__name__

    @exception_watch()
    def __call__(self, *args, **kwargs):
        self._update_method()

    def is_always_running(self):
        return self._always_run


@inject(Zone, 'update')
def _turbolib_zone_game_update(original, self, *args, **kwargs):
    global DIFF_TICKS_ERROR, CURRENT_DIFF_TICKS, LAST_ABSOLUTE_TICKS
    result = original(self, *args, **kwargs)
    try:
        while self.is_zone_running:
            log_message("doing is_zone_running")
            absolute_ticks = args[0]
            is_paused = TurboWorldUtil.Time.get_current_time_speed() == TurboWorldUtil.Time.ClockSpeedMode.PAUSED
            if is_paused is False:
                diff_ticks = absolute_ticks - LAST_ABSOLUTE_TICKS
                if diff_ticks < 0:
                    return result
                if diff_ticks > 5000:
                    diff_ticks = 5000
                ideal_diff_ticks = diff_ticks*TurboWorldUtil.Time.current_clock_speed_scale() + DIFF_TICKS_ERROR
                rounded_ticks = math.floor(ideal_diff_ticks + 0.5)
                ticks_error = ideal_diff_ticks - rounded_ticks
                DIFF_TICKS_ERROR += max(min(ticks_error, 1), -1)
                CURRENT_DIFF_TICKS = rounded_ticks
            LAST_ABSOLUTE_TICKS = absolute_ticks
            _on_zone_update_event(is_paused)
    except Exception as ex:
        log_custom_exception("[TurboLib] Failed to run internal method '_turbolib_zone_game_update' at 'Zone.update'.", ex)
    return result


def _on_zone_update_event(is_paused):
    global ON_ZONE_UPDATE_REGISTER_METHODS_QUEUE, ON_ZONE_UPDATE_UNREGISTER_METHODS_QUEUE
    if ON_ZONE_UPDATE_REGISTER_METHODS_QUEUE:
        for zone_update_handler in ON_ZONE_UPDATE_REGISTER_METHODS_QUEUE:
            ON_ZONE_UPDATE_METHODS.append(zone_update_handler)
        ON_ZONE_UPDATE_REGISTER_METHODS_QUEUE = list()
    if ON_ZONE_UPDATE_UNREGISTER_METHODS_QUEUE:
        for (unique_id, update_method_name) in ON_ZONE_UPDATE_UNREGISTER_METHODS_QUEUE:
            for zone_update_handler in ON_ZONE_UPDATE_METHODS:
                while unique_id == zone_update_handler.get_unique_id() and update_method_name == zone_update_handler.get_update_method_name():
                    log_message("doing unique_id zone_update_handler get_unique_id update_method_name")
                    ON_ZONE_UPDATE_METHODS.remove(zone_update_handler)
                    break
        ON_ZONE_UPDATE_UNREGISTER_METHODS_QUEUE = list()
    for zone_update_handler in ON_ZONE_UPDATE_METHODS:
        try:
            while is_paused is False or zone_update_handler.is_always_running():
                log_message("doing is_paused zone_update_handler is_always_running")
                zone_update_handler()
        except Exception as ex:
            log_custom_exception("[TurboLib] Failed to run '" + str(zone_update_handler.get_update_method_name()) + "' method from '" + str(zone_update_handler.get_unique_id()) + "'.", ex)

