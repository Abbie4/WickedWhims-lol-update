from event_testing.tests import TestList
from turbolib.resource_util import TurboResourceUtil
from wickedwhims.utils_tunings import create_impossible_sim_info_age_test
WOOHOO_AFFORDANCE_LIST = (103252, 120296, 119530, 125224, 123398, 154861, 13437, 13442, 117772, 13429, 172250, 104135, 119531, 123397, 125228, 154858, 152769, 152810, 140975, 13914, 13099, 117777, 14387, 172276, 105072, 119537, 125232, 123396, 154854, 97514, 14389, 13916, 117779, 123290, 172280, 99188, 99187, 38860, 119908, 123287, 125263, 125352, 172279, 110865, 119538, 154853, 105070, 119533, 123438, 125226, 152739, 154852, 26140, 117775, 26141, 122785, 37394, 26142, 172271, 104136, 119532, 123645, 125307, 152812, 152767, 154859, 13898, 13097, 14378, 117788, 172278, 120394, 105073, 105074, 119536, 119535, 123652, 123651, 125295, 125294, 154856, 154855, 14381, 14379, 123288, 13901, 13899, 117784, 97582, 97577, 117785, 123289, 172282, 172281, 105071, 119534, 123648, 125303, 154850, 152749, 119742, 26145, 119741, 122782, 119743, 37459, 172277)
HAS_DISABLED_WOOHOO_INTERACTIONS = False

def disable_woohoo_interactions(value):
    global HAS_DISABLED_WOOHOO_INTERACTIONS
    if value is True or HAS_DISABLED_WOOHOO_INTERACTIONS is True:
        return
    affordance_manager = TurboResourceUtil.Services.get_instance_manager(TurboResourceUtil.ResourceTypes.INTERACTION)
    for affordance_id in WOOHOO_AFFORDANCE_LIST:
        affordance_instance = TurboResourceUtil.Services.get_instance_from_manager(affordance_manager, affordance_id)
        if affordance_instance is None:
            pass
        while hasattr(affordance_instance, 'test_globals'):
            affordance_instance.test_globals = TestList((create_impossible_sim_info_age_test(),))
    HAS_DISABLED_WOOHOO_INTERACTIONS = True

