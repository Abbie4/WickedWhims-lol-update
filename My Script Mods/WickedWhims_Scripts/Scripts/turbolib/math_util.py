import math
import math as nmath
import services
import sims4.geometry
import sims4.math as smath
import terrain
from objects.components.line_of_sight_component import LineOfSight
from routing import SurfaceIdentifier, SurfaceType

class TurboMathUtil:
    __qualname__ = 'TurboMathUtil'

    class Terrain:
        __qualname__ = 'TurboMathUtil.Terrain'

        @staticmethod
        def get_level_height(x, z, routing_surface):
            return terrain.get_lot_level_height(x, z, routing_surface.secondary_id, routing_surface.primary_id)

    class Location:
        __qualname__ = 'TurboMathUtil.Location'

        @staticmethod
        def get_location(position, level, angle, surface_override=None):
            routing_surface = surface_override if surface_override is not None else TurboMathUtil.Location.create_routing_identifier(level)
            facing = TurboMathUtil.Orientation.convert_angle_to_orientation(angle)
            return smath.Location(TurboMathUtil.Position.get_transform(position, facing), routing_surface)

        @staticmethod
        def get_location_orientation(location):
            return location.transform.orientation

        @staticmethod
        def get_location_translation(location):
            return location.transform.translation

        @staticmethod
        def get_location_level(location):
            if location.routing_surface:
                return location.routing_surface.secondary_id
            return 0

        @staticmethod
        def get_location_routing_surface(location):
            if location.routing_surface:
                return location.routing_surface
            return TurboMathUtil.Location.create_routing_identifier(TurboMathUtil.Location.get_location_level(location))

        @staticmethod
        def create_routing_identifier(level, zone_id=-1, surface_type=SurfaceType.SURFACETYPE_WORLD):
            if zone_id == -1:
                zone_id = services.current_zone_id()
            return SurfaceIdentifier(zone_id, level, surface_type)

        @staticmethod
        def apply_offset(location, x_offset=0, y_offset=0, z_offset=0, orientation_offset=0):
            orientation = location.transform.orientation
            translation = location.transform.translation
            level = location.level
            routing_surface = TurboMathUtil.Location.create_routing_identifier(level)
            position = TurboMathUtil.Position.get_vector3(translation.x + x_offset, translation.y + y_offset, translation.z + z_offset)
            facing = smath.angle_to_yaw_quaternion(smath.yaw_quaternion_to_angle(orientation) + smath.deg_to_rad(orientation_offset))
            return smath.Location(TurboMathUtil.Position.get_transform(position, facing), routing_surface)

    class Position:
        __qualname__ = 'TurboMathUtil.Position'

        @staticmethod
        def get_vector3(x, y, z):
            return smath.Vector3(x, y, z)

        @staticmethod
        def get_transform(position, facing):
            return smath.Transform(position, facing)

        @staticmethod
        def get_distance(position_1, position_2, flat=False):
            return nmath.sqrt(nmath.pow(position_1.x - position_2.x, 2) + (nmath.pow(position_1.y - position_2.y, 2) if flat is False else 0) + nmath.pow(position_1.z - position_2.z, 2))

    class Orientation:
        __qualname__ = 'TurboMathUtil.Orientation'

        @staticmethod
        def get_quaternion(x, y, z, w):
            return smath.Quaternion(x, y, z, w)

        @staticmethod
        def get_quaternion_identity():
            return smath.Quaternion.IDENTITY()

        @staticmethod
        def convert_angle_to_orientation(angle):
            return smath.angle_to_yaw_quaternion(angle)

        @staticmethod
        def convert_orientation_to_angle(orientation):
            return smath.yaw_quaternion_to_angle(orientation)

        @staticmethod
        def get_angle_between_vectors(position_1, position_2):
            return math.atan2(position_2.x - position_1.x, position_2.z - position_1.z)

    class LineOfSight:
        __qualname__ = 'TurboMathUtil.LineOfSight'

        @staticmethod
        def create(routing_surface, init_position, radius, map_divisions=30, simplification_ratio=0.35, boundary_epsilon=0.01):
            los = LineOfSight(radius, map_divisions, simplification_ratio, boundary_epsilon)
            los.generate(init_position, routing_surface, build_convex=True)
            return los

        @staticmethod
        def test(line_of_sight_object, target_position, routing_surface=None, level_height_difference=2.0, skip_level_check=False):
            if skip_level_check is False:
                if routing_surface is not None:
                    if routing_surface.secondary_id != line_of_sight_object._routing_surface.secondary_id:
                        return False
                        if abs(target_position.y - line_of_sight_object._position.y) >= level_height_difference:
                            return False
                elif abs(target_position.y - line_of_sight_object._position.y) >= level_height_difference:
                    return False
            if line_of_sight_object.constraint_convex.geometry is not None:
                return line_of_sight_object.constraint_convex.geometry.contains_point(target_position)
            return False

    class Geometry:
        __qualname__ = 'TurboMathUtil.Geometry'

        @staticmethod
        def is_intersecting_polygons(polygon_corners_1, polygon_corners_2):
            polygon_1 = sims4.geometry.CompoundPolygon(sims4.geometry.Polygon(polygon_corners_1))
            polygon_2 = sims4.geometry.CompoundPolygon(sims4.geometry.Polygon(polygon_corners_2))
            intersection = polygon_2.intersect(polygon_1)
            return len(intersection) >= 1

