'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''from turbolib.manager_util import TurboManagerUtilfrom turbolib.resource_util import TurboResourceUtilfrom turbolib.sim_util import TurboSimUtil
def change_relationship_with_sim(sim_identifier, target_identifier, rel_track_type, score, create=False):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    target_sim_info = TurboManagerUtil.Sim.get_sim_info(target_identifier)
    relationship_track_instance = TurboResourceUtil.Services.get_instance(TurboResourceUtil.ResourceTypes.STATISTIC, int(rel_track_type))
    if relationship_track_instance is None:
        return
    if create is True:
        TurboSimUtil.Relationship.create_relationship(sim_info, target_sim_info, relationship_track_instance)
    TurboSimUtil.Relationship.change_relationship_score(sim_info, target_sim_info, relationship_track_instance, score)

def get_relationship_with_sim(sim_identifier, target_identifier, rel_track_type, create=False):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    target_sim_info = TurboManagerUtil.Sim.get_sim_info(target_identifier)
    relationship_track_instance = TurboResourceUtil.Services.get_instance(TurboResourceUtil.ResourceTypes.STATISTIC, int(rel_track_type))
    if relationship_track_instance is None:
        return 0.0
    if create is True:
        TurboSimUtil.Relationship.create_relationship(sim_info, target_sim_info, relationship_track_instance)
    return TurboSimUtil.Relationship.get_relationship_score(sim_info, target_sim_info, relationship_track_instance)

def add_relationsip_bit_with_sim(sim_identifier, target_identifier, rel_bit_type, force_add=False):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    target_sim_info = TurboManagerUtil.Sim.get_sim_info(target_identifier)
    relationship_bit_instance = TurboResourceUtil.Services.get_instance(TurboResourceUtil.ResourceTypes.RELATIONSHIP_BIT, int(rel_bit_type))
    if relationship_bit_instance is None:
        return
    TurboSimUtil.Relationship.add_relationship_bit(sim_info, target_sim_info, relationship_bit_instance, force_add=force_add)

def remove_relationsip_bit_with_sim(sim_identifier, target_identifier, rel_bit_type):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    target_sim_info = TurboManagerUtil.Sim.get_sim_info(target_identifier)
    relationship_bit_instance = TurboResourceUtil.Services.get_instance(TurboResourceUtil.ResourceTypes.RELATIONSHIP_BIT, int(rel_bit_type))
    if relationship_bit_instance is None:
        return
    TurboSimUtil.Relationship.remove_relationship_bit(sim_info, target_sim_info, relationship_bit_instance)

def has_relationship_bit_with_sim(sim_identifier, target_identifier, rel_bit_type):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    target_sim_info = TurboManagerUtil.Sim.get_sim_info(target_identifier)
    relationship_bit_instance = TurboResourceUtil.Services.get_instance(TurboResourceUtil.ResourceTypes.RELATIONSHIP_BIT, int(rel_bit_type))
    if relationship_bit_instance is None:
        return False
    return TurboSimUtil.Relationship.has_relationship_bit(sim_info, target_sim_info, relationship_bit_instance)

def get_sim_ids_with_relationsip_bit(sim_identifier, rel_bit_type):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    relationship_bit_instance = TurboResourceUtil.Services.get_instance(TurboResourceUtil.ResourceTypes.RELATIONSHIP_BIT, int(rel_bit_type))
    if relationship_bit_instance is None:
        return ()
    return TurboSimUtil.Relationship.get_target_ids_with_relationship_bit(sim_info, relationship_bit_instance)
