'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''from turbolib.manager_util import TurboManagerUtilfrom wickedwhims.main.sim_ev_handler import sim_evfrom wickedwhims.sxex_bridge.statistics import get_global_ww_statistics, set_global_ww_statisticsfrom wickedwhims.utils_saves.save_main import get_save_dir, set_has_save_loading_error, get_save_id, load_json_file, save_json_fileSTATISTICS_SAVE_DATA = dict()
def load_statistics_save_data(slot_id=-1):
    global STATISTICS_SAVE_DATA
    save_id = get_save_id('statistics', slot_id=slot_id)
    load_file_path = get_save_dir() + save_id + '.json'
    try:
        STATISTICS_SAVE_DATA = load_json_file(load_file_path) or dict()
    except:
        set_has_save_loading_error()
        STATISTICS_SAVE_DATA = dict()

def save_statistics_save_data():
    save_id = get_save_id('statistics')
    save_file_path = get_save_dir() + save_id + '.json'
    save_json_file(save_file_path, STATISTICS_SAVE_DATA)

def update_statistics_save_data(sim_identifier):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    STATISTICS_SAVE_DATA[str(TurboManagerUtil.Sim.get_sim_id(sim_info))] = sim_ev(sim_info).special_statistics.copy()

def update_global_statistics_save_data():
    STATISTICS_SAVE_DATA['_global'] = get_global_ww_statistics().copy()

def apply_statistics_save_data(sim_identifier):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    if str(TurboManagerUtil.Sim.get_sim_id(sim_info)) not in STATISTICS_SAVE_DATA:
        return
    sim_ev(sim_info).special_statistics = STATISTICS_SAVE_DATA[str(TurboManagerUtil.Sim.get_sim_id(sim_info))]

def apply_global_statistics_save_data():
    if '_global' not in STATISTICS_SAVE_DATA:
        return
    set_global_ww_statistics(STATISTICS_SAVE_DATA['_global'])
    update_global_statistics_save_data()
