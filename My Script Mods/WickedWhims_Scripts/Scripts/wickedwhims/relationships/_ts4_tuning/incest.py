from turbolib.resource_util import TurboResourceUtil
from wickedwhims.relationships._ts4_tuning.romance_affordances import get_romance_affordances
HAS_DISABLED_INTERACTIONS_INCEST_TEST = False

def unlock_incest_for_interactions(value):
    global HAS_DISABLED_INTERACTIONS_INCEST_TEST
    if value is True or HAS_DISABLED_INTERACTIONS_INCEST_TEST is True:
        return
    affordance_manager = TurboResourceUtil.Services.get_instance_manager(TurboResourceUtil.ResourceTypes.INTERACTION)
    for affordance_id in get_romance_affordances():
        affordance_instance = TurboResourceUtil.Services.get_instance_from_manager(affordance_manager, affordance_id)
        while not affordance_instance is None:
            if not hasattr(affordance_instance, 'test_incest'):
                pass
            affordance_instance.test_incest = False
    HAS_DISABLED_INTERACTIONS_INCEST_TEST = True

