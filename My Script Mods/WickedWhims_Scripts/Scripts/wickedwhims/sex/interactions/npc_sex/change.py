from turbolib.sim_util import TurboSimUtil
from turbolib.types_util import TurboTypesUtil
from turbolib.wrappers.interactions import TurboImmediateSuperInteraction, TurboInteractionStartMixin
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.sex.animations.animations_operator import has_animations_with_params, get_random_animation
from wickedwhims.sex.dialogs.sex_change import open_change_sex_animations_picker_dialog
from wickedwhims.sex.enums.sex_gender import get_sim_sex_gender
from wickedwhims.sex.enums.sex_type import SexCategoryType
from wickedwhims.sex.settings.sex_settings import SexSetting, get_sex_setting
from wickedwhims.sex.sex_handlers.active.active_sex_handler_updates import try_progress_sex_interaction
from wickedwhims.sex.sex_privileges import is_sim_allowed_for_animation, display_not_allowed_message
from wickedwhims.utils_interfaces import display_ok_dialog

def _test_for_npc_sex_change(interaction_target, sex_category_types):
    if not get_sex_setting(SexSetting.MANUAL_NPC_SEX_STATE, variable_type=bool):
        return False
    if interaction_target is None or not TurboTypesUtil.Sims.is_sim(interaction_target) or TurboSimUtil.Sim.is_player(interaction_target):
        return False
    active_sex_handler = sim_ev(interaction_target).active_sex_handler
    if active_sex_handler is None:
        return False
    if active_sex_handler.is_playing is False or not active_sex_handler.is_npc_only():
        return False
    genders_list = list()
    for actor_sim_info in active_sex_handler.get_actors_sim_info_gen():
        genders_list.append(get_sim_sex_gender(actor_sim_info))
    for sex_category_type in sex_category_types:
        while has_animations_with_params(sex_category_type, active_sex_handler.get_object_identifier(), genders_list):
            return True
    return False


def _change_npc_sex(interaction_target, sex_category_type):
    sex_allowed = is_sim_allowed_for_animation(sim_ev(interaction_target).active_sex_handler.get_actors_sim_info_gen(), sex_category_type)
    if not sex_allowed:
        display_not_allowed_message(sex_allowed)
        return False
    open_change_sex_animations_picker_dialog(sim_ev(interaction_target).active_sex_handler, sex_category_type)
    return True


class ChangeNPCSexTeasingInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'ChangeNPCSexTeasingInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _test_for_npc_sex_change(interaction_target, (SexCategoryType.TEASING,))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return _change_npc_sex(cls.get_interaction_target(interaction_instance), SexCategoryType.TEASING)


class ChangeNPCSexHandjobInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'ChangeNPCSexHandjobInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _test_for_npc_sex_change(interaction_target, (SexCategoryType.HANDJOB,))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return _change_npc_sex(cls.get_interaction_target(interaction_instance), SexCategoryType.HANDJOB)


class ChangeNPCSexFootjobInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'ChangeNPCSexFootjobInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _test_for_npc_sex_change(interaction_target, (SexCategoryType.FOOTJOB,))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return _change_npc_sex(cls.get_interaction_target(interaction_instance), SexCategoryType.FOOTJOB)


class ChangeNPCSexOraljobInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'ChangeNPCSexOraljobInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _test_for_npc_sex_change(interaction_target, (SexCategoryType.ORALJOB,))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return _change_npc_sex(cls.get_interaction_target(interaction_instance), SexCategoryType.ORALJOB)


class ChangeNPCSexVaginalInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'ChangeNPCSexVaginalInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _test_for_npc_sex_change(interaction_target, (SexCategoryType.VAGINAL,))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return _change_npc_sex(cls.get_interaction_target(interaction_instance), SexCategoryType.VAGINAL)


class ChangeNPCSexAnalInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'ChangeNPCSexAnalInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _test_for_npc_sex_change(interaction_target, (SexCategoryType.ANAL,))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return _change_npc_sex(cls.get_interaction_target(interaction_instance), SexCategoryType.ANAL)


class ChangeNPCSexClimaxInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'ChangeNPCSexClimaxInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _test_for_npc_sex_change(interaction_target, (SexCategoryType.CLIMAX,))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return _change_npc_sex(cls.get_interaction_target(interaction_instance), SexCategoryType.CLIMAX)


class ChangeNPCSexRandomInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'ChangeNPCSexRandomInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _test_for_npc_sex_change(interaction_target, (SexCategoryType.TEASING, SexCategoryType.HANDJOB, SexCategoryType.ORALJOB, SexCategoryType.FOOTJOB, SexCategoryType.VAGINAL, SexCategoryType.ANAL))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        active_sex_handler = sim_ev(cls.get_interaction_target(interaction_instance)).active_sex_handler
        random_animation = get_random_animation(active_sex_handler.get_object_identifier(), tuple(active_sex_handler.get_actors_sim_info_gen()))
        if random_animation is None:
            display_ok_dialog(text=1395546180, title=1890248379)
            return False
        active_sex_handler.set_animation_instance(random_animation, is_animation_change=True, is_manual=True)
        active_sex_handler.play(is_animation_change=True)
        return True


class ChangeNPCSexNextInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'ChangeNPCSexNextInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        if not get_sex_setting(SexSetting.MANUAL_NPC_SEX_STATE, variable_type=bool):
            return False
        if interaction_target is None or not TurboTypesUtil.Sims.is_sim(interaction_target) or TurboSimUtil.Sim.is_player(interaction_target):
            return False
        active_sex_handler = sim_ev(interaction_target).active_sex_handler
        if active_sex_handler is None:
            return False
        if active_sex_handler.is_playing is False:
            return False
        return True

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        active_sex_handler = sim_ev(cls.get_interaction_target(interaction_instance)).active_sex_handler
        if active_sex_handler is not None:
            try_progress_sex_interaction(active_sex_handler, is_manual=True)
            return True
        return False

