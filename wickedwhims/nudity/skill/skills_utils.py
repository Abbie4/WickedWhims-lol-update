'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from enums.buffs_enum import SimBuff
from enums.moods_enum import SimMood
from enums.skills_enum import SimSkill
from enums.statistics_enum import SimCommodity
from enums.traits_enum import SimTrait, LotTrait
from turbolib.manager_util import TurboManagerUtil
from turbolib.native.enum import TurboEnum
from turbolib.sim_util import TurboSimUtil
from turbolib.world_util import TurboWorldUtil
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.nudity.nudity_settings import get_nudity_setting, NuditySetting
from wickedwhims.utils_buffs import remove_sim_buff
from wickedwhims.utils_sims import has_sim_mood
from wickedwhims.utils_skills import get_sim_skill_level, has_sim_skill, get_sim_full_skill_value, remove_sim_skill, set_sim_skill_value, set_sim_skill_level, change_sim_skill_percentage_value, has_sim_reached_max_skill_level, get_sim_skill_value
from wickedwhims.utils_statistics import change_sim_statistic_value, get_sim_statistic_value, set_sim_statistic_value
from wickedwhims.utils_traits import has_sim_trait, has_current_lot_trait

class NuditySkillIncreaseReason(TurboEnum):
    __qualname__ = 'NuditySkillIncreaseReason'
    NONE = 0
    BEING_IN_NAKED_OUTFIT = 1
    BEING_IN_BATHING_OUTFIT = 2
    BEING_IN_REVEALING_OUTFIT = 3
    MIRROR_NAKED_OUTFIT = 5
    MIRROR_REVEALING_OUTFIT = 4
    SEEING_NUDITY = 6
    FLASHING_BODY = 7
    SOCIAL_COMPLIMENT = 8
    SOCIAL_CONVINCE = 9
    CONFIDENCE_BONUS = 10
    SHAMELESS_BONUS_BONUS = 11
    LONER_BONUS = 12

NUDITY_SKILL_EXP = {NuditySkillIncreaseReason.BEING_IN_NAKED_OUTFIT: 0.85, NuditySkillIncreaseReason.BEING_IN_BATHING_OUTFIT: 0.25, NuditySkillIncreaseReason.BEING_IN_REVEALING_OUTFIT: 0.1, NuditySkillIncreaseReason.SEEING_NUDITY: 0.1, NuditySkillIncreaseReason.MIRROR_NAKED_OUTFIT: 0.4, NuditySkillIncreaseReason.MIRROR_REVEALING_OUTFIT: 0.15, NuditySkillIncreaseReason.FLASHING_BODY: 5.5, NuditySkillIncreaseReason.SOCIAL_COMPLIMENT: 4.0, NuditySkillIncreaseReason.SOCIAL_CONVINCE: 6.0, NuditySkillIncreaseReason.CONFIDENCE_BONUS: 0.1, NuditySkillIncreaseReason.SHAMELESS_BONUS_BONUS: 0.25, NuditySkillIncreaseReason.LONER_BONUS: 0.15}

def get_nudity_skill_points_modifier(nudity_skill_increase_reason):
    return NUDITY_SKILL_EXP[nudity_skill_increase_reason]

def remove_sim_nudity_skill(sim_identifier):
    if has_sim_trait(sim_identifier, SimTrait.WW_EXHIBITIONIST):
        return remove_sim_skill(sim_identifier, SimSkill.WW_EXHIBITIONISM)
    return remove_sim_skill(sim_identifier, SimSkill.WW_NATURISM)

def set_sim_nudity_skill_level(sim_identifier, level):
    if has_sim_trait(sim_identifier, SimTrait.WW_EXHIBITIONIST):
        return set_sim_skill_level(sim_identifier, level, SimSkill.WW_EXHIBITIONISM)
    return set_sim_skill_level(sim_identifier, level, SimSkill.WW_NATURISM)

def get_nudity_nudity_skill_type(sim_identifier):
    if has_sim_trait(sim_identifier, SimTrait.WW_EXHIBITIONIST):
        return SimSkill.WW_EXHIBITIONISM
    return SimSkill.WW_NATURISM

