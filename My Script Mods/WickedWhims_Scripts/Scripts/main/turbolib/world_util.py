import build_buy
import placement
import routing
import services
from clock import ClockSpeedMode
from protocolbuffers import Consts_pb2
from services import terrain_service
from turbolib.manager_util import TurboManagerUtil
from turbolib.math_util import TurboMathUtil
from turbolib.resource_util import TurboResourceUtil


class TurboWorldUtil:
    __qualname__ = 'TurboWorldUtil'

    class Time:
        __qualname__ = 'TurboWorldUtil.Time'

        class ClockSpeedMode:
            __qualname__ = 'TurboWorldUtil.Time.ClockSpeedMode'

            def _get_clock_speed_mode(*args):
                try:
                    return ClockSpeedMode(args[0])
                except:
                    return

            PAUSED = _get_clock_speed_mode(0)
            NORMAL = _get_clock_speed_mode(1)
            SPEED2 = _get_clock_speed_mode(2)
            SPEED3 = _get_clock_speed_mode(3)
            INTERACTION_STARTUP_SPEED = _get_clock_speed_mode(4)
            SUPER_SPEED3 = _get_clock_speed_mode(5)

        @staticmethod
        def get_current_time_speed():
            return services.game_clock_service().clock_speed

        @staticmethod
        def current_clock_speed_scale():
            return services.game_clock_service().current_clock_speed_scale()

        @staticmethod
        def set_current_time_speed(speed_mode):
            services.game_clock_service().set_clock_speed(speed_mode)

        @staticmethod
        def get_time_service():
            return services.time_service()

        @staticmethod
        def get_absolute_ticks():
            return TurboWorldUtil.Time.get_time_service().sim_now.absolute_ticks()

        @staticmethod
        def get_second_of_minute():
            return int(TurboWorldUtil.Time.get_time_service().sim_now.second())

        @staticmethod
        def get_absolute_seconds():
            return int(TurboWorldUtil.Time.get_time_service().sim_now.absolute_seconds())

        @staticmethod
        def get_minute_of_hour():
            return int(TurboWorldUtil.Time.get_time_service().sim_now.minute())

        @staticmethod
        def get_absolute_minutes():
            return int(TurboWorldUtil.Time.get_time_service().sim_now.absolute_minutes())

        @staticmethod
        def get_hour_of_day():
            return int(TurboWorldUtil.Time.get_time_service().sim_now.hour())

        @staticmethod
        def get_absolute_hours():
            return int(TurboWorldUtil.Time.get_time_service().sim_now.absolute_hours())

        @staticmethod
        def get_day_of_week():
            return int(TurboWorldUtil.Time.get_time_service().sim_now.day())

        @staticmethod
        def get_absolute_days():
            return int(TurboWorldUtil.Time.get_time_service().sim_now.absolute_days())

        @staticmethod
        def get_absolute_weeks():
            return int(TurboWorldUtil.Time.get_time_service().sim_now.week())

    class World:
        __qualname__ = 'TurboWorldUtil.World'

        @staticmethod
        def get_current_world_id():
            persistence_service = services.get_persistence_service()
            return persistence_service.get_world_id_from_zone(services.current_zone_id())

    class Zone:
        __qualname__ = 'TurboWorldUtil.Zone'

        @staticmethod
        def is_sim_renting_zone_id(sim_identifier, zone_id):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
            return sim_info.is_renting_zone(zone_id)

        @staticmethod
        def get_current_zone_id():
            return services.current_zone_id()

        @staticmethod
        def get_current_zone_traits():
            return services.get_zone_modifier_service().get_zone_modifiers(services.current_zone_id(), force_refresh=True)

        @staticmethod
        def get_terrain_service():
            return services.terrain_service

        @staticmethod
        def get_routing_surface_height_at(position, routing_surface):
            return TurboWorldUtil.Zone.get_terrain_service().terrain_object().get_routing_surface_height_at(position.x, position.z, routing_surface)

        @staticmethod
        def get_spawn_position():
            zone = services.current_zone()
            spawn_point = zone.get_spawn_point()
            if spawn_point is not None:
                (trans, _) = spawn_point.next_spawn_spot()
                return trans

        @staticmethod
        def find_good_location(location):
            search_flags = placement.FGLSearchFlagsDefault | placement.FGLSearchFlag.USE_SIM_FOOTPRINT | placement.FGLSearchFlag.SHOULD_TEST_ROUTING
            starting_location = placement.create_starting_location(location=location)
            fgl_context = placement.FindGoodLocationContext(starting_location, additional_avoid_sim_radius=routing.get_sim_extra_clearance_distance(), search_flags=search_flags)
            (trans, _) = placement.find_good_location(fgl_context)
            if trans is None:
                return location
            new_transform = TurboMathUtil.Position.get_transform(trans, TurboMathUtil.Orientation.get_quaternion_identity())
            return location.clone(transform=new_transform)

    class Plex:
        __qualname__ = 'TurboWorldUtil.Plex'

        @staticmethod
        def get_active_zone_plex_id():
            return services.get_plex_service().get_active_zone_plex_id() or 0

    class Venue:
        __qualname__ = 'TurboWorldUtil.Venue'

        @staticmethod
        def get_current_venue_type():
            return build_buy.get_current_venue(TurboWorldUtil.Zone.get_current_zone_id())

        @staticmethod
        def get_current_venue():
            return TurboResourceUtil.Services.get_instance(TurboResourceUtil.ResourceTypes.VENUE, TurboWorldUtil.Venue.get_current_venue_type())

        @staticmethod
        def is_residential(venue_instance):
            return venue_instance.residential

        @staticmethod
        def requires_visitation_rights(venue_instance):
            return venue_instance.requires_visitation_rights

        @staticmethod
        def allows_rolestate_routing(venue_instance):
            return venue_instance.allow_rolestate_routing_on_navmesh

    class Lot:
        __qualname__ = 'TurboWorldUtil.Lot'

        @staticmethod
        def get_active_lot():
            return services.active_lot()

        @staticmethod
        def get_active_lot_id():
            return services.active_lot_id() or -1

        @staticmethod
        def is_position_on_active_lot(position):
            return TurboWorldUtil.Lot.get_active_lot().is_position_on_lot(position)

        @staticmethod
        def is_location_outside(location):
            zone_id = services.current_zone_id()
            try:
                return build_buy.is_location_outside(zone_id, location.transform.translation, location.level)
            except RuntimeError:
                return False

        @staticmethod
        def is_sim_on_home_lot(sim_identifier):
            sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
            return sim.on_home_lot

        @staticmethod
        def get_room_id(location, position=None, level=None):
            zone_id = TurboWorldUtil.Zone.get_current_zone_id()
            return build_buy.get_block_id(zone_id, position if position is not None else TurboMathUtil.Location.get_location_translation(location), level if level is not None else TurboMathUtil.Location.get_location_level(location))

        @staticmethod
        def get_all_rooms_ids():
            return tuple(build_buy.get_all_block_polygons(services.current_zone_id(), TurboWorldUtil.Plex.get_active_zone_plex_id()).keys())

        @staticmethod
        def get_polygons_of_all_rooms():
            return build_buy.get_all_block_polygons(services.current_zone_id(), TurboWorldUtil.Plex.get_active_zone_plex_id())

        @staticmethod
        def get_active_lot_corners():
            active_lot = TurboWorldUtil.Lot.get_active_lot()
            return list(active_lot.corners)

        @staticmethod
        def get_spawn_position():
            zone = services.current_zone()
            spawn_point = zone.active_lot_arrival_spawn_point
            if spawn_point is not None:
                (trans, _) = spawn_point.next_spawn_spot()
                return trans

    class Household:
        __qualname__ = 'TurboWorldUtil.Household'

        @staticmethod
        def get_funds(household):
            return household.funds.money

        @staticmethod
        def add_funds(household, amount):
            household.funds.add(max(0, amount), Consts_pb2.TELEMETRY_MONEY_CHEAT)

        @staticmethod
        def subtract_funds(household, amount):
            return household.funds.try_remove(max(0, amount), Consts_pb2.TELEMETRY_MONEY_CHEAT)

        @staticmethod
        def get_sim_household_zone_id(sim_identifier):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
            return sim_info.household.home_zone_id

        @staticmethod
        def get_household_zone_id(household):
            return household.home_zone_id

        @staticmethod
        def get_current_zone_household():
            current_zone_id = TurboWorldUtil.Zone.get_current_zone_id()
            for household in services.household_manager().get_all():
                while household.home_zone_id == current_zone_id:
                    return household

        @staticmethod
        def get_household_sims(household):
            return tuple(household.sim_info_gen())

        @staticmethod
        def get_free_sims_slots(household):
            return household.free_slot_count

    class Routing:
        __qualname__ = 'TurboWorldUtil.Routing'

        @staticmethod
        def is_location_routable(location):
            return bool(routing.test_point_placement_in_navmesh(TurboMathUtil.Location.get_location_routing_surface(location), TurboMathUtil.Location.get_location_translation(location)))

        @staticmethod
        def is_position_routable(routing_surface, position):
            return bool(routing.test_point_placement_in_navmesh(routing_surface, position))

    class Location:
        __qualname__ = 'TurboWorldUtil.Location'

        @staticmethod
        def move_object_to(game_object, location=None, x_offset=0, y_offset=0, z_offset=0, orientation_offset=0):
            if location is None:
                location = game_object.location
            game_object.location = TurboMathUtil.Location.apply_offset(location, orientation_offset=orientation_offset, x_offset=x_offset, y_offset=y_offset, z_offset=z_offset)

