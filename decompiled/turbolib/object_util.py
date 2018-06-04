'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
import objects.system
import routing
import services
import terrain
from objects.doors.door import Door
from objects.object_enums import ResetReason
from objects.puddles import PuddleSize, PuddleLiquid, create_puddle
from objects.stairs.stairs import Stairs
from placement import get_accurate_placement_footprint_polygon
from turbolib.math_util import TurboMathUtil

class TurboObjectUtil:
    __qualname__ = 'TurboObjectUtil'

    class Definition:
        __qualname__ = 'TurboObjectUtil.Definition'

        @staticmethod
        def get(object_instance_id):
            definition_manager = services.definition_manager()
            return definition_manager.get(object_instance_id)

    class GameObject:
        __qualname__ = 'TurboObjectUtil.GameObject'

        @staticmethod
        def get_all_gen(only_valid_objects=True):
            if only_valid_objects is True:
                for game_object in services.object_manager().valid_objects():
                    yield game_object
            else:
                for game_object in services.object_manager().get_all():
                    yield game_object

        @staticmethod
        def get_object_definition(game_object):
            return game_object.definition

        @staticmethod
        def get_object_with_id(game_object_id):
            if game_object_id is None or game_object_id == -1:
                return
            return services.object_manager().get(game_object_id)

        @staticmethod
        def get_catalog_name(game_object):
            return game_object.catalog_name

        @staticmethod
        def has_parent(game_object):
            return game_object.parent is not None

        @staticmethod
        def get_parent(game_object):

            def _get_parent(child_game_object):
                return child_game_object.parent

            if TurboObjectUtil.GameObject.has_parent(game_object):
                return TurboObjectUtil.GameObject.get_parent(_get_parent(game_object))
            return game_object

        @staticmethod
        def is_in_use(game_object):
            return hasattr(game_object, 'self_or_part_in_use') and game_object.self_or_part_in_use

        @staticmethod
        def create_object(object_instance_id, location=None, household_id=-1):
            game_object = objects.system.create_object(object_instance_id)
            if location is not None:
                game_object.location = location
            if household_id != -1:
                game_object.set_household_owner_id(household_id)
            return game_object

        @staticmethod
        def destroy_object(game_object, cause='TurboLib destroy.'):
            game_object.destroy(cause=cause)

        @staticmethod
        def reset(game_object):
            try:
                game_object.reset(ResetReason.RESET_EXPECTED)
            except:
                pass

        @staticmethod
        def get_game_tags(game_object):
            return game_object.get_tags()

    class Position:
        __qualname__ = 'TurboObjectUtil.Position'

        @staticmethod
        def get_location(game_object):
            return game_object.location

        @staticmethod
        def set_location(game_object, location):
            game_object.location = location

        @staticmethod
        def get_position(game_object):
            return game_object.position

        @staticmethod
        def get_object_forward_vector(game_object, reverse=False):
            if reverse is False:
                return game_object.forward
            return game_object.forward*-1

        @staticmethod
        def get_object_corners_on_flat(game_object):
            polygon = get_accurate_placement_footprint_polygon(game_object.position, game_object.orientation, game_object.scale, game_object.get_footprint())
            return list(polygon)

    class Portal:
        __qualname__ = 'TurboObjectUtil.Portal'

        @staticmethod
        def get_all_gen(only_doors=False, only_stairs=False):
            for portal_object in services.object_manager().portal_cache_gen():
                if only_doors is True:
                    while isinstance(portal_object, Door):
                        yield portal_object
                        if only_stairs is True:
                            while isinstance(portal_object, Stairs):
                                yield portal_object
                                yield portal_object
                        yield portal_object
                if only_stairs is True:
                    while isinstance(portal_object, Stairs):
                        yield portal_object
                        yield portal_object
                yield portal_object

        @staticmethod
        def get_door_sides(portal_object):
            door_pos = portal_object.transform.translation
            door_orient = portal_object.transform.orientation
            pos_offset = door_orient.transform_vector(TurboMathUtil.Position.get_vector3(0.0, 0.0, 0.85))
            door_position_1 = door_pos + pos_offset
            door_position_2 = door_pos - pos_offset
            door_position_1.y = terrain.get_lot_level_height(door_position_1.x, door_position_1.z, portal_object.routing_surface.secondary_id, portal_object.routing_surface.primary_id)
            door_position_2.y = terrain.get_lot_level_height(door_position_2.x, door_position_2.z, portal_object.routing_surface.secondary_id, portal_object.routing_surface.primary_id)
            return (door_position_1, door_position_2)

        @staticmethod
        def get_stairs_sides(portal_object):
            stair_lanes = routing.get_stair_portals(portal_object.id, portal_object.zone_id)
            if stair_lanes is None or len(stair_lanes) == 0:
                return ()
            for lane in stair_lanes:
                for end_set in lane:
                    lane_start = end_set[0]
                    lane_end = end_set[1]
                    start_pos = lane_start[0]
                    end_pos = lane_end[0]
                    stairs_position_1 = TurboMathUtil.Position.get_vector3(start_pos[0], start_pos[1], start_pos[2])
                    stairs_position_1.y = terrain.get_lot_level_height(stairs_position_1.x, stairs_position_1.z, lane_start[1].secondary_id, lane_start[1].primary_id)
                    stairs_level_1 = lane_start[1].secondary_id
                    stairs_position_2 = TurboMathUtil.Position.get_vector3(end_pos[0], end_pos[1], end_pos[2])
                    stairs_position_2.y = terrain.get_lot_level_height(stairs_position_2.x, stairs_position_2.z, lane_end[1].secondary_id, lane_end[1].primary_id)
                    stairs_level_2 = lane_end[1].secondary_id
                    yield (stairs_position_1, stairs_level_1, stairs_position_2, stairs_level_2)
            return ()

    class Mannequin:
        __qualname__ = 'TurboObjectUtil.Mannequin'

        @staticmethod
        def get_component(game_object):
            return game_object.mannequin_component

        @staticmethod
        def get_mannequin_component_sim_info(mannequin_component):
            return mannequin_component.sim_info_data

        @staticmethod
        def populate_mannequin_protocol_buffer(mannequin_component):
            persistence_service = services.get_persistence_service()
            current_zone_id = services.current_zone_id()
            sim_info_data_proto = persistence_service.add_mannequin_proto_buff()
            sim_info_data_proto.zone_id = services.current_zone_id()
            sim_info_data_proto.world_id = persistence_service.get_world_id_from_zone(current_zone_id)
            mannequin_component.populate_sim_info_data_proto(sim_info_data_proto)
            mannequin_component._resend_mannequin_data()

        @staticmethod
        def remove_mannequin_protocol_buffer(game_object):
            persistence_service = services.get_persistence_service()
            persistence_service.del_mannequin_proto_buff(game_object.id)

    class Puddle:
        __qualname__ = 'TurboObjectUtil.Puddle'

        class PuddleSize:
            __qualname__ = 'TurboObjectUtil.Puddle.PuddleSize'

            def _get_puddle_size(*args):
                try:
                    return PuddleSize(args[0])
                except:
                    return

            NoPuddle = _get_puddle_size(0)
            SmallPuddle = _get_puddle_size(1)
            MediumPuddle = _get_puddle_size(2)
            LargePuddle = _get_puddle_size(3)

        class PuddleLiquid:
            __qualname__ = 'TurboObjectUtil.Puddle.PuddleLiquid'

            def _get_puddle_liquid(*args):
                try:
                    return PuddleLiquid(args[0])
                except:
                    return

            WATER = _get_puddle_liquid(0)
            DARK_MATTER = _get_puddle_liquid(1)
            GREEN_GOO = _get_puddle_liquid(2)

        @staticmethod
        def create_puddle(game_object_target, puddle_liquid, puddle_size, max_distance=8):
            puddle = create_puddle(puddle_size, puddle_liquid)
            if puddle:
                puddle.place_puddle(game_object_target, max_distance=max_distance)

    class Special:
        __qualname__ = 'TurboObjectUtil.Special'

        @staticmethod
        def get_object_unique_id(game_object):
            ids_collection = list()
            if hasattr(game_object, 'guid64'):
                ids_collection.append(int(game_object.guid64))
            object_catalog_name = game_object.catalog_name
            if object_catalog_name is not None:
                ids_collection.append(int(object_catalog_name))
            ids_collection.sort()
            hash_value = 3430008
            for item in ids_collection:
                hash_value = eval(hex(1000003*hash_value & 4294967295)[:-1]) ^ item
            hash_value ^= len(ids_collection)
            return abs(hash_value)

