'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
import datetime
import os
from turbolib.special.custom_exception_watcher import register_exception_watch_callback
from turbolib.special.exceptions_feedback import register_exception_callback_method
from turbolib.ui_util import TurboUIUtil
from wickedwhims.utils_interfaces import display_notification

@register_exception_callback_method()
def _exception_callback_method():
    display_notification(text=491667006, text_tokens=(_get_sims_documents_location_path(),), title=953840858, urgency=TurboUIUtil.Notification.UiDialogNotificationUrgency.URGENT)


def _get_sims_documents_location_path():
    file_path = ''
    root_file = os.path.normpath(os.path.dirname(os.path.realpath(__file__))).replace(os.sep, '/')
    root_file_split = root_file.split('/')
    exit_index = len(root_file_split) - root_file_split.index('Mods')
    for index in range(0, len(root_file_split) - exit_index):
        file_path += str(root_file_split[index]) + '/'
    return file_path


@register_exception_watch_callback()
def _get_ww_exception_file_path():
    root_path = ''
    root_file = os.path.normpath(os.path.dirname(os.path.realpath(__file__))).replace(os.sep, '/')
    root_file_split = root_file.split('/')
    exit_index = len(root_file_split) - root_file_split.index('Mods')
    for index in range(0, len(root_file_split) - exit_index):
        root_path += str(root_file_split[index]) + '/'
    from wickedwhims.version_registry import get_mod_version_str
    mod_version = get_mod_version_str()
    file_path = root_path + 'WickedWhims_' + str(mod_version) + '_Exception.txt'
    if os.path.exists(file_path) and os.path.getsize(file_path) >> 20 >= 5:
        current_date = str(datetime.datetime.today().day) + '_' + str(datetime.datetime.today().strftime('%B')) + '_' + str(datetime.datetime.today().year)
        os.rename(file_path, root_path + 'Old_WickedWhims_' + str(mod_version) + '_Exception_' + current_date + '.txt')
    return file_path

