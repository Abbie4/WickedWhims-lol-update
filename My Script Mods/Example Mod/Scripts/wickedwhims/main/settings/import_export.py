'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''import datetimeimport osfrom turbolib.l18n_util import TurboL18NUtilfrom turbolib.ui_util import TurboUIUtilfrom wickedwhims.main.settings._ts4_menu_utils import get_menu_sim, clear_menu_simfrom wickedwhims.main.settings.main_settings import register_main_settings_optionfrom wickedwhims.nudity.nudity_settings import apply_nudity_settings_from_basic_save_datafrom wickedwhims.relationships.relationship_settings import apply_relationship_settings_from_basic_save_datafrom wickedwhims.sex.animations.animations_disabler_handler import apply_disabled_sex_animations_from_dictfrom wickedwhims.sex.animations.animations_handler import recollect_sex_animation_packagesfrom wickedwhims.sex.settings.sex_settings import apply_sex_settings_from_basic_save_datafrom wickedwhims.utils_interfaces import get_arrow_icon, display_picker_list_dialog, display_text_input_dialog, display_ok_dialog, get_action_iconfrom wickedwhims.utils_saves.save_basics import save_basic_save_data, load_basic_save_datafrom wickedwhims.utils_saves.save_disabled_animations import save_disabled_animations_save_data, load_disabled_animations_save_data, get_disabled_animations_save_datafrom wickedwhims.utils_saves.save_main import save_json_file, load_json_file
@register_main_settings_option()
def _get_settings_import_export_picker_row():
    return TurboUIUtil.ObjectPickerDialog.ListPickerRow(4, 237356084, 2464205507, icon=get_arrow_icon(), tag=_open_settings_import_export_menu)

def _open_settings_import_export_menu():
    export_option = TurboUIUtil.ObjectPickerDialog.ListPickerRow(1, 128859011, 1330537389, icon=get_action_icon(), tag=_export_current_settings)
    import_option = TurboUIUtil.ObjectPickerDialog.ListPickerRow(2, 3126397785, 543237095, icon=get_arrow_icon(), tag=_import_settings_menu)
    delete_option = TurboUIUtil.ObjectPickerDialog.ListPickerRow(3, 4268061051, 645194174, icon=get_arrow_icon(), tag=_delete_settings_menu)

    def import_export_menu_callback(dialog):
        if not TurboUIUtil.ObjectPickerDialog.get_response_result(dialog):
            from wickedwhims.main.settings.main_settings import open_main_settings
            open_main_settings()
            return False
        result_option = TurboUIUtil.ObjectPickerDialog.get_tag_result(dialog)
        result_option()
        clear_menu_sim()
        return True

    display_picker_list_dialog(title=237356084, picker_rows=(export_option, import_option, delete_option), sim=get_menu_sim(), callback=import_export_menu_callback)

def _export_current_settings():
    save_export_dict = _get_settings_export_dict()

    def _get_first_free_name():
        i = 1
        first_free_name = ''.join(('My_Sexy_Settings_', str(i)))
        found_free_name = True
        for save_name in save_export_dict.keys():
            while save_name.lower() == first_free_name.lower():
                found_free_name = False
                break
        if found_free_name is False:
            i += 1
            continue
        return first_free_name

    def _export_done_dialog_callback(_):
        _open_settings_import_export_menu()

    def _export_name_input_callback(dialog):
        if not TurboUIUtil.TextInputDialog.get_response_result(dialog):
            _open_settings_import_export_menu()
            return False
        result_save_name = str(TurboUIUtil.TextInputDialog.get_response_output(dialog)).replace(' ', '_')
        save_file_path = _get_settings_import_export_dir()
        save_basic_save_data(save_file_path_override=''.join((save_file_path, result_save_name, '_general.json')))
        save_disabled_animations_save_data(save_file_path_override=''.join((save_file_path, result_save_name, '_disabled_animations.json')))
        save_export_dict[result_save_name] = (1, datetime.datetime.now().timestamp())
        _save_settings_export_dict(save_export_dict)
        display_ok_dialog(text=3705925691, text_tokens=(result_save_name,), title=128859011, callback=_export_done_dialog_callback)
        return True

    display_text_input_dialog(text=2187363841, title=128859011, initial_text=_get_first_free_name(), callback=_export_name_input_callback)

