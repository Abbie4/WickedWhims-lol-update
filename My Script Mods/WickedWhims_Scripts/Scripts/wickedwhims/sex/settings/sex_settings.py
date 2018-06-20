from turbolib.l18n_util import TurboL18NUtil
from turbolib.native.enum import TurboEnum
from wickedwhims.main.basemental_handler import is_basemental_drugs_installed
from wickedwhims.main.settings.builder import SettingsBranchOption, SettingsWindow, SettingsSwitchOption, SettingsSelectorOption, SettingsInputOption, SettingsCallbackOption
from wickedwhims.main.settings.main_settings import register_main_settings_option, open_main_settings
from wickedwhims.sex._ts4_tuning.vanilla_interactions import set_vanilla_interactions_access_in_sex
from wickedwhims.sex._ts4_tuning.woohoo_interactions import disable_woohoo_interactions
from wickedwhims.sex.pregnancy._ts4_pregnancy_utils import set_pregnancy_duration
from wickedwhims.sex.sex_operators.active_sex_handlers_operator import get_active_sex_handlers
from wickedwhims.utils_interfaces import display_ok_dialog
from wickedwhims.utils_saves.save_basics import get_basic_save_data, update_basic_save_data
SEX_SETTINGS_DICT = dict()

class SexSetting:
    __qualname__ = 'SexSetting'
    AUTONOMY_NOTIFICATIONS_STATE = 'sex_autonomy_notification'
    PREGNENCY_NOTIFICATIONS_STATE = 'sex_pregnancy_notification'
    AUTONOMY_LEVEL = 'sex_autonomy_level'
    AUTONOMY_RELATIONSHIP_AWARENESS = 'sex_autonomy_relationship_awareness'
    AUTONOMY_RANDOM_SEX_STATE = 'sex_autonomy_random_switch'
    AUTONOMY_RANDOM_SOLO_SEX_STATE = 'sex_autonomy_random_solo_switch'
    AUTONOMY_ROMANCE_SEX_STATE = 'sex_autonomy_romance_switch'
    AUTONOMY_WATCH_SEX_STATE = 'sex_autonomy_watch_switch'
    JOIN_SEX_AUTONOMY_STATE = 'join_sex_autonomy_switch'
    AUTONOMY_NPC_PREGNANCY_AWARENESS = 'npc_autonomy_sex_pregnancy_awareness'
    PLAYER_AUTONOMY_STATE = 'player_sex_autonomy_switch'
    PLAYER_JOIN_SEX_AUTONOMY_STATE = 'player_join_sex_autonomy_switch'
    AUTONOMY_PLAYER_ASK_PLAYER_DIALOG_STATE = 'player_ask_player_sex_dialog'
    AUTONOMY_NPC_ASK_PLAYER_DIALOG_STATE = 'npc_ask_player_sex_dialog'
    AUTONOMY_PLAYER_ASK_NPC_DIALOG_STATE = 'player_ask_npc_sex_dialog'
    NPC_SEX_DURATION_VALUE = 'npc_sex_interaction_length'
    SEX_PROGRESSION_TYPE = 'progression_level'
    SEX_DURATION_TYPE = 'sex_interaction_length_type'
    SEX_DURATION_VALUE = 'sex_interaction_length'
    CLIMAX_SEX_PROGRESSION_STATE = 'sex_progression_after_climax'
    SEX_UNDRESSING_TYPE = 'undressing_level'
    NPC_SEX_UNDRESSING_TYPE = 'npc_undressing_level'
    OUTFIT_AUTO_DRESS_UP_AFTER_SEX_STATE = 'special_outfit_auto_dress_up_after_sex'
    STRAPON_AUTO_REMOVE_STATE = 'strapon_auto_remove'
    SEX_GENDER_TYPE = 'gender_flag'
    GENDER_RECOGNITION_FEMALE_TO_BOTH_STATE = 'gender_recognition_female_to_both'
    GENDER_RECOGNITION_MALE_TO_BOTH_STATE = 'gender_recognition_male_to_both'
    GENDER_RECOGNITION_SIM_SPECIFIC_STATE = 'gender_recognition_sim_specific'
    PREGNANCY_MODE = 'pregnancy_mode'
    PREGNANCY_DURATION = 'pregnancy_duration'
    BIRTH_CONTROL_MODE = 'birth_control_mode'
    NPC_BIRTH_CONTROL_MODE = 'npc_birth_control_mode'
    BIRTH_CONTROL_AUTO_USE = 'birth_control_auto_use'
    MENSTRUAL_CYCLE_DURATION = 'menstrual_cycle_duration'
    MENSTRUAL_CYCLE_NPC_PREGNANCY = 'menstrual_cycle_npc_pregnancy'
    SIMPLE_PREGNANCY_CHANCE = 'pregnancy_chance'
    SIMPLE_NPC_PREGNANCY_CHANCE = 'npc_pregnancy_chance'
    MISCARRIAGE_SWITCH = 'miscarriage_switch'
    TEENS_SEX_STATE = 'teens_sex_state'
    SEX_INITIATION_TYPE = 'sex_initiation'
    SEX_RELATIONS_IMPACT_STATE = 'sex_relations_impact'
    SEX_ANIMATION_DURATION_OVERRIDE_TYPE = 'sex_animation_length_override'
    SEX_ANIMATION_DURATION_OVERRIDE_VALUE = 'sex_animation_length_override_amount'
    CUM_VISIBILITY_STATE = 'cum_layers_visibility'
    CUM_VISIBILITY_WITH_CONDOM_STATE = 'cum_visibility_with_condom'
    SILENCE_PHONE_STATE = 'silence_phone'
    VANILLA_INTERACTIONS_SWITCH = 'vanilla_interactions_switch'
    DEFAULT_WOOHOO_SWITCH = 'default_woohoo_switch'
    ALWAYS_ACCEPT_STATE = 'always_accept'
    INSTANT_UNDRESSING_STATE = 'instant_undressing_outside_sex'
    MANUAL_NPC_SEX_STATE = 'manual_npc_sex'
    NEEDS_DECAY_STATE = 'needs_decay_in_sex'
    PRIVACY_STATE = 'sex_privacy'
    REACTION_TO_SEX_STATE = 'reactions_to_sex'
    REACTION_TO_CUM_STATE = 'reactions_to_cum'
    REACTION_TO_TEEN_PREGNANCY_STATE = 'reactions_to_teen_pregnancy'


