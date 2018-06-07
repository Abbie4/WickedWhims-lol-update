'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''from turbolib.cas_util import TurboCASUtilfrom turbolib.events.interactions import register_interaction_run_event_methodfrom turbolib.interaction_util import TurboInteractionUtilfrom turbolib.manager_util import TurboManagerUtilfrom turbolib.native.enum import TurboEnumfrom turbolib.resource_util import TurboResourceUtilfrom turbolib.sim_util import TurboSimUtilfrom wickedwhims.main.sim_ev_handler import sim_evfrom wickedwhims.main.tick_handler import register_on_game_update_methodfrom wickedwhims.nudity.nudity_settings import NuditySetting, get_nudity_settingfrom wickedwhims.nudity.underwear.operator import get_sim_underwear_datafrom wickedwhims.sxex_bridge.body import BodyState, get_sim_body_state, set_sim_top_naked_state, set_sim_bottom_naked_state, is_sim_outfit_fullbody, has_sim_outfit_bottomfrom wickedwhims.sxex_bridge.outfit import StripType, strip_outfit, dress_up_outfitfrom wickedwhims.sxex_bridge.underwear import set_sim_bottom_underwear_state, is_sim_top_underwearfrom wickedwhims.utils_cas import get_modified_outfit, get_sim_outfit_cas_part_from_bodytype, set_bodytype_caspartTOILET_USE_INTERACTIONS = (151354, 13443)
class OutfitStateBeforeToiletUse(TurboEnum):
    __qualname__ = 'OutfitStateBeforeToiletUse'
    NONE = -1
    OUTFIT = 1
    UNDERWEAR = 2

@register_interaction_run_event_method(unique_id='WickedWhims')
def _wickedwhims_undress_bottom_on_toilet_use(interaction_instance):
    if not get_nudity_setting(NuditySetting.TOILET_USE_UNDRESS_STATE, variable_type=bool):
        return
    interaction_guid = TurboResourceUtil.Resource.get_guid64(interaction_instance)
    if interaction_guid not in TOILET_USE_INTERACTIONS:
        return
    sim = TurboInteractionUtil.get_interaction_sim(interaction_instance)
    if sim_ev(sim).on_toilet_outfit_state != OutfitStateBeforeToiletUse.NONE:
        return
    if TurboSimUtil.Age.is_younger_than(sim, TurboSimUtil.Age.TEEN):
        return
    if has_sim_outfit_bottom(sim):
        bottom_body_state = get_sim_body_state(sim, 7)
        if bottom_body_state != BodyState.NUDE:
            strip_result = strip_outfit(sim, strip_type_bottom=StripType.NUDE)
            if strip_result is True:
                sim_ev(sim).on_toilet_outfit_state = int(OutfitStateBeforeToiletUse.UNDERWEAR if bottom_body_state == BodyState.UNDERWEAR else OutfitStateBeforeToiletUse.OUTFIT)
                set_sim_bottom_naked_state(sim, True)
                set_sim_bottom_underwear_state(sim, False)
            else:
                sim_ev(sim).on_toilet_outfit_state = int(OutfitStateBeforeToiletUse.NONE)
    else:
        top_state = StripType.NUDE if TurboSimUtil.Gender.is_male(sim) else StripType.UNDERWEAR if is_sim_top_underwear(sim) else StripType.NUDE
        strip_result = strip_outfit(sim, strip_type_top=top_state, strip_type_bottom=StripType.NUDE)
        if is_sim_outfit_fullbody(sim) and strip_result is True:
            sim_ev(sim).on_toilet_outfit_state = int(OutfitStateBeforeToiletUse.OUTFIT)
            set_sim_top_naked_state(sim, True)
            set_sim_bottom_naked_state(sim, True)
            set_sim_bottom_underwear_state(sim, False)

@register_on_game_update_method(interval=1500)
def _update_dress_up_after_toilet_use_on_game_update():
    if not get_nudity_setting(NuditySetting.TOILET_USE_UNDRESS_STATE, variable_type=bool):
        return
    for sim in TurboManagerUtil.Sim.get_all_sim_instance_gen(humans=True, pets=False):
        if sim_ev(sim).on_toilet_outfit_state == OutfitStateBeforeToiletUse.NONE:
            pass
        if TurboSimUtil.Age.is_younger_than(sim, TurboSimUtil.Age.TEEN):
            pass
        is_using_toilet = False
        for affordance_id in TOILET_USE_INTERACTIONS:
            while TurboSimUtil.Interaction.is_running_interaction(sim, affordance_id):
                is_using_toilet = True
                break
        if is_using_toilet is True:
            pass
        sim_ev(sim).on_toilet_outfit_state = int(OutfitStateBeforeToiletUse.NONE)
        current_outfit = TurboSimUtil.CAS.get_current_outfit(sim)
        if not (current_outfit[0] == TurboCASUtil.OutfitCategory.SPECIAL and current_outfit[1] == 0):
            pass
        current_outfit = get_modified_outfit(sim)
        if sim_ev(sim).on_toilet_outfit_state != -1 and has_sim_outfit_bottom(sim, outfit_category_and_index=current_outfit):
            if sim_ev(sim).on_toilet_outfit_state == OutfitStateBeforeToiletUse.OUTFIT:
                part_id = get_sim_outfit_cas_part_from_bodytype(sim, 7, outfit_category_and_index=current_outfit)
            else:
                part_id = get_sim_underwear_data(sim, current_outfit)[1]
            set_bodytype_caspart(sim, (TurboCASUtil.OutfitCategory.SPECIAL, 0), 7, part_id)
            try:
                TurboSimUtil.CAS.refresh_outfit(sim)
            except:
                pass
        elif is_sim_outfit_fullbody(sim, outfit_category_and_index=current_outfit):
            dress_up_outfit(sim)
        else:
            dress_up_outfit(sim)
