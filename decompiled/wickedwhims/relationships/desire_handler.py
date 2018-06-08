'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from enums.buffs_enum import SimBuff
from enums.statistics_enum import SimCommodity
from enums.tags_enum import GameTag
from enums.traits_enum import SimTrait
from turbolib.events.interactions import register_interaction_outcome_event_method
from turbolib.interaction_util import TurboInteractionUtil
from turbolib.manager_util import TurboManagerUtil
from turbolib.sim_util import TurboSimUtil
from wickedwhims.nudity.outfit_utils import get_sim_outfit_level, OutfitLevel
from wickedwhims.relationships.relationship_settings import get_relationship_setting, RelationshipSetting
from wickedwhims.relationships.relationship_utils import get_sim_preferenced_genders
from wickedwhims.sex.pregnancy.menstrual_cycle_handler import is_sim_on_period
from wickedwhims.sex.settings.sex_settings import get_sex_setting, SexSetting
from wickedwhims.sxex_bridge.penis import set_sim_penis_state
from wickedwhims.utils_buffs import has_sim_buff, add_sim_buff, remove_sim_buff
from wickedwhims.utils_statistics import change_sim_statistic_value, get_sim_statistic_value, set_sim_statistic_value
from wickedwhims.utils_traits import has_sim_trait

@register_interaction_outcome_event_method(unique_id='WickedWhims')
def _wickedwhims_on_sims_talking_desire_interactions_outcome(interaction_instance, outcome_result):
    sim_info = TurboManagerUtil.Sim.get_sim_info(TurboInteractionUtil.get_interaction_sim(interaction_instance))
    target_sim_info = TurboManagerUtil.Sim.get_sim_info(TurboInteractionUtil.get_interaction_target(interaction_instance))
    if target_sim_info is None:
        return
    if TurboSimUtil.Age.is_younger_than(sim_info, TurboSimUtil.Age.CHILD) or TurboSimUtil.Age.is_younger_than(target_sim_info, TurboSimUtil.Age.CHILD):
        return
    if not get_sex_setting(SexSetting.TEENS_SEX_STATE, variable_type=bool) and (TurboSimUtil.Age.get_age(sim_info) == TurboSimUtil.Age.TEEN or TurboSimUtil.Age.get_age(sim_info) == TurboSimUtil.Age.CHILD or TurboSimUtil.Age.get_age(target_sim_info) == TurboSimUtil.Age.TEEN or TurboSimUtil.Age.get_age(target_sim_info) == TurboSimUtil.Age.CHILD):
        return
    if (TurboSimUtil.Age.get_age(sim_info) == TurboSimUtil.Age.TEEN or TurboSimUtil.Age.get_age(sim_info) == TurboSimUtil.Age.CHILD) and TurboSimUtil.Age.is_older_than(target_sim_info, TurboSimUtil.Age.CHILD):
        return
    if get_relationship_setting(RelationshipSetting.ROMANCE_AGE_RESTRICTION_STATE, variable_type=bool) or (TurboSimUtil.Age.get_age(target_sim_info) == TurboSimUtil.Age.TEEN or TurboSimUtil.Age.get_age(target_sim_info) == TurboSimUtil.Age.CHILD) and TurboSimUtil.Age.is_older_than(sim_info, TurboSimUtil.Age.CHILD):
        return
    if has_sim_trait(sim_info, SimTrait.WW_SEXUALLY_ABSTINENT):
        set_sim_desire_level(sim_info, 0)
        return
    if int(GameTag.SOCIAL_FLIRTY) in TurboInteractionUtil.get_affordance_tags(interaction_instance):
        if outcome_result is True:
            target_desire_amount = 10
            sim_desire_amount = 5
            if has_sim_trait(sim_info, SimTrait.ALLURING):
                target_desire_amount += 3
            if has_sim_trait(target_sim_info, SimTrait.ROMANTIC):
                target_desire_amount += 3
            if has_sim_trait(target_sim_info, SimTrait.OCCULTVAMPIRE) and is_sim_on_period(sim_info):
                target_desire_amount += 3
            if has_sim_trait(target_sim_info, SimTrait.UNFLIRTY):
                target_desire_amount -= 5
            sim_outfit_level = get_sim_outfit_level(sim_info)
            if sim_outfit_level == OutfitLevel.NUDE or sim_outfit_level == OutfitLevel.BATHING:
                target_desire_amount += 3
            change_sim_desire_level(target_sim_info, target_desire_amount)
            change_sim_desire_level(sim_info, sim_desire_amount)
        else:
            change_sim_desire_level(target_sim_info, -7.5)
            change_sim_desire_level(sim_info, -3.5)
    elif int(GameTag.INTERACTION_FRIENDLY) in TurboInteractionUtil.get_affordance_tags(interaction_instance):
        if outcome_result is True:
            if get_sim_desire_level(sim_info) < 10 and TurboSimUtil.Gender.get_gender(target_sim_info) in get_sim_preferenced_genders(sim_info):
                nudity_multiplier = 0.0
                target_sim_outfit_level = get_sim_outfit_level(target_sim_info)
                if target_sim_outfit_level == OutfitLevel.NUDE or target_sim_outfit_level == OutfitLevel.BATHING:
                    nudity_multiplier += 2.0
                if has_sim_trait(target_sim_info, SimTrait.INCREDIBLYFRIENDLY):
                    change_sim_desire_level(sim_info, 2.5*nudity_multiplier)
                else:
                    change_sim_desire_level(sim_info, 1*nudity_multiplier)
            if get_sim_desire_level(target_sim_info) < 5 and TurboSimUtil.Gender.get_gender(sim_info) in get_sim_preferenced_genders(target_sim_info):
                if has_sim_trait(sim_info, SimTrait.INCREDIBLYFRIENDLY):
                    change_sim_desire_level(target_sim_info, 2.5)
                else:
                    change_sim_desire_level(target_sim_info, 1)
    elif int(GameTag.INTERACTION_MEAN) in TurboInteractionUtil.get_affordance_tags(interaction_instance) and outcome_result is True:
        if not has_sim_trait(target_sim_info, SimTrait.EVIL):
            change_sim_desire_level(target_sim_info, -9)
        if not has_sim_trait(sim_info, SimTrait.EVIL):
            change_sim_desire_level(sim_info, -5)