@register_main_settings_option()
def _register_sex_settings():
    return _get_sex_settings().get_window_picker_row()


def _open_sex_settings():
    _get_sex_settings(show_warning=False).open_window()


def _get_sex_settings(show_warning=True):

    def _open_warning_message():
        if get_active_sex_handlers():
            display_ok_dialog(text=351743462, title=971624425)

    def _exit_setting_update():
        update_sex_settings_to_basic_save_data()
        open_main_settings()

    sex_settings_window = SettingsWindow(2, 971624425, 165875418, open_callback=_open_warning_message if show_warning is True else None, cancel_callback=_exit_setting_update)
    sex_settings_window.add_settings_option(SettingsBranchOption(_notification_settings, allow_open_callback=False))
    sex_settings_window.add_settings_option(SettingsBranchOption(_autonomy_settings, allow_open_callback=False))
    sex_settings_window.add_settings_option(SettingsBranchOption(_interaction_settings, allow_open_callback=False))
    sex_settings_window.add_settings_option(SettingsBranchOption(_outfit_settings, allow_open_callback=False))
    sex_settings_window.add_settings_option(SettingsBranchOption(_gender_settings, allow_open_callback=False))
    sex_settings_window.add_settings_option(SettingsBranchOption(_pregnancy_settings, allow_open_callback=False))
    sex_settings_window.add_settings_option(SettingsBranchOption(_other_settings, allow_open_callback=False))
    sex_settings_window.add_settings_option(SettingsBranchOption(_cheats_settings, allow_open_callback=False))
    from wickedwhims.sex.settings.animation_disabler_settings import open_player_animations_disabler
    sex_settings_window.add_settings_option(SettingsCallbackOption(1853900111, 115716611, open_player_animations_disabler))
    return sex_settings_window


def _setup_settings_variables():
    _setup_settings_variable(SexSetting.AUTONOMY_NOTIFICATIONS_STATE, 1)
    _setup_settings_variable(SexSetting.PREGNENCY_NOTIFICATIONS_STATE, 1)
    _setup_settings_variable(SexSetting.AUTONOMY_LEVEL, 2)
    _setup_settings_variable(SexSetting.AUTONOMY_RELATIONSHIP_AWARENESS, 1)
    _setup_settings_variable(SexSetting.AUTONOMY_RANDOM_SEX_STATE, 1)
    _setup_settings_variable(SexSetting.AUTONOMY_RANDOM_SOLO_SEX_STATE, 1)
    _setup_settings_variable(SexSetting.AUTONOMY_ROMANCE_SEX_STATE, 1)
    _setup_settings_variable(SexSetting.AUTONOMY_WATCH_SEX_STATE, 1)
    _setup_settings_variable(SexSetting.JOIN_SEX_AUTONOMY_STATE, 1)
    _setup_settings_variable(SexSetting.AUTONOMY_NPC_PREGNANCY_AWARENESS, 1)
    _setup_settings_variable(SexSetting.NPC_SEX_DURATION_VALUE, 3)
    _setup_settings_variable(SexSetting.PLAYER_AUTONOMY_STATE, 1)
    _setup_settings_variable(SexSetting.AUTONOMY_PLAYER_ASK_PLAYER_DIALOG_STATE, 0)
    _setup_settings_variable(SexSetting.AUTONOMY_NPC_ASK_PLAYER_DIALOG_STATE, 1)
    _setup_settings_variable(SexSetting.AUTONOMY_PLAYER_ASK_NPC_DIALOG_STATE, 0)
    _setup_settings_variable(SexSetting.PLAYER_JOIN_SEX_AUTONOMY_STATE, 1)
    _setup_settings_variable(SexSetting.SEX_PROGRESSION_TYPE, 2)
    _setup_settings_variable(SexSetting.SEX_DURATION_TYPE, 0)
    _setup_settings_variable(SexSetting.SEX_DURATION_VALUE, 3)
    _setup_settings_variable(SexSetting.CLIMAX_SEX_PROGRESSION_STATE, 0)
    _setup_settings_variable(SexSetting.SEX_UNDRESSING_TYPE, 1)
    _setup_settings_variable(SexSetting.NPC_SEX_UNDRESSING_TYPE, 1)
    _setup_settings_variable(SexSetting.OUTFIT_AUTO_DRESS_UP_AFTER_SEX_STATE, 0)
    _setup_settings_variable(SexSetting.STRAPON_AUTO_REMOVE_STATE, 0)
    _setup_settings_variable(SexSetting.SEX_GENDER_TYPE, 1)
    _setup_settings_variable(SexSetting.GENDER_RECOGNITION_FEMALE_TO_BOTH_STATE, 0)
    _setup_settings_variable(SexSetting.GENDER_RECOGNITION_MALE_TO_BOTH_STATE, 0)
    _setup_settings_variable(SexSetting.GENDER_RECOGNITION_SIM_SPECIFIC_STATE, 0)
    _setup_settings_variable(SexSetting.PREGNANCY_MODE, 1)
    _setup_settings_variable(SexSetting.PREGNANCY_DURATION, 3)
    _setup_settings_variable(SexSetting.BIRTH_CONTROL_MODE, 1)
    _setup_settings_variable(SexSetting.NPC_BIRTH_CONTROL_MODE, 1)
    _setup_settings_variable(SexSetting.BIRTH_CONTROL_AUTO_USE, 0)
    _setup_settings_variable(SexSetting.MENSTRUAL_CYCLE_DURATION, 0)
    _setup_settings_variable(SexSetting.MENSTRUAL_CYCLE_NPC_PREGNANCY, 1)
    _setup_settings_variable(SexSetting.SIMPLE_PREGNANCY_CHANCE, 0)
    _setup_settings_variable(SexSetting.SIMPLE_NPC_PREGNANCY_CHANCE, 0)
    _setup_settings_variable(SexSetting.MISCARRIAGE_SWITCH, 1)
    _setup_settings_variable(SexSetting.TEENS_SEX_STATE, 1)
    _setup_settings_variable(SexSetting.SEX_INITIATION_TYPE, 0)
    _setup_settings_variable(SexSetting.SEX_RELATIONS_IMPACT_STATE, 1)
    _setup_settings_variable(SexSetting.SEX_ANIMATION_DURATION_OVERRIDE_TYPE, 0)
    _setup_settings_variable(SexSetting.SEX_ANIMATION_DURATION_OVERRIDE_VALUE, 15)
    _setup_settings_variable(SexSetting.CUM_VISIBILITY_STATE, 1)
    _setup_settings_variable(SexSetting.CUM_VISIBILITY_WITH_CONDOM_STATE, 1)
    _setup_settings_variable(SexSetting.SILENCE_PHONE_STATE, 1)
    _setup_settings_variable(SexSetting.VANILLA_INTERACTIONS_SWITCH, 0)
    _setup_settings_variable(SexSetting.DEFAULT_WOOHOO_SWITCH, 1)
    _setup_settings_variable(SexSetting.ALWAYS_ACCEPT_STATE, 0)
    _setup_settings_variable(SexSetting.INSTANT_UNDRESSING_STATE, 0)
    _setup_settings_variable(SexSetting.MANUAL_NPC_SEX_STATE, 0)
    _setup_settings_variable(SexSetting.NEEDS_DECAY_STATE, 1)
    _setup_settings_variable(SexSetting.PRIVACY_STATE, 1)
    _setup_settings_variable(SexSetting.REACTION_TO_SEX_STATE, 1)
    _setup_settings_variable(SexSetting.REACTION_TO_CUM_STATE, 1)
    _setup_settings_variable(SexSetting.REACTION_TO_TEEN_PREGNANCY_STATE, 1)


