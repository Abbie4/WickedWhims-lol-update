'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from broadcasters.broadcaster import Broadcaster
from enums.traits_enum import SimTrait
from turbolib.injector_util import inject
from turbolib.resource_util import TurboResourceUtil
from turbolib.special.custom_exception_watcher import log_custom_exception
from wickedwhims.utils_traits import has_sim_trait
JEALOUSY_INTERACTIONS_LIST = (13861, 13862, 13869, 13870, 13871, 13872, 13873, 76327, 76328, 76329, 76429, 76430, 76431, 76433, 76531, 76564, 76566, 76581, 77422, 77423, 77424, 77425, 77426, 77427, 77429, 77430, 119777, 120065, 120066, 120068, 120069, 120071, 120072, 125245, 125373, 127142, 127145)
JEALOUSY_BROADCASTERS_LIST = (76434, 76132, 125246, 125441, 129282, 129459)

@inject(Broadcaster, 'can_affect')
def _wickedwhims_on_broadcaster_can_affect(original, self, *args, **kwargs):
    result = original(self, *args, **kwargs)
    try:
        sim = args[0]
        while sim is not None and (sim.is_sim and self.allow_sims) and TurboResourceUtil.Resource.get_guid64(self) in JEALOUSY_BROADCASTERS_LIST:
            if has_sim_trait(sim, SimTrait.WW_POLYAMOROUS):
                return False
    except Exception as ex:
        log_custom_exception("Failed to prevent broadcaster effect at 'Broadcaster.can_affect'.", ex)
    return result

