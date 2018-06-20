'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from turbolib.events.privacy import register_privacy_sim_test_event_method, PrivacyResult
from wickedwhims.main.sim_ev_handler import sim_ev

@register_privacy_sim_test_event_method(unique_id='WickedWhims', priority=5)
def _wickedwhims_special_additional_los_test(_, tested_sim):
    if sim_ev(tested_sim).active_sex_handler is not None or sim_ev(tested_sim).active_pre_sex_handler is not None:
        return PrivacyResult.ALLOW
    return PrivacyResult.DEFAULT