def _notification_settings():
    settings_option_window = SettingsWindow(0, 3942521497, 2390465803, cancel_callback=_open_sex_settings)
    settings_option_window.add_settings_option(SettingsSwitchOption(3366624962, 3419421543, _notification_settings, SEX_SETTINGS_DICT, SexSetting.AUTONOMY_NOTIFICATIONS_STATE))
    settings_option_window.add_settings_option(SettingsSwitchOption(2850533999, 3244791546, _notification_settings, SEX_SETTINGS_DICT, SexSetting.PREGNENCY_NOTIFICATIONS_STATE))
    return settings_option_window


class SexAutonomyLevelSetting(TurboEnum):
    __qualname__ = 'SexAutonomyLevelSetting'
    DISABLED = 0
    LOW = 1
    NORMAL = 2
    HIGH = 3


def _open_sex_autonomy_settings():
    _autonomy_settings().open_window()


def _autonomy_settings():

    def _open_autonomy_settings():
        _autonomy_settings().open_window()

    settings_option_window = SettingsWindow(0, 772504851, 355353948, cancel_callback=_open_sex_settings)

    def _autonomy_level():
        sex_autonomy_level_window = SettingsWindow(1, 3547420725, 639874934, cancel_callback=_open_autonomy_settings)
        sex_autonomy_level_window.add_settings_option(SettingsSelectorOption(2812893922, 4005573132, _autonomy_level, SEX_SETTINGS_DICT, SexSetting.AUTONOMY_LEVEL, SexAutonomyLevelSetting.DISABLED, allow_change_callback=False))
        sex_autonomy_level_window.add_settings_option(SettingsSelectorOption(1091365348, 1279925819, _autonomy_level, SEX_SETTINGS_DICT, SexSetting.AUTONOMY_LEVEL, SexAutonomyLevelSetting.LOW, allow_change_callback=False))
        sex_autonomy_level_window.add_settings_option(SettingsSelectorOption(1843757931, 2072620352, _autonomy_level, SEX_SETTINGS_DICT, SexSetting.AUTONOMY_LEVEL, SexAutonomyLevelSetting.NORMAL, allow_change_callback=False))
        sex_autonomy_level_window.add_settings_option(SettingsSelectorOption(44141906, 2567448436, _autonomy_level, SEX_SETTINGS_DICT, SexSetting.AUTONOMY_LEVEL, SexAutonomyLevelSetting.HIGH, allow_change_callback=False))
        return sex_autonomy_level_window

    settings_option_window.add_settings_option(SettingsBranchOption(_autonomy_level, allow_open_callback=False))

    def _autonomy_specifics():
        sex_autonomy_specifics_window = SettingsWindow(1, 1837632671, 1237154084, cancel_callback=_open_autonomy_settings)
        sex_autonomy_specifics_window.add_settings_option(SettingsSwitchOption(1958432185, 1853667742, _autonomy_specifics, SEX_SETTINGS_DICT, SexSetting.AUTONOMY_RELATIONSHIP_AWARENESS))
        sex_autonomy_specifics_window.add_settings_option(SettingsSwitchOption(2868453401, 2790533388, _autonomy_specifics, SEX_SETTINGS_DICT, SexSetting.AUTONOMY_RANDOM_SEX_STATE))
        sex_autonomy_specifics_window.add_settings_option(SettingsSwitchOption(702535409, 67063182, _autonomy_specifics, SEX_SETTINGS_DICT, SexSetting.AUTONOMY_RANDOM_SOLO_SEX_STATE))
        sex_autonomy_specifics_window.add_settings_option(SettingsSwitchOption(4290647276, 845223578, _autonomy_specifics, SEX_SETTINGS_DICT, SexSetting.AUTONOMY_ROMANCE_SEX_STATE))
        sex_autonomy_specifics_window.add_settings_option(SettingsSwitchOption(3379481732, 2646001095, _autonomy_specifics, SEX_SETTINGS_DICT, SexSetting.AUTONOMY_WATCH_SEX_STATE))
        sex_autonomy_specifics_window.add_settings_option(SettingsSwitchOption(1504087796, 1846650774, _autonomy_specifics, SEX_SETTINGS_DICT, SexSetting.JOIN_SEX_AUTONOMY_STATE))
        sex_autonomy_specifics_window.add_settings_option(SettingsSwitchOption(4181149639, 1296624804, _autonomy_specifics, SEX_SETTINGS_DICT, SexSetting.AUTONOMY_NPC_PREGNANCY_AWARENESS))
        return sex_autonomy_specifics_window

    settings_option_window.add_settings_option(SettingsBranchOption(_autonomy_specifics, allow_open_callback=False))

    def _autonomy_asking_dialogs():
        sex_autonomy_asking_window = SettingsWindow(1, 2850867506, 1785597846, cancel_callback=_open_autonomy_settings)
        sex_autonomy_asking_window.add_settings_option(SettingsSwitchOption(2452930409, 1667433751, _autonomy_asking_dialogs, SEX_SETTINGS_DICT, SexSetting.AUTONOMY_PLAYER_ASK_PLAYER_DIALOG_STATE))
        sex_autonomy_asking_window.add_settings_option(SettingsSwitchOption(3891041835, 1254474301, _autonomy_asking_dialogs, SEX_SETTINGS_DICT, SexSetting.AUTONOMY_NPC_ASK_PLAYER_DIALOG_STATE))
        sex_autonomy_asking_window.add_settings_option(SettingsSwitchOption(654398743, 4097958165, _autonomy_asking_dialogs, SEX_SETTINGS_DICT, SexSetting.AUTONOMY_PLAYER_ASK_NPC_DIALOG_STATE))
        return sex_autonomy_asking_window

    settings_option_window.add_settings_option(SettingsBranchOption(_autonomy_asking_dialogs, allow_open_callback=False))
    settings_option_window.add_settings_option(SettingsInputOption(2954623901, 270337891, _autonomy_settings, SEX_SETTINGS_DICT[SexSetting.NPC_SEX_DURATION_VALUE], SEX_SETTINGS_DICT, SexSetting.NPC_SEX_DURATION_VALUE, min_value=1))
    settings_option_window.add_settings_option(SettingsSwitchOption(3175007247, 75047863, _autonomy_settings, SEX_SETTINGS_DICT, SexSetting.PLAYER_AUTONOMY_STATE))
    settings_option_window.add_settings_option(SettingsSwitchOption(3877057791, 3708088834, _autonomy_settings, SEX_SETTINGS_DICT, SexSetting.PLAYER_JOIN_SEX_AUTONOMY_STATE))
    from wickedwhims.sex.settings.animation_disabler_settings import open_autonomy_animations_disabler
    settings_option_window.add_settings_option(SettingsCallbackOption(2284702213, 2444846310, open_autonomy_animations_disabler))
    return settings_option_window


