'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''from enums.buffs_enum import SimBufffrom turbolib.cas_util import TurboCASUtilfrom turbolib.manager_util import TurboManagerUtilfrom turbolib.native.enum import TurboEnumfrom turbolib.sim_util import TurboSimUtilfrom wickedwhims.sxex_bridge.body import get_sim_actual_body_state, BodyStatefrom wickedwhims.sxex_bridge.nudity import update_nude_body_datafrom wickedwhims.utils_buffs import has_sim_buff
class OutfitLevel(TurboEnum):
    __qualname__ = 'OutfitLevel'
    OUTFIT = 0
    REVEALING = 1
    UNDERWEAR = 2
    BATHING = 3
    NUDE = 4

def get_sim_outfit_level(sim_identifier, outfit_category_and_index=None):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier, allow_base_wrapper=True)
    sim_nudity_state = OutfitLevel.OUTFIT
    current_outfit = outfit_category_and_index or TurboSimUtil.CAS.get_current_outfit(sim_info)
    if current_outfit[0] == TurboCASUtil.OutfitCategory.BATHING:
        return OutfitLevel.BATHING
    if is_sim_in_revealing_outfit(sim_identifier):
        return OutfitLevel.REVEALING
    if current_outfit[0] == TurboCASUtil.OutfitCategory.SPECIAL and current_outfit[1] == 0:
        update_nude_body_data(sim_info)
        if TurboSimUtil.Gender.is_female(sim_info):
            top_state = get_sim_actual_body_state(sim_info, TurboCASUtil.BodyType.UPPER_BODY)
            if top_state == BodyState.NUDE:
                return OutfitLevel.NUDE
            if top_state == BodyState.UNDERWEAR:
                sim_nudity_state = OutfitLevel.UNDERWEAR
            bottom_state = get_sim_actual_body_state(sim_info, TurboCASUtil.BodyType.LOWER_BODY)
            if bottom_state == BodyState.NUDE:
                return OutfitLevel.NUDE
            if bottom_state == BodyState.UNDERWEAR:
                sim_nudity_state = OutfitLevel.UNDERWEAR
                bottom_state = get_sim_actual_body_state(sim_info, TurboCASUtil.BodyType.LOWER_BODY)
                if bottom_state == BodyState.NUDE:
                    return OutfitLevel.NUDE
                if bottom_state == BodyState.UNDERWEAR:
                    return OutfitLevel.UNDERWEAR
        else:
            bottom_state = get_sim_actual_body_state(sim_info, TurboCASUtil.BodyType.LOWER_BODY)
            if bottom_state == BodyState.NUDE:
                return OutfitLevel.NUDE
            if bottom_state == BodyState.UNDERWEAR:
                return OutfitLevel.UNDERWEAR
    return sim_nudity_state

def is_possible_nude_outfit(outfit_category):
    return outfit_category == TurboCASUtil.OutfitCategory.SPECIAL or outfit_category == TurboCASUtil.OutfitCategory.BATHING

def is_sim_in_revealing_outfit(sim_identifier):
    current_outfit = TurboSimUtil.CAS.get_current_outfit(sim_identifier)
    return current_outfit[0] == TurboCASUtil.OutfitCategory.SWIMWEAR or (current_outfit[0] == TurboCASUtil.OutfitCategory.SLEEP or is_sim_in_towel_outfit(sim_identifier))

def is_sim_in_towel_outfit(sim_identifier):
    return has_sim_buff(sim_identifier, SimBuff.ISWEARINGTOWEL)
