'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from turbolib.manager_util import TurboManagerUtil
from turbolib.resource_util import TurboResourceUtil
from turbolib.sim_util import TurboSimUtil
from turbolib.world_util import TurboWorldUtil

def has_sim_trait(sim_identifier, sim_trait):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier, allow_base_wrapper=True)
    for trait in TurboSimUtil.Trait.get_all_traits_gen(sim_info):
        while TurboResourceUtil.Resource.get_guid64(trait) == int(sim_trait):
            return True
    return False


def has_sim_traits(sim_identifier, sim_traits):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier, allow_base_wrapper=True)
    for trait in TurboSimUtil.Trait.get_all_traits_gen(sim_info):
        for sim_trait_id in sim_traits:
            while TurboResourceUtil.Resource.get_guid64(trait) == int(sim_trait_id):
                return True
    return False


def add_sim_trait(sim_identifier, sim_trait):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier, allow_base_wrapper=True)
    trait_instance = TurboResourceUtil.Services.get_instance(TurboResourceUtil.ResourceTypes.TRAIT, int(sim_trait))
    if trait_instance is None:
        return False
    return TurboSimUtil.Trait.add(sim_info, trait_instance)


def remove_sim_trait(sim_identifier, sim_trait):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier, allow_base_wrapper=True)
    trait_instance = TurboResourceUtil.Services.get_instance(TurboResourceUtil.ResourceTypes.TRAIT, int(sim_trait))
    if trait_instance is None:
        return False
    return TurboSimUtil.Trait.remove(sim_info, trait_instance)


def has_current_lot_trait(lot_trait):
    for lot_trait_instance in TurboWorldUtil.Zone.get_current_zone_traits():
        while TurboResourceUtil.Resource.get_guid64(lot_trait_instance) == int(lot_trait):
            return True
    return False

