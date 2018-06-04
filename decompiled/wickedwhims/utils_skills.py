'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from turbolib.components_util import TurboComponentUtil
from turbolib.manager_util import TurboManagerUtil
from turbolib.resource_util import TurboResourceUtil
from turbolib.sim_util import TurboSimUtil

def _get_skill_instance(sim_skill):
    return TurboResourceUtil.Services.get_instance(TurboResourceUtil.ResourceTypes.STATISTIC, int(sim_skill))

def has_sim_skill(sim_identifier, sim_skill):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    if not TurboSimUtil.Component.has_component(sim_info, TurboComponentUtil.ComponentType.STATISTIC):
        return False
    skill_instance = _get_skill_instance(sim_skill)
    if skill_instance is None:
        return False
    return TurboSimUtil.Skill.has_skill(sim_info, skill_instance)

def has_sim_reached_max_skill_level(sim_identifier, sim_skill):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    if not TurboSimUtil.Component.has_component(sim_info, TurboComponentUtil.ComponentType.STATISTIC):
        return False
    skill_instance = _get_skill_instance(sim_skill)
    if skill_instance is None:
        return False
    return TurboSimUtil.Skill.has_reached_max_level(sim_info, skill_instance)

def remove_sim_skill(sim_identifier, sim_skill):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    if not TurboSimUtil.Component.has_component(sim_info, TurboComponentUtil.ComponentType.STATISTIC):
        return False
    skill_instance = _get_skill_instance(sim_skill)
    if skill_instance is None:
        return False
    return TurboSimUtil.Skill.remove_skill(sim_info, skill_instance)

def get_sim_full_skill_value(sim_identifier, sim_skill):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    if not TurboSimUtil.Component.has_component(sim_info, TurboComponentUtil.ComponentType.STATISTIC):
        return False
    skill_instance = _get_skill_instance(sim_skill)
    if skill_instance is None:
        return False
    current_skill_level = TurboSimUtil.Skill.get_skill_level(sim_info, skill_instance)
    current_skill_value = TurboSimUtil.Skill.get_skill_value(sim_info, skill_instance)
    amount_for_current_level = TurboSimUtil.Skill.get_value_for_level(sim_info, skill_instance, current_skill_level)
    amount_for_next_level = TurboSimUtil.Skill.get_value_for_next_level(sim_info, skill_instance)
    if amount_for_current_level <= 0 or amount_for_next_level <= 0:
        return 0
    return (current_skill_value - amount_for_current_level)/amount_for_next_level

def get_sim_skill_value(sim_identifier, sim_skill):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    if not TurboSimUtil.Component.has_component(sim_info, TurboComponentUtil.ComponentType.STATISTIC):
        return 0
    skill_instance = _get_skill_instance(sim_skill)
    if skill_instance is None:
        return 0
    return TurboSimUtil.Skill.get_skill_value(sim_info, skill_instance)

def set_sim_skill_value(sim_identifier, value, sim_skill):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    if not TurboSimUtil.Component.has_component(sim_info, TurboComponentUtil.ComponentType.STATISTIC):
        return
    skill_instance = _get_skill_instance(sim_skill)
    if skill_instance is None:
        return
    TurboSimUtil.Skill.set_skill_value(sim_info, skill_instance, value)

def get_sim_skill_level(sim_identifier, sim_skill):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    if not TurboSimUtil.Component.has_component(sim_info, TurboComponentUtil.ComponentType.STATISTIC):
        return 1
    skill_instance = _get_skill_instance(sim_skill)
    if skill_instance is None:
        return 1
    return max(1, TurboSimUtil.Skill.get_skill_level(sim_info, skill_instance))

def set_sim_skill_level(sim_identifier, value, sim_skill):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    if not TurboSimUtil.Component.has_component(sim_info, TurboComponentUtil.ComponentType.STATISTIC):
        return
    skill_instance = _get_skill_instance(sim_skill)
    if skill_instance is None:
        return
    TurboSimUtil.Skill.set_skill_level(sim_info, skill_instance, value)

def change_sim_skill_percentage_value(sim_identifier, percent_value, sim_skill):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    if not TurboSimUtil.Component.has_component(sim_info, TurboComponentUtil.ComponentType.STATISTIC):
        return False
    skill_instance = _get_skill_instance(sim_skill)
    if skill_instance is None:
        return False
    if TurboSimUtil.Skill.has_reached_max_level(sim_info, skill_instance):
        return False
    amount_for_next_level = TurboSimUtil.Skill.get_value_for_next_level(sim_info, skill_instance)
    current_skill_value = TurboSimUtil.Skill.get_skill_value(sim_info, skill_instance)
    value = amount_for_next_level/100*percent_value
    TurboSimUtil.Skill.set_skill_value(sim_info, skill_instance, current_skill_value + value)
    return True

