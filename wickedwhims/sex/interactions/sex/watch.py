'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from enums.interactions_enum import SimInteraction
from turbolib.manager_util import TurboManagerUtil
from turbolib.sim_util import TurboSimUtil
from turbolib.types_util import TurboTypesUtil
from turbolib.wrappers.interactions import TurboImmediateSuperInteraction, TurboInteractionStartMixin
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.sxex_bridge.sex import is_sim_in_sex

class WatchSexInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'WatchSexInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        if interaction_target is None or not TurboTypesUtil.Sims.is_sim(interaction_target):
            return False
        if is_sim_in_sex(cls.get_interaction_sim(interaction_context)):
            return False
        active_sex_handler = sim_ev(interaction_target).active_sex_handler
        if active_sex_handler is None:
            return False
        if TurboManagerUtil.Sim.get_sim_id(cls.get_interaction_sim(interaction_context)) in active_sex_handler.go_away_sims_list:
            return False
        return True

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        sim_ev(cls.get_interaction_sim(interaction_instance)).watching_sim_id = TurboManagerUtil.Sim.get_sim_id(cls.get_interaction_target(interaction_instance))

class AttemptWatchSexInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'AttemptWatchSexInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        target_sim_id = sim_ev(cls.get_interaction_sim(interaction_context)).watching_sim_id
        if target_sim_id == -1:
            return False
        return True

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        target_sim_id = sim_ev(cls.get_interaction_sim(interaction_instance)).watching_sim_id
        target_sim = TurboManagerUtil.Sim.get_sim_instance(target_sim_id)
        if target_sim is not None:
            TurboSimUtil.Interaction.push_affordance(cls.get_interaction_sim(interaction_instance), SimInteraction.WW_TRIGGER_SEX_WATCH_DEFAULT, target=target_sim)
        sim_ev(cls.get_interaction_sim(interaction_instance)).watching_sim_id = -1