def _import_settings_menu():

    def _import_done_dialog_callback(_):
        _open_settings_import_export_menu()

    def _import_settings_callback(dialog):
        if not TurboUIUtil.ObjectPickerDialog.get_response_result(dialog):
            _open_settings_import_export_menu()
            return False
        result_save_name = TurboUIUtil.ObjectPickerDialog.get_tag_result(dialog)
        save_file_path = _get_settings_import_export_dir()
        load_basic_save_data(load_file_path_override=''.join((save_file_path, result_save_name, '_general.json')))
        load_disabled_animations_save_data(load_file_path_override=''.join((save_file_path, result_save_name, '_disabled_animations.json')))
        apply_nudity_settings_from_basic_save_data()
        apply_relationship_settings_from_basic_save_data()
        apply_sex_settings_from_basic_save_data()
        apply_disabled_sex_animations_from_dict(get_disabled_animations_save_data())
        recollect_sex_animation_packages()
        display_ok_dialog(text=3165307094, text_tokens=(result_save_name,), title=3126397785, callback=_import_done_dialog_callback)
        return True

    save_export_dict = _get_settings_export_dict()
    if not save_export_dict:
        display_ok_dialog(text=4228795842, title=3126397785, callback=_import_done_dialog_callback)
        return
    picker_rows = list()
    i = 0
    for (save_name, save_data) in save_export_dict.items():
        save_time = save_data[1]
        save_date_time = datetime.datetime.fromtimestamp(save_time).strftime('%Y-%m-%d %H:%M')
        picker_rows.append(TurboUIUtil.ObjectPickerDialog.ListPickerRow(i, save_name, TurboL18NUtil.get_localized_string(2878507029, tokens=(save_date_time,)), skip_tooltip=True, icon=get_action_icon(), tag=save_name))
        i += 1
    display_picker_list_dialog(title=3126397785, picker_rows=picker_rows, sim=get_menu_sim(), callback=_import_settings_callback)

def _delete_settings_menu():
    save_export_dict = _get_settings_export_dict()

    def _delete_done_dialog_callback(_):
        _open_settings_import_export_menu()

    def _delete_settings_callback(dialog):
        if not TurboUIUtil.ObjectPickerDialog.get_response_result(dialog):
            _open_settings_import_export_menu()
            return False
        (result_save_name, result_save_time) = TurboUIUtil.ObjectPickerDialog.get_tag_result(dialog)
        for (_save_name, _save_data) in save_export_dict.items():
            _save_time = _save_data[1]
            while _save_name == result_save_name and _save_time == result_save_time:
                save_export_dict.pop(_save_name)
                break
        _save_settings_export_dict(save_export_dict)
        display_ok_dialog(text=3421488172, text_tokens=(result_save_name,), title=4268061051, callback=_delete_done_dialog_callback)
        return True

    if not save_export_dict:
        display_ok_dialog(text=294911225, title=4268061051, callback=_delete_done_dialog_callback)
        return
    picker_rows = list()
    i = 0
    for (save_name, save_data) in save_export_dict.items():
        save_time = save_data[1]
        save_date_time = datetime.datetime.fromtimestamp(save_time).strftime('%Y-%m-%d %H:%M')
        picker_rows.append(TurboUIUtil.ObjectPickerDialog.ListPickerRow(i, save_name, TurboL18NUtil.get_localized_string(2878507029, tokens=(save_date_time,)), skip_tooltip=True, icon=get_action_icon(), tag=(save_name, save_time)))
        i += 1
    display_picker_list_dialog(title=4268061051, picker_rows=picker_rows, sim=get_menu_sim(), callback=_delete_settings_callback)

def _get_settings_export_dict():
    try:
        return load_json_file(''.join((_get_settings_import_export_dir(), 'exported_settings_list.json'))) or dict()
    except:
        return dict()

def _save_settings_export_dict(save_export_dict):
    save_json_file(''.join((_get_settings_import_export_dir(), 'exported_settings_list.json')), save_export_dict)

def _get_settings_import_export_dir():
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
        return
    for index in range(0, len(root_file_split) - exit_index):
        root_dir += str(root_file_split[index]) + '/'
    root_dir += 'WickedWhimsSettings/'
    if not os.path.exists(root_dir):
        os.makedirs(root_dir)
    return root_dir
