'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''from turbolib.events.core import register_zone_load_event_method, register_zone_save_eventfrom turbolib.manager_util import TurboManagerUtilfrom turbolib.resource_util import TurboResourceUtilfrom wickedwhims.main.cas_config_handler import load_cas_parts_from_filefrom wickedwhims.main.sim_ev_handler import sim_ev, reset_sims_ev_datafrom wickedwhims.nudity.nudity_settings import apply_nudity_settings_from_basic_save_datafrom wickedwhims.relationships.relationship_settings import apply_relationship_settings_from_basic_save_datafrom wickedwhims.sex.settings.sex_settings import apply_sex_settings_from_basic_save_datafrom wickedwhims.sex.sex_operators.active_sex_handlers_operator import register_loaded_active_sex_handlers, apply_active_sex_handler_to_simfrom wickedwhims.sxex_bridge.penis import apply_basic_penis_save_datafrom wickedwhims.utils_saves.save_basics import load_basic_save_data, save_basic_save_datafrom wickedwhims.utils_saves.save_disabled_animations import load_disabled_animations_save_data, save_disabled_animations_save_datafrom wickedwhims.utils_saves.save_disabled_locations import load_disabled_locations_save_data, save_disabled_locations_save_datafrom wickedwhims.utils_saves.save_game_events import load_game_events_save_data, save_game_events_save_datafrom wickedwhims.utils_saves.save_main import remove_scratch_save_filesfrom wickedwhims.utils_saves.save_sex_handlers import load_sex_handlers_save_data, save_sex_handlers_save_datafrom wickedwhims.utils_saves.save_sims import load_sims_save_data, update_sim_save_data, save_sims_save_data, apply_sim_save_datafrom wickedwhims.utils_saves.save_statistics import load_statistics_save_data, apply_global_statistics_save_data, update_global_statistics_save_data, update_statistics_save_data, save_statistics_save_data, apply_statistics_save_datafrom wickedwhims.utils_saves.save_version import update_version_save_data, save_version_save_datafrom wickedwhims.version_registry import get_mod_version_intIS_FIRST_LOAD = TrueCURRENT_NON_SCRATCH_SAVE_SLOT = -1
@register_zone_load_event_method(unique_id='WickedWhims', priority=1, early=True)
def _wickedwhims_load_save_data():
    global IS_FIRST_LOAD, CURRENT_NON_SCRATCH_SAVE_SLOT
    save_slot_id = TurboResourceUtil.Persistance.get_save_slot_id()
    if save_slot_id != 0:
        if save_slot_id != CURRENT_NON_SCRATCH_SAVE_SLOT:
            IS_FIRST_LOAD = True
            _reset_data_cache()
        CURRENT_NON_SCRATCH_SAVE_SLOT = save_slot_id

def _reset_data_cache():
    reset_sims_ev_data()

@register_zone_load_event_method(unique_id='WickedWhims', priority=2, early=True)
def _wickedwhims_load_settings_save_data():
    load_cas_parts_from_file()
    load_basic_save_data()
    load_disabled_animations_save_data()
    load_disabled_locations_save_data()
    apply_nudity_settings_from_basic_save_data()
    apply_basic_penis_save_data()
    apply_relationship_settings_from_basic_save_data()
    apply_sex_settings_from_basic_save_data()

@register_zone_load_event_method(unique_id='WickedWhims', priority=3, late=True)
def _wickedwhims_apply_loaded_save_data():
    global IS_FIRST_LOAD
    slot_id_override = -1
    if IS_FIRST_LOAD is True and TurboResourceUtil.Persistance.get_save_slot_id() == 0:
        slot_id_override = CURRENT_NON_SCRATCH_SAVE_SLOT
    IS_FIRST_LOAD = False
    load_game_events_save_data(slot_id=slot_id_override)
    load_sims_save_data(slot_id=slot_id_override)
    load_statistics_save_data(slot_id=slot_id_override)
    load_sex_handlers_save_data(slot_id=slot_id_override)
    apply_global_statistics_save_data()
    register_loaded_active_sex_handlers()
    for sim_info in TurboManagerUtil.Sim.get_all_sim_info_gen(humans=True, pets=False):
        apply_sim_save_data(sim_info)
        apply_statistics_save_data(sim_info)
        apply_active_sex_handler_to_sim(sim_info)
        sim_ev(sim_info).ready()

@register_zone_load_event_method(unique_id='WickedWhims', priority=100, late=True)
def _wickedwhims_remove_scratch_save_data():
    remove_scratch_save_files()

@register_zone_save_event(unique_id='WickedWhims')
def _wickedwhims_save_all_services():
    update_version_save_data({'version': get_mod_version_int()})
    save_version_save_data()
    update_global_statistics_save_data()
    save_disabled_animations_save_data()
    save_disabled_locations_save_data()
    save_basic_save_data()
    save_game_events_save_data()
    for sim_info in TurboManagerUtil.Sim.get_all_sim_info_gen(humans=True, pets=False):
        while sim_ev(sim_info).is_ready():
            update_sim_save_data(sim_info)
            update_statistics_save_data(sim_info)
    save_sex_handlers_save_data()
    save_sims_save_data()
    save_statistics_save_data()
