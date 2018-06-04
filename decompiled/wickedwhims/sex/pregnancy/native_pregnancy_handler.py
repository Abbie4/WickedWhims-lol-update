'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from enums.buffs_enum import SimBuff
from enums.statistics_enum import SimCommodity
from enums.traits_enum import SimTrait
from turbolib.manager_util import TurboManagerUtil
from turbolib.resource_util import TurboResourceUtil
from turbolib.sim_util import TurboSimUtil
from turbolib.world_util import TurboWorldUtil
from wickedwhims.sex.settings.sex_settings import get_sex_setting, SexSetting
from wickedwhims.sxex_bridge.statistics import increase_sim_ww_statistic
from wickedwhims.utils_buffs import remove_sim_buff
from wickedwhims.utils_interfaces import display_notification
from wickedwhims.utils_traits import has_sim_trait

def try_sim_pregnancy(sim_identifier, partner_sim_identifier):
    if not can_sim_get_pregnant(sim_identifier):
        return False
    if not can_sim_impregnate(partner_sim_identifier):
        return False
    return apply_sim_pregnancy(sim_identifier, partner_sim_identifier)

def can_sim_get_pregnant(sim_identifier):
    if TurboSimUtil.Age.is_younger_than(sim_identifier, TurboSimUtil.Age.CHILD):
        return False
    if TurboSimUtil.Age.get_age(sim_identifier) == TurboSimUtil.Age.CHILD and not get_sex_setting(SexSetting.PRECOCIOUS_PUBERTY_STATE, variable_type=bool) and not has_sim_trait(sim_identifier, SimTrait.WW_PRECOCIOUS_PUBERTY):
        return False
    if TurboSimUtil.Age.is_older_than(sim_identifier, TurboSimUtil.Age.ADULT):
        return False
    if not has_sim_trait(sim_identifier, SimTrait.GENDEROPTIONS_PREGNANCY_CANBEIMPREGNATED) or has_sim_trait(sim_identifier, SimTrait.GENDEROPTIONS_PREGNANCY_CANNOT_BEIMPREGNATED):
        return False
    if has_sim_trait(sim_identifier, SimTrait.WW_INFERTILE):
        return False
    household = TurboSimUtil.Household.get_household(sim_identifier)
    if household is None:
        return False
    if TurboWorldUtil.Household.get_free_sims_slots(household) <= 0:
        return False
    return True

def can_sim_impregnate(sim_identifier):
    if TurboSimUtil.Age.is_younger_than(sim_identifier, TurboSimUtil.Age.CHILD):
        return False
    if TurboSimUtil.Age.get_age(sim_identifier) == TurboSimUtil.Age.CHILD and not get_sex_setting(SexSetting.PRECOCIOUS_PUBERTY_STATE, variable_type=bool) and not has_sim_trait(sim_identifier, SimTrait.WW_PRECOCIOUS_PUBERTY):
        return False
    if not has_sim_trait(sim_identifier, SimTrait.GENDEROPTIONS_PREGNANCY_CANIMPREGNATE) or has_sim_trait(sim_identifier, SimTrait.GENDEROPTIONS_PREGNANCY_CANNOTIMPREGNATE):
        return False
    if has_sim_trait(sim_identifier, SimTrait.WW_INFERTILE):
        return False
    return True

def apply_sim_pregnancy(sim_identifier, partner_sim_identifier):
    pregnancy_result = TurboSimUtil.Pregnancy.start_pregnancy(sim_identifier, partner_sim_identifier)
    if pregnancy_result is False:
        return False
    remove_sim_buff(sim_identifier, SimBuff.WW_PREGNANCY_PERIOD_FINE)
    remove_sim_buff(sim_identifier, SimBuff.WW_PREGNANCY_PERIOD_FLIRTY)
    remove_sim_buff(sim_identifier, SimBuff.WW_PREGNANCY_PERIOD_DAZED)
    remove_sim_buff(sim_identifier, SimBuff.WW_PREGNANCY_PERIOD_SAD)
    remove_sim_buff(sim_identifier, SimBuff.WW_PREGNANCY_PERIOD_TENSE)
    remove_sim_buff(sim_identifier, SimBuff.WW_PREGNANCY_PERIOD_UNCOMFORTABLE)
    remove_sim_buff(sim_identifier, SimBuff.WW_PREGNANCY_PERIOD_VAMPIRE_UNCOMFORTABLE)
    remove_sim_buff(sim_identifier, SimBuff.WW_PREGNANCY_CRAMPS_LOW)
    remove_sim_buff(sim_identifier, SimBuff.WW_PREGNANCY_CRAMPS_MEDIUM)
    remove_sim_buff(sim_identifier, SimBuff.WW_PREGNANCY_CRAMPS_HIGH)
    remove_sim_buff(sim_identifier, SimBuff.WW_PREGNANCY_TERMINATION_HAPPY)
    remove_sim_buff(sim_identifier, SimBuff.WW_PREGNANCY_TERMINATION_SAD)
    remove_sim_buff(sim_identifier, SimBuff.WW_PREGNANCY_MISCARRIAGE)
    increase_sim_ww_statistic(partner_sim_identifier, 'times_impregnated')
    increase_sim_ww_statistic(sim_identifier, 'times_got_pregnant')
    return True

def remove_sim_pregnancy(sim_identifier):
    return TurboSimUtil.Pregnancy.clear_pregnancy(sim_identifier)

def get_sim_pregnancy_discovery_state(sim_identifier):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    statistic_instance = TurboResourceUtil.Services.get_instance(TurboResourceUtil.ResourceTypes.STATISTIC, SimCommodity.PREGNANCYDISCOVERY)
    if statistic_instance is None:
        return False
    return TurboSimUtil.Statistic.get_statistic_value(sim_info, statistic_instance) > TurboSimUtil.Statistic.get_statistic_min_value(statistic_instance)

def set_sim_pregnancy_discovery(sim_identifier, state):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    statistic_instance = TurboResourceUtil.Services.get_instance(TurboResourceUtil.ResourceTypes.STATISTIC, SimCommodity.PREGNANCYDISCOVERY)
    if statistic_instance is None:
        return False
    if state is True:
        if get_sex_setting(SexSetting.PREGNENCY_NOTIFICATIONS_STATE, variable_type=bool) and TurboSimUtil.Sim.is_player(sim_info):
            display_notification(text=332111907, text_tokens=(sim_info,), title=2364600527, secondary_icon=sim_info)
        TurboSimUtil.Statistic.set_statistic_value(sim_info, statistic_instance, TurboSimUtil.Statistic.get_statistic_max_value(statistic_instance))
    else:
        TurboSimUtil.Statistic.set_statistic_value(sim_info, statistic_instance, TurboSimUtil.Statistic.get_statistic_min_value(statistic_instance))
    return True

