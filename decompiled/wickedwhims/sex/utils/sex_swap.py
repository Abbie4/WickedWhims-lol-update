'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from turbolib.sim_util import TurboSimUtil
from wickedwhims.sex.enums.sex_gender import SexGenderType, get_sim_sex_gender
from wickedwhims.sex.settings.sex_settings import SexGenderTypeSetting, SexSetting, get_sex_setting

def is_compatible_actor(sim_identifier, sim_actor, target_sim_identifier, target_actor):
    if get_sex_setting(SexSetting.SEX_GENDER_TYPE, variable_type=int) == SexGenderTypeSetting.ANY_BASED:
        return True
    if sim_actor.get_gender_type() == target_actor.get_gender_type() or TurboSimUtil.Gender.get_gender(sim_identifier) == TurboSimUtil.Gender.get_gender(target_sim_identifier):
        return True
    if (get_sim_sex_gender(sim_identifier) == target_actor.get_gender_type() or target_actor.get_gender_type() == SexGenderType.BOTH or target_actor.get_gender_type() == SexGenderType.CBOTH) and (get_sim_sex_gender(target_sim_identifier) == sim_actor.get_gender_type() or sim_actor.get_gender_type() == SexGenderType.BOTH or sim_actor.get_gender_type() == SexGenderType.CBOTH):
        return True
    return False

