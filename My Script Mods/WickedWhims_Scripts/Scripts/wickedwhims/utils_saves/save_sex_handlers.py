from wickedwhims.utils_saves.save_main import get_save_dir, set_has_save_loading_error, get_save_id, load_json_file, save_json_file
SEX_HANDLERS_SAVE_DATA = dict()

def get_sex_handlers_save_data():
    return SEX_HANDLERS_SAVE_DATA


def load_sex_handlers_save_data(slot_id=-1):
    global SEX_HANDLERS_SAVE_DATA
    save_id = get_save_id('sex_handlers', slot_id=slot_id)
    load_file_path = get_save_dir() + save_id + '.json'
    try:
        SEX_HANDLERS_SAVE_DATA = load_json_file(load_file_path) or dict()
    except:
        set_has_save_loading_error()
        SEX_HANDLERS_SAVE_DATA = dict()


def save_sex_handlers_save_data():
    save_id = get_save_id('sex_handlers')
    save_file_path = get_save_dir() + save_id + '.json'
    save_json_file(save_file_path, SEX_HANDLERS_SAVE_DATA)


def update_sex_handlers_save_data(sex_handlers_data):
    global SEX_HANDLERS_SAVE_DATA
    SEX_HANDLERS_SAVE_DATA = sex_handlers_data.copy()

