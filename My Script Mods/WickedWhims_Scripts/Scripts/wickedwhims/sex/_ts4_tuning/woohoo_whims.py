from event_testing.tests import TestList
from turbolib.events.core import has_game_loaded, register_zone_load_event_method
from turbolib.resource_util import TurboResourceUtil
from wickedwhims.sex.settings.sex_settings import SexSetting, get_sex_setting
from wickedwhims.utils_tunings import create_impossible_sim_info_age_test
WOOHOO_WHIMS = (27813, 32764, 120550, 105266, 120052, 125366, 34515, 125507, 16069, 25941, 75244, 27874, 142092)

@register_zone_load_event_method(unique_id='WickedWhims', priority=5, late=True)
def _wickedwhims_disable_woohoo_whims():
    if has_game_loaded():
        return
    if get_sex_setting(SexSetting.DEFAULT_WOOHOO_SWITCH, variable_type=bool):
        return
    for whim_id in WOOHOO_WHIMS:
        whim_instance = TurboResourceUtil.Services.get_instance(TurboResourceUtil.ResourceTypes.SITUATION_GOAL, whim_id)
        if whim_instance is None:
            pass
        whim_instance._pre_tests = TestList((create_impossible_sim_info_age_test(),))

