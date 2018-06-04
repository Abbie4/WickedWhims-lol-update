'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from event_testing.tests import TestList
from turbolib.events.core import has_game_loaded, register_zone_load_event_method
from turbolib.events.interactions import manual_register_interaction_run_event_method
from turbolib.resource_util import TurboResourceUtil
from wickedwhims.utils_tunings import create_impossible_sim_info_age_test
DISABLE_AFFORDANCE_LIST = (128922, 129168, 128960, 142210, 17608706005782878675, 12431788248176075451, 10828959797335572444, 12516343241685269456, 16297228746575716883, 13258313599595875556, 16875503987194119605, 12636033218878615981, 17374295281070487723, 14656923424809181984, 16326278886595631926, 15286967377262639021, 14560787529546277264, 11684400009477505491, 15737321479036399539, 10472213825985425269, 10131617488783268407, 14095893074987087031, 11817165607087252481, 9406555401387075395, 10666333101205759175, 9615182269863451479, 12740796355475362029, 16467130614656358501, 11394497587744204993, 13177949309899868700, 12129102406248772938, 14626384720351351857, 15307547829518071061)

@register_zone_load_event_method(unique_id='WickedWhims', priority=5, late=True)
def _wickedwhims_disable_nudity_related_interactions():
    if has_game_loaded():
        return

    def _wickedwhims_not_right_in_front_of_my_salad(interaction_instance):
        interaction_guid = TurboResourceUtil.Resource.get_guid64(interaction_instance)
        if interaction_guid in (17608706005782878675, 12431788248176075451, 10828959797335572444, 12516343241685269456, 16297228746575716883, 13258313599595875556, 16875503987194119605, 12636033218878615981, 17374295281070487723, 14656923424809181984, 16326278886595631926, 15286967377262639021, 14560787529546277264, 11684400009477505491, 15737321479036399539, 10472213825985425269, 10131617488783268407, 14095893074987087031, 11817165607087252481, 9406555401387075395, 10666333101205759175, 9615182269863451479, 12740796355475362029, 16467130614656358501, 11394497587744204993, 13177949309899868700, 12129102406248772938, 14626384720351351857, 15307547829518071061):
            _affordance_instance = TurboResourceUtil.Services.get_instance(TurboResourceUtil.ResourceTypes.INTERACTION, affordance_id)
            if _affordance_instance is not None and hasattr(_affordance_instance, 'test_globals'):
                _affordance_instance.test_globals = TestList((create_impossible_sim_info_age_test(),))

    manual_register_interaction_run_event_method(_wickedwhims_not_right_in_front_of_my_salad, unique_id='WickedWhims')
    affordance_manager = TurboResourceUtil.Services.get_instance_manager(TurboResourceUtil.ResourceTypes.INTERACTION)
    for affordance_id in DISABLE_AFFORDANCE_LIST:
        affordance_instance = TurboResourceUtil.Services.get_instance_from_manager(affordance_manager, affordance_id)
        if affordance_instance is None:
            pass
        while hasattr(affordance_instance, 'test_globals'):
            affordance_instance.test_globals = TestList((create_impossible_sim_info_age_test(),))

