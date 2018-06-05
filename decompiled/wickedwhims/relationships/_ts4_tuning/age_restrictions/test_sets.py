'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from event_testing.tests import CompoundTestList
from turbolib.resource_util import TurboResourceUtil
from turbolib.sim_util import TurboSimUtil
from turbolib.tunable_util import TurboTunableUtil
from wickedwhims.utils_tunings import modify_sim_info_test_ages
TEENS_TEST_SETS = (100585, 100793, 129094)

def unlock_testsets_for_teens():
    snippet_manager = TurboResourceUtil.Services.get_instance_manager(TurboResourceUtil.ResourceTypes.SNIPPET)
    for snippet_id in TEENS_TEST_SETS:
        snippet_instance = TurboResourceUtil.Services.get_instance_from_manager(snippet_manager, snippet_id)
        if snippet_instance is None:
            pass
        testset_groups_list = list()
        for test_group in snippet_instance.test:
            tests_list = list()
            for test in test_group:
                if TurboTunableUtil.Tests.SimInfo.is_sim_info_test(test) and TurboTunableUtil.Tests.SimInfo.is_age_test(test):
                    test = modify_sim_info_test_ages(test, add_ages=(TurboSimUtil.Age.CHILD, TurboSimUtil.Age.TEEN,))
                tests_list.append(test)
            testset_groups_list.append(tuple(tests_list))
        snippet_instance.test = CompoundTestList(list(testset_groups_list))

