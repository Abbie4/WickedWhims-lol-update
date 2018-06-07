'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''from turbolib.components_util import TurboComponentUtilfrom turbolib.manager_util import TurboManagerUtilfrom turbolib.sim_util import TurboSimUtil
def is_sim_allowed_for_autonomy(sim_identifier):
    sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
    if not TurboSimUtil.Component.has_component(sim, TurboComponentUtil.ComponentType.AUTONOMY):
        return False
    if not TurboSimUtil.Autonomy.is_in_full_autonomy(sim):
        return False
    if TurboSimUtil.Spawner.is_leaving(sim):
        return False
    return True
