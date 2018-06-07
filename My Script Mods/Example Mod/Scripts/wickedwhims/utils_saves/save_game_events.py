'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''from wickedwhims.utils_saves.save_main import get_save_dir, set_has_save_loading_error, get_save_id, load_json_file, save_json_fileGAME_EVENTS_DATA = dict()
def get_game_events_save_data():
    return GAME_EVENTS_DATA

def load_game_events_save_data(slot_id=-1):
    global GAME_EVENTS_DATA
    save_id = get_save_id('game_events', slot_id=slot_id)
    load_file_path = get_save_dir() + save_id + '.json'
    try:
        GAME_EVENTS_DATA = load_json_file(load_file_path) or dict()
    except:
        set_has_save_loading_error()
        GAME_EVENTS_DATA = dict()

def save_game_events_save_data():
    save_id = get_save_id('game_events')
    save_file_path = get_save_dir() + save_id + '.json'
    save_json_file(save_file_path, GAME_EVENTS_DATA)

def update_game_events_save_data(game_events_data):
    global GAME_EVENTS_DATA
    game_events_save_data_copy = GAME_EVENTS_DATA.copy()
    game_events_save_data_copy.update(game_events_data)
    GAME_EVENTS_DATA = game_events_save_data_copy
