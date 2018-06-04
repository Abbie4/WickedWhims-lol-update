'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from enums.buffs_enum import SimBuff
from enums.motives_enum import SimMotive
from turbolib.manager_util import TurboManagerUtil
from turbolib.resource_util import TurboResourceUtil
from turbolib.sim_util import TurboSimUtil
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.sex.settings.sex_settings import get_sex_setting, SexSetting
from wickedwhims.utils_buffs import has_sim_buff
from wickedwhims.utils_motives import get_sim_motive_value, set_sim_motive_value

def get_sim_sex_state_snapshot(sim_identifier):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    return {'mood': TurboResourceUtil.Resource.get_guid64(TurboSimUtil.Mood.get_mood(sim_info)), 'motive_fun': get_sim_motive_value(sim_info, SimMotive.FUN), 'motive_social': get_sim_motive_value(sim_info, SimMotive.SOCIAL), 'motive_hygiene': get_sim_motive_value(sim_info, SimMotive.HYGIENE), 'motive_bladder': get_sim_motive_value(sim_info, SimMotive.BLADDER), 'motive_energy': get_sim_motive_value(sim_info, SimMotive.ENERGY), 'motive_hunger': get_sim_motive_value(sim_info, SimMotive.HUNGER), 'motive_vampire_power': get_sim_motive_value(sim_info, SimMotive.VAMPIRE_POWER), 'motive_vampire_thirst': get_sim_motive_value(sim_info, SimMotive.VAMPIRE_THIRST), 'motive_plantsim_water': get_sim_motive_value(sim_info, SimMotive.PLANTSIM_WATER), 'has_positive_desire_buff': has_sim_buff(sim_info, SimBuff.WW_DESIRE_POSITIVE)}

def modify_sim_sex_snapshot_motive(sim_info, sim_motive, snapshot_state, modify_value, min_value=None, max_value=None):
    sim_state_snapshot = sim_ev(sim_info).sim_sex_state_snapshot
    if snapshot_state not in sim_state_snapshot:
        return
    if not get_sex_setting(SexSetting.NEEDS_DECAY_STATE, variable_type=bool):
        set_sim_motive_value(sim_info, sim_motive, sim_state_snapshot[snapshot_state], skip_disabled=True)
    else:
        motive_value = get_sim_motive_value(sim_info, sim_motive) + modify_value
        if min_value is not None and motive_value < min_value:
            motive_value = min_value
        if max_value is not None and motive_value > max_value:
            motive_value = max_value
        set_sim_motive_value(sim_info, sim_motive, motive_value, skip_disabled=True)
        sim_state_snapshot[snapshot_state] = motive_value

