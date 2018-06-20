'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from enums.traits_enum import SimTrait
from turbolib.manager_util import TurboManagerUtil
from turbolib.math_util import TurboMathUtil
from turbolib.sim_util import TurboSimUtil
from turbolib.world_util import TurboWorldUtil
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.sex.animations.animations_handler import get_hidden_animations
from wickedwhims.sex.enums.sex_type import SexCategoryType
from wickedwhims.sex.sex_handlers.pre_sex_handler import PreSexInteractionHandler
from wickedwhims.sex.sex_location_handler import SexInteractionLocationType
from wickedwhims.sex.sex_operators.pre_sex_handlers_operator import start_sex_interaction_from_pre_sex_handler
from wickedwhims.utils_traits import has_sim_trait

def start_cuckold_solo_sex_interaction(sim_identifier, active_sex_handler):
    sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
    if has_sim_trait(sim, SimTrait.GENDEROPTIONS_TOILET_STANDING):
        animation_instance = _get_animation_with_stage_name(get_hidden_animations(), 'TURBODRIVER:SAM:Solo_Male_Masturbation_1')
    else:
        animation_instance = _get_animation_with_stage_name(get_hidden_animations(), 'TURBODRIVER:Amra72:Solo_Female_Masturbation_1')
    if animation_instance is None:
        return False
    location = TurboWorldUtil.Zone.find_good_location(TurboSimUtil.Location.get_location(sim))
    location_position = TurboMathUtil.Location.get_location_translation(location)
    line_of_sight = TurboMathUtil.LineOfSight.create(TurboSimUtil.Location.get_routing_surface(sim), location_position, 8.0)
    if not TurboMathUtil.LineOfSight.test(line_of_sight, TurboMathUtil.Location.get_location_translation(active_sex_handler.get_location())):
        return False
    location_level = TurboMathUtil.Location.get_location_level(location)
    location_angle = TurboMathUtil.Orientation.get_angle_between_vectors(location_position, TurboMathUtil.Location.get_location_translation(active_sex_handler.get_location()))
    pre_sex_handler = PreSexInteractionHandler(SexCategoryType.HANDJOB, TurboManagerUtil.Sim.get_sim_id(sim), SexInteractionLocationType.FLOOR_TYPE, -1, 0, TurboWorldUtil.Lot.get_active_lot_id(), location_position.x, location_position.y, location_position.z, location_level, location_angle, location_position.x, location_position.y, location_position.z, location_level, is_autonomy=True)
    pre_sex_handler.set_animation_instance(animation_instance)
    pre_sex_handler.pause_timer()
    pre_sex_handler.pause_animation()
    pre_sex_handler.link_active_sex_handler(active_sex_handler)
    pre_sex_handler.add_sim(TurboManagerUtil.Sim.get_sim_id(sim))
    sim_ev(sim).active_pre_sex_handler = pre_sex_handler
    return start_sex_interaction_from_pre_sex_handler(pre_sex_handler)


def _get_animation_with_stage_name(animations_list, stage_name):
    stage_name = stage_name.lower()
    for animation_instance in animations_list:
        while animation_instance.get_stage_name() == stage_name:
            return animation_instance