class SexProgressionLevelSetting(TurboEnum):
    __qualname__ = 'SexProgressionLevelSetting'
    DISABLED = 0
    STAGE_ONLY = 1
    FULL = 2
    RANDOM = 3


class SexInteractionDurationTypeSetting(TurboEnum):
    __qualname__ = 'SexInteractionDurationTypeSetting'
    TIME_LIMIT = 0
    CLIMAX = 1


def _interaction_settings():

    def _open_interaction_settings():
        _interaction_settings().open_window()

    settings_option_window = SettingsWindow(0, 679078101, 2235096818, cancel_callback=_open_sex_settings)

    def _sex_progression_level():
        sex_progression_level_window = SettingsWindow(1, 2252255568, 2366957964, cancel_callback=_open_interaction_settings)
        sex_progression_level_window.add_settings_option(SettingsSelectorOption(3375283059, 1955101260, _sex_progression_level, SEX_SETTINGS_DICT, SexSetting.SEX_PROGRESSION_TYPE, SexProgressionLevelSetting.DISABLED, allow_change_callback=False))
        sex_progression_level_window.add_settings_option(SettingsSelectorOption(4196260323, 1029205692, _sex_progression_level, SEX_SETTINGS_DICT, SexSetting.SEX_PROGRESSION_TYPE, SexProgressionLevelSetting.STAGE_ONLY, allow_change_callback=False))
        sex_progression_level_window.add_settings_option(SettingsSelectorOption(793763770, 2858531257, _sex_progression_level, SEX_SETTINGS_DICT, SexSetting.SEX_PROGRESSION_TYPE, SexProgressionLevelSetting.FULL, allow_change_callback=False))
        sex_progression_level_window.add_settings_option(SettingsSelectorOption(1272575900, 3811352518, _sex_progression_level, SEX_SETTINGS_DICT, SexSetting.SEX_PROGRESSION_TYPE, SexProgressionLevelSetting.RANDOM, allow_change_callback=False))
        return sex_progression_level_window

    settings_option_window.add_settings_option(SettingsBranchOption(_sex_progression_level, allow_open_callback=False))

    def _sex_duration_settings():
        sex_duration_type_window = SettingsWindow(2, 2304850363, 2697283065, cancel_callback=_open_interaction_settings)
        sex_duration_type_window.add_settings_option(SettingsSelectorOption(3718931206, 1812879384, _sex_duration_settings, SEX_SETTINGS_DICT, SexSetting.SEX_DURATION_TYPE, SexInteractionDurationTypeSetting.TIME_LIMIT, allow_change_callback=False))
        sex_duration_type_window.add_settings_option(SettingsSelectorOption(91570471, 406726944, _sex_duration_settings, SEX_SETTINGS_DICT, SexSetting.SEX_DURATION_TYPE, SexInteractionDurationTypeSetting.CLIMAX, allow_change_callback=False))
        if SEX_SETTINGS_DICT[SexSetting.SEX_DURATION_TYPE] == SexInteractionDurationTypeSetting.TIME_LIMIT:
            sex_duration_type_window.add_settings_option(SettingsInputOption(3275682984, 1812879384, _sex_duration_settings, SEX_SETTINGS_DICT[SexSetting.SEX_DURATION_VALUE], SEX_SETTINGS_DICT, SexSetting.SEX_DURATION_VALUE, min_value=1))
        return sex_duration_type_window

    settings_option_window.add_settings_option(SettingsBranchOption(_sex_duration_settings, allow_open_callback=False))
    settings_option_window.add_settings_option(SettingsSwitchOption(3424533837, 878801550, _interaction_settings, SEX_SETTINGS_DICT, SexSetting.CLIMAX_SEX_PROGRESSION_STATE))
    return settings_option_window


class SexUndressingLevelSetting(TurboEnum):
    __qualname__ = 'SexUndressingLevelSetting'
    DISABLED = 0
    AUTO = 1
    COMPLETE = 2


