'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from event_testing.tests import TestList
from interactions.utils.outcome import InteractionOutcomeNone
from turbolib.events.core import has_game_loaded, register_zone_load_event_method
from turbolib.resource_util import TurboResourceUtil
from turbolib.sim_util import TurboSimUtil
from turbolib.tunable_util import TurboTunableUtil
from wickedwhims.utils_tunings import modify_sim_info_test_ages
SHARE_PREGNANCY_NEWS_INTERACTION = 28831

@register_zone_load_event_method(unique_id='WickedWhims', priority=5, late=True)
def _wickedwhims_disable_share_pregnancy_news_interaction_for_teens():
    if has_game_loaded():
        return
    affordance_instance = TurboResourceUtil.Services.get_instance(TurboResourceUtil.ResourceTypes.INTERACTION, SHARE_PREGNANCY_NEWS_INTERACTION)
    if affordance_instance is None:
        return
    if hasattr(affordance_instance, 'test_globals') and affordance_instance.test_globals:
        tests_list = list()
        for test in affordance_instance.test_globals:
            if TurboTunableUtil.Tests.SimInfo.is_sim_info_test(test) and TurboTunableUtil.Tests.SimInfo.is_age_test(test):
                test = modify_sim_info_test_ages(test, remove_ages=(TurboSimUtil.Age.TEEN, TurboSimUtil.Age.CHILD))
            tests_list.append(test)
        affordance_instance.test_globals = TestList(tests_list)

PREGNANCY_START_SHOWING_INTERACTION = 13831

@register_zone_load_event_method(unique_id='WickedWhims', priority=5, late=True)
def _wickedwhims_disable_pregnancy_start_interaction_outcome():
    if has_game_loaded():
        return
    affordance_instance = TurboResourceUtil.Services.get_instance(TurboResourceUtil.ResourceTypes.INTERACTION, PREGNANCY_START_SHOWING_INTERACTION)
    if affordance_instance is None:
        return
    if hasattr(affordance_instance, 'outcome'):
        affordance_instance.outcome = InteractionOutcomeNone()

PREGNANCY_FAMILY_LEAVE_NOTIFICATION_LOOT = 110613

@register_zone_load_event_method(unique_id='WickedWhims', priority=5, late=True)
def _wickedwhims_disable_pregnancy_family_leave_notification_loot():
    if has_game_loaded():
        return
    action_instance = TurboResourceUtil.Services.get_instance(TurboResourceUtil.ResourceTypes.ACTION, PREGNANCY_FAMILY_LEAVE_NOTIFICATION_LOOT)
    if action_instance is None:
        return
    if hasattr(action_instance, 'loot_actions'):
        action_instance.loot_actions = ()

