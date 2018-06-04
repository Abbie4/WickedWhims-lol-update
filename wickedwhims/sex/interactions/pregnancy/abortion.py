'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from enums.buffs_enum import SimBuff
from enums.interactions_enum import SimInteraction
from enums.traits_enum import SimTrait
from turbolib.interaction_util import TurboInteractionUtil
from turbolib.manager_util import TurboManagerUtil
from turbolib.sim_util import TurboSimUtil
from turbolib.world_util import TurboWorldUtil
from turbolib.wrappers.interactions import TurboImmediateSuperInteraction, TurboInteractionStartMixin
from wickedwhims.sxex_bridge.statistics import increase_sim_ww_statistic
from wickedwhims.utils_buffs import add_sim_buff
from wickedwhims.utils_interfaces import display_notification
from wickedwhims.utils_traits import has_sim_trait

class CompleteTerminatePregnancyInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'CompleteTerminatePregnancyInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return True

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        sim = cls.get_interaction_sim(interaction_instance)
        household = TurboSimUtil.Household.get_household(sim)
        if household is None:
            return False
        if not TurboWorldUtil.Household.subtract_funds(household, 1500):
            return False
        sim_info = TurboManagerUtil.Sim.get_sim_info(sim)
        TurboSimUtil.Pregnancy.clear_pregnancy(sim_info)
        if has_sim_trait(sim_info, SimTrait.HATESCHILDREN):
            add_sim_buff(sim_info, SimBuff.WW_PREGNANCY_TERMINATION_HAPPY, reason=3441893392)
        else:
            add_sim_buff(sim_info, SimBuff.WW_PREGNANCY_TERMINATION_SAD, reason=3441893392)
        display_notification(text=3344178125, text_tokens=(sim_info,), title=2364600527, secondary_icon=sim_info)
        increase_sim_ww_statistic(sim_info, 'times_terminated_pregnancy')
        TurboSimUtil.Interaction.push_affordance(sim, SimInteraction.WW_GO_HOME, interaction_context=TurboInteractionUtil.InteractionContext.SOURCE_SCRIPT, insert_strategy=TurboInteractionUtil.QueueInsertStrategy.NEXT, must_run_next=True, priority=TurboInteractionUtil.Priority.Critical, run_priority=TurboInteractionUtil.Priority.Critical)
        return True