def update_sims_high_desire(sim_identifier):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    if get_sim_desire_level(sim_info) > 60:
        set_sim_penis_state(sim_info, True, 8, set_if_nude=True)

def get_sim_desire_level(sim_identifier):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    return get_sim_statistic_value(sim_info, SimCommodity.WW_SEX_MASTER_DESIRE)

def set_sim_desire_level(sim_identifier, amount):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    if TurboSimUtil.Age.is_younger_than(sim_info, TurboSimUtil.Age.CHILD):
        return
    set_sim_statistic_value(sim_info, amount, SimCommodity.WW_SEX_MASTER_DESIRE)
    _update_sim_desire_effects(sim_info)

def change_sim_desire_level(sim_identifier, amount):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    if TurboSimUtil.Age.is_younger_than(sim_info, TurboSimUtil.Age.CHILD):
        return
    change_sim_statistic_value(sim_info, amount, SimCommodity.WW_SEX_MASTER_DESIRE)
    _update_sim_desire_effects(sim_info)

def _update_sim_desire_effects(sim_identifier):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    master_desire_level = get_sim_statistic_value(sim_info, SimCommodity.WW_SEX_MASTER_DESIRE)
    if master_desire_level >= 85:
        if not has_sim_buff(sim_info, SimBuff.WW_DESIRE_NEGATIVE):
            remove_sim_buff(sim_info, SimBuff.WW_DESIRE_POSITIVE)
            add_sim_buff(sim_info, SimBuff.WW_DESIRE_NEGATIVE, reason=2404119453)
    elif not (master_desire_level >= 50 and has_sim_buff(sim_info, SimBuff.WW_DESIRE_POSITIVE)):
        add_sim_buff(sim_info, SimBuff.WW_DESIRE_POSITIVE, reason=2404119453)

