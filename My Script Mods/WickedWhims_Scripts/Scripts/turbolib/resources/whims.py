from sims4.tuning.instance_manager import InstanceManager
from turbolib.injector_util import inject
from turbolib.resource_util import TurboResourceUtil
from turbolib.special.custom_exception_watcher import log_custom_exception
WHIM_REGISTRATION_CLASSES = list()

def register_whim_class():
    '''
    Use as a decorator on every WhimRegistration class to register it.
    '''

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
        '''
        Should be overridden to return a collection of tuples with whim ids and weights.
        :return: tuple or list or set -> collection of tuples with whim ids and weights that will be injected
        '''
        raise NotImplementedError

    def _get_whim_instances(self):
        '''
        :return: tuple -> whim instances from the get_whim_references method
        '''
        if self.whims:
            return tuple(self.whims)
        self.whims = list()
        whims_manager = TurboResourceUtil.Services.get_instance_manager(TurboResourceUtil.ResourceTypes.SITUATION_GOAL)
        for (whim_id, whim_weight) in self.get_whim_references():
            whim_instance = TurboResourceUtil.Services.get_instance_from_manager(whims_manager, whim_id)
            if whim_instance is None:
                pass
            immutable_slots_class = TurboResourceUtil.Collections.get_immutable_slots_class({'goal', 'weight'})
            whim_goal = immutable_slots_class(dict(goal=whim_instance, weight=whim_weight))
            self.whims.append(whim_goal)
        return tuple(self.whims)

    def get_whim_set_references(self):
        '''
        Should be overridden to return a collection of whim set ids.
        :return: tuple or list or set -> collection of whim set ids that will be injected
        '''
        raise NotImplementedError

    def _get_whim_set_instances(self, instance_manager):
        if self.whim_sets:
            return tuple(self.whim_sets)
        self.whim_sets = list()
        for whim_set_type in self.get_whim_set_references():
            key = TurboResourceUtil.ResourceTypes.get_resource_key(TurboResourceUtil.ResourceTypes.ASPIRATION, int(whim_set_type))
            whimset_instance = instance_manager._tuned_classes.get(key)
            if whimset_instance is None:
                pass
            self.whim_sets.append(whimset_instance)
        return tuple(self.whim_sets)


@inject(InstanceManager, 'load_data_into_class_instances')
def _turbolib_load_whims_into_whim_sets(original, self, *args, **kwargs):
    result = original(self, *args, **kwargs)
    if self.TYPE != TurboResourceUtil.ResourceTypes.ASPIRATION:
        return result
    for whim_class in WHIM_REGISTRATION_CLASSES:
        try:
            for whimset_instance in whim_class._get_whim_set_instances(self):
                whimset_instance.whims = whimset_instance.whims + whim_class._get_whim_instances()
        except Exception as ex:
            log_custom_exception("[TurboLib] Failed to run 'WhimRegistration' class at 'InstanceManager.load_data_into_class_instances'.", ex)
    return result

