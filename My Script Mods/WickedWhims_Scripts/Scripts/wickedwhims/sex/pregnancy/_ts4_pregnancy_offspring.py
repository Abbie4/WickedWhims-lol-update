from sims.pregnancy.pregnancy_tracker import PregnancyTracker
from turbolib.injector_util import inject
from turbolib.sim_util import TurboSimUtil
from turbolib.special.custom_exception_watcher import log_custom_exception

@inject(PregnancyTracker, 'create_sim_info')
def _wickedwhims_on_pregnancy_create_sim_info(original, self, *args, **kwargs):
    result = None
    try:
        (parent_a, parent_b) = self.get_parents()
        parent_a_age = TurboSimUtil.Age.get_age(parent_a)
        if parent_a_age == TurboSimUtil.Age.TEEN or parent_a_age == TurboSimUtil.Age.CHILD:
            parent_a.age = TurboSimUtil.Age.YOUNGADULT
            parent_a._base.update_for_age(TurboSimUtil.Age.YOUNGADULT)
        parent_b_age = TurboSimUtil.Age.get_age(parent_b)
        if parent_b_age == TurboSimUtil.Age.TEEN or parent_b_age == TurboSimUtil.Age.CHILD:
            parent_b.age = TurboSimUtil.Age.YOUNGADULT
            parent_b._base.update_for_age(TurboSimUtil.Age.YOUNGADULT)
        result = original(self, *args, **kwargs)
        if parent_a_age == TurboSimUtil.Age.TEEN or parent_a_age == TurboSimUtil.Age.CHILD:
            parent_a.age = parent_a_age
            parent_a._base.update_for_age(parent_a_age)
        if parent_b_age == TurboSimUtil.Age.TEEN or parent_b_age == TurboSimUtil.Age.CHILD:
            parent_b.age = parent_b_age
            parent_b._base.update_for_age(parent_b_age)
    except Exception as ex:
        log_custom_exception("Failed to create new sim 'PregnancyTracker.create_sim_info'.", ex)
    return result or original(self, *args, **kwargs)

