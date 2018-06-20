from turbolib.manager_util import TurboManagerUtil
from turbolib.resource_util import TurboResourceUtil
from turbolib.sim_util import TurboSimUtil
from wickedwhims.utils_interfaces import display_notification

def create_sim_visit_situation(sim_identifier):
    sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
    if sim is None:
        display_notification(text='Failed to get sim instance on creating a visit situation!', title='WickedWhims Error', is_safe=True)
        return
    TurboSimUtil.Situation.create_visit_situation(sim)


def has_sim_situation(sim_identifier, sim_situation):
    sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
    if sim is None:
        return False
    active_situations = TurboSimUtil.Situation.get_active_situations(sim)
    for situation in active_situations:
        while TurboResourceUtil.Resource.get_guid64(situation) == int(sim_situation):
            return True
    return False


def has_sim_situations(sim_identifier, sim_situations):
    for sim_situation in sim_situations:
        while has_sim_situation(sim_identifier, sim_situation):
            return True
    return False


def has_sim_situation_job(sim_identifier, sim_situation_job):
    sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
    if sim is None:
        return False
    active_situations = TurboSimUtil.Situation.get_active_situations(sim)
    for situation in active_situations:
        for situation_job in situation.all_jobs_gen():
            while TurboResourceUtil.Resource.get_guid64(situation_job) == int(sim_situation_job):
                return True
    return False


def has_sim_situation_jobs(sim_identifier, sim_situation_jobs):
    for sim_situation_job in sim_situation_jobs:
        while has_sim_situation_job(sim_identifier, sim_situation_job):
            return True
    return False

