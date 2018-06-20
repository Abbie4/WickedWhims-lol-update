'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
import random
from enums.tags_enum import GameTag
from turbolib.events.buildbuy import register_buildbuy_state_change_event_method
from turbolib.events.core import register_zone_load_event_method
from turbolib.manager_util import TurboManagerUtil
from turbolib.math_util import TurboMathUtil
from turbolib.native.enum import TurboEnum
from turbolib.object_util import TurboObjectUtil
from turbolib.sim_util import TurboSimUtil
from turbolib.types_util import TurboTypesUtil
from turbolib.world_util import TurboWorldUtil
from wickedwhims.sex.animations.animations_handler import get_available_sex_animations
from wickedwhims.sex.sex_location_handler import SexInteractionLocationType
from wickedwhims.utils_objects import get_object_fixed_direction
LOT_DATA_CACHE = None

class RoomType(TurboEnum):
    __qualname__ = 'RoomType'
    OUTSIDE = 0
    BATHROOM = 1
    KITCHEN = 2
    BEDROOM = 3
    LIVINGROOM = 4
    OFFICEROOM = 5
    KIDSROOM = 6
    LOCKER_ROOM = 10
    GYM = 11


@register_zone_load_event_method(unique_id='WickedWhims', priority=50, late=True)
def _update_lot_structure_data_on_zone_load():
    _update_lot_structrue_data()


@register_buildbuy_state_change_event_method(unique_id='WickedWhims', priority=0, on_exit=True)
def _update_lot_structure_data_on_buildbuy_exit():
    _update_lot_structrue_data()


def _update_lot_structrue_data():
    global LOT_DATA_CACHE
    LOT_DATA_CACHE = LotStructureData()


def get_lot_structure_data():
    if LOT_DATA_CACHE is None:
        _update_lot_structrue_data()
    return LOT_DATA_CACHE


class LotStructureData:
    __qualname__ = 'LotStructureData'

    def __init__(self):
        self._size = self._get_lot_size()
        self._rooms = list()
        self._cache_rooms()

    def get_size(self):
        return self._size

    def _get_lot_size(self):
        lot_polygon = TurboWorldUtil.Lot.get_active_lot_corners()
        lot_size = 0
        for corner_num in range(len(lot_polygon)):
            lot_size += (lot_polygon[corner_num - 1].x + lot_polygon[corner_num].x)*(lot_polygon[corner_num - 1].z - lot_polygon[corner_num].z)
        lot_size /= 2
        return lot_size

    def get_rooms_structure_data_gen(self):
        for room_structure_data in self._rooms:
            if not room_structure_data.is_valid():
                pass
            yield room_structure_data

    def _cache_rooms(self):
        for room_id in TurboWorldUtil.Lot.get_all_rooms_ids():
            self._rooms.append(RoomStructureData(room_id))
        random.shuffle(self._rooms)

    def __repr__(self):
        debug = ''
        debug += 'Lot:\n'
        debug += '  size: ' + str(self._size) + '\n'
        debug += '  rooms: ' + str(len(self._rooms)) + '\n'
        return debug


