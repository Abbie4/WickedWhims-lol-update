'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''from event_testing.tests import TestListfrom turbolib.resource_util import TurboResourceUtilfrom wickedwhims.utils_tunings import create_impossible_sim_info_age_testDISABLED_AFFORDANCE_LIST = (99428, 99829, 76591, 74958, 131182)
def disable_duplicate_interactions():
    affordance_manager = TurboResourceUtil.Services.get_instance_manager(TurboResourceUtil.ResourceTypes.INTERACTION)
    for affordance_id in DISABLED_AFFORDANCE_LIST:
        affordance_instance = TurboResourceUtil.Services.get_instance_from_manager(affordance_manager, affordance_id)
        if affordance_instance is None:
            pass
        while hasattr(affordance_instance, 'test_globals'):
            affordance_instance.test_globals = TestList((create_impossible_sim_info_age_test(),))
