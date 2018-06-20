'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from wickedwhims.utils_saves.save_main import get_save_dir, set_has_save_loading_error, get_save_id, load_json_file, save_json_file
DISABLED_LOCATIONS_SAVE_DATA = dict()

def get_disabled_locations_save_data():
    return DISABLED_LOCATIONS_SAVE_DATA


def load_disabled_locations_save_data(slot_id=-1):
    global DISABLED_LOCATIONS_SAVE_DATA
    save_id = get_save_id('disabled_locations', slot_id=slot_id)
    load_file_path = get_save_dir() + save_id + '.json'
    try:
        DISABLED_LOCATIONS_SAVE_DATA = load_json_file(load_file_path) or dict()
    except:
        set_has_save_loading_error()
        DISABLED_LOCATIONS_SAVE_DATA = dict()


def save_disabled_locations_save_data():
    save_id = get_save_id('disabled_locations')
    save_file_path = get_save_dir() + save_id + '.json'
    save_json_file(save_file_path, DISABLED_LOCATIONS_SAVE_DATA)


def update_disabled_locations_save_data(disabled_locations_data):
    global DISABLED_LOCATIONS_SAVE_DATA
    disabled_locations_save_data_copy = DISABLED_LOCATIONS_SAVE_DATA.copy()
    disabled_locations_save_data_copy.update(disabled_locations_data)
    DISABLED_LOCATIONS_SAVE_DATA = disabled_locations_save_data_copy