class RoomStructureData:
    __qualname__ = 'RoomStructureData'

    def __init__(self, room_id):
        self._id = room_id
        self._size = self._get_room_size()
        self._location = self._get_room_location()
        self._safe_location = self._get_room_safe_location()
        self._objects = list()
        self._sims = list()
        self._types = list()
        self._cache_objects()

    def get_id(self):
        return self._id

    def get_size(self):
        return self._size

    def _get_room_size(self):
        rooms_polygons = TurboWorldUtil.Lot.get_polygons_of_all_rooms()
        if self._id not in rooms_polygons:
            return 0
        room_polygons = rooms_polygons[self._id]
        room_size = 0
        for polygon in room_polygons[0]:
            polygon_area = 0
            for corner_num in range(len(polygon)):
                polygon_area += (polygon[corner_num - 1].x + polygon[corner_num].x)*(polygon[corner_num - 1].z - polygon[corner_num].z)
            polygon_area /= 2
            room_size += polygon_area
        return room_size

    def get_location(self):
        return self._location

    def get_safe_location(self):
        return self._safe_location

    def _get_room_location(self):
        rooms_polygons = TurboWorldUtil.Lot.get_polygons_of_all_rooms()
        if self._id not in rooms_polygons:
            return
        room_data = rooms_polygons[self._id]
        room_level = room_data[1]
        room_position = TurboMathUtil.Position.get_vector3(0, 0, 0)
        vectors_count = 0
        for polygon in room_data[0]:
            for polygon_corner in polygon:
                room_position += polygon_corner
                vectors_count += 1
        room_position /= max(1, vectors_count)
        routing_surface = TurboMathUtil.Location.create_routing_identifier(room_level)
        room_position.y = TurboWorldUtil.Zone.get_routing_surface_height_at(room_position, routing_surface)
        return TurboMathUtil.Location.get_location(room_position, room_level, 0, surface_override=routing_surface)

    def _get_room_safe_location(self):
        if self._location is None:
            return
        safe_location = TurboWorldUtil.Zone.find_good_location(self._location)
        if TurboWorldUtil.Lot.get_room_id(safe_location) != self._id:
            return self._location
        return safe_location

    def is_accessible_by_sim(self, sim):
        return TurboSimUtil.Routing.has_location_connectivity(sim, self.get_safe_location())

    def get_objects_structure_data_gen(self, only_accessible=False):
        for object_structure_data in self._objects:
            if not object_structure_data.is_accessible() and only_accessible is True:
                pass
            if not object_structure_data.is_valid():
                pass
            yield object_structure_data

    def get_types(self):
        return self._types

    def _cache_objects(self):
        room_types_count = 0
        room_types = dict()
        for game_object in TurboObjectUtil.GameObject.get_all_gen():
            if TurboTypesUtil.Sims.is_sim(game_object):
                pass
            object_position = TurboObjectUtil.Position.get_position(game_object) + get_object_fixed_direction(game_object)
            room_id = TurboWorldUtil.Lot.get_room_id(TurboObjectUtil.Position.get_location(game_object), position=object_position)
            if room_id != self._id:
                pass
            while not room_id == TurboWorldUtil.Plex.get_active_zone_plex_id():
                if not TurboWorldUtil.Lot.is_position_on_active_lot(TurboObjectUtil.Position.get_position(game_object)):
                    pass
                object_room_types = get_object_association_to_room_type(game_object)
                if object_room_types:
                    for room_type in object_room_types:
                        room_types[room_type] = 1 if room_type not in room_types else room_types[room_type] + 1
                    room_types_count += len(object_room_types)
                self._objects.append(ObjectStructureData(game_object))
        random.shuffle(self._objects)
        for (room_type, types_amount) in room_types.items():
            self._types.append((room_type, types_amount/room_types_count))

    def is_valid(self):
        return self._location is not None

    def __repr__(self):
        room_position = TurboMathUtil.Location.get_location_translation(self.get_location())
        room_safe_position = TurboMathUtil.Location.get_location_translation(self.get_safe_location())
        debug = ''
        debug += 'Room:\n'
        debug += '  id: ' + str(self._id) + '\n'
        debug += '  size: ' + str(self._size) + '\n'
        debug += '  position: ' + str(room_position.x) + '/' + str(room_position.y) + '/' + str(room_position.z) + '\n'
        debug += '  safe_position: ' + str(room_safe_position.x) + '/' + str(room_safe_position.y) + '/' + str(room_safe_position.z) + '\n'
        debug += '  types: ' + str(self._types) + '\n'
        debug += '  objects: ' + str(len(self._objects)) + '\n'
        return debug


