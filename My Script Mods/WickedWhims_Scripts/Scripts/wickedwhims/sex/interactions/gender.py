'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from turbolib.sim_util import TurboSimUtil
from turbolib.types_util import TurboTypesUtil
from turbolib.wrappers.interactions import TurboImmediateSuperInteraction, TurboInteractionStartMixin
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.sex.settings.sex_settings import get_sex_setting, SexSetting, SexGenderTypeSetting
from wickedwhims.sxex_bridge.sex import is_sim_in_sex, is_sim_planning_for_sex

class SetSimGenderRecognitionAsMaleInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'SetSimGenderRecognitionAsMaleInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        if not get_sex_setting(SexSetting.GENDER_RECOGNITION_SIM_SPECIFIC_STATE, variable_type=bool):
            return False
        if get_sex_setting(SexSetting.SEX_GENDER_TYPE, variable_type=int) == SexGenderTypeSetting.SEX_BASED:
            return False
        if interaction_target is None or not TurboTypesUtil.Sims.is_sim(interaction_target):
            return False
        if is_sim_in_sex(interaction_target) or is_sim_planning_for_sex(interaction_target):
            return False
        if sim_ev(interaction_target).gender_recognition == int(TurboSimUtil.Gender.MALE):
            return False
        return True

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        sim_ev(cls.get_interaction_target(interaction_instance)).gender_recognition = int(TurboSimUtil.Gender.MALE)
        return True


class SetSimGenderRecognitionAsFemaleInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'SetSimGenderRecognitionAsFemaleInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        if not get_sex_setting(SexSetting.GENDER_RECOGNITION_SIM_SPECIFIC_STATE, variable_type=bool):
            return False
        if get_sex_setting(SexSetting.SEX_GENDER_TYPE, variable_type=int) == SexGenderTypeSetting.SEX_BASED:
            return False
        if interaction_target is None or not TurboTypesUtil.Sims.is_sim(interaction_target):
            return False
        if is_sim_in_sex(interaction_target) or is_sim_planning_for_sex(interaction_target):
            return False
        if sim_ev(interaction_target).gender_recognition == int(TurboSimUtil.Gender.FEMALE):
            return False
        return True

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        sim_ev(cls.get_interaction_target(interaction_instance)).gender_recognition = int(TurboSimUtil.Gender.FEMALE)
        return True


class SetSimGenderRecognitionAsDefaultInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'SetSimGenderRecognitionAsDefaultInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        if not get_sex_setting(SexSetting.GENDER_RECOGNITION_SIM_SPECIFIC_STATE, variable_type=bool):
            return False
        if get_sex_setting(SexSetting.SEX_GENDER_TYPE, variable_type=int) == SexGenderTypeSetting.SEX_BASED:
            return False
        if interaction_target is None or not TurboTypesUtil.Sims.is_sim(interaction_target):
            return False
        if is_sim_in_sex(interaction_target) or is_sim_planning_for_sex(interaction_target):
            return False
        if sim_ev(interaction_target).gender_recognition == 0:
            return False
        return True

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        sim_ev(cls.get_interaction_target(interaction_instance)).gender_recognition = 0
        return True