def _outfit_settings():

    def _open_interaction_settings():
        _outfit_settings().open_window()

    settings_option_window = SettingsWindow(3, 4282949192, 1311817416, cancel_callback=_open_sex_settings)

    def _sex_undressing_level():
        sex_undressing_level_window = SettingsWindow(1, 1198907594, 20176818, cancel_callback=_open_interaction_settings)
        sex_undressing_level_window.add_settings_option(SettingsSelectorOption(170791406, 1387510539, _sex_undressing_level, SEX_SETTINGS_DICT, SexSetting.SEX_UNDRESSING_TYPE, SexUndressingLevelSetting.DISABLED, allow_change_callback=False))
        sex_undressing_level_window.add_settings_option(SettingsSelectorOption(1669970287, 3534301752, _sex_undressing_level, SEX_SETTINGS_DICT, SexSetting.SEX_UNDRESSING_TYPE, SexUndressingLevelSetting.AUTO, allow_change_callback=False))
        sex_undressing_level_window.add_settings_option(SettingsSelectorOption(1122202719, 1550925065, _sex_undressing_level, SEX_SETTINGS_DICT, SexSetting.SEX_UNDRESSING_TYPE, SexUndressingLevelSetting.COMPLETE, allow_change_callback=False))
        return sex_undressing_level_window

    settings_option_window.add_settings_option(SettingsBranchOption(_sex_undressing_level, allow_open_callback=False))

    def _npc_sex_undressing_level():
        sex_undressing_level_window = SettingsWindow(1, 2532050121, 235100229, cancel_callback=_open_interaction_settings)
        sex_undressing_level_window.add_settings_option(SettingsSelectorOption(170791406, 1387510539, _npc_sex_undressing_level, SEX_SETTINGS_DICT, SexSetting.NPC_SEX_UNDRESSING_TYPE, SexUndressingLevelSetting.DISABLED, allow_change_callback=False))
        sex_undressing_level_window.add_settings_option(SettingsSelectorOption(1669970287, 3534301752, _npc_sex_undressing_level, SEX_SETTINGS_DICT, SexSetting.NPC_SEX_UNDRESSING_TYPE, SexUndressingLevelSetting.AUTO, allow_change_callback=False))
        sex_undressing_level_window.add_settings_option(SettingsSelectorOption(1122202719, 1550925065, _npc_sex_undressing_level, SEX_SETTINGS_DICT, SexSetting.NPC_SEX_UNDRESSING_TYPE, SexUndressingLevelSetting.COMPLETE, allow_change_callback=False))
        return sex_undressing_level_window

    settings_option_window.add_settings_option(SettingsBranchOption(_npc_sex_undressing_level, allow_open_callback=False))
    settings_option_window.add_settings_option(SettingsSwitchOption(3237215331, 1958038349, _outfit_settings, SEX_SETTINGS_DICT, SexSetting.OUTFIT_AUTO_DRESS_UP_AFTER_SEX_STATE))
    settings_option_window.add_settings_option(SettingsSwitchOption(2301375032, 1690045821, _outfit_settings, SEX_SETTINGS_DICT, SexSetting.STRAPON_AUTO_REMOVE_STATE))
    return settings_option_window


class SexGenderTypeSetting(TurboEnum):
    __qualname__ = 'SexGenderTypeSetting'
    SEX_BASED = 0
    GENDER_BASED = 1
    ANY_BASED = 2


def _gender_settings():

    def _open_gender_settings():
        _gender_settings().open_window()

    settings_option_window = SettingsWindow(0, 1255756570, 2104076668, cancel_callback=_open_sex_settings)

    def _sex_gender_type():
        sex_gender_type_window = SettingsWindow(1, 1788660950, 5799974, cancel_callback=_open_gender_settings)
        sex_gender_type_window.add_settings_option(SettingsSelectorOption(2575413641, 3674097914, _sex_gender_type, SEX_SETTINGS_DICT, SexSetting.SEX_GENDER_TYPE, SexGenderTypeSetting.SEX_BASED, allow_change_callback=False))
        sex_gender_type_window.add_settings_option(SettingsSelectorOption(581623950, 728075106, _sex_gender_type, SEX_SETTINGS_DICT, SexSetting.SEX_GENDER_TYPE, SexGenderTypeSetting.GENDER_BASED, allow_change_callback=False))
        sex_gender_type_window.add_settings_option(SettingsSelectorOption(656988476, 2871758999, _sex_gender_type, SEX_SETTINGS_DICT, SexSetting.SEX_GENDER_TYPE, SexGenderTypeSetting.ANY_BASED, allow_change_callback=False))
        return sex_gender_type_window

    settings_option_window.add_settings_option(SettingsBranchOption(_sex_gender_type, allow_open_callback=False))
    settings_option_window.add_settings_option(SettingsSwitchOption(3804026130, 1632529084, _gender_settings, SEX_SETTINGS_DICT, SexSetting.GENDER_RECOGNITION_FEMALE_TO_BOTH_STATE))
    settings_option_window.add_settings_option(SettingsSwitchOption(1983215653, 108985975, _gender_settings, SEX_SETTINGS_DICT, SexSetting.GENDER_RECOGNITION_MALE_TO_BOTH_STATE))
    settings_option_window.add_settings_option(SettingsSwitchOption(491871453, 4192011344, _gender_settings, SEX_SETTINGS_DICT, SexSetting.GENDER_RECOGNITION_SIM_SPECIFIC_STATE))
    return settings_option_window


class PregnancyModeSetting(TurboEnum):
    __qualname__ = 'PregnancyModeSetting'
    DISABLED = 0
    MENSTRUAL_CYCLE = 1
    SIMPLE = 2


class MenstrualCycleDurationSetting(TurboEnum):
    __qualname__ = 'MenstrualCycleDurationSetting'
    AUTO = 0
    SHORT = 1
    NORMAL = 2
    LONG = 3
    VERY_LONG = 4


class BirthControlModeSetting(TurboEnum):
    __qualname__ = 'BirthControlModeSetting'
    PERFECT = 0
    REALISTIC = 1


class NPCBirthControlModeSetting(TurboEnum):
    __qualname__ = 'NPCBirthControlModeSetting'
    SAFE = 0
    MODERATE = 1
    UNSAFE = 2


