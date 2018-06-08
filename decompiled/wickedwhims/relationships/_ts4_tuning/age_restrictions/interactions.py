'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from event_testing.tests import TestList, CompoundTestList
from turbolib.resource_util import TurboResourceUtil
from turbolib.sim_util import TurboSimUtil
from turbolib.tunable_util import TurboTunableUtil
from wickedwhims.relationships._ts4_tuning.age_restrictions.buffs import unlock_buffs_for_teens
from wickedwhims.relationships._ts4_tuning.age_restrictions.disable_interactions import disable_duplicate_interactions
from wickedwhims.relationships._ts4_tuning.age_restrictions.sims_filters import unlock_sims_filters_for_teens
from wickedwhims.relationships._ts4_tuning.age_restrictions.situations import unlock_situations_for_teens
from wickedwhims.relationships._ts4_tuning.age_restrictions.test_sets import unlock_testsets_for_teens
from wickedwhims.relationships._ts4_tuning.romance_affordances import get_romance_affordances
from wickedwhims.utils_tunings import modify_sim_info_test_ages
HAS_DISABLED_ROMANCE_AGE_RESTRICTION_TESTS = False

def remove_romance_age_restrictions(value):
    global HAS_DISABLED_ROMANCE_AGE_RESTRICTION_TESTS
    if value is False or HAS_DISABLED_ROMANCE_AGE_RESTRICTION_TESTS is True:
        return
    affordance_manager = TurboResourceUtil.Services.get_instance_manager(TurboResourceUtil.ResourceTypes.INTERACTION)
    snippet_manager = TurboResourceUtil.Services.get_instance_manager(TurboResourceUtil.ResourceTypes.SNIPPET)
    default_age_test = TurboResourceUtil.Services.get_instance_from_manager(snippet_manager, 100790)
    only_teen_age_test = TurboResourceUtil.Services.get_instance_from_manager(snippet_manager, 74830)
    teen_adult_test = TurboResourceUtil.Services.get_instance_from_manager(snippet_manager, 16594383779498847541)
    for affordance_id in get_romance_affordances():
        affordance_instance = TurboResourceUtil.Services.get_instance_from_manager(affordance_manager, affordance_id)
        if affordance_instance is None:
            pass
        if hasattr(affordance_instance, 'test_globals') and affordance_instance.test_globals:
            tests_list = list()
            for test in affordance_instance.test_globals:
                if test is only_teen_age_test:
                    pass
                if test is default_age_test:
                    test = teen_adult_test
                elif TurboTunableUtil.Tests.SimInfo.is_sim_info_test(test) and TurboTunableUtil.Tests.SimInfo.is_age_test(test):
                    test = modify_sim_info_test_ages(test, add_ages=(TurboSimUtil.Age.CHILD, TurboSimUtil.Age.TEEN, TurboSimUtil.Age.YOUNGADULT, TurboSimUtil.Age.ADULT, TurboSimUtil.Age.ELDER))
                tests_list.append(test)
            affordance_instance.test_globals = TestList(tests_list)
        while hasattr(affordance_instance, 'tests') and affordance_instance.tests:
            tests_group_list = list()
            for test_group in affordance_instance.tests:
                test_tests_list = list()
                for test in test_group:
                    if test is only_teen_age_test:
                        pass
                    if test is default_age_test:
                        test = teen_adult_test
                    elif TurboTunableUtil.Tests.SimInfo.is_sim_info_test(test) and TurboTunableUtil.Tests.SimInfo.is_age_test(test):
                        test = modify_sim_info_test_ages(test, add_ages=(TurboSimUtil.Age.CHILD, TurboSimUtil.Age.TEEN, TurboSimUtil.Age.YOUNGADULT, TurboSimUtil.Age.ADULT, TurboSimUtil.Age.ELDER))
                    test_tests_list.append(test)
                tests_group_list.append(tuple(test_tests_list))
            affordance_instance.tests = CompoundTestList(tests_group_list)
    unlock_buffs_for_teens()
    unlock_testsets_for_teens()
    unlock_sims_filters_for_teens()
    unlock_situations_for_teens()
    disable_duplicate_interactions()
    HAS_DISABLED_ROMANCE_AGE_RESTRICTION_TESTS = True

