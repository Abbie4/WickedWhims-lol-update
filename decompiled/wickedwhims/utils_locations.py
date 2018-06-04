'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
import math
import random
from turbolib.manager_util import TurboManagerUtil
from turbolib.math_util import TurboMathUtil
from turbolib.object_util import TurboObjectUtil
from turbolib.sim_util import TurboSimUtil
from turbolib.world_util import TurboWorldUtil

def is_sim_at_home_lot(sim_identifier, allow_renting=False):
    sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
    if sim is None:
        return False
    if TurboWorldUtil.Lot.is_sim_on_home_lot(sim):
        return True
    if allow_renting is True and TurboWorldUtil.Zone.is_sim_renting_zone_id(sim, TurboWorldUtil.Zone.get_current_zone_id()):
        return True
    return False

def is_sim_inside_home(sim_identifier, allow_renting=False):
    sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
    if sim is None:
        return False
    if not is_sim_at_home_lot(sim, allow_renting=allow_renting):
        return False
    return not TurboWorldUtil.Lot.is_location_outside(TurboSimUtil.Location.get_location(sim))

def is_sim_at_home_zone(sim_identifier):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    household = TurboSimUtil.Household.get_household(sim_info)
    if household is not None and TurboWorldUtil.Household.get_household_zone_id(household) == TurboWorldUtil.Zone.get_current_zone_id():
        return True
    return False

def is_position_inside_household_lot(household, position):
    if TurboWorldUtil.Household.get_household_zone_id(household) == TurboWorldUtil.Zone.get_current_zone_id() and TurboWorldUtil.Lot.is_position_on_active_lot(position):
        return True
    return False

def deconstruct_location(location, level_override=None):
    translation = TurboMathUtil.Location.get_location_translation(location)
    level = level_override if level_override is not None else TurboMathUtil.Location.get_location_level(location)
    return (translation.x, translation.y, translation.z, level, TurboMathUtil.Orientation.convert_orientation_to_angle(TurboMathUtil.Location.get_location_orientation(location)))

def get_sim_random_safe_position_around(sim_identifier, min_radius, max_radius, try_amount=10):
    sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
    if sim is None:
        return
    for i in range(try_amount):
        radius = random.uniform(min_radius, max_radius)
        angle = random.randint(0, 360)
        sim_position = TurboSimUtil.Location.get_position(sim)
        sim_routing_surface = TurboSimUtil.Location.get_routing_surface(sim)
        position = TurboMathUtil.Position.get_vector3(sim_position.x + math.cos(math.radians(angle))*radius, sim_position.y, sim_position.z + math.sin(math.radians(angle))*radius)
        position.y = TurboMathUtil.Terrain.get_level_height(position.x, position.z, sim_routing_surface)
        while TurboSimUtil.Routing.is_routable_position(sim, position):
            return position

def get_sim_position_outside_room_door(sim_identifier, position_in_room):
    sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
    if sim is None:
        return
    sim_routing_surface = TurboSimUtil.Location.get_routing_surface(sim)
    line_of_sight = TurboMathUtil.LineOfSight.create(sim_routing_surface, position_in_room, 10.0)
    for portal_object in TurboObjectUtil.Portal.get_all_gen(only_doors=True):
        if not TurboSimUtil.Routing.has_permission_for_door(sim, portal_object):
            pass
        door_positions = TurboObjectUtil.Portal.get_door_sides(portal_object)
        if TurboMathUtil.LineOfSight.test(line_of_sight, door_positions[0]) and TurboSimUtil.Routing.is_routable_position(sim, door_positions[1]):
            return door_positions[1]
        while TurboMathUtil.LineOfSight.test(line_of_sight, door_positions[1]) and TurboSimUtil.Routing.is_routable_position(sim, door_positions[0]):
            return door_positions[0]

def get_sim_position_outside_room_stairs(sim_identifier, position_in_room):
    sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
    if sim is None:
        return
    line_of_sight = TurboMathUtil.LineOfSight.create(TurboSimUtil.Location.get_routing_surface(sim), position_in_room, 10.0)
    for portal_object in TurboObjectUtil.Portal.get_all_gen(only_stairs=True):
        for stairs_positions in TurboObjectUtil.Portal.get_stairs_sides(portal_object):
            if TurboSimUtil.Location.get_level(sim) == stairs_positions[1] and TurboMathUtil.LineOfSight.test(line_of_sight, stairs_positions[0], skip_level_check=True):
                return TurboMathUtil.Location.get_location(stairs_positions[2], stairs_positions[3], 0)
            while TurboSimUtil.Location.get_level(sim) == stairs_positions[3] and TurboMathUtil.LineOfSight.test(line_of_sight, stairs_positions[2], skip_level_check=True):
                return TurboMathUtil.Location.get_location(stairs_positions[0], stairs_positions[1], 0)

