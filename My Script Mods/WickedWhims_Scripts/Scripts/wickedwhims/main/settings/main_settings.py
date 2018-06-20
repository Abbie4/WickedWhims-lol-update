'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
import webbrowser
from turbolib.command_util import TurboCommandUtil
from turbolib.resources.affordances import AffordanceRegistration, register_affordance_class
from turbolib.types_util import TurboTypesUtil
from turbolib.ui_util import TurboUIUtil
from turbolib.world_util import TurboWorldUtil
from turbolib.wrappers.interactions import TurboTerrainImmediateSuperInteraction, TurboInteractionStartMixin
from wickedwhims.main.settings._ts4_menu_utils import get_menu_sim, clear_menu_sim
from wickedwhims.utils_interfaces import display_picker_list_dialog, display_okcancel_dialog, get_question_icon, get_arrow_icon, get_action_icon
MAIN_SETTINGS_OPTIONS = list()
IS_TIME_PAUSED = True

class DisplayMainSettingsInteraction(TurboTerrainImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'DisplayMainSettingsInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        if TurboTypesUtil.Sims.is_sim(interaction_target):
            return True
        if TurboTypesUtil.Objects.is_game_object(interaction_target):
            from wickedwhims.sex.animations.animations_operator import has_object_any_animations
            from wickedwhims.sex.enums.sex_gender import get_sim_sex_gender
            if has_object_any_animations(interaction_target, get_sim_sex_gender(cls.get_interaction_sim(interaction_context))):
                return True
        elif TurboTypesUtil.Objects.is_terrain(interaction_target) and cls.is_terrain_location_valid(interaction_target, interaction_context):
            return True
        return False

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        global IS_TIME_PAUSED
        IS_TIME_PAUSED = TurboWorldUtil.Time.get_current_time_speed() == TurboWorldUtil.Time.ClockSpeedMode.PAUSED
        TurboWorldUtil.Time.set_current_time_speed(TurboWorldUtil.Time.ClockSpeedMode.PAUSED)
        open_main_settings()


def register_main_settings_option():

    def regiser_to_collection(method):
        MAIN_SETTINGS_OPTIONS.append(method)
        return method

    return regiser_to_collection


def open_main_settings():
    list_options = list()
    headline_effects_menu_option = TurboUIUtil.ObjectPickerDialog.ListPickerRow(6, 3283606570, 3906855187, icon=get_arrow_icon(), tag=open_headline_effects_menu)
    more_informations_option = TurboUIUtil.ObjectPickerDialog.ListPickerRow(7, 3921925930, 1456337762, icon=get_question_icon(), tag=open_more_informations_dialog)
    for setting_option in MAIN_SETTINGS_OPTIONS:
        list_options.append(setting_option())
    list_options.append(headline_effects_menu_option)
    list_options.append(more_informations_option)
    list_options = sorted(list_options, key=lambda x: x.get_option_id())

    def _main_settings_menu_callback(dialog):
        if not TurboUIUtil.ObjectPickerDialog.get_response_result(dialog):
            if IS_TIME_PAUSED is False:
                TurboWorldUtil.Time.set_current_time_speed(TurboWorldUtil.Time.ClockSpeedMode.NORMAL)
            clear_menu_sim()
            return False
        result_option = TurboUIUtil.ObjectPickerDialog.get_tag_result(dialog)
        result_option()
        return True

    display_picker_list_dialog(title=137933503, picker_rows=list_options, sim=get_menu_sim(), callback=_main_settings_menu_callback)


def open_more_informations_dialog():

    def _more_info_dialog_callback(dialog):
        if not TurboUIUtil.ObjectPickerDialog.get_response_result(dialog):
            open_main_settings()
            return False
        webbrowser.open('https://wickedwhimsmod.com/')
        TurboWorldUtil.Time.set_current_time_speed(TurboWorldUtil.Time.ClockSpeedMode.PAUSED)
        clear_menu_sim()
        return True

    display_okcancel_dialog(text=3349884559, title=3921925930, callback=_more_info_dialog_callback)


def open_headline_effects_menu():
    enabled_option = TurboUIUtil.ObjectPickerDialog.ListPickerRow(1, 366188754, 4060605351, icon=get_action_icon())
    disabled_option = TurboUIUtil.ObjectPickerDialog.ListPickerRow(2, 2403236729, 1479275710, icon=get_action_icon())

    def _headline_effects_menu_callback(dialog):
        if not TurboUIUtil.ObjectPickerDialog.get_response_result(dialog):
            open_main_settings()
            return False
        result = TurboUIUtil.ObjectPickerDialog.get_tag_result(dialog)
        if result == 1:
            TurboCommandUtil.invoke_command('headlineeffects on')
        elif result == 2:
            TurboCommandUtil.invoke_command('headlineeffects off')
        clear_menu_sim()
        return True

    display_picker_list_dialog(title=3283606570, picker_rows=(enabled_option, disabled_option), sim=get_menu_sim(), callback=_headline_effects_menu_callback)


@register_affordance_class()
class SettingsTerrainAffordanceRegisterClass(AffordanceRegistration):
    __qualname__ = 'SettingsTerrainAffordanceRegisterClass'

    def get_affordance_references(self):
        return (9482161985439680682,)

    def is_terrain(self):
        return True


@register_affordance_class()
class SettingsObjectsAffordanceRegisterClass(AffordanceRegistration):
    __qualname__ = 'SettingsObjectsAffordanceRegisterClass'

    def get_affordance_references(self):
        return (9482161985439680682,)

    def is_script_object(self, script_object):
        return TurboTypesUtil.Objects.is_game_object(script_object)

