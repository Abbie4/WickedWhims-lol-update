from turbolib.object_util import TurboObjectUtil
from turbolib.sim_util import TurboSimUtil
from turbolib.types_util import TurboTypesUtil
from turbolib.world_util import TurboWorldUtil
from turbolib.wrappers.interactions import TurboTerrainImmediateSuperInteraction, TurboInteractionStartMixin
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.sex._ts4_sex_utils import is_safe_floor_object_position, get_floor_object_position
from wickedwhims.sex.animations.animations_operator import has_object_identifier_animations
from wickedwhims.sex.enums.sex_gender import get_sim_sex_gender
from wickedwhims.sex.enums.sex_type import SexCategoryType
from wickedwhims.sex.settings.sex_settings import SexSetting, get_sex_setting
from wickedwhims.sex.sex_location_handler import SexInteractionLocationType
from wickedwhims.sex.sex_operators.sex_init_operator import start_new_player_sex_interaction
from wickedwhims.sxex_bridge.sex import is_sim_ready_for_sex
from wickedwhims.utils_routes import is_sim_allowed_on_active_lot

def _test_for_sex_start(interaction_context, interaction_sim, interaction_target, sex_category_types):
    if interaction_target is None:
        return False
    if not is_sim_ready_for_sex(interaction_sim) or sim_ev(interaction_sim).active_pre_sex_handler is not None:
        return False
    if not get_sex_setting(SexSetting.TEENS_SEX_STATE, variable_type=bool) and (TurboSimUtil.Age.get_age(interaction_sim) == TurboSimUtil.Age.TEEN or TurboSimUtil.Age.get_age(interaction_sim) == TurboSimUtil.Age.CHILD):
        return False
    if TurboTypesUtil.Objects.is_game_object(interaction_target):
        interaction_target = TurboObjectUtil.GameObject.get_parent(interaction_target)
        if not is_sim_allowed_on_active_lot(interaction_sim) and TurboWorldUtil.Lot.is_position_on_active_lot(TurboObjectUtil.Position.get_position(interaction_target)):
            return False
    else:
        if not is_safe_floor_object_position(interaction_target, interaction_context):
            return False
        if TurboTypesUtil.Objects.is_terrain(interaction_target) and not is_sim_allowed_on_active_lot(interaction_sim) and TurboWorldUtil.Lot.is_position_on_active_lot(get_floor_object_position(interaction_target, interaction_context)):
            return False
    object_identifier = SexInteractionLocationType.get_location_identifier(interaction_target)
    sim_gender = get_sim_sex_gender(interaction_sim)
    for sex_category_type in sex_category_types:
        if sex_category_type is None:
            continue
        if has_object_identifier_animations(object_identifier, sex_category_type, sim_gender):
            return True
    return False


class StartSexTeasingInteraction(TurboTerrainImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'StartSexTeasingInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _test_for_sex_start(interaction_context, cls.get_interaction_sim(interaction_context), interaction_target, (SexCategoryType.TEASING,))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return start_new_player_sex_interaction(cls.get_interaction_sim(interaction_instance), cls.get_interaction_target(interaction_instance), interaction_context=cls.get_interaction_context(interaction_instance), interaction_type=SexCategoryType.TEASING)


class StartSexHandjobInteraction(TurboTerrainImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'StartSexHandjobInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _test_for_sex_start(interaction_context, cls.get_interaction_sim(interaction_context), interaction_target, (SexCategoryType.HANDJOB,))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return start_new_player_sex_interaction(cls.get_interaction_sim(interaction_instance), cls.get_interaction_target(interaction_instance), interaction_context=cls.get_interaction_context(interaction_instance), interaction_type=SexCategoryType.HANDJOB)


class StartSexFootjobInteraction(TurboTerrainImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'StartSexFootjobInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _test_for_sex_start(interaction_context, cls.get_interaction_sim(interaction_context), interaction_target, (SexCategoryType.FOOTJOB,))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return start_new_player_sex_interaction(cls.get_interaction_sim(interaction_instance), cls.get_interaction_target(interaction_instance), interaction_context=cls.get_interaction_context(interaction_instance), interaction_type=SexCategoryType.FOOTJOB)


class StartSexOraljobInteraction(TurboTerrainImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'StartSexOraljobInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _test_for_sex_start(interaction_context, cls.get_interaction_sim(interaction_context), interaction_target, (SexCategoryType.ORALJOB,))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return start_new_player_sex_interaction(cls.get_interaction_sim(interaction_instance), cls.get_interaction_target(interaction_instance), interaction_context=cls.get_interaction_context(interaction_instance), interaction_type=SexCategoryType.ORALJOB)


class StartSexVaginalInteraction(TurboTerrainImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'StartSexVaginalInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _test_for_sex_start(interaction_context, cls.get_interaction_sim(interaction_context), interaction_target, (SexCategoryType.VAGINAL,))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return start_new_player_sex_interaction(cls.get_interaction_sim(interaction_instance), cls.get_interaction_target(interaction_instance), interaction_context=cls.get_interaction_context(interaction_instance), interaction_type=SexCategoryType.VAGINAL)


class StartSexAnalInteraction(TurboTerrainImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'StartSexAnalInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _test_for_sex_start(interaction_context, cls.get_interaction_sim(interaction_context), interaction_target, (SexCategoryType.ANAL,))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return start_new_player_sex_interaction(cls.get_interaction_sim(interaction_instance), cls.get_interaction_target(interaction_instance), interaction_context=cls.get_interaction_context(interaction_instance), interaction_type=SexCategoryType.ANAL)


class StartSexRandomInteraction(TurboTerrainImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'StartSexRandomInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _test_for_sex_start(interaction_context, cls.get_interaction_sim(interaction_context), interaction_target, (SexCategoryType.TEASING, SexCategoryType.HANDJOB, SexCategoryType.ORALJOB, SexCategoryType.FOOTJOB, SexCategoryType.VAGINAL, SexCategoryType.ANAL))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return start_new_player_sex_interaction(cls.get_interaction_sim(interaction_instance), cls.get_interaction_target(interaction_instance), interaction_context=cls.get_interaction_context(interaction_instance), interaction_type=None)

