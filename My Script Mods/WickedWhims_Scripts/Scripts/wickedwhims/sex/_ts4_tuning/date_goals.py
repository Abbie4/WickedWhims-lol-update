'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from turbolib.events.core import has_game_loaded, register_zone_load_event_method
from turbolib.resource_util import TurboResourceUtil
GOALS_TO_REPLACE = ((29675, (17127167598028976579,)), (76582, (17127167598028976579,)))

@register_zone_load_event_method(unique_id='WickedWhims', priority=5, late=True)
def _wickedwhims_replace_woohoo_date_goals():
    if has_game_loaded():
        return
    for (goal_set_id, goal_ids) in GOALS_TO_REPLACE:
        goal_set_instance = TurboResourceUtil.Services.get_instance(TurboResourceUtil.ResourceTypes.SITUATION_GOAL_SET, goal_set_id)
        if goal_set_instance is None:
            pass
        new_goals = list()
        for goal_id in goal_ids:
            goal_instance = TurboResourceUtil.Services.get_instance(TurboResourceUtil.ResourceTypes.SITUATION_GOAL, goal_id)
            if goal_instance is None:
                pass
            immutable_slots_class = TurboResourceUtil.Collections.get_immutable_slots_class(['goal', 'weight'])
            immutable_slots = immutable_slots_class(dict(goal=goal_instance, weight=1.0))
            new_goals.append(immutable_slots)
        goal_set_instance.goals = tuple(new_goals)

