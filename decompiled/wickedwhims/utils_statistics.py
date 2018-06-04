'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from turbolib.manager_util import TurboManagerUtil
from turbolib.resource_util import TurboResourceUtil
from turbolib.sim_util import TurboSimUtil

def _get_statistic_instance(sim_statistic):
    return TurboResourceUtil.Services.get_instance(TurboResourceUtil.ResourceTypes.STATISTIC, int(sim_statistic))

def get_sim_statistic_value(sim_identifier, sim_statistic, add=False):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    statistic_instance = _get_statistic_instance(sim_statistic)
    if statistic_instance is None:
        return 0
    return TurboSimUtil.Statistic.get_statistic_value(sim_info, statistic_instance, add=add)

def set_sim_statistic_value(sim_identifier, value, sim_statistic):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    statistic_instance = _get_statistic_instance(sim_statistic)
    if statistic_instance is None:
        return
    TurboSimUtil.Statistic.set_statistic_value(sim_info, statistic_instance, value)

def change_sim_statistic_value(sim_identifier, value, sim_statistic):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    statistic_instance = _get_statistic_instance(sim_statistic)
    if statistic_instance is None:
        return
    TurboSimUtil.Statistic.change_tracker_statistic(sim_info, statistic_instance, value)

