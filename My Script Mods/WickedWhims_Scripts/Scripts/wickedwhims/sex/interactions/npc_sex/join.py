from turbolib.types_util import TurboTypesUtil
from turbolib.wrappers.interactions import TurboImmediateSuperInteraction, TurboInteractionStartMixin
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.sex.animations.animations_cache import get_animation_max_amount_of_actors
from wickedwhims.sex.dialogs.sex_join import open_join_sims_picker_dialog
from wickedwhims.sex.enums.sex_type import SexCategoryType
from wickedwhims.sex.settings.sex_settings import SexSetting, get_sex_setting

def _test_join_to_npc_sex_multiple_interaction(interaction_target, sex_category_types):
    if not get_sex_setting(SexSetting.MANUAL_NPC_SEX_STATE, variable_type=bool):
        return False
    if interaction_target is None or not TurboTypesUtil.Sims.is_sim(interaction_target):
        return False
    if sim_ev(interaction_target).active_sex_handler is None:
        return False
    active_sex_handler = sim_ev(interaction_target).active_sex_handler
    if active_sex_handler.is_playing is False or not active_sex_handler.is_npc_only():
        return False
    if sim_ev(interaction_target).active_pre_sex_handler is not None and sim_ev(interaction_target).active_pre_sex_handler.get_identifier() != active_sex_handler.get_identifier():
        return False
    for sex_category_type in sex_category_types:
        while get_animation_max_amount_of_actors(sex_category_type, active_sex_handler.get_object_identifier()[0]) > active_sex_handler.get_actors_amount() or get_animation_max_amount_of_actors(sex_category_type, active_sex_handler.get_object_identifier()[1]) > active_sex_handler.get_actors_amount():
            return True
    return False


def _open_join_npc_sex_sim_selector(sex_category_type, interaction_target):
    active_sex_handler = sim_ev(interaction_target).active_sex_handler
    if active_sex_handler is None:
        return False
    pre_sex_handler = active_sex_handler.get_pre_sex_handler(is_joining=True)
    open_join_sims_picker_dialog(pre_sex_handler, sex_category_type)
    return True


class JoinNPCSexMultipleTeasingInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'JoinNPCSexMultipleTeasingInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _test_join_to_npc_sex_multiple_interaction(interaction_target, (SexCategoryType.TEASING,))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return _open_join_npc_sex_sim_selector(SexCategoryType.TEASING, cls.get_interaction_target(interaction_instance))


class JoinNPCSexMultipleHandjobInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'JoinNPCSexMultipleHandjobInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _test_join_to_npc_sex_multiple_interaction(interaction_target, (SexCategoryType.HANDJOB,))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return _open_join_npc_sex_sim_selector(SexCategoryType.HANDJOB, cls.get_interaction_target(interaction_instance))


class JoinNPCSexMultipleFootjobInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'JoinNPCSexMultipleFootjobInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _test_join_to_npc_sex_multiple_interaction(interaction_target, (SexCategoryType.FOOTJOB,))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return _open_join_npc_sex_sim_selector(SexCategoryType.FOOTJOB, cls.get_interaction_target(interaction_instance))


class JoinNPCSexMultipleOraljobInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'JoinNPCSexMultipleOraljobInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _test_join_to_npc_sex_multiple_interaction(interaction_target, (SexCategoryType.ORALJOB,))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return _open_join_npc_sex_sim_selector(SexCategoryType.ORALJOB, cls.get_interaction_target(interaction_instance))


class JoinNPCSexMultipleVaginalInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'JoinNPCSexMultipleVaginalInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _test_join_to_npc_sex_multiple_interaction(interaction_target, (SexCategoryType.VAGINAL,))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return _open_join_npc_sex_sim_selector(SexCategoryType.VAGINAL, cls.get_interaction_target(interaction_instance))


class JoinNPCSexMultipleAnalInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'JoinNPCSexMultipleAnalInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _test_join_to_npc_sex_multiple_interaction(interaction_target, (SexCategoryType.ANAL,))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return _open_join_npc_sex_sim_selector(SexCategoryType.ANAL, cls.get_interaction_target(interaction_instance))


class JoinNPCSexMultipleRandomInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'JoinNPCSexMultipleRandomInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _test_join_to_npc_sex_multiple_interaction(interaction_target, (SexCategoryType.TEASING, SexCategoryType.HANDJOB, SexCategoryType.ORALJOB, SexCategoryType.FOOTJOB, SexCategoryType.VAGINAL, SexCategoryType.ANAL))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return _open_join_npc_sex_sim_selector(None, cls.get_interaction_target(interaction_instance))

