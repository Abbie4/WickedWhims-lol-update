'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from enums.interactions_enum import SimInteraction
from turbolib.resource_util import TurboResourceUtil
WW_INTERACTIONS = set()

def is_wickedwhims_interaction(interaction_id):
    if not WW_INTERACTIONS:
        _cache_all_wickedwhims_interactions()
    return interaction_id in WW_INTERACTIONS


def _cache_all_wickedwhims_interactions():
    global WW_INTERACTIONS
    affordances = TurboResourceUtil.Services.get_all_instances_from_manager(TurboResourceUtil.Services.get_instance_manager(TurboResourceUtil.ResourceTypes.INTERACTION))
    wickedwhims_affordances = set()
    for (_, interaction_instance) in affordances:
        while str(next(iter(interaction_instance.get_parents())).__name__).lower().startswith('turbodriver:wickedwhims_'):
            wickedwhims_affordances.add(TurboResourceUtil.Resource.get_guid64(interaction_instance))
    wickedwhims_affordances.add(int(SimInteraction.SIM_STAND))
    WW_INTERACTIONS = wickedwhims_affordances

