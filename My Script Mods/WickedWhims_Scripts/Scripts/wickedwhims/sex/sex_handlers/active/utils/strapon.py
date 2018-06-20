from enums.traits_enum import SimTrait
from turbolib.cas_util import TurboCASUtil
from turbolib.manager_util import TurboManagerUtil
from turbolib.sim_util import TurboSimUtil
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.sex.enums.sex_gender import SexGenderType
from wickedwhims.sex.settings.sex_settings import SexSetting, get_sex_setting, SexUndressingLevelSetting
from wickedwhims.sex.strapon.operator import has_loaded_strapon, get_sim_strapon_part_id, is_strapon_on_sim
from wickedwhims.sxex_bridge.body import is_sim_outfit_fullbody, set_sim_top_naked_state, set_sim_bottom_naked_state, get_sim_actual_body_state, BodyState
from wickedwhims.sxex_bridge.outfit import StripType, strip_outfit
from wickedwhims.sxex_bridge.underwear import is_underwear_outfit, is_sim_top_underwear, set_sim_top_underwear_state, set_sim_bottom_underwear_state
from wickedwhims.utils_cas import set_bodytype_caspart, get_modified_outfit
from wickedwhims.utils_traits import has_sim_trait

def update_stapon(sim_identifier, actor_data=None, is_npc_only=False, force_remove=False):
    if not has_loaded_strapon():
        return False
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    if force_remove is True and is_strapon_on_sim(sim_info):
        _undress_bottom(sim_info)
        return False
    if is_npc_only is False:
        undressing_type = get_sex_setting(SexSetting.SEX_UNDRESSING_TYPE, variable_type=int)
    else:
        undressing_type = get_sex_setting(SexSetting.NPC_SEX_UNDRESSING_TYPE, variable_type=int)
    if has_sim_trait(sim_info, SimTrait.GENDEROPTIONS_TOILET_STANDING):
        return False
    if sim_ev(sim_info).is_strapon_allowed is False:
        if get_sex_setting(SexSetting.STRAPON_AUTO_REMOVE_STATE, variable_type=bool) and is_strapon_on_sim(sim_info):
            _undress_bottom(sim_info)
        return False
    allows_strapon = False
    if actor_data is not None and actor_data.is_allowing_strapon():
        allows_strapon = True
    elif actor_data is not None and actor_data.get_final_gender_type() == SexGenderType.MALE:
        allows_strapon = True
    if is_strapon_on_sim(sim_info):
        if allows_strapon is False and get_sex_setting(SexSetting.STRAPON_AUTO_REMOVE_STATE, variable_type=bool):
            _undress_bottom(sim_info)
            return False
        return True
    if allows_strapon is False:
        return False
    if undressing_type == SexUndressingLevelSetting.DISABLED and get_sim_actual_body_state(sim_info, TurboCASUtil.BodyType.LOWER_BODY) != BodyState.NUDE:
        return False
    _undress_bottom(sim_info)
    set_bodytype_caspart(sim_info, (TurboCASUtil.OutfitCategory.SPECIAL, 0), TurboCASUtil.BodyType.LOWER_BODY, get_sim_strapon_part_id(sim_info))
    try:
        TurboSimUtil.CAS.refresh_outfit(sim_info)
    except:
        pass


def _undress_bottom(sim_info):
    has_top_underwear_on = TurboSimUtil.Gender.is_female(sim_info) and (is_underwear_outfit(get_modified_outfit(sim_info)[0]) and is_sim_top_underwear(sim_info))
    strip_type_top = StripType.NONE if not is_sim_outfit_fullbody(sim_info) else StripType.UNDERWEAR if has_top_underwear_on else StripType.NUDE
    strip_outfit(sim_info, strip_type_top=strip_type_top, strip_type_bottom=StripType.NUDE)
    set_sim_top_naked_state(sim_info, strip_type_top == StripType.NUDE)
    set_sim_bottom_naked_state(sim_info, True)
    set_sim_top_underwear_state(sim_info, strip_type_top == StripType.UNDERWEAR)
    set_sim_bottom_underwear_state(sim_info, False)

