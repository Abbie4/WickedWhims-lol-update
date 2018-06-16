import enum
from enums.traits_enum import SimTrait
from turbolib.cas_util import TurboCASUtil
from turbolib.events.interactions import register_interaction_run_event_method
from turbolib.interaction_util import TurboInteractionUtil
from turbolib.manager_util import TurboManagerUtil
from turbolib.sim_util import TurboSimUtil
from turbolib.types_util import TurboTypesUtil
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.sxex_bridge.body import set_sim_top_naked_state, set_sim_bottom_naked_state
from wickedwhims.sxex_bridge.underwear import set_sim_top_underwear_state, set_sim_bottom_underwear_state
from wickedwhims.utils_cas import get_modified_outfit, is_sim_in_special_outfit, get_previous_modified_outfit, copy_outfit_to_special
from wickedwhims.utils_traits import has_sim_trait
from wickedwhims.sxex_bridge.sex import is_sim_in_sex, is_sim_going_to_sex


class StripType(enum.Int, export=False):
    __qualname__ = 'StripType'
    NONE = 0
    UNDERWEAR = 1
    NUDE = 2


def strip_outfit(sim_identifier, strip_type_top=StripType.NONE, strip_type_bottom=StripType.NONE, strip_bodytype=-1, save_original=True, skip_outfit_change=False, allow_stripping_gloves=None, allow_stripping_feet=None, allow_stripping_socks=None, allow_stripping_leggings=None):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    TurboSimUtil.CAS.reset_appearance_modifiers_owner(sim_info)
    current_outfit_category_and_index = get_modified_outfit(sim_info)
    from wickedwhims.sxex_bridge.nudity import update_nude_body_data
    update_nude_body_data(sim_info)
    if not is_sim_in_special_outfit(sim_info):
        copy_outfit_to_special(sim_info, set_special_outfit=False)
    else:
        save_original = False
    try:
        outfit_editor = TurboCASUtil.OutfitEditor(sim_info, outfit_category_and_index=(TurboCASUtil.OutfitCategory.SPECIAL, 0))
    except RuntimeError:
        return False
    from wickedwhims.nudity.nudity_settings import NuditySetting, get_nudity_setting
    strip_result = False
    special_strip_gloves_with_top = allow_stripping_gloves if allow_stripping_gloves is not None else get_nudity_setting(NuditySetting.OUTFIT_AUTO_UNDRESS_GLOVES_STATE, variable_type=bool)
    special_strip_feet_with_bottom = allow_stripping_feet if allow_stripping_feet is not None else get_nudity_setting(NuditySetting.OUTFIT_AUTO_UNDRESS_SHOES_STATE, variable_type=bool)
    special_strip_socks_with_shoes = allow_stripping_socks if allow_stripping_socks is not None else get_nudity_setting(NuditySetting.OUTFIT_AUTO_UNDRESS_SOCKS_STATE, variable_type=bool)
    special_strip_leggings_with_bottom = allow_stripping_leggings if allow_stripping_leggings is not None else get_nudity_setting(NuditySetting.OUTFIT_AUTO_UNDRESS_LEGGINGS_STATE, variable_type=bool)
    special_strip_feet = False
    if (not get_nudity_setting(NuditySetting.UNDERWEAR_SWITCH_STATE, variable_type=bool) or has_sim_trait(sim_info, SimTrait.WW_NO_UNDERWEAR)) and strip_type_top == StripType.UNDERWEAR:
        strip_type_top = StripType.NUDE
    strip_cas_part = -1
    if strip_type_top == StripType.UNDERWEAR:
        from wickedwhims.nudity.underwear.operator import get_sim_underwear_data
        underwear_parts = get_sim_underwear_data(sim_info, current_outfit_category_and_index)
        strip_cas_part = underwear_parts[0]
    elif strip_type_top == StripType.NUDE and TurboCASUtil.BodyType.UPPER_BODY in sim_ev(sim_info).nude_outfit_parts:
        strip_cas_part = sim_ev(sim_info).nude_outfit_parts[TurboCASUtil.BodyType.UPPER_BODY]
    if strip_cas_part != -1:
        strip_result = outfit_editor.add_cas_part(TurboCASUtil.BodyType.UPPER_BODY, strip_cas_part)
    if strip_type_top != StripType.NONE and special_strip_gloves_with_top is True:
        outfit_editor.remove_body_type(TurboCASUtil.BodyType.GLOVES)
    if (not get_nudity_setting(NuditySetting.UNDERWEAR_SWITCH_STATE, variable_type=bool) or has_sim_trait(sim_info, SimTrait.WW_NO_UNDERWEAR)) and strip_type_bottom == StripType.UNDERWEAR:
        strip_type_bottom = StripType.NUDE
    strip_cas_part = -1
    if strip_type_bottom == StripType.UNDERWEAR:
        from wickedwhims.nudity.underwear.operator import get_sim_underwear_data
        underwear_parts = get_sim_underwear_data(sim_info, current_outfit_category_and_index)
        strip_cas_part = underwear_parts[1]
    elif strip_type_bottom == StripType.NUDE and TurboCASUtil.BodyType.LOWER_BODY in sim_ev(sim_info).nude_outfit_parts:
        strip_cas_part = sim_ev(sim_info).nude_outfit_parts[TurboCASUtil.BodyType.LOWER_BODY]
    if strip_cas_part != -1:
        strip_result = outfit_editor.add_cas_part(TurboCASUtil.BodyType.LOWER_BODY, strip_cas_part)
        if special_strip_feet_with_bottom is True:
            special_strip_feet = True
    if strip_type_bottom != StripType.NONE and (special_strip_leggings_with_bottom is True or not outfit_editor.has_body_type(TurboCASUtil.BodyType.SHOES)):
        outfit_editor.remove_body_type(TurboCASUtil.BodyType.TIGHTS)
    if strip_type_top != StripType.NONE and strip_type_bottom != StripType.NONE:
        outfit_editor.remove_body_type(TurboCASUtil.BodyType.FULL_BODY)
    has_stripped_bodytype = False
    if TurboCASUtil.BodyType.SHOES in sim_ev(sim_info).nude_outfit_parts:
        strip_cas_part = sim_ev(sim_info).nude_outfit_parts[TurboCASUtil.BodyType.SHOES]
        if strip_cas_part != -1:
            strip_result = outfit_editor.add_cas_part(TurboCASUtil.BodyType.SHOES, strip_cas_part)
            has_stripped_bodytype = True
    if (strip_bodytype == TurboCASUtil.BodyType.SHOES or special_strip_feet is True) and special_strip_socks_with_shoes is True:
        outfit_editor.remove_body_type(TurboCASUtil.BodyType.SOCKS)
    if strip_bodytype != -1 and has_stripped_bodytype is False:
        strip_result = outfit_editor.remove_body_type(strip_bodytype)
    if save_original is True:
        sim_ev(sim_info).has_original_outfit_modifications = True
        sim_ev(sim_info).original_outfit_category = int(current_outfit_category_and_index[0])
        sim_ev(sim_info).original_outfit_index = int(current_outfit_category_and_index[1])
    outfit_editor.apply(apply_to_outfit_category=TurboCASUtil.OutfitCategory.SPECIAL, skip_client_update=skip_outfit_change)
    if skip_outfit_change is False:
        sim_ev(sim_info).is_outfit_update_locked = True
        TurboSimUtil.CAS.set_current_outfit(sim_info, (TurboCASUtil.OutfitCategory.SPECIAL, 0))
        TurboSimUtil.CAS.update_previous_outfit(sim_info)
        sim_ev(sim_info).is_outfit_update_locked = False
        try:
            TurboSimUtil.CAS.refresh_outfit(sim_info)
        except:
            pass
    else:
        TurboSimUtil.CAS.set_outfit_category_dirty(sim_info, TurboCASUtil.OutfitCategory.SPECIAL, True)
    return strip_result


