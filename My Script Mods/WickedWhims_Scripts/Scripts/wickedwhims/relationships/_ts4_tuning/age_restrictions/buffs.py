'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''from event_testing.tests import CompoundTestListfrom turbolib.resource_util import TurboResourceUtilfrom turbolib.sim_util import TurboSimUtilfrom turbolib.tunable_util import TurboTunableUtilfrom wickedwhims.utils_tunings import modify_sim_info_test_agesTEENS_BUFFS_LIST = (103279, 98944, 102773, 104000, 12560, 12561, 12562, 12563, 75271, 113493, 102464, 102465, 102466, 102463, 102462, 97309, 97310, 97311)
def unlock_buffs_for_teens():
    buffs_manager = TurboResourceUtil.Services.get_instance_manager(TurboResourceUtil.ResourceTypes.BUFF)
    for buff_id in TEENS_BUFFS_LIST:
        buff_instance = TurboResourceUtil.Services.get_instance_from_manager(buffs_manager, buff_id)
        if buff_instance is None:
            pass
        buff_group_tests_list = list()
        for test_group in buff_instance._add_test_set:
            tests_list = list()
            for test in test_group:
                if TurboTunableUtil.Tests.SimInfo.is_sim_info_test(test) and TurboTunableUtil.Tests.SimInfo.is_age_test(test):
                    test = modify_sim_info_test_ages(test, add_ages=(TurboSimUtil.Age.TEEN,))
                tests_list.append(test)
            buff_group_tests_list.append(tuple(tests_list))
        buff_instance._add_test_set = CompoundTestList(list(buff_group_tests_list))
