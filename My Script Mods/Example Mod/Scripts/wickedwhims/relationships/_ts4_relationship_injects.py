'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''from sims.sim_info import SimInfofrom enums.traits_enum import SimTraitfrom turbolib.injector_util import injectfrom turbolib.special.custom_exception_watcher import log_custom_exceptionfrom wickedwhims.relationships.relationship_settings import get_relationship_setting, RelationshipSettingfrom wickedwhims.utils_traits import has_sim_trait
@inject(SimInfo, 'incest_prevention_test')
def _wickedwhims_on_incest_prevention_test(original, self, *args, **kwargs):
    try:
        target_sim_info = args[0]
        if get_relationship_setting(RelationshipSetting.INCEST_STATE, variable_type=bool) or has_sim_trait(self, SimTrait.WW_INCEST) and has_sim_trait(target_sim_info, SimTrait.WW_INCEST):
            return True
    except Exception as ex:
        log_custom_exception("Failed to edit incest test at 'SimInfo.incest_prevention_test'.", ex)
    return original(self, *args, **kwargs)
