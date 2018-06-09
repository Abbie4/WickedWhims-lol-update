from turbolib.manager_util import TurboManagerUtil
from turbolib.sim_util import TurboSimUtil
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.utils_sims import is_sim_available

def is_sim_in_sex(sim_identifier):
    if sim_ev(sim_identifier).active_sex_handler is not None:
        return True
    return False


def is_sim_going_to_sex(sim_identifier):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    if sim_ev(sim_info).is_ready_to_sex is True or sim_ev(sim_info).is_in_process_to_sex is True:
        return True
    return False


def is_sim_ready_for_sex(sim_identifier):
    sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
    if sim_ev(sim).active_sex_handler is not None:
        return False
    if sim_ev(sim).is_ready_to_sex is True:
        return False
    if TurboSimUtil.Age.is_younger_than(sim, TurboSimUtil.Age.TEEN):
        return False
    if not is_sim_available(sim):
        return False
    return True


def is_sim_planning_for_sex(sim_identifier):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    if sim_ev(sim_info).active_pre_sex_handler is not None:
        return True
    return False

