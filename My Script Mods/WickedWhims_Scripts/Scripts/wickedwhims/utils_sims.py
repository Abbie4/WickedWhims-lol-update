'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from enums.buffs_enum import SimBuff
from enums.moods_enum import SimMood
from enums.situations_enum import SimSituation
from turbolib.manager_util import TurboManagerUtil
from turbolib.resource_util import TurboResourceUtil
from turbolib.sim_util import TurboSimUtil
from wickedwhims.utils_buffs import has_sim_buff
from wickedwhims.utils_situations import has_sim_situation

def is_sim_available(sim_identifier):
    if has_sim_mood(sim_identifier, SimMood.SLEEPING):
        return False
    if has_sim_buff(sim_identifier, SimBuff.SIM_ISDYING):
        return False
    sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
    if not TurboSimUtil.Location.is_visible(sim):
        return False
    if has_sim_situation(sim, SimSituation.LEAVE) or TurboSimUtil.Spawner.is_leaving(sim):
        return False
    return True


def has_sim_mood(sim_identifier, sim_mood):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    return TurboResourceUtil.Resource.get_guid64(TurboSimUtil.Mood.get_mood(sim_info)) == int(sim_mood)

