'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from enums.statistics_enum import SimCommodity
from turbolib.manager_util import TurboManagerUtil
from wickedwhims.debug.debug_controller import is_main_debug_flag_enabled
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.utils_interfaces import display_notification
from wickedwhims.utils_statistics import set_sim_statistic_value

def clear_sims_sex_extra_data(sims_list, only_active_data=False, only_pre_active_data=False):
    for sim in sims_list:
        clear_sim_sex_extra_data(sim, only_active_data=only_active_data, only_pre_active_data=only_pre_active_data)


def clear_sim_sex_extra_data(sim_identifier, only_active_data=False, only_pre_active_data=False):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    if only_pre_active_data is False:
        sim_ev(sim_info).is_playing_sex = False
        sim_ev(sim_info).active_sex_handler_identifier = '-1'
        sim_ev(sim_info).active_sex_handler = None
        sim_ev(sim_info).sim_sex_state_snapshot = dict()
        sim_ev(sim_info).sim_immutable_sex_state_snapshot = dict()
        set_sim_statistic_value(sim_info, 0, SimCommodity.WW_READY_TO_CLIMAX)
        if is_main_debug_flag_enabled():
            display_notification(text='Cleared Sim Active Sex Data', title='Sex Extra Data Clear', secondary_icon=sim_info)
    if only_active_data is False:
        sim_ev(sim_info).has_setup_sex = False
        sim_ev(sim_info).active_pre_sex_handler = None
        sim_ev(sim_info).is_ready_to_sex = False
        sim_ev(sim_info).is_in_process_to_sex = False
        sim_ev(sim_info).in_sex_process_interaction = None
        set_sim_statistic_value(sim_info, 0, SimCommodity.WW_IS_SIM_IN_SEX)
        if is_main_debug_flag_enabled():
            display_notification(text='Cleared Sim Pre Sex Data', title='Sex Extra Data Clear', secondary_icon=sim_info)


def get_all_unique_sex_handlers():
    sex_handlers = dict()
    for sim in TurboManagerUtil.Sim.get_all_sim_instance_gen(humans=True, pets=False):
        sex_handler = sim_ev(sim).active_sex_handler or sim_ev(sim).active_pre_sex_handler
        while sex_handler is not None:
            sex_handlers[sex_handler.get_identifier()] = sex_handler
    return sex_handlers.values()

