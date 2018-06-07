'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''from turbolib.resource_util import TurboResourceUtilfrom turbolib.sim_util import TurboSimUtil
def _get_static_commodity_instance(sim_commodity):
    return TurboResourceUtil.Services.get_instance(TurboResourceUtil.ResourceTypes.STATIC_COMMODITY, int(sim_commodity))

def add_sim_static_commodity(sim_identifier, sim_commodity):
    commodity_instance = _get_static_commodity_instance(sim_commodity)
    if commodity_instance is None:
        return
    TurboSimUtil.Statistic.add_tracked_statistic(sim_identifier, commodity_instance, None)

def remove_sim_static_commodity(sim_identifier, sim_commodity):
    commodity_instance = _get_static_commodity_instance(sim_commodity)
    if commodity_instance is None:
        return
    TurboSimUtil.Statistic.remove_tracked_statistic(sim_identifier, commodity_instance)
