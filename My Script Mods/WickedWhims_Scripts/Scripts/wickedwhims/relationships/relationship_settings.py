'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''from wickedwhims.main.settings.builder import SettingsWindow, SettingsSelectorOption, SettingsBranchOptionfrom wickedwhims.main.settings.main_settings import open_main_settings, register_main_settings_optionfrom wickedwhims.relationships._ts4_tuning.age_restrictions.interactions import remove_romance_age_restrictionsfrom wickedwhims.relationships._ts4_tuning.incest import unlock_incest_for_interactionsfrom wickedwhims.relationships._ts4_tuning.jealousy import disable_jealousy_broadcastersfrom wickedwhims.relationships._ts4_tuning.polygamy import unlock_polygamy_for_interactionsfrom wickedwhims.utils_interfaces import display_ok_dialogfrom wickedwhims.utils_saves.save_basics import get_basic_save_data, update_basic_save_dataRELATIONSHIP_SETTINGS_DICT = dict()
class RelationshipSetting:
    __qualname__ = 'RelationshipSetting'
    ROMANCE_AGE_RESTRICTION_STATE = 'romance_age_restrictions'
    POLYGAMY_STATE = 'polygamy_flag'
    JEALOUSY_STATE = 'jealousy_relations_impact'
    INCEST_STATE = 'incest_flag'

@register_main_settings_option()
def _register_relationship_settings():
    return _get_relationship_settings().get_window_picker_row()

def _open_relationship_settings():
    _get_relationship_settings().open_window()

def _get_relationship_settings():

    def _exit_setting_update():
        update_relationship_settings_to_basic_save_data()
        open_main_settings()

    relationship_settings_window = SettingsWindow(3, 3341159695, 1970181669, cancel_callback=_exit_setting_update)
    relationship_settings_window.add_settings_option(SettingsBranchOption(_romance_age_restrictions_settings, allow_open_callback=False))
    relationship_settings_window.add_settings_option(SettingsBranchOption(_polyamory_settings, allow_open_callback=False))
    relationship_settings_window.add_settings_option(SettingsBranchOption(_global_no_jealousy_cheat_settings, allow_open_callback=True))
    relationship_settings_window.add_settings_option(SettingsBranchOption(_global_incest_cheat_settings, allow_open_callback=True))
    return relationship_settings_window

def _setup_settings_variables():
    _setup_settings_variable(RelationshipSetting.ROMANCE_AGE_RESTRICTION_STATE, 0)
    _setup_settings_variable(RelationshipSetting.POLYGAMY_STATE, 0)
    _setup_settings_variable(RelationshipSetting.JEALOUSY_STATE, 1)
    _setup_settings_variable(RelationshipSetting.INCEST_STATE, 0)

def _romance_age_restrictions_settings():

    def _change_warning_message():
        display_ok_dialog(text=926615894, title=3579577312)

    settings_option_window = SettingsWindow(0, 3579577312, 689435193, change_callback=_change_warning_message, cancel_callback=_open_relationship_settings)
    settings_option_window.add_settings_option(SettingsSelectorOption(1972153895, 0, _romance_age_restrictions_settings, RELATIONSHIP_SETTINGS_DICT, RelationshipSetting.ROMANCE_AGE_RESTRICTION_STATE, 1, allow_change_callback=False))
    settings_option_window.add_settings_option(SettingsSelectorOption(1840687547, 0, _romance_age_restrictions_settings, RELATIONSHIP_SETTINGS_DICT, RelationshipSetting.ROMANCE_AGE_RESTRICTION_STATE, 0, allow_change_callback=RELATIONSHIP_SETTINGS_DICT[RelationshipSetting.ROMANCE_AGE_RESTRICTION_STATE] == 1))
    return settings_option_window

