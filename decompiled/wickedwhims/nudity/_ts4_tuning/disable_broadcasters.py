'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from turbolib.events.core import has_game_loaded, register_zone_load_event_method
from turbolib.resource_util import TurboResourceUtil
NUDE_CLOTHING_BUFF = 128807

@register_zone_load_event_method(unique_id='WickedWhims', priority=5, late=True)
def _wickedwhims_disable_nudity_buff_broadcaster():
    if has_game_loaded():
        return
    buff_instance = TurboResourceUtil.Services.get_instance(TurboResourceUtil.ResourceTypes.BUFF, NUDE_CLOTHING_BUFF)
    if buff_instance is not None:
        buff_instance.broadcaster = None

