'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from turbolib.native.enum import TurboEnum
from wickedwhims.main.settings.builder import SettingsBranchOption, SettingsWindow, SettingsSwitchOption, SettingsSelectorOption
from wickedwhims.main.settings.main_settings import open_main_settings, register_main_settings_option
from wickedwhims.utils_saves.save_basics import update_basic_save_data, get_basic_save_data
NUDITY_SETTINGS_DICT = dict()

class NuditySetting:
    __qualname__ = 'NuditySetting'
    NUDITY_SWITCH_STATE = 'exhibitionism_switch'
    UNDERWEAR_SWITCH_STATE = 'underwear_switch'
    COMPLETE_UNDRESSING_TYPE = 'complete_undressing_type'
    OUTFIT_AUTO_UNDRESS_GLOVES_STATE = 'special_outfit_auto_undress_gloves'
    OUTFIT_AUTO_UNDRESS_SHOES_STATE = 'special_outfit_auto_undress_shoes'
    OUTFIT_AUTO_UNDRESS_LEGGINGS_STATE = 'special_outfit_auto_undress_leggings'
    OUTFIT_AUTO_UNDRESS_SOCKS_STATE = 'special_outfit_auto_undress_socks'
    NOTIFICATIONS_VISBILITY_TYPE = 'notification_level'
    NOTIFICATIONS_HOUSEHOLD_LIMIT_STATE = 'notification_household_flag'
    AUTONOMY_TYPE = 'autonomy_level'
    INTERACTION_AUTONOMY_UNDRESSING_TYPE = 'interaction_autonomy_undressing_type'
    STORY_PROGRESSION_STATE = 'story_progression_flag'
    TEENS_NUDITY_STATE = 'teens_nudity_switch'
    NUDITY_ASSURANCE_STATE = 'nude_outfit_assurance'
    TOILET_USE_UNDRESS_STATE = 'toilet_undress_flag'
    BREAST_FEEDING_UNDRESS_STATE = 'breast_feed_undress_flag'
    NUDITY_PRIVACY = 'nudity_privacy'
    REACTION_TO_NUDITY_STATE = 'nudity_reactions'

@register_main_settings_option()
def _register_nudity_settings():
    return _get_nudity_settings().get_window_picker_row()

def _open_nudity_settings():
    _get_nudity_settings().open_window()

def _get_nudity_settings():

    def _exit_setting_update():
        update_nudity_settings_to_basic_save_data()
        open_main_settings()

    nudity_settings_window = SettingsWindow(1, 3482616025, 1935908617, cancel_callback=_exit_setting_update)
    nudity_settings_window.add_settings_option(SettingsSwitchOption(453629989, 3027443619, _get_nudity_settings, NUDITY_SETTINGS_DICT, NuditySetting.NUDITY_SWITCH_STATE))
    nudity_settings_window.add_settings_option(SettingsSwitchOption(1578351482, 2573526312, _get_nudity_settings, NUDITY_SETTINGS_DICT, NuditySetting.UNDERWEAR_SWITCH_STATE))
    nudity_settings_window.add_settings_option(SettingsBranchOption(_outfit_settings, allow_open_callback=False))
    nudity_settings_window.add_settings_option(SettingsBranchOption(_notification_settings, allow_open_callback=False))
    nudity_settings_window.add_settings_option(SettingsBranchOption(_autonomy_settings, allow_open_callback=False))
    nudity_settings_window.add_settings_option(SettingsBranchOption(_story_progression_settings, allow_open_callback=False))
    nudity_settings_window.add_settings_option(SettingsBranchOption(_other_settings, allow_open_callback=False))
    nudity_settings_window.add_settings_option(SettingsBranchOption(_cheats_settings, allow_open_callback=False))
    return nudity_settings_window

