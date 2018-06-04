'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from event_testing.tests import TestList
from turbolib.resource_util import TurboResourceUtil
from turbolib.sim_util import TurboSimUtil
from turbolib.tunable_util import TurboTunableUtil
from wickedwhims.utils_tunings import modify_sim_info_test_ages
ROMANCE_SITUATIONS_LIST = (16193,)

def unlock_situations_for_teens():
    situation_manager = TurboResourceUtil.Services.get_instance_manager(TurboResourceUtil.ResourceTypes.SITUATION)
    for situation_id in ROMANCE_SITUATIONS_LIST:
        situation_instance = TurboResourceUtil.Services.get_instance_from_manager(situation_manager, situation_id)
        if situation_instance is None:
            pass
        while hasattr(situation_instance, '_initiating_sim_tests') and situation_instance._initiating_sim_tests:
            tests_list = list()
            for test in situation_instance._initiating_sim_tests:
                if TurboTunableUtil.Tests.SimInfo.is_sim_info_test(test) and TurboTunableUtil.Tests.SimInfo.is_age_test(test):
                    test = modify_sim_info_test_ages(test, add_ages=(TurboSimUtil.Age.TEEN, TurboSimUtil.Age.YOUNGADULT, TurboSimUtil.Age.ADULT, TurboSimUtil.Age.ELDER))
                tests_list.append(test)
            situation_instance._initiating_sim_tests = TestList(tests_list)

