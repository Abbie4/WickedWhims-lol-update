'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
import random
from turbolib.math_util import TurboMathUtil
from turbolib.object_util import TurboObjectUtil
from turbolib.resource_util import TurboResourceUtil
from turbolib.types_util import TurboTypesUtil
from wickedwhims.sex._ts4_sex_utils import get_floor_object_position, get_floor_object_level
from wickedwhims.sex.animations.animations_operator import get_random_animation
from wickedwhims.sex.dialogs.sex_change import open_change_sex_location_animations_picker_dialog
from wickedwhims.sex.sex_location_handler import SexInteractionLocationType
from wickedwhims.utils_interfaces import display_ok_dialog
from wickedwhims.utils_objects import get_object_fixed_position, get_object_fixed_direction

def change_player_sex_interaction_location(active_sex_handler, location_object, interaction_context=None, interaction_type=None):
    object_identifier = SexInteractionLocationType.get_location_identifier(location_object)
    if TurboTypesUtil.Objects.is_game_object(location_object):
        location_object = TurboObjectUtil.GameObject.get_parent(location_object)
        game_object_id = TurboResourceUtil.Resource.get_id(location_object)
        location_position = get_object_fixed_position(location_object)
        location_level = TurboMathUtil.Location.get_location_level(TurboObjectUtil.Position.get_location(location_object))
        location_angle = TurboMathUtil.Orientation.convert_orientation_to_angle(TurboMathUtil.Location.get_location_orientation(TurboObjectUtil.Position.get_location(location_object)))
        location_route_position = TurboObjectUtil.Position.get_position(location_object) + get_object_fixed_direction(location_object)
    elif interaction_context is not None:
        game_object_id = -1
        location_position = get_floor_object_position(location_object, interaction_context)
        location_level = get_floor_object_level(location_object, interaction_context)
        location_angle = random.randint(0, 360)
        location_route_position = location_position
    else:
        return
    if interaction_type is not None:
        open_change_sex_location_animations_picker_dialog(active_sex_handler, interaction_type, object_identifier, game_object_id, 0, location_position.x, location_position.y, location_position.z, location_level, location_angle, location_route_position.x, location_route_position.y, location_route_position.z, location_level)
    else:
        random_animation = get_random_animation(object_identifier, tuple(active_sex_handler.get_actors_sim_info_gen()))
        if random_animation is None:
            display_ok_dialog(text=2459296019, title=1890248379)
            return
        active_sex_handler.set_animation_instance(random_animation, is_manual=True)
        active_sex_handler.set_object_identifier(object_identifier)
        active_sex_handler.set_game_object_id(game_object_id)
        active_sex_handler.set_object_height(0)
        active_sex_handler.set_location(location_position.x, location_position.y, location_position.z, location_level, location_angle)
        active_sex_handler.set_route_position(location_route_position.x, location_route_position.y, location_route_position.z, location_level)
        active_sex_handler.reassign_actors()
        active_sex_handler.restart()

