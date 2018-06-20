'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
import webbrowser
from turbolib.events.core import register_zone_load_event_method, has_game_loaded
from turbolib.ui_util import TurboUIUtil
from turbolib.world_util import TurboWorldUtil
from wickedwhims.utils_interfaces import display_okcancel_dialog
from wickedwhims.utils_saves.save_version import update_version_save_data, get_version_save_data
from wickedwhims.version_control import is_mod_outdated
from wickedwhims.version_registry import is_patreon_release

@register_zone_load_event_method(unique_id='WickedWhims', priority=500, late=True)
def _wickedwhims_check_for_updates():
    if has_game_loaded():
        return
    save_version_dict = get_version_save_data()
    if save_version_dict is not None and (len(save_version_dict) > 0 and 'ignore_update' in save_version_dict) and save_version_dict['ignore_update'] is True:
        return
    if not is_mod_outdated():
        return
    open_update_asking_dialog()


def open_update_asking_dialog():

    def _update_asking_callback(dialog):
        if not TurboUIUtil.ObjectPickerDialog.get_response_result(dialog):
            update_version_save_data({'ignore_update': True})
            return False
        if is_patreon_release():
            webbrowser.open('https://www.patreon.com/wickedwoohoo/posts')
        else:
            webbrowser.open('https://wickedwhimsmod.com/')
        TurboWorldUtil.Time.set_current_time_speed(TurboWorldUtil.Time.ClockSpeedMode.PAUSED)
        return True

    display_okcancel_dialog(text=1408374347, title=1056912566, ok_text=3339076708, cancel_text=3870501498, callback=_update_asking_callback)

