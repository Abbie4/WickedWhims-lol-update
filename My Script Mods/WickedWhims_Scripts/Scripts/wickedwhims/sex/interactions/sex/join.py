from turbolib.manager_util import TurboManagerUtil
from turbolib.types_util import TurboTypesUtil
from turbolib.wrappers.interactions import TurboImmediateSuperInteraction, TurboInteractionStartMixin
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.relationships.relationship_settings import get_relationship_setting, RelationshipSetting
from wickedwhims.sex.animations.animations_cache import get_animation_max_amount_of_actors
from wickedwhims.sex.animations.animations_operator import has_animations_with_params, get_random_animation
from wickedwhims.sex.dialogs.sex_join import open_join_sims_picker_dialog, open_join_sex_animations_picker_dialog
from wickedwhims.sex.enums.sex_gender import get_sim_sex_gender
from wickedwhims.sex.enums.sex_type import SexCategoryType
from wickedwhims.sex.sex_operators.pre_sex_handlers_operator import join_sex_interaction_from_pre_sex_handler
from wickedwhims.sex.sex_privileges import is_sim_allowed_for_animation, display_not_allowed_message
from wickedwhims.sex.utils.sex_init import get_age_limits_for_sex, get_nearby_sims_for_sex, get_sims_for_sex
from wickedwhims.sxex_bridge.sex import is_sim_ready_for_sex
from wickedwhims.utils_interfaces import display_ok_dialog

def _test_join_to_sex_single_interaction(interaction_sim, interaction_target, sex_category_types):
    '''
    :param interaction_sim: Sim that wants to join to an existing sex interaction
    :param interaction_target: Sim that owns an existing interaction
    '''
    if interaction_target is None or not TurboTypesUtil.Sims.is_sim(interaction_target):
        return False
    if sim_ev(interaction_target).active_sex_handler is None:
        return False
    if not is_sim_ready_for_sex(interaction_sim):
        return False
    active_sex_handler = sim_ev(interaction_target).active_sex_handler
    if sim_ev(interaction_target).active_pre_sex_handler is not None and sim_ev(interaction_target).active_pre_sex_handler.get_identifier() != active_sex_handler.get_identifier():
        return False
    genders_list = list()
    for actor_sim_info in active_sex_handler.get_actors_sim_info_gen():
        genders_list.append(get_sim_sex_gender(actor_sim_info))
    genders_list.append(get_sim_sex_gender(interaction_sim))
    has_animations = False
    for sex_category_type in sex_category_types:
        while has_animations_with_params(sex_category_type, active_sex_handler.get_object_identifier(), genders_list):
            has_animations = True
            break
    if has_animations is False:
        return False
    test_incest_of_sims = () if get_relationship_setting(RelationshipSetting.INCEST_STATE, variable_type=bool) else tuple(active_sex_handler.get_actors_sim_info_gen())
    (min_age_limit, max_age_limit) = get_age_limits_for_sex(tuple(active_sex_handler.get_actors_sim_info_gen()))
    skip_sims_ids = [TurboManagerUtil.Sim.get_sim_id(actor_sim_info) for actor_sim_info in active_sex_handler.get_actors_sim_info_gen()]
    target_sim_id = TurboManagerUtil.Sim.get_sim_id(interaction_sim)
    for sim_id in get_sims_for_sex(relative_sims=test_incest_of_sims, min_sims_age=min_age_limit, max_sims_age=max_age_limit, skip_sims_ids=skip_sims_ids):
        while sim_id == target_sim_id:
            return True
    return False


def _join_to_sex_single_interaction(sex_category_type, interaction_sim, interaction_target):
    '''
    :param interaction_sim: Sim that is joining to an existing sex interaction
    :param interaction_target: Sim that owns an existing interaction
    '''
    active_sex_handler = sim_ev(interaction_target).active_sex_handler
    if active_sex_handler is None:
        return False
    pre_sex_handler = active_sex_handler.get_pre_sex_handler(is_joining=True)
    pre_sex_handler.add_sim(interaction_sim)
    if sex_category_type is not None:
        sex_allowed = is_sim_allowed_for_animation(tuple(pre_sex_handler.get_actors_sim_info_gen()), sex_category_type, is_joining=True)
        if not sex_allowed:
            display_not_allowed_message(sex_allowed)
            return False
    if sex_category_type is not None:
        open_join_sex_animations_picker_dialog(pre_sex_handler, (interaction_sim,), sex_category_type, flip_relationship_check=True)
    else:
        random_animation = get_random_animation(pre_sex_handler.get_object_identifier(), tuple(pre_sex_handler.get_actors_sim_info_gen()))
        if random_animation is None:
            display_ok_dialog(text=1395546180, title=1890248379)
            return False
        pre_sex_handler.set_animation_instance(random_animation)
        join_sex_interaction_from_pre_sex_handler(pre_sex_handler, (interaction_sim,), flip_relationship_check=True)
    return True


class JoinSexSingleTeasingInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'JoinSexSingleTeasingInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _test_join_to_sex_single_interaction(cls.get_interaction_sim(interaction_context), interaction_target, (SexCategoryType.TEASING,))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return _join_to_sex_single_interaction(SexCategoryType.TEASING, cls.get_interaction_sim(interaction_instance), cls.get_interaction_target(interaction_instance))


class JoinSexSingleHandjobInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'JoinSexSingleHandjobInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _test_join_to_sex_single_interaction(cls.get_interaction_sim(interaction_context), interaction_target, (SexCategoryType.HANDJOB,))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return _join_to_sex_single_interaction(SexCategoryType.HANDJOB, cls.get_interaction_sim(interaction_instance), cls.get_interaction_target(interaction_instance))


class JoinSexSingleFootjobInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'JoinSexSingleFootjobInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _test_join_to_sex_single_interaction(cls.get_interaction_sim(interaction_context), interaction_target, (SexCategoryType.FOOTJOB,))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return _join_to_sex_single_interaction(SexCategoryType.FOOTJOB, cls.get_interaction_sim(interaction_instance), cls.get_interaction_target(interaction_instance))


class JoinSexSingleOraljobInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'JoinSexSingleOraljobInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _test_join_to_sex_single_interaction(cls.get_interaction_sim(interaction_context), interaction_target, (SexCategoryType.ORALJOB,))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return _join_to_sex_single_interaction(SexCategoryType.ORALJOB, cls.get_interaction_sim(interaction_instance), cls.get_interaction_target(interaction_instance))


class JoinSexSingleVaginalInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'JoinSexSingleVaginalInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _test_join_to_sex_single_interaction(cls.get_interaction_sim(interaction_context), interaction_target, (SexCategoryType.VAGINAL,))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return _join_to_sex_single_interaction(SexCategoryType.VAGINAL, cls.get_interaction_sim(interaction_instance), cls.get_interaction_target(interaction_instance))


class JoinSexSingleAnalInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'JoinSexSingleAnalInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _test_join_to_sex_single_interaction(cls.get_interaction_sim(interaction_context), interaction_target, (SexCategoryType.ANAL,))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return _join_to_sex_single_interaction(SexCategoryType.ANAL, cls.get_interaction_sim(interaction_instance), cls.get_interaction_target(interaction_instance))


class JoinSexSingleRandomInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'JoinSexSingleRandomInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _test_join_to_sex_single_interaction(cls.get_interaction_sim(interaction_context), interaction_target, (SexCategoryType.TEASING, SexCategoryType.HANDJOB, SexCategoryType.ORALJOB, SexCategoryType.FOOTJOB, SexCategoryType.VAGINAL, SexCategoryType.ANAL))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return _join_to_sex_single_interaction(None, cls.get_interaction_sim(interaction_instance), cls.get_interaction_target(interaction_instance))


def _test_join_to_sex_multiple_interaction(interaction_sim, interaction_target, sex_category_types):
    if interaction_target is None or not TurboTypesUtil.Sims.is_sim(interaction_target):
        return False
    if sim_ev(interaction_sim).active_sex_handler is None:
        return False
    active_sex_handler = sim_ev(interaction_sim).active_sex_handler
    if sim_ev(interaction_target).active_pre_sex_handler is not None and sim_ev(interaction_target).active_pre_sex_handler.get_identifier() != active_sex_handler.get_identifier():
        return False
    if sim_ev(interaction_target).active_sex_handler is None or sim_ev(interaction_sim).active_sex_handler is sim_ev(interaction_target).active_sex_handler:
        test_incest_of_sims = () if get_relationship_setting(RelationshipSetting.INCEST_STATE, variable_type=bool) else tuple(active_sex_handler.get_actors_sim_info_gen())
        (min_age_limit, max_age_limit) = get_age_limits_for_sex(tuple(active_sex_handler.get_actors_sim_info_gen()))
        skip_sims_ids = [TurboManagerUtil.Sim.get_sim_id(actor_sim_info) for actor_sim_info in active_sex_handler.get_actors_sim_info_gen()]
        target_sim_id = TurboManagerUtil.Sim.get_sim_id(interaction_target)
        has_target_sim = False
        for sim_id in get_nearby_sims_for_sex(active_sex_handler.get_los_position(), radius=16, relative_sims=test_incest_of_sims, min_sims_age=min_age_limit, max_sims_age=max_age_limit, skip_sims_ids=skip_sims_ids):
            while sim_id == target_sim_id:
                has_target_sim = True
                break
        if interaction_sim is not interaction_target and has_target_sim is False:
            return False
        for sex_category_type in sex_category_types:
            while get_animation_max_amount_of_actors(sex_category_type, active_sex_handler.get_object_identifier()[0]) > active_sex_handler.get_actors_amount() or get_animation_max_amount_of_actors(sex_category_type, active_sex_handler.get_object_identifier()[1]) > active_sex_handler.get_actors_amount():
                return True
    return False


