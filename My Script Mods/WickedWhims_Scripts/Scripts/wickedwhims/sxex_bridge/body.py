'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''from enums.statistics_enum import SimCommodityfrom turbolib.manager_util import TurboManagerUtilfrom turbolib.native.enum import TurboEnumfrom turbolib.sim_util import TurboSimUtilfrom wickedwhims.main.cas_config_handler import get_penis_part_idsfrom wickedwhims.main.sim_ev_handler import sim_evfrom wickedwhims.sxex_bridge.nudity import update_nude_body_datafrom wickedwhims.utils_cas import get_sim_outfit_cas_part_from_bodytype, get_modified_outfit, has_sim_body_partfrom wickedwhims.utils_statistics import set_sim_statistic_value
def update_sim_body_data(sim_identifier, override_outfit_category_and_index=None):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier, allow_base_wrapper=True)
    sim_ev(sim_info).body_state_cache = dict()
    sim_ev(sim_info).additional_body_state_cache = dict()
    if override_outfit_category_and_index is None:
        outfit_category_and_index = TurboSimUtil.CAS.get_current_outfit(sim_info)
    else:
        outfit_category_and_index = override_outfit_category_and_index
    sim_ev(sim_info).outfit_parts_cache = TurboSimUtil.CAS.get_outfit_parts(sim_info, outfit_category_and_index)

class BodyState(TurboEnum):
    __qualname__ = 'BodyState'
    OUTFIT = 1
    UNDERWEAR = 2
    NUDE = 3

class AdditionalBodyState(TurboEnum):
    __qualname__ = 'AdditionalBodyState'
    NONE = 1
    STRAPON = 4

def get_sim_body_state(sim_identifier, bodytype, outfit_category_and_index=None):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    if bodytype in sim_ev(sim_info).body_state_cache:
        return sim_ev(sim_info).body_state_cache[bodytype]
    result = _get_sim_body_state(sim_info, bodytype, outfit_category_and_index=outfit_category_and_index)
    sim_ev(sim_info).body_state_cache[bodytype] = result
    return result

def _get_sim_body_state(sim_identifier, bodytype, outfit_category_and_index=None):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    part_id = get_sim_outfit_cas_part_from_bodytype(sim_info, bodytype, outfit_category_and_index=outfit_category_and_index)
    nude_part_id = sim_ev(sim_info).nude_outfit_parts[bodytype] if bodytype in sim_ev(sim_info).nude_outfit_parts else -1
    if part_id == nude_part_id and nude_part_id != -1:
        return BodyState.NUDE
    if bodytype == 7 and part_id != -1 and part_id in get_penis_part_ids():
        return BodyState.NUDE
    if bodytype == 6 or bodytype == 7:
        current_outfit_category_and_index = get_modified_outfit(sim_info)
        from wickedwhims.nudity.underwear.operator import get_sim_underwear_data
        underwear_data = get_sim_underwear_data(sim_info, current_outfit_category_and_index)
        if part_id != -1 and part_id == underwear_data[0 if bodytype == 6 else 1]:
            return BodyState.UNDERWEAR
    return BodyState.OUTFIT

def get_sim_additional_body_state(sim_identifier, bodytype, bodystate, outfit_category_and_index=None):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    if bodytype in sim_ev(sim_info).additional_body_state_cache:
        return sim_ev(sim_info).additional_body_state_cache[bodytype]
    result = _get_sim_additional_body_state(sim_info, bodytype, bodystate, outfit_category_and_index=outfit_category_and_index)
    sim_ev(sim_info).additional_body_state_cache[bodytype] = result
    return result

def _get_sim_additional_body_state(sim_identifier, bodytype, bodystate, outfit_category_and_index=None):
    part_id = get_sim_outfit_cas_part_from_bodytype(sim_identifier, bodytype, outfit_category_and_index=outfit_category_and_index)
    if part_id == -1:
        return AdditionalBodyState.NONE
    if bodystate == BodyState.OUTFIT:
        from wickedwhims.sex.strapon.operator import get_sim_strapon_part_id
        strapon_part_id = get_sim_strapon_part_id(sim_identifier)
        if strapon_part_id != -1 and part_id == strapon_part_id:
            return AdditionalBodyState.STRAPON
    return AdditionalBodyState.NONE

def get_sim_actual_body_state(sim_identifier, bodytype, outfit_category_and_index=None):
    body_state = get_sim_body_state(sim_identifier, bodytype, outfit_category_and_index=outfit_category_and_index)
    if body_state == BodyState.OUTFIT:
        additional_body_state = get_sim_additional_body_state(sim_identifier, bodytype, body_state, outfit_category_and_index=outfit_category_and_index)
        if additional_body_state == AdditionalBodyState.STRAPON:
            return BodyState.NUDE
    return body_state

def is_sim_outfit_fullbody(sim_identifier, outfit_category_and_index=None):
    return has_sim_body_part(sim_identifier, 5, outfit_category_and_index=outfit_category_and_index)

def has_sim_outfit_top(sim_identifier, outfit_category_and_index=None):
    return has_sim_body_part(sim_identifier, 6, outfit_category_and_index=outfit_category_and_index)

def has_sim_outfit_bottom(sim_identifier, outfit_category_and_index=None):
    return has_sim_body_part(sim_identifier, 7, outfit_category_and_index=outfit_category_and_index)

def update_sim_body_flags(sim_identifier, update_nude_outfit_data=False):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    if update_nude_outfit_data is True:
        update_nude_body_data(sim_info)
    top_state = get_sim_body_state(sim_info, 6)
    if top_state == BodyState.NUDE:
        set_sim_top_naked_state(sim_info, True)
    else:
        set_sim_top_naked_state(sim_info, False)
    bottom_state = get_sim_body_state(sim_info, 7)
    if bottom_state == BodyState.NUDE:
        set_sim_bottom_naked_state(sim_info, True)
    else:
        set_sim_bottom_naked_state(sim_info, False)

def set_sim_top_naked_state(sim_identifier, state):
    set_sim_statistic_value(sim_identifier, 1 if state is True else 0, SimCommodity.WW_NUDITY_IS_TOP_NAKED)

def set_sim_bottom_naked_state(sim_identifier, state):
    set_sim_statistic_value(sim_identifier, 1 if state is True else 0, SimCommodity.WW_NUDITY_IS_BOTTOM_NAKED)
