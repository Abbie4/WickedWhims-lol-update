'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from enums.traits_enum import SimTrait
from turbolib.resource_util import TurboResourceUtil
from turbolib.sim_util import TurboSimUtil
from turbolib.wrappers.interactions import TurboImmediateSuperInteraction, TurboInteractionStartMixin
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.sex.pregnancy.birth_control.condoms import give_sim_condoms, try_to_take_and_use_condoms
from wickedwhims.sex.pregnancy.birth_control.pills import take_birth_control_pill, give_sim_birth_control_pills
from wickedwhims.utils_traits import has_sim_trait

class UseCondomsInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'UseCondomsInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        sim = cls.get_interaction_sim(interaction_context)
        if sim_ev(sim).active_sex_handler is None:
            return False
        actors_amount = sim_ev(sim).active_sex_handler.get_actors_amount()
        if actors_amount <= 1:
            return False
        sims_that_can_impregnate_count = 0
        for actor_sim in sim_ev(sim).active_sex_handler.get_actors_sim_info_gen():
            while sim_ev(actor_sim).has_condom_on is False and has_sim_trait(actor_sim, SimTrait.GENDEROPTIONS_PREGNANCY_CANIMPREGNATE):
                sims_that_can_impregnate_count += 1
        if sims_that_can_impregnate_count > 0:
            return True
        return False

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return try_to_take_and_use_condoms(cls.get_interaction_sim(interaction_instance))

class UnpackCondomsBoxInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'UnpackCondomsBoxInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return True

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        sim = cls.get_interaction_sim(interaction_instance)
        TurboSimUtil.Inventory.remove_object_by_id(sim, TurboResourceUtil.Resource.get_id(cls.get_interaction_target(interaction_instance)))
        give_sim_condoms(sim, amount=24)
        return True

class AllowCondomsAutoUseInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'AllowCondomsAutoUseInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        if sim_ev(cls.get_interaction_sim(interaction_context)).auto_use_of_condoms is False:
            return True
        return False

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        sim_ev(cls.get_interaction_sim(interaction_instance)).auto_use_of_condoms = True
        return True

class DisallowCondomsAutoUseInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'DisallowCondomsAutoUseInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        if sim_ev(cls.get_interaction_sim(interaction_context)).auto_use_of_condoms is True:
            return True
        return False

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        sim_ev(cls.get_interaction_sim(interaction_instance)).auto_use_of_condoms = False
        return True

class TakeBirthControlPillInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'TakeBirthControlPillInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return True

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return take_birth_control_pill(cls.get_interaction_sim(interaction_instance))

class UnpackBirthControlPillsBoxInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'UnpackBirthControlPillsBoxInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return True

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        sim = cls.get_interaction_sim(interaction_instance)
        TurboSimUtil.Inventory.remove_object_by_id(sim, TurboResourceUtil.Resource.get_id(cls.get_interaction_target(interaction_instance)))
        give_sim_birth_control_pills(sim, amount=28)
        return True

class AllowBirthControlPillsAutoUseInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'AllowBirthControlPillsAutoUseInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        if sim_ev(cls.get_interaction_sim(interaction_context)).auto_use_of_birth_pills is False:
            return True
        return False

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        sim_ev(cls.get_interaction_sim(interaction_instance)).auto_use_of_birth_pills = True
        return True

class DisallowBirthControlPillsAutoUseInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'DisallowBirthControlPillsAutoUseInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        if sim_ev(cls.get_interaction_sim(interaction_context)).auto_use_of_birth_pills is True:
            return True
        return False

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        sim_ev(cls.get_interaction_sim(interaction_instance)).auto_use_of_birth_pills = False
        return True

