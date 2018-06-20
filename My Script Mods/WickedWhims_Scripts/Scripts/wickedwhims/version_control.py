'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
import threading
import urllib.request
from wickedwhims.version_registry import get_mod_version_control_data, is_patreon_release
VERSION_CONTROL = None

def _retrieve_version_control():
    global VERSION_CONTROL
    if is_patreon_release():
        url = 'http://pastebin.com/raw/AtvxnZn5'
    else:
        url = 'http://pastebin.com/raw/sMmkykvC'
    try:
        with urllib.request.urlopen(url, timeout=4.0) as response:
            VERSION_CONTROL = _parse_version_control(str(response.read().decode('utf-8')).strip())
    except:
        pass


def _parse_version_control(version_data):
    if len(version_data) <= 1 or len(version_data) > 10:
        return
    version_data_split = version_data.split('|')
    if len(version_data_split) < 2:
        return
    try:
        return tuple([int(v) for v in version_data_split])
    except:
        return


def _async_retrieve_version_control():
    threading.Thread(target=_retrieve_version_control, daemon=True).start()

_async_retrieve_version_control()

def is_mod_outdated():
    if VERSION_CONTROL is None:
        return False
    (current_release_number, current_hotfix_number) = get_mod_version_control_data()
    (control_release_number, control_hotfix_number) = VERSION_CONTROL
    if current_release_number < control_release_number:
        return True
    if current_release_number == control_release_number and current_hotfix_number < control_hotfix_number:
        return True
    return False

