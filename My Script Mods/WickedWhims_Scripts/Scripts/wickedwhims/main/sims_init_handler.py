'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''from turbolib.events.core import register_zone_load_event_method, is_game_loadingfrom turbolib.events.sims import register_sim_info_instance_init_event_methodfrom turbolib.manager_util import TurboManagerUtilfrom turbolib.sim_util import TurboSimUtilfrom wickedwhims.main.sim_ev_handler import sim_evfrom wickedwhims.nudity.sims_init_handler import init_nudity_sim_ev_datafrom wickedwhims.sex.sims_init_handler import init_sex_sim_ev_datafrom wickedwhims.sxex_bridge.nudity import setup_sim_nude_outfit
@register_sim_info_instance_init_event_method(unique_id='WickedWhims', priority=0, early=True)
def _wickedwhims_init_ev_variables(sim_info):
    if sim_ev(sim_info).is_ready():
        return
    sim_ev(sim_info).unready()
    init_main_sim_ev_data(sim_info)
    init_nudity_sim_ev_data(sim_info)
    init_sex_sim_ev_data(sim_info)
    sim_ev(sim_info).ready()

@register_sim_info_instance_init_event_method(unique_id='WickedWhims', priority=1, late=True)
def _wickedwhims_update_sim_data_on_new_sim(sim_info):
    if is_game_loading():
        return
    if TurboSimUtil.Species.is_human(sim_info):
        _update_sim_data(sim_info)

@register_zone_load_event_method(unique_id='WickedWhims', priority=50, late=True)
def _wickedwhims_update_sims_data_on_load():
    for sim_info in TurboManagerUtil.Sim.get_all_sim_info_gen(humans=True, pets=False):
        _update_sim_data(sim_info)

def _update_sim_data(sim_info):
    current_outfit = TurboSimUtil.CAS.get_current_outfit(sim_info)
    setup_sim_nude_outfit(sim_info)
    TurboSimUtil.CAS.set_current_outfit(sim_info, current_outfit, dirty=True)

def init_main_sim_ev_data(sim_identifier):
    sim_ev(sim_identifier).outfit_parts_cache = dict()
    sim_ev(sim_identifier).appearance_modifiers_parts_cache = dict()
    sim_ev(sim_identifier).body_state_cache = dict()
    sim_ev(sim_identifier).additional_body_state_cache = dict()
    sim_ev(sim_identifier).special_statistics = dict()