def _open_join_sex_sim_selector(sex_category_type, interaction_sim, interaction_target):
    active_sex_handler = sim_ev(interaction_sim).active_sex_handler
    if active_sex_handler is None:
        return False
    pre_sex_handler = active_sex_handler.get_pre_sex_handler(is_joining=True)
    selected_sims_ids = (TurboManagerUtil.Sim.get_sim_id(interaction_target),) if interaction_target is not None and TurboTypesUtil.Sims.is_sim(interaction_target) else ()
    open_join_sims_picker_dialog(pre_sex_handler, sex_category_type, selected_sims_ids=selected_sims_ids)
    return True


class JoinSexMultipleTeasingInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'JoinSexMultipleTeasingInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _test_join_to_sex_multiple_interaction(cls.get_interaction_sim(interaction_context), interaction_target, (SexCategoryType.TEASING,))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return _open_join_sex_sim_selector(SexCategoryType.TEASING, cls.get_interaction_sim(interaction_instance), cls.get_interaction_target(interaction_instance))


class JoinSexMultipleHandjobInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'JoinSexMultipleHandjobInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _test_join_to_sex_multiple_interaction(cls.get_interaction_sim(interaction_context), interaction_target, (SexCategoryType.HANDJOB,))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return _open_join_sex_sim_selector(SexCategoryType.HANDJOB, cls.get_interaction_sim(interaction_instance), cls.get_interaction_target(interaction_instance))


class JoinSexMultipleFootjobInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'JoinSexMultipleFootjobInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _test_join_to_sex_multiple_interaction(cls.get_interaction_sim(interaction_context), interaction_target, (SexCategoryType.FOOTJOB,))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return _open_join_sex_sim_selector(SexCategoryType.FOOTJOB, cls.get_interaction_sim(interaction_instance), cls.get_interaction_target(interaction_instance))


class JoinSexMultipleOraljobInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'JoinSexMultipleOraljobInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _test_join_to_sex_multiple_interaction(cls.get_interaction_sim(interaction_context), interaction_target, (SexCategoryType.ORALJOB,))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return _open_join_sex_sim_selector(SexCategoryType.ORALJOB, cls.get_interaction_sim(interaction_instance), cls.get_interaction_target(interaction_instance))


class JoinSexMultipleVaginalInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'JoinSexMultipleVaginalInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _test_join_to_sex_multiple_interaction(cls.get_interaction_sim(interaction_context), interaction_target, (SexCategoryType.VAGINAL,))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return _open_join_sex_sim_selector(SexCategoryType.VAGINAL, cls.get_interaction_sim(interaction_instance), cls.get_interaction_target(interaction_instance))


class JoinSexMultipleAnalInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'JoinSexMultipleAnalInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _test_join_to_sex_multiple_interaction(cls.get_interaction_sim(interaction_context), interaction_target, (SexCategoryType.ANAL,))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return _open_join_sex_sim_selector(SexCategoryType.ANAL, cls.get_interaction_sim(interaction_instance), cls.get_interaction_target(interaction_instance))


class JoinSexMultipleRandomInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'JoinSexMultipleRandomInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _test_join_to_sex_multiple_interaction(cls.get_interaction_sim(interaction_context), interaction_target, (SexCategoryType.TEASING, SexCategoryType.HANDJOB, SexCategoryType.ORALJOB, SexCategoryType.FOOTJOB, SexCategoryType.VAGINAL, SexCategoryType.ANAL))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return _open_join_sex_sim_selector(None, cls.get_interaction_sim(interaction_instance), cls.get_interaction_target(interaction_instance))

