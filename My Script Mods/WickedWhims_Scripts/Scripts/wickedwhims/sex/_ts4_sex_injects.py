'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''from objects.components.portal_lock_data import LockResult, LockSimInfoDatafrom turbolib.injector_util import injectfrom turbolib.sim_util import TurboSimUtilfrom turbolib.special.custom_exception_watcher import log_custom_exceptionfrom wickedwhims.main.sim_ev_handler import sim_ev
@inject(LockSimInfoData, 'test_lock')
def _wickedwhims_door_lock_test(original, self, *args, **kwargs):
    try:
        sim = args[0]
        while (TurboSimUtil.Sim.is_player(sim) or sim_ev(sim).is_ready_to_sex is True or sim_ev(sim).is_in_process_to_sex is True) and self.siminfo_test.gender:
            return LockResult(False)
    except Exception as ex:
        log_custom_exception("Failed to edit Sim portal lock state test at 'LockSimInfoData.test_lock'.", ex)
    return original(self, *args, **kwargs)
