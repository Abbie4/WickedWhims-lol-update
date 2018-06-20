'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from turbolib.sim_util import TurboSimUtil
from turbolib.wrappers.interactions import TurboImmediateSuperInteraction, TurboInteractionStartMixin
from wickedwhims.sex.pregnancy.menstrual_cycle_handler import get_sim_current_menstrual_pregnancy_chance, get_sim_days_till_ovulation
from wickedwhims.sex.pregnancy.pregnancy_interface import get_sim_current_pregnancy_chance
from wickedwhims.sex.settings.sex_settings import PregnancyModeSetting, SexSetting, get_sex_setting
from wickedwhims.utils_interfaces import display_notification

class PrePregnancyTakeFertilityTestInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'PrePregnancyTakeFertilityTestInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        if get_sex_setting(SexSetting.PREGNANCY_MODE, variable_type=int) != PregnancyModeSetting.MENSTRUAL_CYCLE:
            return False
        sim = cls.get_interaction_sim(interaction_context)
        if TurboSimUtil.Gender.is_female(sim) and TurboSimUtil.Age.get_age(sim) == TurboSimUtil.Age.ELDER:
            return False
        return True

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return True


class PregnancyTakeFertilityTestOutcomeInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'PregnancyTakeFertilityTestOutcomeInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return True

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        sim = cls.get_interaction_sim(interaction_instance)
        if get_sex_setting(SexSetting.PREGNANCY_MODE, variable_type=int) == PregnancyModeSetting.MENSTRUAL_CYCLE:
            pregnancy_chance = int(get_sim_current_menstrual_pregnancy_chance(sim)*100)
            days_till_ovulation = get_sim_days_till_ovulation(sim)
            display_notification(text=2475884372, text_tokens=(sim, str(pregnancy_chance), str(days_till_ovulation)), title=2800719885, secondary_icon=sim)
        else:
            pregnancy_chance = int(get_sim_current_pregnancy_chance(sim)*100)
            display_notification(text=72538425, text_tokens=(sim, str(pregnancy_chance)), title=2800719885, secondary_icon=sim)
        return True

