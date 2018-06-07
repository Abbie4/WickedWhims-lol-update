'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''import jsonimport os.pathfrom turbolib.resource_util import TurboResourceUtilfrom turbolib.ui_util import TurboUIUtilfrom wickedwhims.utils_interfaces import display_notificationHAS_ERROR_WHEN_LOADING = False
def set_has_save_loading_error():
    global HAS_ERROR_WHEN_LOADING
    HAS_ERROR_WHEN_LOADING = True

def display_save_loading_error_notification():
    if HAS_ERROR_WHEN_LOADING is True:
        display_notification(text=3371966942, urgency=TurboUIUtil.Notification.UiDialogNotificationUrgency.URGENT, is_safe=True)

def remove_scratch_save_files():
    remove_file(get_save_dir() + get_save_id('disabled_animations', slot_id=0) + '.json')
    remove_file(get_save_dir() + get_save_id('game_events', slot_id=0) + '.json')
    remove_file(get_save_dir() + get_save_id('sex_handlers', slot_id=0) + '.json')
    remove_file(get_save_dir() + get_save_id('sim', slot_id=0) + '.json')
    remove_file(get_save_dir() + get_save_id('statistics', slot_id=0) + '.json')
    remove_file(get_save_dir() + get_save_id('version', slot_id=0) + '.json')
    remove_file(get_save_dir() + get_save_id('general', slot_id=0) + '.json')

def get_save_id(prefix, slot_id=-1):
    current_save_slot_id = slot_id if slot_id != -1 else TurboResourceUtil.Persistance.get_save_slot_id()
    return prefix + '_slot_' + str(current_save_slot_id) + '_guid_' + str(TurboResourceUtil.Persistance.get_save_guid())

def get_save_dir():
    root_dir = ''
    root_file = os.path.normpath(os.path.dirname(os.path.realpath(__file__))).replace(os.sep, '/')
    root_file_split = root_file.split('/')
    exit_index = len(root_file_split) - root_file_split.index('Mods')
    for index in range(0, len(root_file_split) - exit_index):
        root_dir += str(root_file_split[index]) + '/'
    root_dir += 'saves/WickedWhimsMod/'
    if not os.path.exists(root_dir):
        os.makedirs(root_dir)
    return root_dir

def save_json_file(file_path, file_dict_data):
    try:
        save_file_open = open(file_path, 'w', encoding='utf-8')
        json.dump(file_dict_data, save_file_open)
        save_file_open.close()
        return True
    except:
        return False

def load_json_file(file_path):
    if not os.path.isfile(file_path):
        return
    save_file_open = open(file_path, encoding='utf-8')
    raw_json = save_file_open.read()
    json_data = json.loads(raw_json)
    return json_data

def remove_file(file_path):
    try:
        if not os.path.isfile(file_path):
            return False
        os.remove(file_path)
        return True
    except:
        return False
