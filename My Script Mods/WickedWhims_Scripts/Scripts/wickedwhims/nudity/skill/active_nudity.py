'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from enums.relationship_enum import SimRelationshipBit, RelationshipTrackType
from turbolib.manager_util import TurboManagerUtil
from turbolib.math_util import TurboMathUtil
from turbolib.sim_util import TurboSimUtil
from wickedwhims.nudity.nudity_settings import NuditySetting, get_nudity_setting
from wickedwhims.nudity.outfit_utils import get_sim_outfit_level, OutfitLevel
from wickedwhims.nudity.skill.skills_utils import increase_sim_nudity_skill, get_nudity_skill_points_modifier, NuditySkillIncreaseReason, get_sim_nudity_skill_level, apply_nudity_skill_influence, is_sim_naturist
from wickedwhims.sxex_bridge.relationships import is_true_family_relationship
from wickedwhims.sxex_bridge.sex import is_sim_in_sex, is_sim_going_to_sex
from wickedwhims.utils_relations import has_relationship_bit_with_sim, get_relationship_with_sim
from wickedwhims.utils_sims import is_sim_available

def update_sim_nudity_skill_on_active_nudity(sim_identifier):
    if TurboSimUtil.Age.is_younger_than(sim_identifier, TurboSimUtil.Age.TEEN):
        return
    if not get_nudity_setting(NuditySetting.TEENS_NUDITY_STATE, variable_type=bool) and TurboSimUtil.Age.get_age(sim_identifier) == TurboSimUtil.Age.TEEN:
        return
    if is_sim_in_sex(sim_identifier) or is_sim_going_to_sex(sim_identifier):
        return
    if not is_sim_available(sim_identifier):
        return
    sim_outfit_level = get_sim_outfit_level(sim_identifier)
    if sim_outfit_level == OutfitLevel.OUTFIT:
        return
    sims_around_value = _get_sims_around_value(sim_identifier, max_sims=6)
    if sim_outfit_level == OutfitLevel.NUDE:
        increase_sim_nudity_skill(sim_identifier, sims_around_value*get_nudity_skill_points_modifier(NuditySkillIncreaseReason.BEING_IN_NAKED_OUTFIT), extra_fatigue=0.05, reason=NuditySkillIncreaseReason.BEING_IN_NAKED_OUTFIT)
    elif sim_outfit_level == OutfitLevel.BATHING:
        sim_nudity_skill_level = get_sim_nudity_skill_level(sim_identifier)
        increase_sim_nudity_skill(sim_identifier, sims_around_value*(get_nudity_skill_points_modifier(NuditySkillIncreaseReason.BEING_IN_BATHING_OUTFIT)/sim_nudity_skill_level), extra_fatigue=0.15, reason=NuditySkillIncreaseReason.BEING_IN_BATHING_OUTFIT)
    elif sim_outfit_level == OutfitLevel.REVEALING or sim_outfit_level == OutfitLevel.UNDERWEAR:
        sim_nudity_skill_level = get_sim_nudity_skill_level(sim_identifier)
        increase_sim_nudity_skill(sim_identifier, sims_around_value*(get_nudity_skill_points_modifier(NuditySkillIncreaseReason.BEING_IN_REVEALING_OUTFIT)/(sim_nudity_skill_level*sim_nudity_skill_level)), extra_fatigue=0.15, reason=NuditySkillIncreaseReason.BEING_IN_REVEALING_OUTFIT)


def update_sim_nudity_skill_on_seeing_nudity(sim, target):
    skill_points = _get_sim_nudity_value(target, sim)*get_nudity_skill_points_modifier(NuditySkillIncreaseReason.SEEING_NUDITY)
    if TurboSimUtil.Age.get_age(sim) == TurboSimUtil.Age.CHILD and is_sim_naturist(target):
        apply_nudity_skill_influence(sim, skill_points, overall_limit=200.0)
        return
    increase_sim_nudity_skill(sim, skill_points, extra_fatigue=0.05, reason=NuditySkillIncreaseReason.SEEING_NUDITY)