def _setup_settings_variables():
    _setup_settings_variable(NuditySetting.NUDITY_SWITCH_STATE, 1)
    _setup_settings_variable(NuditySetting.UNDERWEAR_SWITCH_STATE, 1)
    _setup_settings_variable(NuditySetting.COMPLETE_UNDRESSING_TYPE, 1)
    _setup_settings_variable(NuditySetting.OUTFIT_AUTO_UNDRESS_GLOVES_STATE, 1)
    _setup_settings_variable(NuditySetting.OUTFIT_AUTO_UNDRESS_SHOES_STATE, 1)
    _setup_settings_variable(NuditySetting.OUTFIT_AUTO_UNDRESS_LEGGINGS_STATE, 1)
    _setup_settings_variable(NuditySetting.OUTFIT_AUTO_UNDRESS_SOCKS_STATE, 1)
    _setup_settings_variable(NuditySetting.NOTIFICATIONS_VISBILITY_TYPE, 1)
    _setup_settings_variable(NuditySetting.NOTIFICATIONS_HOUSEHOLD_LIMIT_STATE, 0)
    _setup_settings_variable(NuditySetting.AUTONOMY_TYPE, 2)
    _setup_settings_variable(NuditySetting.INTERACTION_AUTONOMY_UNDRESSING_TYPE, 1)
    _setup_settings_variable(NuditySetting.STORY_PROGRESSION_STATE, 1)
    _setup_settings_variable(NuditySetting.TEENS_NUDITY_STATE, 1)
    _setup_settings_variable(NuditySetting.NUDITY_ASSURANCE_STATE, 1)
    _setup_settings_variable(NuditySetting.TOILET_USE_UNDRESS_STATE, 1)
    _setup_settings_variable(NuditySetting.BREAST_FEEDING_UNDRESS_STATE, 1)
    _setup_settings_variable(NuditySetting.NUDITY_PRIVACY, 1)
    _setup_settings_variable(NuditySetting.REACTION_TO_NUDITY_STATE, 1)

class CompleteUndressingTypeSetting(TurboEnum):
    __qualname__ = 'CompleteUndressingTypeSetting'
    DEFAULT = 0
    SPECIAL = 1

def _outfit_settings():

    def _open_outfit_settings():
        _outfit_settings().open_window()

    settings_option_window = SettingsWindow(0, 1926714507, 3432297298, cancel_callback=_open_nudity_settings)

    def _complete_undressing_type():
        complete_undressing_type_window = SettingsWindow(1, 692689912, 3042534075, cancel_callback=_open_outfit_settings)
        complete_undressing_type_window.add_settings_option(SettingsSelectorOption(1221347836, 1256816785, _complete_undressing_type, NUDITY_SETTINGS_DICT, NuditySetting.COMPLETE_UNDRESSING_TYPE, CompleteUndressingTypeSetting.DEFAULT, allow_change_callback=False))
        complete_undressing_type_window.add_settings_option(SettingsSelectorOption(2744873298, 1134862513, _complete_undressing_type, NUDITY_SETTINGS_DICT, NuditySetting.COMPLETE_UNDRESSING_TYPE, CompleteUndressingTypeSetting.SPECIAL, allow_change_callback=False))
        return complete_undressing_type_window

    settings_option_window.add_settings_option(SettingsBranchOption(_complete_undressing_type, allow_open_callback=False))
    settings_option_window.add_settings_option(SettingsSwitchOption(2858014063, 119403953, _outfit_settings, NUDITY_SETTINGS_DICT, NuditySetting.OUTFIT_AUTO_UNDRESS_GLOVES_STATE))
    settings_option_window.add_settings_option(SettingsSwitchOption(950164393, 2917956641, _outfit_settings, NUDITY_SETTINGS_DICT, NuditySetting.OUTFIT_AUTO_UNDRESS_SHOES_STATE))
    settings_option_window.add_settings_option(SettingsSwitchOption(2384648499, 2997894284, _outfit_settings, NUDITY_SETTINGS_DICT, NuditySetting.OUTFIT_AUTO_UNDRESS_SOCKS_STATE))
    settings_option_window.add_settings_option(SettingsSwitchOption(3473641235, 2662606901, _outfit_settings, NUDITY_SETTINGS_DICT, NuditySetting.OUTFIT_AUTO_UNDRESS_LEGGINGS_STATE))
    return settings_option_window

