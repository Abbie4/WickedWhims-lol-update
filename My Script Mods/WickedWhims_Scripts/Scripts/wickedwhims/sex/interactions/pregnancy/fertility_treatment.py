'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from enums.interactions_enum import SimInteraction
from turbolib.interaction_util import TurboInteractionUtil
from turbolib.manager_util import TurboManagerUtil
from turbolib.sim_util import TurboSimUtil
from turbolib.world_util import TurboWorldUtil
from turbolib.wrappers.interactions import TurboSuperInteraction, TurboImmediateSuperInteraction, TurboInteractionStartMixin
from wickedwhims.sex.pregnancy.menstrual_cycle_handler import apply_pregnancy_boost_data
from wickedwhims.sex.settings.sex_settings import PregnancyModeSetting, SexSetting, get_sex_setting
from wickedwhims.utils_interfaces import display_notification

class PhonePregnancyFertilityTreatmentInteraction(TurboSuperInteraction):
    __qualname__ = 'PhonePregnancyFertilityTreatmentInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        if get_sex_setting(SexSetting.PREGNANCY_MODE, variable_type=int) == PregnancyModeSetting.MENSTRUAL_CYCLE:
            return True
        return False

    @classmethod
    def on_interaction_run(cls, interaction_instance):
        return True


class CompletePregnancyFertilityTreatmentInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'CompletePregnancyFertilityTreatmentInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return True

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        sim = cls.get_interaction_sim(interaction_instance)
        household = TurboSimUtil.Household.get_household(sim)
        if household is None:
            return False
        if not TurboWorldUtil.Household.subtract_funds(household, 950):
            return False
        sim_info = TurboManagerUtil.Sim.get_sim_info(sim)
        apply_pregnancy_boost_data(sim_info)
        display_notification(text=2518175852, text_tokens=(sim_info,), title=518027626, secondary_icon=sim_info)
        TurboSimUtil.Interaction.push_affordance(sim, SimInteraction.WW_GO_HOME, interaction_context=TurboInteractionUtil.InteractionContext.SOURCE_SCRIPT, insert_strategy=TurboInteractionUtil.QueueInsertStrategy.NEXT, must_run_next=True, priority=TurboInteractionUtil.Priority.Critical, run_priority=TurboInteractionUtil.Priority.Critical)
        return True

