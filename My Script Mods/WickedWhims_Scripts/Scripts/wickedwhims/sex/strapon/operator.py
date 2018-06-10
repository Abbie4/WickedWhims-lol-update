from turbolib.manager_util import TurboManagerUtil
from wickedwhims.main.cas_config_handler import get_strapon_part_ids, get_child_strapon_part_ids
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.sxex_bridge.body import get_sim_body_state, AdditionalBodyState, get_sim_additional_body_state
from turbolib.sim_util import TurboSimUtil
HAS_STARPON_LOADED = None
DEFAULT_STRAPON_PART_ID = -1
DEFAULT_CHILD_STRAPON_PART_ID = -1


def has_loaded_strapon():
    global HAS_STARPON_LOADED, DEFAULT_STRAPON_PART_ID, DEFAULT_CHILD_STRAPON_PART_ID
    if HAS_STARPON_LOADED is not None:
        return HAS_STARPON_LOADED
    HAS_STARPON_LOADED = False
    strapon_cas_id_parts_list = get_strapon_part_ids()
    child_strapon_cas_id_parts_list = get_child_strapon_part_ids()
    if strapon_cas_id_parts_list:
        HAS_STARPON_LOADED = True
        DEFAULT_STRAPON_PART_ID = int(strapon_cas_id_parts_list[0])
    if child_strapon_cas_id_parts_list:
        HAS_STARPON_LOADED = True
        DEFAULT_CHILD_STRAPON_PART_ID = int(child_strapon_cas_id_parts_list[0])
    return HAS_STARPON_LOADED


def is_strapon_on_sim(sim_identifier):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    return get_sim_additional_body_state(sim_info, 7, get_sim_body_state(sim_info, 7)) == AdditionalBodyState.STRAPON


def get_sim_strapon_part_id(sim_identifier):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    sim_is_child = TurboSimUtil.Age.get_age(sim_info) == TurboSimUtil.Age.CHILD
    sim_strapon_part_id = sim_ev(sim_info).strapon_part_id
    if sim_is_child:
        sim_ev(sim_info).strapon_part_id = DEFAULT_CHILD_STRAPON_PART_ID
    elif sim_strapon_part_id == -1:
        sim_ev(sim_info).strapon_part_id = DEFAULT_STRAPON_PART_ID
    return sim_ev(sim_info).strapon_part_id