def increase_sim_nudity_skill(sim_identifier, amount, extra_fatigue=0.0, reason=NuditySkillIncreaseReason.NONE):
    if amount <= 0:
        return
    if TurboSimUtil.Age.is_younger_than(sim_identifier, TurboSimUtil.Age.TEEN):
        return
    if not get_nudity_setting(NuditySetting.TEENS_NUDITY_STATE, variable_type=bool) and TurboSimUtil.Age.is_younger_than(sim_identifier, TurboSimUtil.Age.TEEN, or_equal=True):
        return
    if reason == NuditySkillIncreaseReason.BEING_IN_NAKED_OUTFIT or reason == NuditySkillIncreaseReason.BEING_IN_BATHING_OUTFIT or reason == NuditySkillIncreaseReason.BEING_IN_REVEALING_OUTFIT:
        if has_sim_trait(sim_identifier, SimTrait.SHAMELESS):
            amount += get_nudity_skill_points_modifier(NuditySkillIncreaseReason.SHAMELESS_BONUS_BONUS)
        if has_sim_mood(sim_identifier, SimMood.CONFIDENT) or has_sim_trait(sim_identifier, SimTrait.SELFASSURED):
            amount += get_nudity_skill_points_modifier(NuditySkillIncreaseReason.CONFIDENCE_BONUS)
    elif (reason == NuditySkillIncreaseReason.MIRROR_REVEALING_OUTFIT or reason == NuditySkillIncreaseReason.MIRROR_NAKED_OUTFIT or reason == NuditySkillIncreaseReason.SEEING_NUDITY) and has_sim_trait(sim_identifier, SimTrait.LONER):
        amount += get_nudity_skill_points_modifier(NuditySkillIncreaseReason.SHAMELESS_BONUS_BONUS)
    nudity_skill_level = get_sim_nudity_skill_level(sim_identifier)
    amount /= nudity_skill_level
    nudity_skill_fatigue = get_sim_statistic_value(sim_identifier, SimCommodity.WW_NUDITY_SKILL_FATIGUE, add=True)
    amount *= nudity_skill_fatigue/100
    set_sim_statistic_value(sim_identifier, max(0, nudity_skill_fatigue - (amount*nudity_skill_level + extra_fatigue)), SimCommodity.WW_NUDITY_SKILL_FATIGUE)
    if has_current_lot_trait(LotTrait.WW_LOTTRAIT_NUDIST):
        sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
        if sim is not None and TurboWorldUtil.Lot.is_position_on_active_lot(TurboSimUtil.Location.get_position(sim)):
            amount *= 0.25
    change_sim_skill_percentage_value(sim_identifier, amount, get_nudity_nudity_skill_type(sim_identifier))
    set_sim_statistic_value(sim_identifier, get_sim_nudity_skill_level(sim_identifier), SimCommodity.WW_NUDITY_SKILL_LEVEL)

def get_sim_nudity_skill_level(sim_identifier):
    if has_sim_trait(sim_identifier, SimTrait.WW_EXHIBITIONIST):
        return get_sim_skill_level(sim_identifier, SimSkill.WW_EXHIBITIONISM)
    return get_sim_skill_level(sim_identifier, SimSkill.WW_NATURISM)

def get_sim_nudity_skill_progress(sim_identifier):
    if has_sim_trait(sim_identifier, SimTrait.WW_EXHIBITIONIST):
        return get_sim_full_skill_value(sim_identifier, SimSkill.WW_EXHIBITIONISM)
    return get_sim_full_skill_value(sim_identifier, SimSkill.WW_NATURISM)

def has_sim_reached_max_nudity_skill_level(sim_identifier):
    if has_sim_trait(sim_identifier, SimTrait.WW_EXHIBITIONIST):
        return has_sim_reached_max_skill_level(sim_identifier, SimSkill.WW_EXHIBITIONISM)
    return has_sim_reached_max_skill_level(sim_identifier, SimSkill.WW_NATURISM)

def is_sim_naturist(sim_identifier):
    return not has_sim_trait(sim_identifier, SimTrait.WW_EXHIBITIONIST)

def is_sim_exhibitionist(sim_identifier):
    return has_sim_trait(sim_identifier, SimTrait.WW_EXHIBITIONIST)

def convert_sim_nudity_skill(sim_identifier):
    if has_sim_skill(sim_identifier, SimSkill.WW_EXHIBITIONISM):
        remove_sim_skill(sim_identifier, SimSkill.WW_EXHIBITIONISM)
    if has_sim_skill(sim_identifier, SimSkill.WW_NATURISM):
        naturism_skill_level = get_sim_skill_level(sim_identifier, SimSkill.WW_NATURISM)
        naturism_skill_value = get_sim_skill_value(sim_identifier, SimSkill.WW_NATURISM)
        remove_sim_skill(sim_identifier, SimSkill.WW_NATURISM)
        set_sim_skill_level(sim_identifier, naturism_skill_level, SimSkill.WW_EXHIBITIONISM)
        set_sim_skill_value(sim_identifier, naturism_skill_value, SimSkill.WW_EXHIBITIONISM)
        remove_sim_buff(sim_identifier, SimBuff.WW_NUDITY_IS_NAKED_HIGH)
        TurboSimUtil.CAS.set_current_outfit(sim_identifier, TurboSimUtil.CAS.get_current_outfit(sim_identifier), dirty=True)

def apply_nudity_skill_influence(sim_identifier, amount, overall_limit=7.0):
    current_influence_score = sim_ev(sim_identifier).nudity_skill_influence_score
    if current_influence_score <= overall_limit:
        current_influence_score += amount
        sim_ev(sim_identifier).nudity_skill_influence_score = current_influence_score

def update_sim_nudity_skill_fatigue(sim_identifier):
    change_sim_statistic_value(sim_identifier, 0.1, SimCommodity.WW_NUDITY_SKILL_FATIGUE)