def _pregnancy_settings():

    def _open_pregnancy_settings():
        _pregnancy_settings().open_window()

    def _exit_pregnancy_settings():
        if get_sex_setting(SexSetting.PREGNANCY_MODE, variable_type=int) != PregnancyModeSetting.DISABLED:
            set_pregnancy_duration(get_sex_setting(SexSetting.PREGNANCY_DURATION, variable_type=int))
        _open_sex_settings()

    settings_option_window = SettingsWindow(0, 4283337872, 509549869, cancel_callback=_exit_pregnancy_settings)

    def _pregnancy_mode():
        pregnancy_mode_window = SettingsWindow(1, 3511666942, 47964663, cancel_callback=_open_pregnancy_settings)
        pregnancy_mode_window.add_settings_option(SettingsSelectorOption(1502510716, 438007632, _pregnancy_mode, SEX_SETTINGS_DICT, SexSetting.PREGNANCY_MODE, PregnancyModeSetting.DISABLED, allow_change_callback=False))
        pregnancy_mode_window.add_settings_option(SettingsSelectorOption(1885043084, 932412252, _pregnancy_mode, SEX_SETTINGS_DICT, SexSetting.PREGNANCY_MODE, PregnancyModeSetting.MENSTRUAL_CYCLE, allow_change_callback=False))
        pregnancy_mode_window.add_settings_option(SettingsSelectorOption(2261619077, 4118916902, _pregnancy_mode, SEX_SETTINGS_DICT, SexSetting.PREGNANCY_MODE, PregnancyModeSetting.SIMPLE, allow_change_callback=False))
        return pregnancy_mode_window

    settings_option_window.add_settings_option(SettingsBranchOption(_pregnancy_mode, allow_open_callback=False))

    def _menstrual_cycle_duration():
        cycle_duration_window = SettingsWindow(1, 3329620855, 2700070040, cancel_callback=_open_pregnancy_settings)
        cycle_duration_window.add_settings_option(SettingsSelectorOption(2942546179, 3427448649, _menstrual_cycle_duration, SEX_SETTINGS_DICT, SexSetting.MENSTRUAL_CYCLE_DURATION, MenstrualCycleDurationSetting.AUTO, allow_change_callback=False))
        cycle_duration_window.add_settings_option(SettingsSelectorOption(2977040698, 2146497004, _menstrual_cycle_duration, SEX_SETTINGS_DICT, SexSetting.MENSTRUAL_CYCLE_DURATION, MenstrualCycleDurationSetting.VERY_LONG, allow_change_callback=False))
        cycle_duration_window.add_settings_option(SettingsSelectorOption(2384666054, 2690713490, _menstrual_cycle_duration, SEX_SETTINGS_DICT, SexSetting.MENSTRUAL_CYCLE_DURATION, MenstrualCycleDurationSetting.LONG, allow_change_callback=False))
        cycle_duration_window.add_settings_option(SettingsSelectorOption(3875124511, 2803796174, _menstrual_cycle_duration, SEX_SETTINGS_DICT, SexSetting.MENSTRUAL_CYCLE_DURATION, MenstrualCycleDurationSetting.NORMAL, allow_change_callback=False))
        cycle_duration_window.add_settings_option(SettingsSelectorOption(3424872466, 209206419, _menstrual_cycle_duration, SEX_SETTINGS_DICT, SexSetting.MENSTRUAL_CYCLE_DURATION, MenstrualCycleDurationSetting.SHORT, allow_change_callback=False))
        return cycle_duration_window

    if get_sex_setting(SexSetting.PREGNANCY_MODE, variable_type=int) == PregnancyModeSetting.MENSTRUAL_CYCLE:
        settings_option_window.add_settings_option(SettingsBranchOption(_menstrual_cycle_duration, allow_open_callback=False))
        settings_option_window.add_settings_option(SettingsSwitchOption(619151676, 3609080218, _pregnancy_settings, SEX_SETTINGS_DICT, SexSetting.MENSTRUAL_CYCLE_NPC_PREGNANCY))

    def _simple_pregnancy_chance():
        pregnancy_chance_window = SettingsWindow(1, 2995617922, 1003291803, cancel_callback=_open_pregnancy_settings)
        pregnancy_chance_window.add_settings_option(SettingsSelectorOption(TurboL18NUtil.get_localized_string(182912662, tokens=('0%',)), 0, _simple_pregnancy_chance, SEX_SETTINGS_DICT, SexSetting.SIMPLE_PREGNANCY_CHANCE, 0, allow_change_callback=False))
        pregnancy_chance_window.add_settings_option(SettingsSelectorOption(TurboL18NUtil.get_localized_string(182912662, tokens=('1%',)), 0, _simple_pregnancy_chance, SEX_SETTINGS_DICT, SexSetting.SIMPLE_PREGNANCY_CHANCE, 1, allow_change_callback=False))
        pregnancy_chance_window.add_settings_option(SettingsSelectorOption(TurboL18NUtil.get_localized_string(182912662, tokens=('2%',)), 0, _simple_pregnancy_chance, SEX_SETTINGS_DICT, SexSetting.SIMPLE_PREGNANCY_CHANCE, 2, allow_change_callback=False))
        pregnancy_chance_window.add_settings_option(SettingsSelectorOption(TurboL18NUtil.get_localized_string(182912662, tokens=('3%',)), 0, _simple_pregnancy_chance, SEX_SETTINGS_DICT, SexSetting.SIMPLE_PREGNANCY_CHANCE, 3, allow_change_callback=False))
        pregnancy_chance_window.add_settings_option(SettingsSelectorOption(TurboL18NUtil.get_localized_string(182912662, tokens=('4%',)), 0, _simple_pregnancy_chance, SEX_SETTINGS_DICT, SexSetting.SIMPLE_PREGNANCY_CHANCE, 4, allow_change_callback=False))
        for i in range(1, 21):
            option_title = TurboL18NUtil.get_localized_string(182912662, tokens=(TurboL18NUtil.get_localized_string(str(i*5) + '%'),))
            pregnancy_chance_window.add_settings_option(SettingsSelectorOption(option_title, 0, _simple_pregnancy_chance, SEX_SETTINGS_DICT, SexSetting.SIMPLE_PREGNANCY_CHANCE, i*5, allow_change_callback=False))
        return pregnancy_chance_window

    if get_sex_setting(SexSetting.PREGNANCY_MODE, variable_type=int) == PregnancyModeSetting.SIMPLE:
        settings_option_window.add_settings_option(SettingsBranchOption(_simple_pregnancy_chance, allow_open_callback=False))

    def _simple_npc_pregnancy_chance():
        pregnancy_chance_window = SettingsWindow(1, 713658988, 3667660227, cancel_callback=_open_pregnancy_settings)
        pregnancy_chance_window.add_settings_option(SettingsSelectorOption(TurboL18NUtil.get_localized_string(182912662, tokens=('0%',)), 0, _simple_npc_pregnancy_chance, SEX_SETTINGS_DICT, SexSetting.SIMPLE_NPC_PREGNANCY_CHANCE, 0, allow_change_callback=False))
        pregnancy_chance_window.add_settings_option(SettingsSelectorOption(TurboL18NUtil.get_localized_string(182912662, tokens=('1%',)), 0, _simple_npc_pregnancy_chance, SEX_SETTINGS_DICT, SexSetting.SIMPLE_NPC_PREGNANCY_CHANCE, 1, allow_change_callback=False))
        pregnancy_chance_window.add_settings_option(SettingsSelectorOption(TurboL18NUtil.get_localized_string(182912662, tokens=('2%',)), 0, _simple_npc_pregnancy_chance, SEX_SETTINGS_DICT, SexSetting.SIMPLE_NPC_PREGNANCY_CHANCE, 2, allow_change_callback=False))
        pregnancy_chance_window.add_settings_option(SettingsSelectorOption(TurboL18NUtil.get_localized_string(182912662, tokens=('3%',)), 0, _simple_npc_pregnancy_chance, SEX_SETTINGS_DICT, SexSetting.SIMPLE_NPC_PREGNANCY_CHANCE, 3, allow_change_callback=False))
        pregnancy_chance_window.add_settings_option(SettingsSelectorOption(TurboL18NUtil.get_localized_string(182912662, tokens=('4%',)), 0, _simple_npc_pregnancy_chance, SEX_SETTINGS_DICT, SexSetting.SIMPLE_NPC_PREGNANCY_CHANCE, 4, allow_change_callback=False))
        for i in range(1, 21):
            option_title = TurboL18NUtil.get_localized_string(182912662, tokens=(TurboL18NUtil.get_localized_string(str(i*5) + '%'),))
            pregnancy_chance_window.add_settings_option(SettingsSelectorOption(option_title, 0, _simple_npc_pregnancy_chance, SEX_SETTINGS_DICT, SexSetting.SIMPLE_NPC_PREGNANCY_CHANCE, i*5, allow_change_callback=False))
        return pregnancy_chance_window

    if get_sex_setting(SexSetting.PREGNANCY_MODE, variable_type=int) == PregnancyModeSetting.SIMPLE:
        settings_option_window.add_settings_option(SettingsBranchOption(_simple_npc_pregnancy_chance, allow_open_callback=False))
    settings_option_window.add_settings_option(SettingsInputOption(556352433, 1728685938, _pregnancy_settings, SEX_SETTINGS_DICT[SexSetting.PREGNANCY_DURATION], SEX_SETTINGS_DICT, SexSetting.PREGNANCY_DURATION, min_value=1))

    def _birth_control_mode():
        birth_control_mode_window = SettingsWindow(1, 2645678251, 2237541236, cancel_callback=_open_pregnancy_settings)
        birth_control_mode_window.add_settings_option(SettingsSelectorOption(3625448012, 944923656, _birth_control_mode, SEX_SETTINGS_DICT, SexSetting.BIRTH_CONTROL_MODE, BirthControlModeSetting.PERFECT, allow_change_callback=False))
        birth_control_mode_window.add_settings_option(SettingsSelectorOption(2936152503, 1099359772, _birth_control_mode, SEX_SETTINGS_DICT, SexSetting.BIRTH_CONTROL_MODE, BirthControlModeSetting.REALISTIC, allow_change_callback=False))
        return birth_control_mode_window

    settings_option_window.add_settings_option(SettingsBranchOption(_birth_control_mode, allow_open_callback=False))

    def _npc_birth_control_mode():
        npc_birth_control_mode_window = SettingsWindow(1, 3306556634, 2735186651, cancel_callback=_open_pregnancy_settings)
        npc_birth_control_mode_window.add_settings_option(SettingsSelectorOption(1445725124, 1875877528, _npc_birth_control_mode, SEX_SETTINGS_DICT, SexSetting.NPC_BIRTH_CONTROL_MODE, NPCBirthControlModeSetting.SAFE, allow_change_callback=False))
        npc_birth_control_mode_window.add_settings_option(SettingsSelectorOption(1631987776, 4199709209, _npc_birth_control_mode, SEX_SETTINGS_DICT, SexSetting.NPC_BIRTH_CONTROL_MODE, NPCBirthControlModeSetting.MODERATE, allow_change_callback=False))
        npc_birth_control_mode_window.add_settings_option(SettingsSelectorOption(3220390137, 4218021585, _npc_birth_control_mode, SEX_SETTINGS_DICT, SexSetting.NPC_BIRTH_CONTROL_MODE, NPCBirthControlModeSetting.UNSAFE, allow_change_callback=False))
        return npc_birth_control_mode_window

    settings_option_window.add_settings_option(SettingsBranchOption(_npc_birth_control_mode, allow_open_callback=False))
    settings_option_window.add_settings_option(SettingsSwitchOption(1288635396, 3520888385, _pregnancy_settings, SEX_SETTINGS_DICT, SexSetting.BIRTH_CONTROL_AUTO_USE))
    if is_basemental_drugs_installed():
        settings_option_window.add_settings_option(SettingsSwitchOption(2235486711, 4073427182, _pregnancy_settings, SEX_SETTINGS_DICT, SexSetting.MISCARRIAGE_SWITCH))
    return settings_option_window


