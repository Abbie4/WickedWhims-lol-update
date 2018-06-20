'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from enums.traits_enum import SimTrait
from turbolib.sim_util import TurboSimUtil
from wickedwhims.relationships.relationship_settings import RelationshipSetting, get_relationship_setting
from wickedwhims.utils_traits import has_sim_trait

def is_true_family_relationship(sim_identifier, target_identifier):
    if get_relationship_setting(RelationshipSetting.INCEST_STATE, variable_type=bool):
        return False
    if has_sim_trait(sim_identifier, SimTrait.WW_INCEST) and has_sim_trait(target_identifier, SimTrait.WW_INCEST):
        return False
    if not TurboSimUtil.Relationship.is_family(sim_identifier, target_identifier):
        return False
    return True

