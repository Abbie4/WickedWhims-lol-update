'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''from wickedwhims.utils_saves.save_main import get_save_dir, set_has_save_loading_error, get_save_id, load_json_file, save_json_fileDISABLED_ANIMATIONS_SAVE_DATA = dict()
def get_disabled_animations_save_data():
    return DISABLED_ANIMATIONS_SAVE_DATA

def load_disabled_animations_save_data(slot_id=-1, load_file_path_override=None):
    global DISABLED_ANIMATIONS_SAVE_DATA
    if load_file_path_override is None:
        load_file_path = ''.join((get_save_dir(), get_save_id('disabled_animations', slot_id=slot_id), '.json'))
    else:
        load_file_path = load_file_path_override
    try:
        DISABLED_ANIMATIONS_SAVE_DATA = load_json_file(load_file_path) or dict()
    except:
        set_has_save_loading_error()
        DISABLED_ANIMATIONS_SAVE_DATA = dict()

def save_disabled_animations_save_data(save_file_path_override=None):
    if save_file_path_override is None:
        save_file_path = ''.join((get_save_dir(), get_save_id('disabled_animations'), '.json'))
    else:
        save_file_path = save_file_path_override
    save_json_file(save_file_path, DISABLED_ANIMATIONS_SAVE_DATA)

def update_disabled_animations_save_data(disabled_animations_data):
    global DISABLED_ANIMATIONS_SAVE_DATA
    disabled_animations_save_data_copy = DISABLED_ANIMATIONS_SAVE_DATA.copy()
    disabled_animations_save_data_copy.update(disabled_animations_data)
    DISABLED_ANIMATIONS_SAVE_DATA = disabled_animations_save_data_copy
