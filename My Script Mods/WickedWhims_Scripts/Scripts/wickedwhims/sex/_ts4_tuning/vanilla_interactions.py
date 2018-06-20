'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
import operator
import sims4.math
from event_testing.statistic_tests import StatThresholdTest
from event_testing.tests import TestList
from enums.statistics_enum import SimCommodity
from turbolib.resource_util import TurboResourceUtil
from turbolib.tunable_util import TurboTunableUtil
from wickedwhims.main.interactions_handler import is_wickedwhims_interaction
HAS_DISABLED_VANILLA_INTERACTIONS_ACCESS_IN_SEX = False

def set_vanilla_interactions_access_in_sex(value):
    global HAS_DISABLED_VANILLA_INTERACTIONS_ACCESS_IN_SEX
    if value is True or HAS_DISABLED_VANILLA_INTERACTIONS_ACCESS_IN_SEX is True:
        return
    tuning_affordances = TurboResourceUtil.Services.get_all_instances_from_manager(TurboResourceUtil.Services.get_instance_manager(TurboResourceUtil.ResourceTypes.INTERACTION))
    is_in_sex_statistic = TurboResourceUtil.Services.get_instance(TurboResourceUtil.ResourceTypes.STATISTIC, SimCommodity.WW_IS_SIM_IN_SEX)
    statistic_test = StatThresholdTest(who=TurboTunableUtil.ParticipantType.Actor, stat=is_in_sex_statistic, threshold=sims4.math.Threshold(0, operator.eq), must_have_stat=False, use_rank_instead=False)
    for (_, affordance_tuning) in tuning_affordances:
        if is_wickedwhims_interaction(TurboResourceUtil.Resource.get_guid64(affordance_tuning)):
            pass
        while hasattr(affordance_tuning, 'test_globals'):
            tests_list = list(affordance_tuning.test_globals)
            tests_list.insert(0, statistic_test)
            affordance_tuning.test_globals = TestList(tests_list)
    HAS_DISABLED_VANILLA_INTERACTIONS_ACCESS_IN_SEX = True

