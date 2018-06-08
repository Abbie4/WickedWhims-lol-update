'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from turbolib.math_util import TurboMathUtil
from turbolib.object_util import TurboObjectUtil
from wickedwhims.utils_objects import get_object_fixed_direction

class SexInteractionHandler:
    __qualname__ = 'SexInteractionHandler'

    def __init__(self, creator_sim_id, object_identifier, game_object_id, object_height, lot_id, location_x, location_y, location_z, location_level, location_angle, route_x, route_y, route_z, route_level, is_manual=False, is_autonomy=False):
        self._animation_instance = None
        self._object_identifier = object_identifier
        self._game_object_id = game_object_id
        self._object_height = object_height
        self._creator_sim_id = creator_sim_id
        self._lot_id = lot_id
        self.location_x = location_x
        self.location_y = location_y
        self.location_z = location_z
        self.location_level = location_level
        self.location_angle = location_angle
        self._location_cache = TurboMathUtil.Location.get_location(TurboMathUtil.Position.get_vector3(self.location_x, self.location_y, self.location_z), self.location_level, self.location_angle)
        self.route_x = route_x
        self.route_y = route_y
        self.route_z = route_z
        self.route_level = route_level
        self._route_cache = TurboMathUtil.Position.get_vector3(self.route_x, self.route_y, self.route_z)
        self._is_autonomy = is_autonomy
        self._is_manual = is_manual

    def get_identifier(self):
        raise NotImplementedError

    def get_animation_instance(self):
        return self._animation_instance

    def set_animation_instance(self, animation_instance):
        self._animation_instance = animation_instance

    def get_object_identifier(self):
        return self._object_identifier

    def set_object_identifier(self, object_identifier):
        self._object_identifier = object_identifier

    def get_game_object_id(self):
        return self._game_object_id

    def set_game_object_id(self, game_object_id):
        self._game_object_id = game_object_id

    def get_object_height(self):
        return self._object_height

    def set_object_height(self, object_height):
        self._object_height = object_height

    def get_creator_sim_id(self):
        return int(self._creator_sim_id)

    def get_lot_id(self):
        return self._lot_id

    def get_location(self):
        if self._location_cache is None:
            self._location_cache = TurboMathUtil.Location.get_location(TurboMathUtil.Position.get_vector3(self.location_x, self.location_y, self.location_z), self.location_level, self.location_angle)
        return self._location_cache

    def set_location(self, x, y, z, level, angle):
        self.location_x = x
        self.location_y = y
        self.location_z = z
        self.location_level = level
        self.location_angle = angle
        self._location_cache = None

    def get_los_position(self):
        if self._game_object_id == -1:
            return TurboMathUtil.Position.get_vector3(self.location_x, self.location_y, self.location_z)
        game_object = TurboObjectUtil.GameObject.get_object_with_id(self._game_object_id)
        if game_object is None:
            return TurboMathUtil.Position.get_vector3(self.location_x, self.location_y, self.location_z)
        gameobject_position = game_object.position + get_object_fixed_direction(game_object)
        return TurboMathUtil.Position.get_vector3(gameobject_position.x, gameobject_position.y, gameobject_position.z)

    def get_route_position(self):
        if self._route_cache is None:
            self._route_cache = TurboMathUtil.Position.get_vector3(self.route_x, self.route_y, self.route_z)
        return self._route_cache

    def get_route_level(self):
        return self.route_level

    def set_route_position(self, x, y, z, level):
        self.route_x = x
        self.route_y = y
        self.route_z = z
        self.route_level = level
        self._route_cache = None

    def is_autonomy_sex(self):
        return self._is_autonomy

    def is_manual_sex(self):
        return self._is_manual

    def get_save_dict(self):
        save_data = dict()
        save_data['animation_identifier'] = self._animation_instance.get_identifier()
        save_data['object_identifier_name'] = self._object_identifier[0]
        save_data['object_identifier_guid'] = self._object_identifier[1]
        save_data['gameobject_id'] = self._game_object_id
        save_data['object_height'] = self._object_height
        save_data['creator_sim'] = self._creator_sim_id
        save_data['lot_id'] = self._lot_id
        save_data['location_x'] = self.location_x
        save_data['location_y'] = self.location_y
        save_data['location_z'] = self.location_z
        save_data['location_level'] = self.location_level
        save_data['location_angle'] = self.location_angle
        save_data['route_x'] = self.route_x
        save_data['route_y'] = self.route_y
        save_data['route_z'] = self.route_z
        save_data['route_level'] = self.route_level
        save_data['is_autonomy'] = self._is_autonomy
        save_data['is_manual'] = self._is_manual
        return save_data

    def get_string_data(self):
        return 'Creator Sim ID: ' + str(self.get_creator_sim_id()) + '\
 Game Object ID: ' + str(self.get_game_object_id()) + '\
 Object Identifier Name: ' + str(self._object_identifier[0]) + '\
 Object Identifier GUID: ' + str(self._object_identifier[1]) + '\
 Object Height: ' + str(self.get_object_height()) + '\
 Lot ID: ' + str(self._lot_id) + '\
 Location X: ' + str(self.location_x) + '\
 Location Y: ' + str(self.location_y) + '\
 Location Z: ' + str(self.location_z) + '\
 Location Level: ' + str(self.location_level) + '\
 Location Angle: ' + str(self.location_angle) + '\
 Route X: ' + str(self.route_x) + '\
 Route Y: ' + str(self.route_y) + '\
 Route Z: ' + str(self.route_z) + '\
 Route Level: ' + str(self.route_level) + '\
 Animation_identifier: ' + str('' if self.get_animation_instance() is None else self.get_animation_instance().get_identifier())

