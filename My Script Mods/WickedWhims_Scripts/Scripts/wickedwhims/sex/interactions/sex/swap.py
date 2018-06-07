'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''from turbolib.manager_util import TurboManagerUtilfrom turbolib.types_util import TurboTypesUtilfrom turbolib.wrappers.interactions import TurboImmediateSuperInteraction, TurboInteractionStartMixinfrom wickedwhims.main.sim_ev_handler import sim_evfrom wickedwhims.sex.dialogs.sex_swap import open_swap_sex_sims_picker_dialogfrom wickedwhims.sex.settings.sex_settings import SexSetting, get_sex_settingfrom wickedwhims.sex.utils.sex_swap import is_compatible_actor
class SwapActorSexSpotInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'SwapActorSexSpotInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        if interaction_target is None or not TurboTypesUtil.Sims.is_sim(interaction_target):
            return False
        if not get_sex_setting(SexSetting.MANUAL_NPC_SEX_STATE, variable_type=bool):
            if sim_ev(cls.get_interaction_sim(interaction_context)).active_sex_handler is None:
                return False
            if sim_ev(cls.get_interaction_sim(interaction_context)).active_sex_handler is not sim_ev(interaction_target).active_sex_handler:
                return False
        elif sim_ev(interaction_target).active_sex_handler is None:
            return False
        active_sex_handler = sim_ev(interaction_target).active_sex_handler
        target_actor_id = active_sex_handler.get_actor_id_by_sim_id(TurboManagerUtil.Sim.get_sim_id(interaction_target))
        target_actor_data = active_sex_handler.get_animation_instance().get_actor(target_actor_id)
        if target_actor_data is None:
            return False
        for (actor_id, actor_sim) in active_sex_handler.get_sims_list():
            if actor_id == target_actor_id:
                pass
            actor_data = active_sex_handler.get_animation_instance().get_actor(actor_id)
            if actor_data is None:
                return False
            while is_compatible_actor(actor_sim, actor_data, interaction_target, target_actor_data):
                return True
        return False

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        active_sex_handler = sim_ev(cls.get_interaction_target(interaction_instance)).active_sex_handler
        if active_sex_handler is None:
            return False
        open_swap_sex_sims_picker_dialog(active_sex_handler, cls.get_interaction_target(interaction_instance))
        return True
