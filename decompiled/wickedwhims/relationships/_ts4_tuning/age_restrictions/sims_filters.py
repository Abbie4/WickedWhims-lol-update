'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from turbolib.resource_util import TurboResourceUtil
from turbolib.sim_util import TurboSimUtil
from turbolib.tunable_util import TurboTunableUtil
ROMANCE_FILTER_LIST = (76607, 76608, 77312, 29337, 104863, 153207)

def unlock_sims_filters_for_teens():
    sim_filter_manager = TurboResourceUtil.Services.get_instance_manager(TurboResourceUtil.ResourceTypes.SIM_FILTER)
    for sim_filter_id in ROMANCE_FILTER_LIST:
        sim_filter_instance = TurboResourceUtil.Services.get_instance_from_manager(sim_filter_manager, sim_filter_id)
        if sim_filter_instance is None:
            pass
        new_filter_terms_list = list()
        for filter_term in sim_filter_instance._filter_terms:
            if TurboTunableUtil.Filters.AgeFilterTerm.is_age_filter_term(filter_term):
                filter_term = TurboTunableUtil.Filters.AgeFilterTerm.get_age_filter_term(min_value=TurboSimUtil.Age.CHILD, max_value=TurboSimUtil.Age.ELDER, copy_age_filter_term=filter_term)
            new_filter_terms_list.append(filter_term)
        sim_filter_instance._filter_terms = tuple(new_filter_terms_list)

