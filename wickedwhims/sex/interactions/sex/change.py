'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from turbolib.resource_util import TurboResourceUtil
from turbolib.types_util import TurboTypesUtil
from turbolib.wrappers.interactions import TurboImmediateSuperInteraction, TurboInteractionStartMixin
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.sex.animations.animations_operator import has_animations_with_params, get_random_animation
from wickedwhims.sex.dialogs.sex_change import open_change_sex_animations_picker_dialog
from wickedwhims.sex.enums.sex_gender import get_sim_sex_gender
from wickedwhims.sex.enums.sex_type import SexCategoryType
from wickedwhims.sex.sex_handlers.active.active_sex_handler_updates import try_progress_sex_interaction
from wickedwhims.sex.sex_privileges import is_sim_allowed_for_animation, display_not_allowed_message
from wickedwhims.utils_interfaces import display_ok_dialog

def _test_for_sex_change(interaction_sim, interaction_target, sex_category_types):
    if interaction_target is None:
        return False
    if interaction_sim is interaction_target or TurboTypesUtil.Sims.is_sim(interaction_target) and sim_ev(interaction_sim).active_sex_handler is sim_ev(interaction_target).active_sex_handler or TurboTypesUtil.Objects.is_game_object(interaction_target) and sim_ev(interaction_sim).active_sex_handler is not None and sim_ev(interaction_sim).active_sex_handler.get_game_object_id() == TurboResourceUtil.Resource.get_id(interaction_target):
        active_sex_handler = sim_ev(interaction_sim).active_sex_handler or (sim_ev(interaction_target).active_sex_handler if TurboTypesUtil.Sims.is_sim(interaction_target) else None)
        if active_sex_handler is None:
            return False
        if active_sex_handler.is_playing is False:
            return False
        genders_list = list()
        for actor_sim_info in active_sex_handler.get_actors_sim_info_gen():
            genders_list.append(get_sim_sex_gender(actor_sim_info))
        for sex_category_type in sex_category_types:
            while has_animations_with_params(sex_category_type, active_sex_handler.get_object_identifier(), genders_list):
                return True
    return False

def _change_sex(interaction_sim, sex_category_type):
    sex_allowed = is_sim_allowed_for_animation(sim_ev(interaction_sim).active_sex_handler.get_actors_sim_info_gen(), sex_category_type)
    if not sex_allowed:
        display_not_allowed_message(sex_allowed)
        return False
    open_change_sex_animations_picker_dialog(sim_ev(interaction_sim).active_sex_handler, sex_category_type)
    return True

class ChangeSexTeasingInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'ChangeSexTeasingInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _test_for_sex_change(cls.get_interaction_sim(interaction_context), interaction_target, (SexCategoryType.TEASING,))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return _change_sex(cls.get_interaction_sim(interaction_instance), SexCategoryType.TEASING)

class ChangeSexHandjobInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'ChangeSexHandjobInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _test_for_sex_change(cls.get_interaction_sim(interaction_context), interaction_target, (SexCategoryType.HANDJOB,))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return _change_sex(cls.get_interaction_sim(interaction_instance), SexCategoryType.HANDJOB)

class ChangeSexFootjobInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'ChangeSexFootjobInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _test_for_sex_change(cls.get_interaction_sim(interaction_context), interaction_target, (SexCategoryType.FOOTJOB,))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return _change_sex(cls.get_interaction_sim(interaction_instance), SexCategoryType.FOOTJOB)

class ChangeSexOraljobInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'ChangeSexOraljobInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _test_for_sex_change(cls.get_interaction_sim(interaction_context), interaction_target, (SexCategoryType.ORALJOB,))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return _change_sex(cls.get_interaction_sim(interaction_instance), SexCategoryType.ORALJOB)

class ChangeSexVaginalInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'ChangeSexVaginalInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _test_for_sex_change(cls.get_interaction_sim(interaction_context), interaction_target, (SexCategoryType.VAGINAL,))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return _change_sex(cls.get_interaction_sim(interaction_instance), SexCategoryType.VAGINAL)

class ChangeSexAnalInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'ChangeSexAnalInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _test_for_sex_change(cls.get_interaction_sim(interaction_context), interaction_target, (SexCategoryType.ANAL,))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return _change_sex(cls.get_interaction_sim(interaction_instance), SexCategoryType.ANAL)

class ChangeSexClimaxInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'ChangeSexClimaxInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _test_for_sex_change(cls.get_interaction_sim(interaction_context), interaction_target, (SexCategoryType.CLIMAX,))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return _change_sex(cls.get_interaction_sim(interaction_instance), SexCategoryType.CLIMAX)

class ChangeSexRandomInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'ChangeSexRandomInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _test_for_sex_change(cls.get_interaction_sim(interaction_context), interaction_target, (SexCategoryType.TEASING, SexCategoryType.HANDJOB, SexCategoryType.ORALJOB, SexCategoryType.FOOTJOB, SexCategoryType.VAGINAL, SexCategoryType.ANAL))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        active_sex_handler = sim_ev(cls.get_interaction_sim(interaction_instance)).active_sex_handler
        random_animation = get_random_animation(active_sex_handler.get_object_identifier(), tuple(active_sex_handler.get_actors_sim_info_gen()))
        if random_animation is None:
            display_ok_dialog(text=1395546180, title=1890248379)
            return False
        active_sex_handler.set_animation_instance(random_animation, is_animation_change=True, is_manual=True)
        active_sex_handler.play(is_animation_change=True)
        return True

class ChangeSexNextInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'ChangeSexNextInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        if interaction_target is None:
            return False
        sim = cls.get_interaction_sim(interaction_context)
        if sim is interaction_target or TurboTypesUtil.Sims.is_sim(interaction_target) and sim_ev(sim).active_sex_handler is sim_ev(interaction_target).active_sex_handler or TurboTypesUtil.Objects.is_game_object(interaction_target) and sim_ev(sim).active_sex_handler is not None and sim_ev(sim).active_sex_handler.get_game_object_id() == TurboResourceUtil.Resource.get_id(interaction_target):
            active_sex_handler = sim_ev(sim).active_sex_handler or (sim_ev(interaction_target).active_sex_handler if TurboTypesUtil.Sims.is_sim(interaction_target) else None)
            if active_sex_handler is None:
                return False
            if active_sex_handler.is_playing is False:
                return False
            return True
        return False

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        active_sex_handler = sim_ev(cls.get_interaction_sim(interaction_instance)).active_sex_handler
        if active_sex_handler is not None:
            try_progress_sex_interaction(active_sex_handler, is_manual=True)
            return True
        return False

