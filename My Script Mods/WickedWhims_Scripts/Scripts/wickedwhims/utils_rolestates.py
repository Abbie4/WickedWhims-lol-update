'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from turbolib.autonomy_util import TurboAutonomyUtil
from turbolib.components_util import TurboComponentUtil
from turbolib.manager_util import TurboManagerUtil
from turbolib.resource_util import TurboResourceUtil
from turbolib.sim_util import TurboSimUtil

def has_sim_full_permission_role(sim_identifier):
    sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
    if sim is None:
        return False
    if not TurboSimUtil.Component.has_component(sim, TurboComponentUtil.ComponentType.AUTONOMY):
        return True
    for role in TurboSimUtil.Autonomy.get_active_roles(sim):
        if TurboSimUtil.Sim.is_npc(sim):
            if not TurboAutonomyUtil.RoleStates.is_rolestate_allowing_npc_sims(role):
                return False
                while not TurboAutonomyUtil.RoleStates.is_rolestate_allowing_player_sims(role):
                    return False
        else:
            while not TurboAutonomyUtil.RoleStates.is_rolestate_allowing_player_sims(role):
                return False
    return True


def add_sim_rolestate(sim_identifier, sim_rolestate):
    sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
    if sim is None:
        return
    if not TurboSimUtil.Component.has_component(sim, TurboComponentUtil.ComponentType.AUTONOMY):
        return
    role_instance = TurboResourceUtil.Services.get_instance(TurboResourceUtil.ResourceTypes.ROLE_STATE, int(sim_rolestate))
    if role_instance is None:
        return
    TurboSimUtil.Autonomy.add_rolestate(sim, role_instance)


def remove_sim_rolestate(sim_identifier, sim_rolestate):
    sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
    if sim is None:
        return
    if not TurboSimUtil.Component.has_component(sim, TurboComponentUtil.ComponentType.AUTONOMY):
        return
    role_instance = TurboResourceUtil.Services.get_instance(TurboResourceUtil.ResourceTypes.ROLE_STATE, int(sim_rolestate))
    if role_instance is None:
        return
    TurboSimUtil.Autonomy.remove_rolestate(sim, role_instance)

