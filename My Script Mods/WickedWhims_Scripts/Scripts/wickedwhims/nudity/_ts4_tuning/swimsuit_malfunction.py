from turbolib.events.core import register_zone_load_event_method
from turbolib.resource_util import TurboResourceUtil
SWIMSUIT_MALFUNCTION_LOOT = 128662

@register_zone_load_event_method(unique_id='WickedWhims', priority=5, late=True)
def _wickedwhims_disable_swimsuit_malfunction_loot():
    loot_actions_instance = TurboResourceUtil.Services.get_instance(TurboResourceUtil.ResourceTypes.ACTION, SWIMSUIT_MALFUNCTION_LOOT)
    if loot_actions_instance is not None:
        loot_actions_instance.loot_actions = tuple()

