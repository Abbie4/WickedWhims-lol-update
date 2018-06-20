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

def _get_motive_instance(sim_motive):
    return TurboResourceUtil.Services.get_instance(TurboResourceUtil.ResourceTypes.STATISTIC, int(sim_motive))


def has_sim_motive(sim_identifier, sim_motive):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    if not TurboSimUtil.Component.has_component(sim_info, TurboComponentUtil.ComponentType.STATISTIC):
        return False
    motive_instance = _get_motive_instance(sim_motive)
    if motive_instance is None:
        return False
    return TurboSimUtil.Statistic.has_tracked_statistic(sim_info, motive_instance)


def get_sim_motive_value(sim_identifier, sim_motive):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    if not TurboSimUtil.Component.has_component(sim_info, TurboComponentUtil.ComponentType.STATISTIC):
        return 0
    motive_instance = _get_motive_instance(sim_motive)
    if motive_instance is None:
        return 0
    return TurboSimUtil.Statistic.get_statistic_value(sim_info, motive_instance, add=False)


def set_sim_motive_value(sim_identifier, sim_motive, value, skip_disabled=False):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    if not TurboSimUtil.Component.has_component(sim_info, TurboComponentUtil.ComponentType.STATISTIC):
        return
    motive_instance = _get_motive_instance(sim_motive)
    if motive_instance is None:
        return
    if skip_disabled is True and TurboSimUtil.Motive.is_motive_disabled(sim_info, motive_instance, add=False):
        return
    TurboSimUtil.Statistic.set_statistic_value(sim_info, motive_instance, value, add=False)

