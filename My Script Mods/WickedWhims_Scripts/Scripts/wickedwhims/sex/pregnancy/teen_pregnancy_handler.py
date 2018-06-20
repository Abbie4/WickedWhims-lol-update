'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from enums.buffs_enum import SimBuff
from turbolib.events.core import register_zone_load_event_method, is_game_loading
from turbolib.events.sims import register_sim_occult_type_change_event_method, register_sim_info_instance_init_event_method
from turbolib.manager_util import TurboManagerUtil
from turbolib.resource_util import TurboResourceUtil
from turbolib.sim_util import TurboSimUtil
from wickedwhims.utils_buffs import has_sim_buff
PREGNANCY_BUFFS = (SimBuff.PREGNANCY_INLABOR, SimBuff.PREGNANCY_INLABOR_MALE, SimBuff.PREGNANCY_TRIMESTER3, SimBuff.PREGNANCY_TRIMESTER3_MALE, SimBuff.PREGNANCY_TRIMESTER3_HATESCHILDREN, SimBuff.PREGNANCY_TRIMESTER2, SimBuff.PREGNANCY_TRIMESTER2_MALE, SimBuff.PREGNANCY_TRIMESTER2_HATESCHILDREN, SimBuff.PREGNANCY_TRIMESTER1, SimBuff.PREGNANCY_TRIMESTER1_MALE, SimBuff.PREGNANCY_TRIMESTER1_HATESCHILDREN)

@register_sim_info_instance_init_event_method(unique_id='WickedWhims', priority=1, late=True)
def _wickedwooooh_register_pregnancy_buff_callback_on_new_sim(sim_info):
    if is_game_loading():
        return
    if TurboSimUtil.Species.is_human(sim_info):
        TurboSimUtil.Buff.register_for_buff_added_callback(sim_info, _on_sim_pregnancy_buff_added_and_removed)
        TurboSimUtil.Buff.register_for_buff_removed_callback(sim_info, _on_sim_pregnancy_buff_added_and_removed)


@register_zone_load_event_method(unique_id='WickedWhims', priority=40, late=True)
def _wickedwhims_register_pregnancy_buff_callback():
    for sim_info in TurboManagerUtil.Sim.get_all_sim_info_gen(humans=True, pets=False):
        TurboSimUtil.Buff.register_for_buff_added_callback(sim_info, _on_sim_pregnancy_buff_added_and_removed)
        TurboSimUtil.Buff.register_for_buff_removed_callback(sim_info, _on_sim_pregnancy_buff_added_and_removed)


@register_sim_occult_type_change_event_method(unique_id='WickedWhims', priority=1)
def _wickedwhims_update_sim_pregnancy_visuals(sim_info, _):
    if TurboSimUtil.Age.get_age(sim_info) != TurboSimUtil.Age.TEEN:
        return
    _update_sim_pregnancy_data(sim_info)


def _get_sim_appearance_data_for_pregnancy(sim_identifier):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    if has_sim_buff(sim_info, SimBuff.PREGNANCY_INLABOR) or has_sim_buff(sim_info, SimBuff.PREGNANCY_INLABOR_MALE):
        if TurboSimUtil.Gender.is_female(sim_info):
            return (16391756994022883177, 1.0)
        return (5705220627947342604, 1.0)
    elif has_sim_buff(sim_info, SimBuff.PREGNANCY_TRIMESTER3) or has_sim_buff(sim_info, SimBuff.PREGNANCY_TRIMESTER3_MALE) or has_sim_buff(sim_info, SimBuff.PREGNANCY_TRIMESTER3_HATESCHILDREN):
        if TurboSimUtil.Gender.is_female(sim_info):
            return (16391756994022883177, 0.95)
        return (5705220627947342604, 0.95)
    elif has_sim_buff(sim_info, SimBuff.PREGNANCY_TRIMESTER2) or has_sim_buff(sim_info, SimBuff.PREGNANCY_TRIMESTER2_MALE) or has_sim_buff(sim_info, SimBuff.PREGNANCY_TRIMESTER2_HATESCHILDREN):
        if TurboSimUtil.Gender.is_female(sim_info):
            return (16391756994022883177, 0.75)
        return (5705220627947342604, 0.75)
    elif has_sim_buff(sim_info, SimBuff.PREGNANCY_TRIMESTER1) or has_sim_buff(sim_info, SimBuff.PREGNANCY_TRIMESTER1_MALE) or has_sim_buff(sim_info, SimBuff.PREGNANCY_TRIMESTER1_HATESCHILDREN):
        if TurboSimUtil.Gender.is_female(sim_info):
            return (16391756994022883177, 0.5)
        return (5705220627947342604, 0.5)
    if TurboSimUtil.Gender.is_female(sim_info):
        return (16391756994022883177, 0.0)
    return (5705220627947342604, 0.0)


def _on_sim_pregnancy_buff_added_and_removed(buff_type, sim_id):
    if buff_type is None:
        return
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_id)
    if sim_info is None:
        return
    if TurboSimUtil.Age.get_age(sim_info) != TurboSimUtil.Age.TEEN:
        return
    if TurboResourceUtil.Resource.get_guid64(buff_type) not in PREGNANCY_BUFFS:
        return
    _update_sim_pregnancy_data(sim_info)


def _update_sim_pregnancy_data(sim_info):
    (key, value) = _get_sim_appearance_data_for_pregnancy(sim_info)
    TurboSimUtil.AppearanceAttributes.set_appearance_attribute(sim_info, key, value, remove=value == 0.0)

