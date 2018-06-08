'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from turbolib.l18n_util import TurboL18NUtil
from turbolib.manager_util import TurboManagerUtil
from turbolib.resource_util import TurboResourceUtil
from turbolib.sim_util import TurboSimUtil

def _get_buff_instance(sim_buff):
    return TurboResourceUtil.Services.get_instance(TurboResourceUtil.ResourceTypes.BUFF, int(sim_buff))

def has_sim_buff(sim_identifier, sim_buff):
    buff_instance = _get_buff_instance(int(sim_buff))
    if buff_instance is None:
        return False
    return TurboSimUtil.Buff.has(sim_identifier, buff_instance)

def has_sim_buffs(sim_identifier, sim_buffs):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    for buff in TurboSimUtil.Buff.get_all_buffs_gen(sim_info):
        for sim_buff_id in sim_buffs:
            while TurboResourceUtil.Resource.get_guid64(buff) == int(sim_buff_id):
                return True
    return False

def add_sim_buff(sim_identifier, sim_buff, reason=None):
    buff_instance = _get_buff_instance(int(sim_buff))
    if buff_instance is None:
        return False
    if reason is not None:
        reason = TurboL18NUtil.get_localized_string(reason)
    return TurboSimUtil.Buff.add(sim_identifier, buff_instance, buff_reason=reason)

def remove_sim_buff(sim_identifier, sim_buff):
    buff_instance = _get_buff_instance(int(sim_buff))
    if buff_instance is None:
        return False
    return TurboSimUtil.Buff.remove(sim_identifier, buff_instance)

