from enums.statistics_enum import SimCommodity
from enums.traits_enum import SimTrait
from turbolib.cas_util import TurboCASUtil
from turbolib.manager_util import TurboManagerUtil
from turbolib.sim_util import TurboSimUtil
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.sxex_bridge.body import get_sim_body_state, BodyState
from wickedwhims.utils_statistics import set_sim_statistic_value
from wickedwhims.utils_traits import has_sim_trait
UNDERWEAR_OUTFITS = (TurboCASUtil.OutfitCategory.EVERYDAY, TurboCASUtil.OutfitCategory.FORMAL, TurboCASUtil.OutfitCategory.ATHLETIC, TurboCASUtil.OutfitCategory.PARTY, TurboCASUtil.OutfitCategory.CAREER, TurboCASUtil.OutfitCategory.SITUATION, TurboCASUtil.OutfitCategory.SPECIAL)

def is_underwear_outfit(outfit_category):
    return outfit_category in UNDERWEAR_OUTFITS


def set_sim_top_underwear_state(sim_identifier, state):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    set_sim_statistic_value(sim_info, 1 if state is True else 0, SimCommodity.WW_NUDITY_IS_TOP_UNDERWEAR)
    sim_ev(sim_info).underwear_flags['top'] = state


def set_sim_bottom_underwear_state(sim_identifier, state):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    set_sim_statistic_value(sim_info, 1 if state is True else 0, SimCommodity.WW_NUDITY_IS_BOTTOM_UNDERWEAR)
    sim_ev(sim_info).underwear_flags['bottom'] = state


def is_sim_top_underwear(sim_identifier):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    return sim_ev(sim_info).underwear_flags['top']


def is_sim_bottom_underwear(sim_identifier):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    return sim_ev(sim_info).underwear_flags['bottom']


def update_sim_underwear_data(sim_identifier):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    current_outfit_category = TurboSimUtil.CAS.get_current_outfit(sim_info)[0]
    if current_outfit_category == TurboCASUtil.OutfitCategory.SPECIAL:
        return
    from wickedwhims.nudity.nudity_settings import get_nudity_setting, NuditySetting
    if get_nudity_setting(NuditySetting.UNDERWEAR_SWITCH_STATE, variable_type=bool) and not has_sim_trait(sim_info, SimTrait.WW_NO_UNDERWEAR) and is_underwear_outfit(current_outfit_category):
        set_sim_top_underwear_state(sim_info, True if TurboSimUtil.Gender.is_female(sim_info) else False)
        set_sim_bottom_underwear_state(sim_info, True)
        top_state = get_sim_body_state(sim_info, 6)
        bottom_state = get_sim_body_state(sim_info, 7)
        if top_state == BodyState.UNDERWEAR:
            set_sim_top_underwear_state(sim_info, True)
        elif top_state == BodyState.NUDE:
            set_sim_top_underwear_state(sim_info, False)
        if bottom_state == BodyState.UNDERWEAR:
            set_sim_bottom_underwear_state(sim_info, True)
        else:
            set_sim_bottom_underwear_state(sim_info, False)
    else:
        set_sim_top_underwear_state(sim_info, False)
        set_sim_bottom_underwear_state(sim_info, False)

