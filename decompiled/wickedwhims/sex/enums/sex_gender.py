'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from enums.traits_enum import SimTrait
from turbolib.manager_util import TurboManagerUtil
from turbolib.native.enum import TurboEnum
from turbolib.sim_util import TurboSimUtil
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.sex.settings.sex_settings import get_sex_setting, SexSetting, SexGenderTypeSetting
from wickedwhims.utils_traits import has_sim_trait

class SexGenderType(TurboEnum):
    __qualname__ = 'SexGenderType'
    NONE = 0
    MALE = 1
    FEMALE = 2
    BOTH = 3
    VAMPIRE_MALE = 4
    VAMPIRE_FEMALE = 5
    VAMPIRE_BOTH = 6
    GHOST_MALE = 7
    GHOST_FEMALE = 8
    GHOST_BOTH = 9
    ALIEN_MALE = 10
    ALIEN_FEMALE = 11
    ALIEN_BOTH = 12

def get_sim_sex_gender(sim_identifier, ignore_sim_specific_gender=False):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    if get_sex_setting(SexSetting.SEX_GENDER_TYPE, variable_type=int) == SexGenderTypeSetting.SEX_BASED:
        if TurboSimUtil.Gender.get_gender(sim_info) == TurboSimUtil.Gender.MALE:
            return SexGenderType.MALE
        return SexGenderType.FEMALE
    else:
        if sim_ev(sim_info).gender_recognition == TurboSimUtil.Gender.MALE:
            return SexGenderType.MALE
        if ignore_sim_specific_gender is False and get_sex_setting(SexSetting.GENDER_RECOGNITION_SIM_SPECIFIC_STATE, variable_type=bool) and sim_ev(sim_info).gender_recognition == TurboSimUtil.Gender.FEMALE:
            return SexGenderType.FEMALE
        if has_sim_trait(sim_info, SimTrait.GENDEROPTIONS_TOILET_STANDING):
            return SexGenderType.MALE
        return SexGenderType.FEMALE

def get_sex_gender_type_by_name(name):
    name = name.upper()
    if name == 'MALE':
        return SexGenderType.MALE
    if name == 'FEMALE':
        return SexGenderType.FEMALE
    if name == 'BOTH':
        return SexGenderType.BOTH
    return SexGenderType.NONE

