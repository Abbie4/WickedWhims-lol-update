'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
import random
from turbolib.manager_util import TurboManagerUtil
from turbolib.math_util import TurboMathUtil
from turbolib.object_util import TurboObjectUtil
from turbolib.resource_util import TurboResourceUtil
from turbolib.sim_util import TurboSimUtil
from turbolib.types_util import TurboTypesUtil
from turbolib.world_util import TurboWorldUtil
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.sex._ts4_sex_utils import get_floor_object_level, get_floor_object_position
from wickedwhims.sex.dialogs.npc_sex_init import open_sex_npc_sims_picker_dialog, open_random_sex_npc_sims_picker_dialog
from wickedwhims.sex.dialogs.sex_init import open_start_sex_sims_picker_dialog, open_start_random_sex_sims_picker_dialog
from wickedwhims.sex.sex_handlers.pre_sex_handler import PreSexInteractionHandler
from wickedwhims.sex.sex_location_handler import SexInteractionLocationType
from wickedwhims.sex.sex_operators.pre_sex_handlers_operator import start_sex_interaction_from_pre_sex_handler
from wickedwhims.utils_objects import get_object_fixed_direction, get_object_fixed_position

def start_new_player_sex_interaction(sim_identifier, location_object, interaction_context=None, origin_position=None, interaction_type=None):
    location_object = TurboObjectUtil.GameObject.get_parent(location_object)
    location_identifier = SexInteractionLocationType.get_location_identifier(location_object)
    if TurboTypesUtil.Objects.is_game_object(location_object):
        game_object_id = TurboResourceUtil.Resource.get_id(location_object)
        location_position = get_object_fixed_position(location_object)
        location_level = TurboMathUtil.Location.get_location_level(TurboObjectUtil.Position.get_location(location_object))
        location_angle = TurboMathUtil.Orientation.convert_orientation_to_angle(TurboMathUtil.Location.get_location_orientation(TurboObjectUtil.Position.get_location(location_object)))
        location_route_position = TurboObjectUtil.Position.get_position(location_object) + get_object_fixed_direction(location_object)
    elif interaction_context is not None:
        game_object_id = -1
        location_position = get_floor_object_position(location_object, interaction_context)
        location_level = get_floor_object_level(location_object, interaction_context)
        location_angle = TurboMathUtil.Orientation.convert_orientation_to_angle(TurboMathUtil.Location.get_location_orientation(TurboSimUtil.Location.get_location(sim_identifier)))
        location_route_position = location_position
    else:
        return
    origin_position = TurboSimUtil.Location.get_position(sim_identifier) if origin_position is None else origin_position
    pre_sex_handler = PreSexInteractionHandler(interaction_type, TurboManagerUtil.Sim.get_sim_id(sim_identifier), location_identifier, game_object_id, 0, TurboWorldUtil.Lot.get_active_lot_id(), location_position.x, location_position.y, location_position.z, location_level, location_angle, location_route_position.x, location_route_position.y, location_route_position.z, location_level)
    sim_ev(sim_identifier).active_pre_sex_handler = pre_sex_handler
    if interaction_type is not None:
        open_start_sex_sims_picker_dialog(origin_position, pre_sex_handler)
    else:
        open_start_random_sex_sims_picker_dialog(origin_position, pre_sex_handler)

def start_new_npc_sex_interaction(location_object, interaction_context=None, interaction_type=None, is_manual=False):
    location_object = TurboObjectUtil.GameObject.get_parent(location_object)
    location_identifier = SexInteractionLocationType.get_location_identifier(location_object)
    if TurboTypesUtil.Objects.is_game_object(location_object):
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
        open_sex_npc_sims_picker_dialog(location_position, interaction_type, location_identifier, game_object_id, 0, TurboWorldUtil.Lot.get_active_lot_id(), location_position, location_level, location_angle, location_route_position, location_level, is_manual=is_manual)
    else:
        open_random_sex_npc_sims_picker_dialog(location_position, location_identifier, game_object_id, 0, TurboWorldUtil.Lot.get_active_lot_id(), location_position, location_level, location_angle, location_route_position, location_level, is_manual=is_manual)

def start_new_direct_sex_interaction(sims_list, location_object, animation_instance, is_autonomy=True):
    creator_sim = TurboManagerUtil.Sim.get_sim_instance(next(iter(sims_list)))
    location_object = TurboObjectUtil.GameObject.get_parent(location_object)
    location_identifier = SexInteractionLocationType.get_location_identifier(location_object)
    if TurboTypesUtil.Objects.is_game_object(location_object):
        game_object_id = TurboResourceUtil.Resource.get_id(location_object)
        location_position = get_object_fixed_position(location_object)
        location_level = TurboMathUtil.Location.get_location_level(TurboObjectUtil.Position.get_location(location_object))
        location_angle = TurboMathUtil.Orientation.convert_orientation_to_angle(TurboMathUtil.Location.get_location_orientation(TurboObjectUtil.Position.get_location(location_object)))
        location_route_position = TurboObjectUtil.Position.get_position(location_object) + get_object_fixed_direction(location_object)
    elif TurboTypesUtil.Data.is_location(location_object):
        game_object_id = -1
        location_position = TurboMathUtil.Location.get_location_translation(location_object)
        location_level = TurboMathUtil.Location.get_location_level(location_object)
        location_angle = TurboMathUtil.Orientation.convert_orientation_to_angle(TurboMathUtil.Location.get_location_orientation(TurboSimUtil.Location.get_location(creator_sim)))
        location_route_position = location_position
    else:
        return False
    pre_sex_handler = PreSexInteractionHandler(animation_instance.get_sex_category(), TurboManagerUtil.Sim.get_sim_id(creator_sim), location_identifier, game_object_id, 0, TurboWorldUtil.Lot.get_active_lot_id(), location_position.x, location_position.y, location_position.z, location_level, location_angle, location_route_position.x, location_route_position.y, location_route_position.z, location_level, is_autonomy=is_autonomy)
    pre_sex_handler.set_animation_instance(animation_instance)
    for sim in sims_list:
        pre_sex_handler.add_sim(TurboManagerUtil.Sim.get_sim_id(sim))
        sim_ev(sim).active_pre_sex_handler = pre_sex_handler
    return start_sex_interaction_from_pre_sex_handler(pre_sex_handler)

