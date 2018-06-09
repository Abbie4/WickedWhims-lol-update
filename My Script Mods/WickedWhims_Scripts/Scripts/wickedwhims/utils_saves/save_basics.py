from wickedwhims.utils_saves.save_main import get_save_dir, set_has_save_loading_error, get_save_id, load_json_file, save_json_file
BASIC_SAVE_DATA = dict()

def get_basic_save_data():
    return BASIC_SAVE_DATA


def load_basic_save_data(slot_id=-1, load_file_path_override=None):
    global BASIC_SAVE_DATA
    if load_file_path_override is None:
        load_file_path = ''.join((get_save_dir(), get_save_id('general', slot_id=slot_id), '.json'))
    else:
        load_file_path = load_file_path_override
    try:
        BASIC_SAVE_DATA = load_json_file(load_file_path) or dict()
    except:
        set_has_save_loading_error()
        BASIC_SAVE_DATA = dict()


def save_basic_save_data(save_file_path_override=None):
    if save_file_path_override is None:
        save_file_path = ''.join((get_save_dir(), get_save_id('general'), '.json'))
    else:
        save_file_path = save_file_path_override
    save_json_file(save_file_path, BASIC_SAVE_DATA)


def update_basic_save_data(general_data):
    global BASIC_SAVE_DATA
    general_save_data_copy = BASIC_SAVE_DATA.copy()
    general_save_data_copy.update(general_data)
    BASIC_SAVE_DATA = general_save_data_copy

