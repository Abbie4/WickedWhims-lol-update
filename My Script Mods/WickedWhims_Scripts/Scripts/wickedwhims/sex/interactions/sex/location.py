'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from turbolib.math_util import TurboMathUtil
from turbolib.object_util import TurboObjectUtil
from turbolib.resource_util import TurboResourceUtil
from turbolib.types_util import TurboTypesUtil
from turbolib.world_util import TurboWorldUtil
from turbolib.wrappers.interactions import TurboTerrainImmediateSuperInteraction, TurboInteractionStartMixin
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.sex._ts4_sex_utils import is_safe_floor_object_position, get_floor_object_position, get_floor_object_level
from wickedwhims.sex.animations.animations_operator import has_animations_with_params
from wickedwhims.sex.enums.sex_gender import get_sim_sex_gender
from wickedwhims.sex.enums.sex_type import SexCategoryType
from wickedwhims.sex.sex_location_handler import SexInteractionLocationType
from wickedwhims.sex.sex_operators.sex_change_location_operator import change_player_sex_interaction_location
from wickedwhims.sex.sex_privileges import is_sim_allowed_for_animation, display_not_allowed_message
from wickedwhims.utils_objects import get_object_fixed_direction
from wickedwhims.utils_routes import is_sim_allowed_on_active_lot

def _test_for_change_sex_location(interaction_context, interaction_sim, interaction_target, sex_category_types):
    if interaction_target is None:
        return False
    active_sex_handler = sim_ev(interaction_sim).active_sex_handler
    if active_sex_handler is None:
        return False
    if active_sex_handler.is_playing is False:
        return False
    if TurboTypesUtil.Objects.is_game_object(interaction_target):
        object_position = TurboObjectUtil.Position.get_position(interaction_target) + get_object_fixed_direction(interaction_target)
        target_room_id = TurboWorldUtil.Lot.get_room_id(TurboObjectUtil.Position.get_location(interaction_target), position=object_position)
    elif interaction_context is not None:
        target_room_id = TurboWorldUtil.Lot.get_room_id(TurboMathUtil.Location.get_location(get_floor_object_position(interaction_target, interaction_context), get_floor_object_level(interaction_target, interaction_context), 0))
    else:
        return False
    if target_room_id != TurboWorldUtil.Lot.get_room_id(active_sex_handler.get_location()):
        return False
    if TurboTypesUtil.Objects.is_game_object(interaction_target):
        interaction_target = TurboObjectUtil.GameObject.get_parent(interaction_target)
        if active_sex_handler.get_game_object_id() == TurboResourceUtil.Resource.get_id(interaction_target):
            return False
        if not is_sim_allowed_on_active_lot(interaction_sim) and TurboWorldUtil.Lot.is_position_on_active_lot(TurboObjectUtil.Position.get_position(interaction_target)):
            return False
    else:
        if not is_safe_floor_object_position(interaction_target, interaction_context):
            return False
        if TurboTypesUtil.Objects.is_terrain(interaction_target) and not is_sim_allowed_on_active_lot(interaction_sim) and TurboWorldUtil.Lot.is_position_on_active_lot(get_floor_object_position(interaction_target, interaction_context)):
            return False
    object_identifier = SexInteractionLocationType.get_location_identifier(interaction_target)
    genders_list = list()
    for actor_sim_info in active_sex_handler.get_actors_sim_info_gen():
        genders_list.append(get_sim_sex_gender(actor_sim_info))
    has_animations = False
    for sex_category_type in sex_category_types:
        while has_animations_with_params(sex_category_type, object_identifier, genders_list):
            has_animations = True
            break
    if has_animations is False:
        return False
    return True


