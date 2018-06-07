'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''from turbolib.cas_util import TurboCASUtilfrom turbolib.manager_util import TurboManagerUtilfrom turbolib.sim_util import TurboSimUtilfrom turbolib.ui_util import TurboUIUtilfrom wickedwhims.main.sim_ev_handler import sim_evfrom wickedwhims.sex.sex_operators.active_sex_handlers_operator import reset_active_sex_handlersfrom wickedwhims.utils_interfaces import display_notificationfrom wickedwhims.version_registry import get_mod_version_strHAS_UPDATED_THE_MOD = False
def set_mod_update_status(status):
    global HAS_UPDATED_THE_MOD
    HAS_UPDATED_THE_MOD = status

def reset_mod_on_update():
    if HAS_UPDATED_THE_MOD is False:
        return
    display_notification(text=4037785225, text_tokens=(get_mod_version_str(),), title='WickedWhims', information_level=TurboUIUtil.Notification.UiDialogNotificationLevel.PLAYER, is_safe=True)
    reset_active_sex_handlers()
    from wickedwhims.sex.sex_operators.general_sex_handlers_operator import clear_sim_sex_extra_data
    for sim_info in TurboManagerUtil.Sim.get_all_sim_info_gen(humans=True, pets=False):
        pre_sex_handler = sim_ev(sim_info).active_pre_sex_handler
        active_sex_handler = sim_ev(sim_info).active_sex_handler
        clear_sim_sex_extra_data(sim_info)
        try:
            while active_sex_handler is not None:
                active_sex_handler.stop(hard_stop=True, is_end=True, stop_reason='On stop sex command.')
        except:
            pass
        while pre_sex_handler is not None or active_sex_handler is not None:
            if not TurboSimUtil.CAS.has_outfit(sim_info, (TurboCASUtil.OutfitCategory.EVERYDAY, 0)):
                TurboSimUtil.CAS.generate_outfit(sim_info, (TurboCASUtil.OutfitCategory.EVERYDAY, 0))
                TurboSimUtil.CAS.set_current_outfit(sim_info, (TurboCASUtil.OutfitCategory.EVERYDAY, 0))
                TurboSimUtil.CAS.update_previous_outfit(sim_info)
            TurboSimUtil.Sim.reset_sim(sim_info)
