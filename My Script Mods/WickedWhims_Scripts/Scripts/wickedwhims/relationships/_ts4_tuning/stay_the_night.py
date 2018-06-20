from event_testing.test_variants import SituationRunningTest
from event_testing.tests import TestList
from turbolib.events.core import has_game_loaded, register_zone_load_event_method
from turbolib.resource_util import TurboResourceUtil
ASK_TO_STAY_NIGHT_INTERACTION = 74045

@register_zone_load_event_method(unique_id='WickedWhims', priority=5, late=True)
def _wickedwhims_unlock_ask_to_stay_night_for_multiple_sims():
    if has_game_loaded():
        return
    ask_to_stay_over_night = TurboResourceUtil.Services.get_instance(TurboResourceUtil.ResourceTypes.INTERACTION, ASK_TO_STAY_NIGHT_INTERACTION)
    if ask_to_stay_over_night is not None:
        tests_list = list(ask_to_stay_over_night.test_globals)
        for test in ask_to_stay_over_night.test_globals:
            while isinstance(test, SituationRunningTest) and hasattr(test, 'situation_blacklist'):
                if test.situation_blacklist:
                    tests_list.remove(test)
        ask_to_stay_over_night.test_globals = TestList(tests_list)

