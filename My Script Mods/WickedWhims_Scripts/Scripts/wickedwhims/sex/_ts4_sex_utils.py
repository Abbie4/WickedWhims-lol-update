'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''import routing.connectivityfrom interactions.privacy import Privacyfrom server.pick_info import PickTypefrom enums.interactions_enum import SimInteractionfrom turbolib.interaction_util import TurboInteractionUtilfrom turbolib.manager_util import TurboManagerUtilfrom turbolib.math_util import TurboMathUtilfrom turbolib.object_util import TurboObjectUtilfrom turbolib.resource_util import TurboResourceUtilfrom turbolib.types_util import TurboTypesUtilfrom turbolib.world_util import TurboWorldUtil
def is_safe_floor_object_position(location_object, interaction_context):
    if not TurboTypesUtil.Objects.is_terrain(location_object):
        return False
    if interaction_context is not None and interaction_context.pick is not None and isinstance(interaction_context.pick.pick_type, PickType):
        if interaction_context.pick.pick_type != PickType.PICK_TERRAIN and interaction_context.pick.pick_type != PickType.PICK_FLOOR:
            return False
        position = interaction_context.pick.location
        surface = interaction_context.pick.routing_surface
    else:
        position = location_object.position
        surface = location_object.routing_surface
    if surface is None or position is None:
        return False
    if not routing.test_point_placement_in_navmesh(surface, position):
        return False
    return True

def get_floor_object_position(location_object, interaction_context):
    if interaction_context.pick is None:
        return location_object.position
    position = interaction_context.pick.location
    surface = interaction_context.pick.routing_surface
    position.y = TurboWorldUtil.Zone.get_routing_surface_height_at(position, surface)
    return position

def get_floor_object_level(location_object, interaction_context):
    if interaction_context.pick is None:
        return TurboMathUtil.Location.get_location_level(TurboObjectUtil.Position.get_location(location_object))
    return interaction_context.pick.routing_surface.secondary_id

def route_sim_away_from_interaction(source_interaction, target_sim):
    embarrassed_affordance = TurboResourceUtil.Services.get_instance(TurboResourceUtil.ResourceTypes.INTERACTION, SimInteraction.STAND_PASSIVE)
    privacy = Privacy(source_interaction, (), (), 8, 30, 0.35, 0.01, 0.1, False, None, None, embarrassed_affordance, None)
    for sim in TurboManagerUtil.Sim.get_all_sim_instance_gen(humans=True, pets=False):
        privacy.add_exempt_sim(sim)
    privacy.build_privacy(target=TurboInteractionUtil.get_interaction_target(source_interaction))
    privacy.remove_privacy()
    result = privacy._route_sim_away(target_sim)
    return bool(result)

def apply_pressure_to_interactions_queue(sim):
    if sim.queue is not None:
        sim.queue._apply_next_pressure()
