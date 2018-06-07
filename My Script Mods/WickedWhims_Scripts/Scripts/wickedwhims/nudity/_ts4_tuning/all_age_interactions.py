'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''from event_testing.tests import CompoundTestList, TestListfrom turbolib.events.core import register_zone_load_event_method, has_game_loadedfrom turbolib.resource_util import TurboResourceUtilfrom turbolib.sim_util import TurboSimUtilfrom turbolib.tunable_util import TurboTunableUtilfrom wickedwhims.utils_tunings import modify_sim_info_test_agesNUDITY_AFFORDANCE_LIST = (120455, 120453, 128625, 129163, 117339, 26878)
@register_zone_load_event_method(unique_id='WickedWhims', priority=5, late=True)
def _wickedwhims_enable_nudity_interactions_for_teens():
    if has_game_loaded():
        return
    affordance_manager = TurboResourceUtil.Services.get_instance_manager(TurboResourceUtil.ResourceTypes.INTERACTION)
    for affordance_id in NUDITY_AFFORDANCE_LIST:
        affordance_instance = TurboResourceUtil.Services.get_instance_from_manager(affordance_manager, affordance_id)
        if affordance_instance is None:
            pass
        if hasattr(affordance_instance, 'test_globals') and affordance_instance.test_globals:
            affordance_tests_list = list()
            for test in affordance_instance.test_globals:
                if TurboTunableUtil.Tests.SimInfo.is_sim_info_test(test) and TurboTunableUtil.Tests.SimInfo.is_age_test(test):
                    test = modify_sim_info_test_ages(test, add_ages=(TurboSimUtil.Age.TEEN,))
                affordance_tests_list.append(test)
            affordance_instance.test_globals = TestList(affordance_tests_list)
        if hasattr(affordance_instance, 'sim_tests') and affordance_instance.sim_tests:
            simtests_group_list = list()
            for test_group in affordance_instance.sim_tests:
                simtests_test_list = list()
                for test in test_group:
                    if TurboTunableUtil.Tests.SimInfo.is_sim_info_test(test) and TurboTunableUtil.Tests.SimInfo.is_age_test(test):
                        test = modify_sim_info_test_ages(test, add_ages=(TurboSimUtil.Age.TEEN,))
                    simtests_test_list.append(test)
                simtests_group_list.append(tuple(simtests_test_list))
            affordance_instance.sim_tests = CompoundTestList(simtests_group_list)
        while hasattr(affordance_instance, 'tests') and affordance_instance.tests:
            tests_group_list = list()
            for test_group in affordance_instance.tests:
                test_tests_list = list()
                for test in test_group:
                    if TurboTunableUtil.Tests.SimInfo.is_sim_info_test(test) and TurboTunableUtil.Tests.SimInfo.is_age_test(test):
                        test = modify_sim_info_test_ages(test, add_ages=(TurboSimUtil.Age.TEEN,))
                    test_tests_list.append(test)
                tests_group_list.append(tuple(test_tests_list))
            affordance_instance.tests = CompoundTestList(tests_group_list)