def dress_up_outfit(sim_identifier, override_outfit_category_and_index=None, skip_outfit_change=False):
    sim_name = TurboSimUtil.Name.get_name(sim_identifier)
    if is_sim_in_sex(sim_identifier) or is_sim_going_to_sex(sim_identifier):
        return -1
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    set_sim_top_naked_state(sim_info, False)
    set_sim_bottom_naked_state(sim_info, False)
    set_sim_top_underwear_state(sim_info, True if TurboSimUtil.Gender.is_female(sim_info) else False)
    set_sim_bottom_underwear_state(sim_info, True)
    sim_ev(sim_info).is_flashing = False
    if override_outfit_category_and_index is None:
        outfit_category_and_index = get_modified_outfit(sim_info)
        outfit_category_and_index = get_previous_modified_outfit(sim_info)
    else:
        outfit_category_and_index = override_outfit_category_and_index
    if outfit_category_and_index[0] == TurboCASUtil.OutfitCategory.BATHING or outfit_category_and_index[0] == TurboCASUtil.OutfitCategory.SPECIAL or not TurboSimUtil.CAS.has_outfit(sim_info, outfit_category_and_index):
        outfit_category_and_index = (TurboCASUtil.OutfitCategory.EVERYDAY, 0)
    if skip_outfit_change is False:
        TurboSimUtil.CAS.set_current_outfit(sim_info, outfit_category_and_index)
        TurboSimUtil.CAS.update_previous_outfit(sim_info)
    sim_ev(sim_info).has_original_outfit_modifications = False
    sim_ev(sim_info).original_outfit_category = -1
    sim_ev(sim_info).original_outfit_index = -1
    sim_ev(sim_info).is_flashing = False
    return outfit_category_and_index


@register_interaction_run_event_method(unique_id='WickedWhims')
def _wickedwhims_revert_outfit_on_lot_leave(interaction_instance):
    sim = TurboInteractionUtil.get_interaction_sim(interaction_instance)
    if sim_ev(sim).is_ready() and sim_ev(sim).has_original_outfit_modifications is True and TurboTypesUtil.Interactions.is_npc_leave_lot_interaction(interaction_instance):
        dress_up_outfit(sim)

