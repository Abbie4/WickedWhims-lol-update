from sims4.tuning.instance_manager import InstanceManager
from turbolib.injector_util import inject
from turbolib.resource_util import TurboResourceUtil
from turbolib.special.custom_exception_watcher import log_custom_exception, log_message
WHIM_REGISTRATION_CLASSES = list()


def register_whim_class():
    def _wrapper(whim_class):
        WHIM_REGISTRATION_CLASSES.append(whim_class())
        return whim_class

    return _wrapper


class WhimRegistration:
    __qualname__ = 'WhimRegistration'

    def __init__(self):
        self.whims = None
        self.whim_sets = None

    def get_whim_references(self):
        log_message("inccorectly grabbing whim_references: " + self.__class__.__name__)
        raise NotImplementedError

    def _get_whim_instances(self):
        log_message("getting whims for: " + self.__class__.__name__)
        if self.whims:
            return tuple(self.whims)
        log_message("whims found for: " + self.__class__.__name__)
        self.whims = list()
        whims_manager = TurboResourceUtil.Services.get_instance_manager(TurboResourceUtil.ResourceTypes.SITUATION_GOAL)
        whim_references = self.get_whim_references()
        try:
            for (whim_id, whim_weight) in whim_references:
                whim_instance = TurboResourceUtil.Services.get_instance_from_manager(whims_manager, whim_id)
                if whim_instance is None:
                    pass
                immutable_slots_class = TurboResourceUtil.Collections.get_immutable_slots_class({'goal', 'weight'})
                whim_goal = immutable_slots_class(dict(goal=whim_instance, weight=whim_weight))
                self.whims.append(whim_goal)
            log_message("finishing whims for: " + self.__class__.__name__)
        except TypeError as te:
            whim_id = whim_references[0]
            whim_weight = whim_references[1]
            whim_instance = TurboResourceUtil.Services.get_instance_from_manager(whims_manager, whim_id)
            if whim_instance is None:
                return tuple(self.whims)
            immutable_slots_class = TurboResourceUtil.Collections.get_immutable_slots_class({'goal', 'weight'})
            whim_goal = immutable_slots_class(dict(goal=whim_instance, weight=whim_weight))
            self.whims.append(whim_goal)
            log_message("finishing whims for two: " + self.__class__.__name__)
        log_message("done with whims: " + self.__class__.__name__)
        return tuple(self.whims)

    def get_whim_set_references(self):
        raise NotImplementedError

    def _get_whim_set_instances(self, instance_manager):
        log_message("getting whimsets for: " + self.__class__.__name__)
        if self.whim_sets:
            return tuple(self.whim_sets)
        log_message("whimsets found for: " + self.__class__.__name__)
        self.whim_sets = list()
        whim_set_references = self.get_whim_set_references()
        log_message("looking at whimsets: " + self.__class__.__name__)
        try:
            for whim_set_type in whim_set_references:
                key = TurboResourceUtil.ResourceTypes.get_resource_key(TurboResourceUtil.ResourceTypes.ASPIRATION, int(whim_set_type))
                whimset_instance = instance_manager._tuned_classes.get(key)
                if whimset_instance is None:
                    pass
                self.whim_sets.append(whimset_instance)
            log_message("finishing whimsets for: " + self.__class__.__name__)
        except TypeError as te:
            key = TurboResourceUtil.ResourceTypes.get_resource_key(TurboResourceUtil.ResourceTypes.ASPIRATION, int(whim_set_references))
            whimset_instance = instance_manager._tuned_classes.get(key)
            if whimset_instance is None:
                pass
            self.whim_sets.append(whimset_instance)
            log_message("finishing whimsets for two: " + self.__class__.__name__)
        log_message("done with whimsets: " + self.__class__.__name__)
        return tuple(self.whim_sets)


@inject(InstanceManager, 'load_data_into_class_instances')
def _turbolib_load_whims_into_whim_sets(original, self, *args, **kwargs):
    result = original(self, *args, **kwargs)
    if self.TYPE != TurboResourceUtil.ResourceTypes.ASPIRATION:
        return result
    for whim_class in WHIM_REGISTRATION_CLASSES:
        log_message("starting whim class: " + whim_class.__class__.__name__)
        try:
            for whimset_instance in whim_class._get_whim_set_instances(self):
                log_message("looking at: " + self.__class__.__name__ + " " + whimset_instance)
                whimsetWhims = whimset_instance.whims
                whimInstances = whim_class._get_whim_instances()
                whimset_instance.whims = whimsetWhims + whimInstances
                log_message("done with whim instance: " + self.__class__.__name__ + " " + whimset_instance)
        except Exception as ex:
            log_custom_exception("[TurboLib] Failed to run 'WhimRegistration' class at 'InstanceManager.load_data_into_class_instances'." + whim_class.__class__.__name__, ex)
        log_message("done with whim class: " + whim_class.__class__.__name__)
    return result

