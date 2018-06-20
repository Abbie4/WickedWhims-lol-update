import random
from enums.buffs_enum import SimBuff
from turbolib.cas_util import TurboCASUtil
from turbolib.events.interactions import register_interaction_run_event_method
from turbolib.interaction_util import TurboInteractionUtil
from turbolib.manager_util import TurboManagerUtil
from turbolib.resource_util import TurboResourceUtil
from turbolib.sim_util import TurboSimUtil
from wickedwhims.nudity.nudity_settings import NuditySetting, get_nudity_setting
from wickedwhims.nudity.permissions.test import has_sim_permission_for_nudity
from wickedwhims.sxex_bridge.body import is_sim_outfit_fullbody, BodyState, get_sim_body_state, set_sim_bottom_naked_state, set_sim_top_naked_state
from wickedwhims.sxex_bridge.outfit import StripType, strip_outfit
from wickedwhims.utils_buffs import add_sim_buff
from wickedwhims.utils_cas import get_modified_outfit
from wickedwhims.utils_interfaces import display_notification
JUMPING_INTERACTIONS = (128702, 128703, 128704, 128705)

@register_interaction_run_event_method(unique_id='WickedWhims')
def _wickedwhims_undress_swimwear_on_jumping_to_water(interaction_instance):
    if not get_nudity_setting(NuditySetting.NUDITY_SWITCH_STATE, variable_type=bool):
        return
    interaction_guid = TurboResourceUtil.Resource.get_guid64(interaction_instance)
    if interaction_guid not in JUMPING_INTERACTIONS:
        return
    sim_info = TurboManagerUtil.Sim.get_sim_info(TurboInteractionUtil.get_interaction_sim(interaction_instance))
    if TurboSimUtil.Age.is_younger_than(sim_info, TurboSimUtil.Age.CHILD):
        return
    if get_modified_outfit(sim_info)[0] != TurboCASUtil.OutfitCategory.SWIMWEAR:
        return
    if is_sim_outfit_fullbody(sim_info):
        return
    if random.uniform(0, 1) > 0.1:
        return
    has_stripped = False
    if TurboSimUtil.Gender.is_male(sim_info):
        if get_sim_body_state(sim_info, 7) != BodyState.OUTFIT:
            return
        strip_result = strip_outfit(sim_info, strip_type_bottom=StripType.NUDE)
        if strip_result is True:
            set_sim_bottom_naked_state(sim_info, True)
            has_stripped = True
    else:
        can_undress_top = get_sim_body_state(sim_info, 6) == BodyState.OUTFIT
        can_undress_bottom = get_sim_body_state(sim_info, 7) == BodyState.OUTFIT
        undress_top = False
        undress_bottom = False
        if can_undress_top is True and can_undress_bottom is True:
            if bool(random.getrandbits(1)):
                undress_top = True
            else:
                undress_bottom = True
        elif can_undress_top is True:
            undress_top = True
        elif can_undress_bottom is True:
            undress_bottom = True
        if undress_top is False and undress_bottom is False:
            return
        if undress_top is True:
            strip_result = strip_outfit(sim_info, strip_type_top=StripType.NUDE)
            if strip_result is True:
                set_sim_top_naked_state(sim_info, True)
                has_stripped = True
        elif undress_bottom is True:
            strip_result = strip_outfit(sim_info, strip_type_bottom=StripType.NUDE)
            if strip_result is True:
                set_sim_bottom_naked_state(sim_info, True)
                has_stripped = True
    if has_stripped is True:
        display_notification(text=267480274, text_tokens=(sim_info,), secondary_icon=sim_info)
        if not has_sim_permission_for_nudity(sim_info)[0]:
            add_sim_buff(sim_info, SimBuff.OBJECT_JUMPSTAND_SWIMSUITMALFUNCTION)
        if random.uniform(0, 1) <= 0.45:
            add_sim_buff(sim_info, SimBuff.WW_NUDITY_TEMPORARY_BRAVE)

