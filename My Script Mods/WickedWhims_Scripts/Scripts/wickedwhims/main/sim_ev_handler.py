'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from turbolib.manager_util import TurboManagerUtil
SIM_INFO_EXTRA_DATA_HANDLER = dict()

class SimInfoExtraData:
    __qualname__ = 'SimInfoExtraData'

    def __init__(self, sim_id):
        self.sim_id = sim_id
        self.is_sim_ready = False

    def unready(self):
        self.is_sim_ready = False

    def ready(self):
        self.is_sim_ready = True

    def is_ready(self):
        return self.is_sim_ready


def sim_ev(sim_identifier):
    return _get_sim_ev_data(sim_identifier)


def set_sim_ev_value(sim_identifier, attribute, value):
    sim_ev_data = _get_sim_ev_data(sim_identifier)
    if sim_ev_data is None:
        return
    setattr(sim_ev_data, attribute, value)


def has_sim_ev_attribute(sim_identifier, attribute):
    sim_ev_data = _get_sim_ev_data(sim_identifier)
    if sim_ev_data is None:
        return False
    return hasattr(sim_ev_data, attribute)


def get_sim_ev_value(sim_identifier, attribute):
    sim_ev_data = _get_sim_ev_data(sim_identifier)
    if sim_ev_data is None:
        return
    if not hasattr(sim_ev_data, attribute):
        return
    return getattr(sim_ev_data, attribute)


def _get_sim_ev_data(sim_identifier):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier, allow_base_wrapper=True)
    if sim_info is None:
        return
    sim_id = str(TurboManagerUtil.Sim.get_sim_id(sim_info))
    if sim_id not in SIM_INFO_EXTRA_DATA_HANDLER:
        SIM_INFO_EXTRA_DATA_HANDLER[sim_id] = SimInfoExtraData(TurboManagerUtil.Sim.get_sim_id(sim_info))
    return SIM_INFO_EXTRA_DATA_HANDLER[sim_id]


def reset_sims_ev_data():
    global SIM_INFO_EXTRA_DATA_HANDLER
    SIM_INFO_EXTRA_DATA_HANDLER = dict()