class SexInitiationTypeSetting(TurboEnum):
    __qualname__ = 'SexInitiationTypeSetting'
    TALK_AND_WALK = 0
    INSTANT_TELEPORT = 1


class SexAnimationDurationOverrideType(TurboEnum):
    __qualname__ = 'SexAnimationDurationOverrideType'
    DEFAULT = 0
    OVERRIDE = 1


def _other_settings():

    def _open_other_settings():
        _other_settings().open_window()

    def _change_warning_message():
        display_ok_dialog(text=2437423776, title=2360091807)

    settings_option_window = SettingsWindow(0, 2360091807, 3065078624, change_callback=_change_warning_message, cancel_callback=_open_sex_settings)
    settings_option_window.add_settings_option(SettingsSwitchOption(307055479, 3218540922, _other_settings, SEX_SETTINGS_DICT, SexSetting.TEENS_SEX_STATE, allow_change_callback=False))
    settings_option_window.add_settings_option(SettingsSwitchOption(364609057, 1827602266, _other_settings, SEX_SETTINGS_DICT, SexSetting.SILENCE_PHONE_STATE, allow_change_callback=False))
    settings_option_window.add_settings_option(SettingsSwitchOption(142564328, 239190384, _other_settings, SEX_SETTINGS_DICT, SexSetting.DEFAULT_WOOHOO_SWITCH, allow_change_callback=True))
    settings_option_window.add_settings_option(SettingsSwitchOption(3571944160, 420791980, _other_settings, SEX_SETTINGS_DICT, SexSetting.VANILLA_INTERACTIONS_SWITCH, allow_change_callback=True))

    def _cum_settings():
        cum_settings_window = SettingsWindow(1, 3875215528, 3025455413, cancel_callback=_open_other_settings)
        cum_settings_window.add_settings_option(SettingsSwitchOption(342798417, 1797015342, _cum_settings, SEX_SETTINGS_DICT, SexSetting.CUM_VISIBILITY_STATE))
        cum_settings_window.add_settings_option(SettingsSwitchOption(749165149, 2755226641, _cum_settings, SEX_SETTINGS_DICT, SexSetting.CUM_VISIBILITY_WITH_CONDOM_STATE))
        return cum_settings_window

    settings_option_window.add_settings_option(SettingsBranchOption(_cum_settings, allow_open_callback=False))

    def _sex_initiation_type():
        sex_gender_type_window = SettingsWindow(1, 2770502675, 1371832521, cancel_callback=_open_other_settings)
        sex_gender_type_window.add_settings_option(SettingsSelectorOption(566493688, 3052811566, _sex_initiation_type, SEX_SETTINGS_DICT, SexSetting.SEX_INITIATION_TYPE, SexInitiationTypeSetting.TALK_AND_WALK, allow_change_callback=False))
        sex_gender_type_window.add_settings_option(SettingsSelectorOption(2533155814, 3856129850, _sex_initiation_type, SEX_SETTINGS_DICT, SexSetting.SEX_INITIATION_TYPE, SexInitiationTypeSetting.INSTANT_TELEPORT, allow_change_callback=False))
        return sex_gender_type_window

    settings_option_window.add_settings_option(SettingsBranchOption(_sex_initiation_type, allow_open_callback=False))

    def _sex_animation_duration_override():
        sex_animation_duration_window = SettingsWindow(1, 4288829144, 21918993, cancel_callback=_open_other_settings)
        sex_animation_duration_window.add_settings_option(SettingsSelectorOption(3057735727, 53147723, _sex_animation_duration_override, SEX_SETTINGS_DICT, SexSetting.SEX_ANIMATION_DURATION_OVERRIDE_TYPE, SexAnimationDurationOverrideType.DEFAULT, allow_change_callback=False))
        sex_animation_duration_window.add_settings_option(SettingsSelectorOption(1667254996, 3491653927, _sex_animation_duration_override, SEX_SETTINGS_DICT, SexSetting.SEX_ANIMATION_DURATION_OVERRIDE_TYPE, SexAnimationDurationOverrideType.OVERRIDE, allow_change_callback=False))
        if SEX_SETTINGS_DICT[SexSetting.SEX_ANIMATION_DURATION_OVERRIDE_TYPE] == SexAnimationDurationOverrideType.OVERRIDE:
            sex_animation_duration_window.add_settings_option(SettingsInputOption(1264078058, 3491653927, _sex_animation_duration_override, SEX_SETTINGS_DICT[SexSetting.SEX_ANIMATION_DURATION_OVERRIDE_VALUE], SEX_SETTINGS_DICT, SexSetting.SEX_ANIMATION_DURATION_OVERRIDE_VALUE, min_value=15))
        return sex_animation_duration_window

    settings_option_window.add_settings_option(SettingsBranchOption(_sex_animation_duration_override, allow_open_callback=False))
    return settings_option_window


