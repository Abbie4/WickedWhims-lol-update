from enums.tags_enum import GameTag
from turbolib.math_util import TurboMathUtil
from turbolib.object_util import TurboObjectUtil
from turbolib.world_util import TurboWorldUtil

def get_object_fixed_direction(game_object):
    object_tags = TurboObjectUtil.GameObject.get_game_tags(game_object)
    if GameTag.BUILD_WINDOW in object_tags:
        return TurboObjectUtil.Position.get_object_forward_vector(game_object, reverse=True)*0.5
    return TurboObjectUtil.Position.get_object_forward_vector(game_object)


def get_object_fixed_position(game_object):
    object_position = TurboObjectUtil.Position.get_position(game_object)
    object_tags = TurboObjectUtil.GameObject.get_game_tags(game_object)
    if GameTag.BUILD_WINDOW in object_tags:
        routing_surface = TurboMathUtil.Location.get_location_routing_surface(TurboObjectUtil.Position.get_location(game_object))
        object_position = TurboMathUtil.Position.get_vector3(object_position.x, TurboWorldUtil.Zone.get_routing_surface_height_at(object_position, routing_surface), object_position.z)
    return object_position

