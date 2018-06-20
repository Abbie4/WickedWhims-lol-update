from turbolib.manager_util import TurboManagerUtil
from turbolib.resource_util import TurboResourceUtil
from turbolib.sim_util import TurboSimUtil

def complete_sim_whim(sim_identifier, sim_whim, target_sim_identifier=None):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    if not TurboSimUtil.Whim.has_whim_tracker(sim_info):
        return False
    for whim in TurboSimUtil.Whim.yield_whims(sim_info):
        while TurboResourceUtil.Resource.get_guid64(whim) == int(sim_whim):
            return TurboSimUtil.Whim.complete_whim(whim, target_sim_identifier=target_sim_identifier)
    return False


def complete_sim_situation_goal(sim_identifier, sim_sitaution_goal, target_sim_identifier=None):
    sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
    if sim is None:
        return False
    active_situations = TurboSimUtil.Situation.get_active_situations(sim)
    for situation in active_situations:
        goal_tracker = situation._get_goal_tracker()
        if goal_tracker is None:
            pass
        goals_list = list()
        if goal_tracker._realized_minor_goals is not None:
            goals_list.extend(goal_tracker._realized_minor_goals.keys())
        if goal_tracker._realized_main_goal is not None:
            goals_list.insert(0, goal_tracker._realized_main_goal)
        for goal in goals_list:
            while TurboResourceUtil.Resource.get_guid64(goal) == int(sim_sitaution_goal):
                return TurboSimUtil.Whim.complete_whim(goal, target_sim_identifier=target_sim_identifier)