class NudityNotificationsTypeSetting(TurboEnum):
    __qualname__ = 'NudityNotificationsTypeSetting'
    DISABLED = 0
    AUTONOMY = 1
    ALL = 2

def _notification_settings():

    def _open_notification_settings():
        _notification_settings().open_window()

    settings_option_window = SettingsWindow(0, 3279709928, 2777387879, cancel_callback=_open_nudity_settings)

    def _notifications_visibility_type():
        notifications_visibility_type_window = SettingsWindow(1, 1049993247, 3978784152, cancel_callback=_open_notification_settings)
        notifications_visibility_type_window.add_settings_option(SettingsSelectorOption(674810031, 3883147319, _notifications_visibility_type, NUDITY_SETTINGS_DICT, NuditySetting.NOTIFICATIONS_VISBILITY_TYPE, NudityNotificationsTypeSetting.DISABLED, allow_change_callback=False))
        notifications_visibility_type_window.add_settings_option(SettingsSelectorOption(3818596707, 4274135008, _notifications_visibility_type, NUDITY_SETTINGS_DICT, NuditySetting.NOTIFICATIONS_VISBILITY_TYPE, NudityNotificationsTypeSetting.AUTONOMY, allow_change_callback=False))
        notifications_visibility_type_window.add_settings_option(SettingsSelectorOption(1487120885, 1289690659, _notifications_visibility_type, NUDITY_SETTINGS_DICT, NuditySetting.NOTIFICATIONS_VISBILITY_TYPE, NudityNotificationsTypeSetting.ALL, allow_change_callback=False))
        return notifications_visibility_type_window

    settings_option_window.add_settings_option(SettingsBranchOption(_notifications_visibility_type, allow_open_callback=False))
    settings_option_window.add_settings_option(SettingsSwitchOption(2284366757, 2211369900, _notification_settings, NUDITY_SETTINGS_DICT, NuditySetting.NOTIFICATIONS_HOUSEHOLD_LIMIT_STATE))
    return settings_option_window

class NudityAutonomyTypeSetting(TurboEnum):
    __qualname__ = 'NudityAutonomyTypeSetting'
    DISABLED = 0
    NPC_ONLY = 1
    FULL = 2

class NudityAutonomyUndressLevelSetting(TurboEnum):
    __qualname__ = 'NudityAutonomyUndressLevelSetting'
    DISABLED = 0
    RANDOM = 1
    ALWAYS = 2

def _autonomy_settings():

    def _open_autonomy_settings():
        _autonomy_settings().open_window()

    settings_option_window = SettingsWindow(0, 2952085198, 4065078282, cancel_callback=_open_nudity_settings)

    def _autonomy_type():
        autonomy_level_window = SettingsWindow(1, 273010132, 3506801424, cancel_callback=_open_autonomy_settings)
        autonomy_level_window.add_settings_option(SettingsSelectorOption(10295473, 3946683557, _autonomy_type, NUDITY_SETTINGS_DICT, NuditySetting.AUTONOMY_TYPE, NudityAutonomyTypeSetting.DISABLED, allow_change_callback=False))
        autonomy_level_window.add_settings_option(SettingsSelectorOption(933284298, 324302165, _autonomy_type, NUDITY_SETTINGS_DICT, NuditySetting.AUTONOMY_TYPE, NudityAutonomyTypeSetting.NPC_ONLY, allow_change_callback=False))
        autonomy_level_window.add_settings_option(SettingsSelectorOption(3903945432, 4227951371, _autonomy_type, NUDITY_SETTINGS_DICT, NuditySetting.AUTONOMY_TYPE, NudityAutonomyTypeSetting.FULL, allow_change_callback=False))
        return autonomy_level_window

    settings_option_window.add_settings_option(SettingsBranchOption(_autonomy_type, allow_open_callback=False))

    def _interaction_undressing_autonomy_type():
        undressing_autonomy_level_window = SettingsWindow(1, 2601174900, 1342392999, cancel_callback=_open_autonomy_settings)
        undressing_autonomy_level_window.add_settings_option(SettingsSelectorOption(469378371, 1366608659, _interaction_undressing_autonomy_type, NUDITY_SETTINGS_DICT, NuditySetting.INTERACTION_AUTONOMY_UNDRESSING_TYPE, NudityAutonomyUndressLevelSetting.DISABLED, allow_change_callback=False))
        undressing_autonomy_level_window.add_settings_option(SettingsSelectorOption(2783019522, 3623010176, _interaction_undressing_autonomy_type, NUDITY_SETTINGS_DICT, NuditySetting.INTERACTION_AUTONOMY_UNDRESSING_TYPE, NudityAutonomyUndressLevelSetting.RANDOM, allow_change_callback=False))
        undressing_autonomy_level_window.add_settings_option(SettingsSelectorOption(1795801803, 2851490907, _interaction_undressing_autonomy_type, NUDITY_SETTINGS_DICT, NuditySetting.INTERACTION_AUTONOMY_UNDRESSING_TYPE, NudityAutonomyUndressLevelSetting.ALWAYS, allow_change_callback=False))
        return undressing_autonomy_level_window

    settings_option_window.add_settings_option(SettingsBranchOption(_interaction_undressing_autonomy_type, allow_open_callback=False))
    return settings_option_window

