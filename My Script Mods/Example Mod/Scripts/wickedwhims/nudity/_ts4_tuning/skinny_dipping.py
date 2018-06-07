'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''from event_testing.tests import CompoundTestListfrom turbolib.events.core import register_zone_load_event_method, has_game_loadedfrom turbolib.resource_util import TurboResourceUtilfrom turbolib.sim_util import TurboSimUtilfrom turbolib.tunable_util import TurboTunableUtilfrom wickedwhims.utils_tunings import modify_sim_info_test_agesSKINNY_DIPPING_TESTSET = 129064
@register_zone_load_event_method(unique_id='WickedWhims', priority=5, late=True)
def _wickedwhims_allow_skinny_dipping_for_all_age():
    if has_game_loaded():
        return
    snippet_instance = TurboResourceUtil.Services.get_instance(TurboResourceUtil.ResourceTypes.SNIPPET, SKINNY_DIPPING_TESTSET)
    if snippet_instance is None:
        return
    testset_group_list = list()
    for test_group in snippet_instance.test:
        testset_test_list = list()
        for test in test_group:
            if TurboTunableUtil.Tests.SimInfo.is_sim_info_test(test) and TurboTunableUtil.Tests.SimInfo.is_age_test(test):
                test = modify_sim_info_test_ages(test, add_ages=(TurboSimUtil.Age.BABY, TurboSimUtil.Age.TODDLER, TurboSimUtil.Age.CHILD, TurboSimUtil.Age.TEEN))
            testset_test_list.append(test)
        testset_group_list.append(tuple(testset_test_list))
    snippet_instance.test = CompoundTestList(list(testset_group_list))
