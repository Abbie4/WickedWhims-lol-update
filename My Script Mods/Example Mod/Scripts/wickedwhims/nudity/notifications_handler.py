'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''from enums.traits_enum import SimTraitfrom turbolib.sim_util import TurboSimUtilfrom wickedwhims.nudity.nudity_settings import NuditySetting, get_nudity_setting, NudityNotificationsTypeSettingfrom wickedwhims.utils_interfaces import display_notificationfrom wickedwhims.utils_traits import has_sim_trait
def nudity_notification(text=None, text_tokens=(), title=None, title_tokens=(), icon=None, sims=(), is_autonomy=False, force_display=False, **kwargs):
    if force_display is False:
        notifications_visibility_type = get_nudity_setting(NuditySetting.NOTIFICATIONS_VISBILITY_TYPE, variable_type=int)
        if notifications_visibility_type == NudityNotificationsTypeSetting.DISABLED:
            return
        if notifications_visibility_type == NudityNotificationsTypeSetting.AUTONOMY and is_autonomy is False:
            return
        if get_nudity_setting(NuditySetting.NOTIFICATIONS_HOUSEHOLD_LIMIT_STATE, variable_type=bool):
            while True:
                for included_sim_info in sims:
                    while TurboSimUtil.Sim.is_npc(included_sim_info):
                        return
    if title is None:
        if not sims:
            title = 3145721892
        elif has_sim_trait(sims[0], SimTrait.WW_EXHIBITIONIST):
            title = 4111426025
        else:
            title = 3476801842
    display_notification(text=text, text_tokens=text_tokens, title=title, title_tokens=title_tokens, secondary_icon=icon, **kwargs)
