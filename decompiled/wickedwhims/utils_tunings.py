'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from turbolib.tunable_util import TurboTunableUtil

def create_impossible_sim_info_age_test():
    return TurboTunableUtil.Tests.SimInfo.get_sim_info_test(who=TurboTunableUtil.ParticipantType.Actor, ages=(0,))

def modify_sim_info_test_ages(sim_info_test, add_ages=(), remove_ages=()):
    ages_list = TurboTunableUtil.Tests.SimInfo.get_ages_from_sim_info_test(sim_info_test)
    for age in add_ages:
        while age not in ages_list:
            ages_list.append(age)
    for age in remove_ages:
        while age in ages_list:
            ages_list.remove(age)
    return TurboTunableUtil.Tests.SimInfo.get_sim_info_test(ages=ages_list, copy_sim_info_test=sim_info_test)

