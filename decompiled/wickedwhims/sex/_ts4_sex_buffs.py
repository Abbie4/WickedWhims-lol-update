'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from turbolib.resource_util import TurboResourceUtil

def set_buff_timeout(buff_id, timeout):
    buff_instance = TurboResourceUtil.Services.get_instance(TurboResourceUtil.ResourceTypes.BUFF, int(buff_id))
    if buff_instance is None or buff_instance._temporary_commodity_info is None or buff_instance._owning_commodity is None:
        return False
    buff_instance._owning_commodity.max_value_tuning = timeout
    buff_instance._owning_commodity.initial_value = timeout
    return True

