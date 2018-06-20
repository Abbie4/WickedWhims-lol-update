'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from turbolib.cas_util import TurboCASUtil
from turbolib.events.core import register_zone_load_event_method, is_game_loading
from turbolib.events.sims import register_sim_occult_type_change_event_method, register_sim_info_instance_init_event_method
from turbolib.manager_util import TurboManagerUtil
from turbolib.sim_util import TurboSimUtil
from turbolib.special.custom_exception_watcher import exception_watch
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.sxex_bridge.body import update_sim_body_flags, update_sim_body_data
from wickedwhims.sxex_bridge.penis import update_sim_penis_texture
from wickedwhims.sxex_bridge.underwear import update_sim_underwear_data
from wickedwhims.utils_cas import copy_outfit_to_special

@register_sim_info_instance_init_event_method(unique_id='WickedWhims', priority=1, late=True)
def _wickedwhims_register_nudity_outfit_change_callback_on_new_sim(sim_info):
    if is_game_loading():
        return
    if TurboSimUtil.Species.is_human(sim_info):
        TurboSimUtil.CAS.register_for_outfit_changed_callback(sim_info, _on_sim_outfit_change)
        TurboSimUtil.CAS.register_for_appearance_tracker_changed_callback(sim_info, _on_sim_appearance_tracker_change)


@register_zone_load_event_method(unique_id='WickedWhims', priority=30, late=True)
def _wickedwhims_register_nudity_outfit_change_callback():
    for sim_info in TurboManagerUtil.Sim.get_all_sim_info_gen(humans=True, pets=False):
        TurboSimUtil.CAS.register_for_outfit_changed_callback(sim_info, _on_sim_outfit_change)
        TurboSimUtil.CAS.register_for_appearance_tracker_changed_callback(sim_info, _on_sim_appearance_tracker_change)


@register_sim_occult_type_change_event_method(unique_id='WickedWhims', priority=0)
def _wickedwhims_update_sim_outfit_on_occult_change(sim_info, _):
    try:
        TurboSimUtil.CAS.refresh_outfit(sim_info)
    except:
        pass


@exception_watch()
def _on_sim_outfit_change(sim_info, category_and_index):
    update_sim_body_data(sim_info, override_outfit_category_and_index=category_and_index)
    _handle_special_outfit(sim_info, category_and_index)
    _handle_sim_outfit_variables(sim_info, category_and_index)
    _handle_body_data(sim_info)
    _handle_underwear_data(sim_info, category_and_index)
    update_sim_penis_texture(sim_info, outfit_category_and_index=category_and_index)


def _handle_sim_outfit_variables(sim_info, category_and_index):
    previous_category_and_index = TurboSimUtil.CAS.get_previous_outfit(sim_info)
    if previous_category_and_index[0] != TurboCASUtil.OutfitCategory.BATHING and previous_category_and_index[0] != TurboCASUtil.OutfitCategory.SPECIAL:
        sim_ev(sim_info).previous_outfit_category = int(previous_category_and_index[0])
        sim_ev(sim_info).previous_outfit_index = int(previous_category_and_index[1])
    if category_and_index[0] != TurboCASUtil.OutfitCategory.SPECIAL:
        sim_ev(sim_info).current_outfit_category = int(category_and_index[0])
        sim_ev(sim_info).current_outfit_index = int(category_and_index[1])


def _handle_special_outfit(sim_info, category_and_index):
    if category_and_index[0] == TurboCASUtil.OutfitCategory.SPECIAL:
        sim_ev(sim_info).original_outfit_category = int(sim_ev(sim_info).current_outfit_category)
        sim_ev(sim_info).original_outfit_index = int(sim_ev(sim_info).current_outfit_index)
        if category_and_index[1] != 0:
            copy_outfit_to_special(sim_info, set_special_outfit=True, outfit_category_and_index=(TurboCASUtil.OutfitCategory.SPECIAL, category_and_index[1]))
        else:
            try:
                TurboSimUtil.CAS.evaluate_appearance_modifiers(sim_info)
                TurboSimUtil.CAS.resend_outfit_data(sim_info)
            except:
                pass


def _handle_underwear_data(sim_info, category_and_index):
    from wickedwhims.nudity.underwear.operator import validate_outfit_underwear
    validate_outfit_underwear(sim_info, category_and_index)
    update_sim_underwear_data(sim_info)


def _handle_body_data(sim_info):
    update_sim_body_flags(sim_info)


@exception_watch()
def _on_sim_appearance_tracker_change(sim_info):
    sim_ev(sim_info).appearance_modifiers_parts_cache = dict()
    appearance_modifiers = TurboCASUtil.AppearanceModifier.get_sim_appearance_modifiers(sim_info, TurboCASUtil.AppearanceModifier.AppearanceModifierType.SET_CAS_PART)
    if not appearance_modifiers:
        return
    update_sim_body_data(sim_info)
    current_outfit_outfit_parts = sim_ev(sim_info).outfit_parts_cache.values()
    for appearance_modifier in appearance_modifiers:
        part_id = int(getattr(appearance_modifier, 'cas_part'))
        if part_id in current_outfit_outfit_parts:
            pass
        body_type = TurboCASUtil.Outfit.get_cas_part_body_type_id(part_id)
        sim_ev(sim_info).appearance_modifiers_parts_cache[body_type] = part_id
    if 5 in sim_ev(sim_info).appearance_modifiers_parts_cache and 5 not in sim_ev(sim_info).outfit_parts_cache:
        sim_ev(sim_info).outfit_parts_cache.pop(6, None)
        sim_ev(sim_info).outfit_parts_cache.pop(7, None)
        sim_ev(sim_info).appearance_modifiers_parts_cache.pop(6, None)
        sim_ev(sim_info).appearance_modifiers_parts_cache.pop(7, None)
    elif 5 not in sim_ev(sim_info).appearance_modifiers_parts_cache and 5 in sim_ev(sim_info).outfit_parts_cache:
        sim_ev(sim_info).outfit_parts_cache.pop(5, None)
        sim_ev(sim_info).appearance_modifiers_parts_cache.pop(5, None)
    for (body_type, part_id) in sim_ev(sim_info).appearance_modifiers_parts_cache.items():
        sim_ev(sim_info).outfit_parts_cache[body_type] = part_id

