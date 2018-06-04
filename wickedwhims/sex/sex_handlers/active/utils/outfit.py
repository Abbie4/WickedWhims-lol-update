'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from turbolib.cas_util import TurboCASUtil
from turbolib.manager_util import TurboManagerUtil
from turbolib.sim_util import TurboSimUtil
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.nudity.nudity_settings import get_nudity_setting, NuditySetting, CompleteUndressingTypeSetting
from wickedwhims.sex.enums.sex_naked_type import SexNakedType
from wickedwhims.sex.settings.sex_settings import get_sex_setting, SexSetting, SexUndressingLevelSetting
from wickedwhims.sxex_bridge.body import BodyState, is_sim_outfit_fullbody, set_sim_top_naked_state, set_sim_bottom_naked_state, get_sim_actual_body_state
from wickedwhims.sxex_bridge.nudity import update_nude_body_data, reset_sim_bathing_outfits
from wickedwhims.sxex_bridge.outfit import strip_outfit, StripType
from wickedwhims.sxex_bridge.underwear import set_sim_top_underwear_state, set_sim_bottom_underwear_state, is_sim_top_underwear, is_sim_bottom_underwear, is_underwear_outfit
from wickedwhims.utils_cas import copy_outfit_to_special, get_modified_outfit

def undress_sim(sim_identifier, actor_data, is_npc_only=False):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    if is_npc_only is False:
        undressing_type = get_sex_setting(SexSetting.SEX_UNDRESSING_TYPE, variable_type=int)
    else:
        undressing_type = get_sex_setting(SexSetting.NPC_SEX_UNDRESSING_TYPE, variable_type=int)
    if undressing_type == SexUndressingLevelSetting.DISABLED:
        return
    update_nude_body_data(sim_info)
    top_body_state = get_sim_actual_body_state(sim_info, TurboCASUtil.BodyType.UPPER_BODY)
    bottom_body_state = get_sim_actual_body_state(sim_info, TurboCASUtil.BodyType.LOWER_BODY)
    hands_body_state = get_sim_actual_body_state(sim_info, TurboCASUtil.BodyType.GLOVES)
    feet_body_state = get_sim_actual_body_state(sim_info, TurboCASUtil.BodyType.SHOES)
    if undressing_type == SexUndressingLevelSetting.COMPLETE:
        if top_body_state == BodyState.NUDE and (bottom_body_state == BodyState.NUDE and hands_body_state == BodyState.NUDE) and feet_body_state == BodyState.NUDE:
            return
        if get_nudity_setting(NuditySetting.COMPLETE_UNDRESSING_TYPE, variable_type=int) == CompleteUndressingTypeSetting.DEFAULT:
            reset_sim_bathing_outfits(sim_info)
            copy_outfit_to_special(sim_info, set_special_outfit=True, outfit_category_and_index=(TurboCASUtil.OutfitCategory.BATHING, 0), override_outfit_parts={115: sim_ev(sim_info).nude_outfit_parts[115]})
        else:
            copy_outfit_to_special(sim_info, set_special_outfit=True, outfit_category_and_index=get_modified_outfit(sim_info), override_outfit_parts={TurboCASUtil.BodyType.UPPER_BODY: sim_ev(sim_info).nude_outfit_parts[TurboCASUtil.BodyType.UPPER_BODY], TurboCASUtil.BodyType.LOWER_BODY: sim_ev(sim_info).nude_outfit_parts[TurboCASUtil.BodyType.LOWER_BODY], TurboCASUtil.BodyType.SHOES: sim_ev(sim_info).nude_outfit_parts[TurboCASUtil.BodyType.SHOES], TurboCASUtil.BodyType.FULL_BODY: 0, TurboCASUtil.BodyType.HAT: 0, TurboCASUtil.BodyType.CUMMERBUND: 0, TurboCASUtil.BodyType.EARRINGS: 0, TurboCASUtil.BodyType.GLASSES: 0, TurboCASUtil.BodyType.NECKLACE: 0, TurboCASUtil.BodyType.GLOVES: 0, TurboCASUtil.BodyType.WRIST_LEFT: 0, TurboCASUtil.BodyType.WRIST_RIGHT: 0, TurboCASUtil.BodyType.SOCKS: 0, TurboCASUtil.BodyType.TIGHTS: 0, 115: sim_ev(sim_info).nude_outfit_parts[115]})
        set_sim_top_naked_state(sim_info, True)
        set_sim_bottom_naked_state(sim_info, True)
        set_sim_top_underwear_state(sim_info, False)
        set_sim_bottom_underwear_state(sim_info, False)
        return
    if actor_data.is_forcing_nude_hands() and hands_body_state != BodyState.NUDE:
        strip_outfit(sim_info, strip_bodytype=TurboCASUtil.BodyType.GLOVES)
    if actor_data.is_forcing_nude_feet() and feet_body_state != BodyState.NUDE:
        strip_outfit(sim_info, strip_bodytype=TurboCASUtil.BodyType.SHOES)
    if actor_data.get_naked_type() == SexNakedType.ALL:
        if top_body_state == BodyState.NUDE and bottom_body_state == BodyState.NUDE:
            return
        strip_outfit(sim_info, strip_type_top=StripType.NUDE, strip_type_bottom=StripType.NUDE)
        set_sim_top_naked_state(sim_info, True)
        set_sim_bottom_naked_state(sim_info, True)
        set_sim_top_underwear_state(sim_info, False)
        set_sim_bottom_underwear_state(sim_info, False)
    elif actor_data.get_naked_type() == SexNakedType.TOP:
        if top_body_state == BodyState.NUDE:
            return
        has_bottom_underwear_on = is_underwear_outfit(get_modified_outfit(sim_info)[0]) and is_sim_bottom_underwear(sim_info)
        strip_type_bottom = StripType.NONE if not is_sim_outfit_fullbody(sim_info) else StripType.UNDERWEAR if has_bottom_underwear_on else StripType.NUDE
        strip_outfit(sim_info, strip_type_top=StripType.NUDE, strip_type_bottom=strip_type_bottom)
        set_sim_top_naked_state(sim_info, True)
        set_sim_bottom_naked_state(sim_info, strip_type_bottom == StripType.NUDE)
        set_sim_top_underwear_state(sim_info, False)
        set_sim_bottom_underwear_state(sim_info, strip_type_bottom == StripType.UNDERWEAR)
    elif actor_data.get_naked_type() == SexNakedType.BOTTOM:
        if bottom_body_state == BodyState.NUDE:
            return
        has_top_underwear_on = TurboSimUtil.Gender.is_female(sim_info) and (is_underwear_outfit(get_modified_outfit(sim_info)[0]) and is_sim_top_underwear(sim_info))
        strip_type_top = StripType.NONE if not is_sim_outfit_fullbody(sim_info) else StripType.UNDERWEAR if has_top_underwear_on else StripType.NUDE
        strip_outfit(sim_info, strip_type_top=strip_type_top, strip_type_bottom=StripType.NUDE)
        set_sim_top_naked_state(sim_info, strip_type_top == StripType.NUDE)
        set_sim_bottom_naked_state(sim_info, True)
        set_sim_top_underwear_state(sim_info, strip_type_top == StripType.UNDERWEAR)
        set_sim_bottom_underwear_state(sim_info, False)

