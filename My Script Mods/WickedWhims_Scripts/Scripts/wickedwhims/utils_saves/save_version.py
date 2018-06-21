from turbolib.events.core import register_zone_load_event_method
from wickedwhims.main.update_handler import set_mod_update_status
from wickedwhims.utils_saves.save_main import get_save_dir, set_has_save_loading_error, get_save_id, load_json_file, save_json_file
from wickedwhims.version_registry import get_mod_version_int
VERSION_SAVE_DATA = dict()

def get_version_save_data():
    return VERSION_SAVE_DATA


def load_version_save_data():
    global VERSION_SAVE_DATA
    save_id = get_save_id('version')
    load_file_path = get_save_dir() + save_id + '.json'
    try:
        VERSION_SAVE_DATA = load_json_file(load_file_path) or dict()
    except:
        set_has_save_loading_error()
        VERSION_SAVE_DATA = dict()


def save_version_save_data():
    save_id = get_save_id('version')
    save_file_path = get_save_dir() + save_id + '.json'
    save_json_file(save_file_path, VERSION_SAVE_DATA)


def update_version_save_data(version_data):
    global VERSION_SAVE_DATA
    version_save_data_copy = VERSION_SAVE_DATA.copy()
    version_save_data_copy.update(version_data)
    VERSION_SAVE_DATA = version_save_data_copy


@register_zone_load_event_method(unique_id='WickedWhims', priority=1, early=True)
def _wickedwhims_test_mod_version():
    load_version_save_data()
    save_version_dict = get_version_save_data()
    if save_version_dict is not None and (len(save_version_dict) > 0 and 'version' in save_version_dict) and get_mod_version_int() == save_version_dict['version']:
        return
    update_version_save_data({'ignore_update': False})
    set_mod_update_status(True)

