'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''from turbolib.types_util import TurboTypesUtilfrom turbolib.wrappers.interactions import TurboSuperInteractionfrom wickedwhims.main.sim_ev_handler import sim_ev
class StopSexInteraction(TurboSuperInteraction):
    __qualname__ = 'StopSexInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        if interaction_target is None or not TurboTypesUtil.Sims.is_sim(interaction_target):
            return False
        if sim_ev(interaction_target).active_sex_handler is None:
            return False
        if sim_ev(cls.get_interaction_sim(interaction_context)).active_sex_handler is sim_ev(interaction_target).active_sex_handler:
            return False
        return True

    @classmethod
    def on_interaction_run(cls, interaction_instance):
        target_sim = cls.get_interaction_target(interaction_instance)
        sim_ev(target_sim).active_sex_handler.is_canceled = True
        sim_ev(target_sim).active_sex_handler.stop(is_end=True, stop_reason='On Normal Sex Stop Interaction.')
        return True
