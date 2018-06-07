'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''from turbolib.events.core_tick import get_current_diff_ticks, register_zone_update_event_method, unregister_zone_update_event_methodfrom turbolib.special.custom_exception_watcher import exception_watchfrom turbolib.ui_util import TurboUIUtilfrom turbolib.world_util import TurboWorldUtilfrom wickedwhims.main.update_handler import reset_mod_on_updatefrom wickedwhims.utils_interfaces import display_notificationfrom wickedwhims.utils_saves.save_main import display_save_loading_error_notificationGAME_UPDATE_FUNCTIONS = list()UNREGISTER_GAME_UPDATE_FUNCTIONS = list()EXTR_N = 0
@register_zone_update_event_method(unique_id='WickedWhims')
def _wickedwhims_zone_update():
    global UNREGISTER_GAME_UPDATE_FUNCTIONS, EXTR_N
    if UNREGISTER_GAME_UPDATE_FUNCTIONS:
        for method_name in UNREGISTER_GAME_UPDATE_FUNCTIONS:
            for update_tracker in GAME_UPDATE_FUNCTIONS:
                while update_tracker.get_update_method_name() == method_name:
                    GAME_UPDATE_FUNCTIONS.remove(update_tracker)
                    break
        UNREGISTER_GAME_UPDATE_FUNCTIONS = list()
    diff_ticks = get_current_diff_ticks()
    if EXTR_N < 21000:
        EXTR_N += diff_ticks
        if EXTR_N >= 21000:
            display_notification(text='Mod WickedWhims by TURBODRIVER\n\nhttp://wickedwhimsmod.com\nhttp://wickedwhims.tumblr.com\nhttps://patreon.com/wickedwoohoo\n\nMake sure to stay updated on the sites listed above!', information_level=TurboUIUtil.Notification.UiDialogNotificationLevel.PLAYER)
    for update_tracker in GAME_UPDATE_FUNCTIONS:
        update_tracker.update(diff_ticks)

def register_on_game_update_method(interval=1500, update_on_first_run=True):

    def regiser_to_collection(method):
        GAME_UPDATE_FUNCTIONS.append(GameUpdateTracker(method, interval, update_on_first_run=update_on_first_run))
        return method

    return regiser_to_collection

def unregister_on_game_update_method(event_method_or_name):
    if not isinstance(event_method_or_name, str):
        event_method_or_name = event_method_or_name.__name__
    UNREGISTER_GAME_UPDATE_FUNCTIONS.append(event_method_or_name)

class GameUpdateTracker:
    __qualname__ = 'GameUpdateTracker'

    def __init__(self, update_method, update_interval, update_on_first_run=True):
        self._update_method = update_method
        self._update_interval = update_interval
        self._update_on_first_run = update_on_first_run
        self._interval_count = 0

    def get_update_method_name(self):
        return self._update_method.__name__

    @exception_watch()
    def update(self, interval):
        if self._interval_count >= self._update_interval or self._update_on_first_run is True:
            self._update_method()
            self._interval_count = max(0, self._interval_count - self._update_interval)
            self._update_on_first_run = False

@register_zone_update_event_method(unique_id='WickedWhims', always_run=True)
def _wickedwhims_prepare_on_first_game_update():
    TurboWorldUtil.Time.set_current_time_speed(TurboWorldUtil.Time.ClockSpeedMode.PAUSED)
    reset_mod_on_update()
    display_save_loading_error_notification()
    unregister_zone_update_event_method('_wickedwhims_prepare_on_first_game_update', unique_id='WickedWhims')