def _story_progression_settings():
    settings_option_window = SettingsWindow(0, 1581732742, 1949040668, cancel_callback=_open_nudity_settings)
    settings_option_window.add_settings_option(SettingsSwitchOption(2988386393, 787091191, _story_progression_settings, NUDITY_SETTINGS_DICT, NuditySetting.STORY_PROGRESSION_STATE))
    return settings_option_window

def _other_settings():
    settings_option_window = SettingsWindow(0, 3347767978, 3482441299, cancel_callback=_open_nudity_settings)
    settings_option_window.add_settings_option(SettingsSwitchOption(4036248285, 1543833768, _other_settings, NUDITY_SETTINGS_DICT, NuditySetting.TEENS_NUDITY_STATE))
    settings_option_window.add_settings_option(SettingsSwitchOption(1224818283, 3312839120, _other_settings, NUDITY_SETTINGS_DICT, NuditySetting.NUDITY_ASSURANCE_STATE))
    settings_option_window.add_settings_option(SettingsSwitchOption(1521332630, 2094981913, _other_settings, NUDITY_SETTINGS_DICT, NuditySetting.TOILET_USE_UNDRESS_STATE))
    settings_option_window.add_settings_option(SettingsSwitchOption(3872449146, 2574151234, _other_settings, NUDITY_SETTINGS_DICT, NuditySetting.BREAST_FEEDING_UNDRESS_STATE))
    return settings_option_window

def _cheats_settings():
    settings_option_window = SettingsWindow(0, 3316653451, 1790619680, cancel_callback=_open_nudity_settings)
    settings_option_window.add_settings_option(SettingsSwitchOption(2493503338, 2379427991, _cheats_settings, NUDITY_SETTINGS_DICT, NuditySetting.NUDITY_PRIVACY))
    settings_option_window.add_settings_option(SettingsSwitchOption(3276318383, 3542627219, _cheats_settings, NUDITY_SETTINGS_DICT, NuditySetting.REACTION_TO_NUDITY_STATE))
    return settings_option_window

def _setup_settings_variable(variable, default_state):
    if variable not in NUDITY_SETTINGS_DICT:
        NUDITY_SETTINGS_DICT[variable] = default_state

def apply_nudity_settings_from_basic_save_data():
    _setup_settings_variables()
    basic_save_data = get_basic_save_data()
    if 'exhibitionism' in basic_save_data:
        nudity_save_data = basic_save_data['exhibitionism']
        for (variable, state) in nudity_save_data.items():
            while variable in NUDITY_SETTINGS_DICT:
                try:
                    NUDITY_SETTINGS_DICT[variable] = int(state)
                except ValueError:
                    pass
    update_nudity_settings_to_basic_save_data()

def update_nudity_settings_to_basic_save_data():
    general_dict = dict()
    general_dict['exhibitionism'] = NUDITY_SETTINGS_DICT
    update_basic_save_data(general_dict)

def get_nudity_setting(variable, variable_type=bool):
    return variable_type(NUDITY_SETTINGS_DICT[variable])