class ObjectStructureData:
    __qualname__ = 'ObjectStructureData'

    def __init__(self, game_object):
        self._game_object = game_object
        self._is_accessible = self._is_accessible(game_object)
        self._sex_identifier = SexInteractionLocationType.get_location_identifier(game_object)
        self._has_sex_animations = self._has_object_sex_animations()

    def get_game_object(self):
        return self._game_object

    def _is_accessible(self, game_object):
        routing_surface = TurboMathUtil.Location.get_location_routing_surface(TurboObjectUtil.Position.get_location(game_object))
        position = TurboObjectUtil.Position.get_position(game_object) + get_object_fixed_direction(game_object)
        return TurboWorldUtil.Routing.is_position_routable(routing_surface, position)

    def is_accessible(self):
        return self._is_accessible

    def get_sex_identifier(self):
        return self._sex_identifier

    def _has_object_sex_animations(self):
        for animation_instance in get_available_sex_animations():
            while animation_instance.can_be_used_with_object(self._sex_identifier):
                return True
        return False

    def has_sex_animations(self):
        return self._has_sex_animations

    def is_valid(self):
        return self._game_object is not None

    def __repr__(self):
        object_position = TurboObjectUtil.Position.get_position(self.get_game_object())
        debug = ''
        debug += 'Object:\n'
        debug += '  position: ' + str(object_position.x) + '/' + str(object_position.y) + '/' + str(object_position.z) + '\n'
        debug += '  sex_identifier: ' + str(self._sex_identifier) + '\n'
        return debug


def get_sims_in_room(room_id):
    sims_list = list()
    for sim in TurboManagerUtil.Sim.get_all_sim_instance_gen(humans=True, pets=False):
        current_room_id = TurboWorldUtil.Lot.get_room_id(TurboObjectUtil.Position.get_location(sim))
        if current_room_id != room_id:
            pass
        while not current_room_id == TurboWorldUtil.Plex.get_active_zone_plex_id():
            if not TurboWorldUtil.Lot.is_position_on_active_lot(TurboObjectUtil.Position.get_position(sim)):
                pass
            sims_list.append(sim)
    return sims_list


def get_object_association_to_room_type(game_object):
    if game_object is None:
        return ()
    object_room_types = set()
    object_tags = TurboObjectUtil.GameObject.get_game_tags(game_object)
    if GameTag.BUYCATPA_SHOWER in object_tags or (GameTag.BUYCATPA_TUB in object_tags or (GameTag.BUYCATPA_TOILET in object_tags and GameTag.FUNC_BLADDER in object_tags or GameTag.BUYCATPA_SINKFREESTANDING in object_tags)) or GameTag.BUYCATLD_BATHROOMACCENT in object_tags:
        object_room_types.add(RoomType.BATHROOM)
    if GameTag.FUNC_FRIDGE in object_tags or GameTag.FUNC_OVEN in object_tags or GameTag.FUNC_MICROWAVE in object_tags:
        object_room_types.add(RoomType.KITCHEN)
    if GameTag.FUNC_DOUBLEBED in object_tags or (GameTag.FUNC_SINGLEBED in object_tags or GameTag.BUYCATSS_DRESSER in object_tags) or GameTag.FUNC_BEDSIDETABLE in object_tags:
        object_room_types.add(RoomType.BEDROOM)
    if GameTag.BUYCATLD_FIREPLACE in object_tags or (GameTag.BUYCATEE_TV in object_tags or (GameTag.FUNC_RECLINER in object_tags or (GameTag.FUNC_COUCH in object_tags or (GameTag.BUYCATMAG_LIVINGROOM in object_tags or GameTag.BUYCATSS_LIVINGCHAIR in object_tags)))) or GameTag.BUYCATSS_COFFEETABLE in object_tags:
        object_room_types.add(RoomType.LIVINGROOM)
    if GameTag.BUYCATSS_DESK in object_tags and GameTag.BUYCATSS_DESKCHAIR in object_tags or GameTag.BUYCATEE_COMPUTER in object_tags and GameTag.FUNC_PROGRAMMING in object_tags:
        object_room_types.add(RoomType.OFFICEROOM)
    if GameTag.BUYCATEE_KIDFURNITURE in object_tags or (GameTag.BUYCATEE_KIDTOY in object_tags or (GameTag.BUYCATLD_KIDDECORATION in object_tags or GameTag.FUNC_KID in object_tags)) or GameTag.FUNC_BED_KID in object_tags:
        object_room_types.add(RoomType.KIDSROOM)
    if GameTag.VENUE_OBJECT_LOCKER in object_tags:
        object_room_types.add(RoomType.LOCKER_ROOM)
    if GameTag.VENUE_OBJECT_EXERCISE in object_tags:
        object_room_types.add(RoomType.GYM)
    return object_room_types

