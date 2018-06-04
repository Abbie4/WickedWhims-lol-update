'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from objects.puddles import PuddleChoices, PuddleSize
from turbolib.events.core import has_game_loaded, register_zone_load_event_method
from turbolib.resource_util import TurboResourceUtil

@register_zone_load_event_method(unique_id='WickedWhims', priority=5, late=True)
def _wickedwhims_add_custom_puddles():
    if has_game_loaded():
        return
    puddle_definitions = dict(PuddleChoices.PUDDLE_DEFINITIONS)
    puddle_definitions[10] = TurboResourceUtil.Collections.get_frozen_attribute_dict({PuddleSize.SmallPuddle: (12327982570318338407,)})
    PuddleChoices.PUDDLE_DEFINITIONS = TurboResourceUtil.Collections.get_frozen_attribute_dict(puddle_definitions)