def _get_sims_around_value(sim_identifier, max_sims=6):
    sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
    max_sims = max_sims if max_sims % 2 == 0 else max_sims + 1
    points_collection = list()
    line_of_sight = TurboMathUtil.LineOfSight.create(TurboSimUtil.Location.get_routing_surface(sim), TurboSimUtil.Location.get_position(sim), 8.0)
    for target in TurboManagerUtil.Sim.get_all_sim_instance_gen(humans=True, pets=False):
        if sim is target:
            pass
        if TurboSimUtil.Age.is_younger_than(target, TurboSimUtil.Age.BABY, or_equal=True):
            pass
        if not is_sim_available(target):
            pass
        if not TurboMathUtil.LineOfSight.test(line_of_sight, TurboSimUtil.Location.get_position(target)):
            pass
        points_collection.append(_get_sim_nudity_value(sim, target))
    points_collection = sorted(points_collection, reverse=True)
    high_value = sum(points_collection[:int(max_sims/2)])
    low_value = sum(points_collection[int(-(max_sims/2)):])
    return max(0, (high_value + low_value)/2)


def _get_sim_nudity_value(sim_identifier, target_sim_identifier):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    target_sim_info = TurboManagerUtil.Sim.get_sim_info(target_sim_identifier)
    score_collection = list()
    if TurboSimUtil.Age.get_age(target_sim_info) == TurboSimUtil.Age.TODDLER:
        base_modifier = -0.5
    elif TurboSimUtil.Age.get_age(target_sim_info) == TurboSimUtil.Age.CHILD:
        base_modifier = -1.0
    else:
        sim_outfit_level = get_sim_outfit_level(sim_info)
        target_outfit_level = get_sim_outfit_level(target_sim_info)
        if TurboSimUtil.Age.is_older_than(target_sim_info, TurboSimUtil.Age.get_age(sim_identifier), or_equal=True):
            base_modifier = 1.0
        else:
            base_modifier = 0.8
        if target_outfit_level >= sim_outfit_level:
            base_modifier = -base_modifier
    if TurboSimUtil.Household.is_same_household(sim_info, target_sim_info):
        if is_sim_naturist(sim_info):
            score_collection.append(-0.01*base_modifier)
        else:
            score_collection.append(-0.05*base_modifier)
    if is_true_family_relationship(sim_info, target_sim_info):
        if is_sim_naturist(sim_info):
            score_collection.append(-0.05*base_modifier)
        else:
            score_collection.append(-0.1*base_modifier)
    if has_relationship_bit_with_sim(sim_info, target_sim_info, SimRelationshipBit.WW_JUST_HAD_SEX):
        score_collection.append(-0.15*base_modifier)
    if has_relationship_bit_with_sim(sim_info, target_sim_info, SimRelationshipBit.ROMANTIC_HAVEDONEWOOHOO_RECENTLY):
        score_collection.append(-0.1*base_modifier)
    elif has_relationship_bit_with_sim(sim_info, target_sim_info, SimRelationshipBit.ROMANTIC_HAVEDONEWOOHOO):
        score_collection.append(-0.02*base_modifier)
    if has_relationship_bit_with_sim(sim_info, target_sim_info, SimRelationshipBit.ROMANTIC_ENGAGED) or has_relationship_bit_with_sim(sim_info, target_sim_info, SimRelationshipBit.ROMANTIC_MARRIED) or has_relationship_bit_with_sim(sim_info, target_sim_info, SimRelationshipBit.ROMANTIC_SIGNIFICANT_OTHER):
        score_collection.append(-0.15*base_modifier)
    current_romance_rel_amount = (get_relationship_with_sim(sim_info, target_sim_info, RelationshipTrackType.ROMANCE) + 100)/200*100
    score_collection.append(max(0, 1.0*((100 - current_romance_rel_amount)/100))*base_modifier)
    if has_relationship_bit_with_sim(sim_info, target_sim_info, SimRelationshipBit.FRIENDSHIP_BFF) or has_relationship_bit_with_sim(sim_info, target_sim_info, SimRelationshipBit.FRIENDSHIP_BFF_EVIL) or has_relationship_bit_with_sim(sim_info, target_sim_info, SimRelationshipBit.FRIENDSHIP_BFF_BROMANTICPARTNER):
        score_collection.append(-0.15*base_modifier)
    current_friendship_rel_amount = (get_relationship_with_sim(sim_info, target_sim_info, RelationshipTrackType.FRIENDSHIP) + 100)/200*100
    score_collection.append(max(0, 1.0*((100 - current_friendship_rel_amount)/100))*base_modifier)
    return sum(score_collection)/len(score_collection)

