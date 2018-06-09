from turbolib.events.core import has_game_loaded, register_zone_load_event_method
from turbolib.resource_util import TurboResourceUtil
PREGNANCY_TEST_LOOT = 11087

@register_zone_load_event_method(unique_id='WickedWhims', priority=5, late=True)
def _wickedwhims_replace_pregnancy_test_loot():
    if has_game_loaded():
        return
    old_loot_actions_instance = TurboResourceUtil.Services.get_instance(TurboResourceUtil.ResourceTypes.ACTION, PREGNANCY_TEST_LOOT)
    new_loot_actions_instance = TurboResourceUtil.Services.get_instance(TurboResourceUtil.ResourceTypes.ACTION, 13344938130388024666)
    if old_loot_actions_instance is None or new_loot_actions_instance is None:
        return
    old_loot_actions_instance.loot_actions = new_loot_actions_instance.loot_actions