def _cheats_settings():
    settings_option_window = SettingsWindow(0, 2605472072, 654545057, cancel_callback=_open_sex_settings)
    settings_option_window.add_settings_option(SettingsSwitchOption(3188897533, 1973509205, _cheats_settings, SEX_SETTINGS_DICT, SexSetting.ALWAYS_ACCEPT_STATE))
    settings_option_window.add_settings_option(SettingsSwitchOption(2732646976, 176843739, _cheats_settings, SEX_SETTINGS_DICT, SexSetting.INSTANT_UNDRESSING_STATE))
    settings_option_window.add_settings_option(SettingsSwitchOption(2408622223, 2329727648, _cheats_settings, SEX_SETTINGS_DICT, SexSetting.MANUAL_NPC_SEX_STATE))
    settings_option_window.add_settings_option(SettingsSwitchOption(3057434828, 318337624, _cheats_settings, SEX_SETTINGS_DICT, SexSetting.NEEDS_DECAY_STATE))
    settings_option_window.add_settings_option(SettingsSwitchOption(1338997908, 1149646106, _other_settings, SEX_SETTINGS_DICT, SexSetting.SEX_RELATIONS_IMPACT_STATE))
    settings_option_window.add_settings_option(SettingsSwitchOption(3063236996, 2458180356, _cheats_settings, SEX_SETTINGS_DICT, SexSetting.PRIVACY_STATE))
    settings_option_window.add_settings_option(SettingsSwitchOption(1413563001, 3687654653, _cheats_settings, SEX_SETTINGS_DICT, SexSetting.REACTION_TO_SEX_STATE))
    settings_option_window.add_settings_option(SettingsSwitchOption(634015514, 1608028199, _cheats_settings, SEX_SETTINGS_DICT, SexSetting.REACTION_TO_CUM_STATE))
    settings_option_window.add_settings_option(SettingsSwitchOption(2657851670, 1137427362, _cheats_settings, SEX_SETTINGS_DICT, SexSetting.REACTION_TO_TEEN_PREGNANCY_STATE))
    return settings_option_window


def _setup_settings_variable(variable, default_state):
    if variable not in SEX_SETTINGS_DICT:
        SEX_SETTINGS_DICT[variable] = default_state


def apply_sex_settings_from_basic_save_data():
    _setup_settings_variables()
    basic_save_data = get_basic_save_data()
    if 'woohoo' in basic_save_data:
        sex_save_data = basic_save_data['woohoo']
        for (variable, state) in sex_save_data.items():
            while variable in SEX_SETTINGS_DICT:
                try:
                    SEX_SETTINGS_DICT[variable] = int(state)
                except ValueError:
                    pass
    if get_sex_setting(SexSetting.PREGNANCY_MODE, variable_type=int) != PregnancyModeSetting.DISABLED:
        set_pregnancy_duration(get_sex_setting(SexSetting.PREGNANCY_DURATION, variable_type=int))
    update_sex_settings_to_basic_save_data()


def update_sex_settings_to_basic_save_data():
    set_vanilla_interactions_access_in_sex(get_sex_setting(SexSetting.VANILLA_INTERACTIONS_SWITCH, variable_type=bool))
    disable_woohoo_interactions(get_sex_setting(SexSetting.DEFAULT_WOOHOO_SWITCH, variable_type=bool))
    general_dict = dict()
    general_dict['woohoo'] = SEX_SETTINGS_DICT
    update_basic_save_data(general_dict)


def get_sex_setting(variable, variable_type=bool):
    return variable_type(SEX_SETTINGS_DICT[variable])