def _change_sex_location(interaction_sim, interaction_target, interaction_context, sex_category_type):
    if sex_category_type is not None:
        sex_allowed = is_sim_allowed_for_animation(sim_ev(interaction_sim).active_sex_handler.get_actors_sim_info_gen(), sex_category_type)
        if not sex_allowed:
            display_not_allowed_message(sex_allowed)
            return False
    active_sex_handler = sim_ev(interaction_sim).active_sex_handler
    if active_sex_handler is None:
        return False
    change_player_sex_interaction_location(active_sex_handler, interaction_target, interaction_context=interaction_context, interaction_type=sex_category_type)
    return True


class ChangeSexLocationTeasingInteraction(TurboTerrainImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'ChangeSexLocationTeasingInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _test_for_change_sex_location(interaction_context, cls.get_interaction_sim(interaction_context), interaction_target, (SexCategoryType.TEASING,))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return _change_sex_location(cls.get_interaction_sim(interaction_instance), cls.get_interaction_target(interaction_instance), cls.get_interaction_context(interaction_instance), sex_category_type=SexCategoryType.TEASING)


class ChangeSexLocationHandjobInteraction(TurboTerrainImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'ChangeSexLocationHandjobInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _test_for_change_sex_location(interaction_context, cls.get_interaction_sim(interaction_context), interaction_target, (SexCategoryType.HANDJOB,))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return _change_sex_location(cls.get_interaction_sim(interaction_instance), cls.get_interaction_target(interaction_instance), cls.get_interaction_context(interaction_instance), sex_category_type=SexCategoryType.HANDJOB)


class ChangeSexLocationFootjobInteraction(TurboTerrainImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'ChangeSexLocationFootjobInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _test_for_change_sex_location(interaction_context, cls.get_interaction_sim(interaction_context), interaction_target, (SexCategoryType.FOOTJOB,))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return _change_sex_location(cls.get_interaction_sim(interaction_instance), cls.get_interaction_target(interaction_instance), cls.get_interaction_context(interaction_instance), sex_category_type=SexCategoryType.FOOTJOB)


class ChangeSexLocationOraljobInteraction(TurboTerrainImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'ChangeSexLocationOraljobInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _test_for_change_sex_location(interaction_context, cls.get_interaction_sim(interaction_context), interaction_target, (SexCategoryType.ORALJOB,))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return _change_sex_location(cls.get_interaction_sim(interaction_instance), cls.get_interaction_target(interaction_instance), cls.get_interaction_context(interaction_instance), sex_category_type=SexCategoryType.ORALJOB)


class ChangeSexLocationVaginalInteraction(TurboTerrainImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'ChangeSexLocationVaginalInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _test_for_change_sex_location(interaction_context, cls.get_interaction_sim(interaction_context), interaction_target, (SexCategoryType.VAGINAL,))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return _change_sex_location(cls.get_interaction_sim(interaction_instance), cls.get_interaction_target(interaction_instance), cls.get_interaction_context(interaction_instance), sex_category_type=SexCategoryType.VAGINAL)


class ChangeSexLocationAnalInteraction(TurboTerrainImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'ChangeSexLocationAnalInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _test_for_change_sex_location(interaction_context, cls.get_interaction_sim(interaction_context), interaction_target, (SexCategoryType.ANAL,))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return _change_sex_location(cls.get_interaction_sim(interaction_instance), cls.get_interaction_target(interaction_instance), cls.get_interaction_context(interaction_instance), sex_category_type=SexCategoryType.ANAL)


class ChangeSexLocationRandomInteraction(TurboTerrainImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'ChangeSexLocationRandomInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _test_for_change_sex_location(interaction_context, cls.get_interaction_sim(interaction_context), interaction_target, (SexCategoryType.TEASING, SexCategoryType.HANDJOB, SexCategoryType.ORALJOB, SexCategoryType.FOOTJOB, SexCategoryType.VAGINAL, SexCategoryType.ANAL))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return _change_sex_location(cls.get_interaction_sim(interaction_instance), cls.get_interaction_target(interaction_instance), cls.get_interaction_context(interaction_instance), sex_category_type=None)