def _polyamory_settings():

    def _change_warning_message():
        display_ok_dialog(text=926615894, title=2064322478)

    settings_option_window = SettingsWindow(0, 2064322478, 606279529, change_callback=_change_warning_message, cancel_callback=_open_relationship_settings)
    settings_option_window.add_settings_option(SettingsSelectorOption(3487178965, 0, _polyamory_settings, RELATIONSHIP_SETTINGS_DICT, RelationshipSetting.POLYGAMY_STATE, 1, allow_change_callback=False))
    settings_option_window.add_settings_option(SettingsSelectorOption(4221398665, 0, _polyamory_settings, RELATIONSHIP_SETTINGS_DICT, RelationshipSetting.POLYGAMY_STATE, 0, allow_change_callback=RELATIONSHIP_SETTINGS_DICT[RelationshipSetting.POLYGAMY_STATE] == 1))
    return settings_option_window

def _global_no_jealousy_cheat_settings():

    def _open_warning_message():
        display_ok_dialog(text=584740058, title=3857402476)

    def _change_warning_message():
        display_ok_dialog(text=926615894, title=3857402476)

    settings_option_window = SettingsWindow(0, 3857402476, 4022532503, open_callback=_open_warning_message, change_callback=_change_warning_message, cancel_callback=_open_relationship_settings)
    settings_option_window.add_settings_option(SettingsSelectorOption(1836796321, 0, _global_no_jealousy_cheat_settings, RELATIONSHIP_SETTINGS_DICT, RelationshipSetting.JEALOUSY_STATE, 1, allow_change_callback=False))
    settings_option_window.add_settings_option(SettingsSelectorOption(1388686066, 0, _global_no_jealousy_cheat_settings, RELATIONSHIP_SETTINGS_DICT, RelationshipSetting.JEALOUSY_STATE, 0, allow_change_callback=RELATIONSHIP_SETTINGS_DICT[RelationshipSetting.JEALOUSY_STATE] == 1))
    return settings_option_window

def _global_incest_cheat_settings():

    def _open_warning_message():
        display_ok_dialog(text=1417105284, title=3799781904)

    def _change_warning_message():
        display_ok_dialog(text=926615894, title=3857402476)

    settings_option_window = SettingsWindow(0, 3799781904, 3384770454, open_callback=_open_warning_message, change_callback=_change_warning_message, cancel_callback=_open_relationship_settings)
    settings_option_window.add_settings_option(SettingsSelectorOption(1836994860, 0, _global_incest_cheat_settings, RELATIONSHIP_SETTINGS_DICT, RelationshipSetting.INCEST_STATE, 1, allow_change_callback=False))
    settings_option_window.add_settings_option(SettingsSelectorOption(3076268239, 0, _global_incest_cheat_settings, RELATIONSHIP_SETTINGS_DICT, RelationshipSetting.INCEST_STATE, 0, allow_change_callback=RELATIONSHIP_SETTINGS_DICT[RelationshipSetting.INCEST_STATE] == 1))
    return settings_option_window

def _setup_settings_variable(variable, default_state):
    if variable not in RELATIONSHIP_SETTINGS_DICT:
        RELATIONSHIP_SETTINGS_DICT[variable] = default_state

def apply_relationship_settings_from_basic_save_data():
    _setup_settings_variables()
    basic_save_data = get_basic_save_data()
    if 'relationships' in basic_save_data:
        relationship_save_data = basic_save_data['relationships']
        for (variable, state) in relationship_save_data.items():
            while variable in RELATIONSHIP_SETTINGS_DICT:
                try:
                    RELATIONSHIP_SETTINGS_DICT[variable] = int(state)
                except ValueError:
                    pass
    update_relationship_settings_to_basic_save_data()

def update_relationship_settings_to_basic_save_data():
    disable_jealousy_broadcasters(get_relationship_setting(RelationshipSetting.JEALOUSY_STATE, variable_type=bool))
    unlock_incest_for_interactions(not get_relationship_setting(RelationshipSetting.INCEST_STATE, variable_type=bool))
    remove_romance_age_restrictions(get_relationship_setting(RelationshipSetting.ROMANCE_AGE_RESTRICTION_STATE, variable_type=bool))
    unlock_polygamy_for_interactions(get_relationship_setting(RelationshipSetting.POLYGAMY_STATE, variable_type=bool))
    general_dict = dict()
    general_dict['relationships'] = RELATIONSHIP_SETTINGS_DICT
    update_basic_save_data(general_dict)

def get_relationship_setting(variable, variable_type=bool):
    return variable_type(RELATIONSHIP_SETTINGS_DICT[variable])
