from turbolib.events.core import has_game_loaded, register_zone_load_event_method
from turbolib.resource_util import TurboResourceUtil
PREGNANCY_IN_LABOR_BUFF = 75271

@register_zone_load_event_method(unique_id='WickedWhims', priority=5, late=True)
def _wickedwhims_add_water_puddle_to_pregnancy_labor_buff():
    if has_game_loaded():
        return
    buff_instance = TurboResourceUtil.Services.get_instance(TurboResourceUtil.ResourceTypes.BUFF, PREGNANCY_IN_LABOR_BUFF)
    loot_action_instance = TurboResourceUtil.Services.get_instance(TurboResourceUtil.ResourceTypes.ACTION, 17130648916201026455)
    if buff_instance is None or loot_action_instance is None:
        return
    loot_actions = list(buff_instance._loot_on_addition)
    loot_actions.append(loot_action_instance)
    buff_instance._loot_on_addition = tuple(loot_actions)

