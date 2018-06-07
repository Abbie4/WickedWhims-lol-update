'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''from turbolib.sim_util import TurboSimUtilfrom turbolib.types_util import TurboTypesUtilfrom turbolib.wrappers.interactions import TurboImmediateSuperInteraction, TurboInteractionStartMixinfrom wickedwhims.main.sim_ev_handler import sim_evfrom wickedwhims.sex.settings.sex_settings import get_sex_setting, SexSetting
class InstantStopNPCSexInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'InstantStopNPCSexInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        if not get_sex_setting(SexSetting.MANUAL_NPC_SEX_STATE, variable_type=bool):
            return False
        if interaction_target is None or not TurboTypesUtil.Sims.is_sim(interaction_target) or TurboSimUtil.Sim.is_player(interaction_target):
            return False
        active_sex_handler = sim_ev(interaction_target).active_sex_handler
        if active_sex_handler is None:
            return False
        if active_sex_handler.is_playing is False or not active_sex_handler.is_npc_only():
            return False
        return True

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        target_sim = cls.get_interaction_target(interaction_instance)
        sim_ev(target_sim).active_sex_handler.is_canceled = True
        sim_ev(target_sim).active_sex_handler.stop(is_end=True, stop_reason='On Instant NPC Sex Stop Interaction.')
        return True
