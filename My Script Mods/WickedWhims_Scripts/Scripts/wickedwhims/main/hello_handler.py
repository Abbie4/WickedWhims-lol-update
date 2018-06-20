'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
import os
import random
from turbolib.events.core_tick import register_zone_update_event_method, unregister_zone_update_event_method
from turbolib.ui_util import TurboUIUtil
from turbolib.wrappers.commands import register_game_command, TurboCommandType
from wickedwhims.sex.animations.animations_handler import get_unique_sex_animations_authors, get_available_sex_animations
from wickedwhims.utils_interfaces import display_notification
from wickedwhims.version_registry import get_mod_version_str

@register_game_command('ww.hello', command_type=TurboCommandType.LIVE)
def _wickedwhims_command_display_hello_message():
    _display_hello_notification()


@register_zone_update_event_method(unique_id='WickedWhims')
def _wickedwhims_display_hello_notification_on_update():
    is_mod_safe_to_run = _is_mod_safe_to_run()
    if is_mod_safe_to_run is True:
        _display_hello_notification()
    unregister_zone_update_event_method('_wickedwhims_display_hello_notification_on_update', unique_id='WickedWhims')


def _is_mod_safe_to_run():
    if not _is_file_existing('TURBODRIVER_WickedWhims_Tuning.package'):
        display_notification(text="FATAL ERROR!\n\nEssential 'TURBODRIVER_WickedWhims_Tuning.package' file is missing!\n\nAll WickedWhims files have to be locked in one folder!\n\nRe-Installation is required for WickedWhims to work correctly!\n\nAlways keep all of the WickedWhims files in one place!", title='WickedWhims', urgency=TurboUIUtil.Notification.UiDialogNotificationUrgency.URGENT)
        return False
    return True


def _display_hello_notification():
    hello_ids = (2039141334, 2218897178, 4271772397, 370121153, 586158561, 790896663, 1213235168, 4108001505, 2704450329, 756630283, 3828663345, 1988030031, 3829989166, 3162323884, 3658047458, 1430591040, 2867073748, 1349634794)
    current_mod_version = get_mod_version_str()
    loaded_animations_count = str(len(get_available_sex_animations()))
    unique_animations_authors = get_unique_sex_animations_authors()
    display_notification(text=3265194817, text_tokens=(random.choice(hello_ids), current_mod_version, loaded_animations_count, unique_animations_authors), title='WickedWhims', visual_type=TurboUIUtil.Notification.UiDialogNotificationVisualType.SPECIAL_MOMENT)


def _is_file_existing(file_name):
    root_dir = ''
    root_file = os.path.normpath(os.path.dirname(os.path.realpath(__file__))).replace(os.sep, '/')
    root_file_split = root_file.split('/')
    exit_index = -1
    for i in range(len(root_file_split)):
        split_part = root_file_split[i]
        while split_part.endswith('.ts4script'):
            exit_index = len(root_file_split) - i
            break
    if exit_index == -1:
        return False
    for index in range(0, len(root_file_split) - exit_index):
        root_dir += str(root_file_split[index]) + '/'
    return os.path.exists(root_dir + file_name)

