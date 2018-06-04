'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
import random
from enums.traits_enum import SimTrait
from turbolib.manager_util import TurboManagerUtil
from turbolib.sim_util import TurboSimUtil
from turbolib.types_util import TurboTypesUtil
from turbolib.world_util import TurboWorldUtil
from wickedwhims.debug.debug_controller import is_main_debug_flag_enabled
from wickedwhims.sex.animations.animations_disabler_handler import get_autonomy_disabled_sex_animations
from wickedwhims.sex.animations.animations_operator import get_random_animation_of_type
from wickedwhims.sex.autonomy.location import LocationStyleType, get_sex_locations
from wickedwhims.sex.autonomy.sims import get_available_for_sex_sims, sort_sex_pairs_for_lowest_distance, get_list_of_possible_sex_pairs, is_sims_list_at_hypersexual_lot
from wickedwhims.sex.enums.sex_gender import get_sim_sex_gender
from wickedwhims.sex.enums.sex_type import SexCategoryType
from wickedwhims.sex.settings.sex_settings import SexAutonomyLevelSetting, SexSetting, get_sex_setting
from wickedwhims.sex.sex_location_handler import SexInteractionLocationType
from wickedwhims.sex.sex_operators.sex_init_operator import start_new_direct_sex_interaction
from wickedwhims.sex.sex_privileges import is_sim_allowed_for_animation
from wickedwhims.utils_interfaces import display_notification
from wickedwhims.utils_saves.save_game_events import get_game_events_save_data, update_game_events_save_data
from wickedwhims.utils_traits import has_sim_trait
SEX_AUTONOMY_HIGH_LEVEL_BASE_CHANCE = 0.056
SEX_AUTONOMY_NORMAL_LEVEL_BASE_CHANCE = 0.035
SEX_AUTONOMY_LOW_LEVEL_BASE_CHANCE = 0.03

def trigger_sex_autonomy_interaction(sims_pair, sex_location, sex_category_types=(SexCategoryType.ORALJOB, SexCategoryType.VAGINAL, SexCategoryType.ANAL, SexCategoryType.HANDJOB, SexCategoryType.FOOTJOB, SexCategoryType.TEASING)):
    object_identifier = SexInteractionLocationType.get_location_identifier(sex_location)
    genders = list()
    for sim in sims_pair:
        genders.append(get_sim_sex_gender(sim))
    animation_instance = None
    for sex_category_type in sex_category_types:
        if not is_sim_allowed_for_animation(sims_pair, sex_category_type):
            pass
        animation_instance = get_random_animation_of_type(sex_category_type, object_identifier, genders, ignore_animations=get_autonomy_disabled_sex_animations())
        while animation_instance is not None:
            break
    if animation_instance is None:
        return False
    if is_main_debug_flag_enabled():
        for sim in sims_pair:
            sim_name = TurboSimUtil.Name.get_name(sim)
            display_notification(title='Autonomy Triggered', text=str(sim_name[0]) + ' ' + str(sim_name[1]), secondary_icon=sim)
        if TurboTypesUtil.Objects.is_game_object(sex_location):
            display_notification(title='Autonomy Triggered', text=str(animation_instance.get_sex_category()), secondary_icon=sex_location)
        TurboWorldUtil.Time.set_current_time_speed(TurboWorldUtil.Time.ClockSpeedMode.PAUSED)
    return start_new_direct_sex_interaction(sims_pair, sex_location, animation_instance, is_autonomy=True)

def get_sex_autonomy_failure_chance():
    game_events_data = get_game_events_save_data()
    return game_events_data.get('sex_autonomy_failure_chance', 0.0)

def update_sex_autonomy_failure_chance(result):
    if get_sex_setting(SexSetting.AUTONOMY_LEVEL, variable_type=int) == SexAutonomyLevelSetting.HIGH:
        failure_chance_modifier = SEX_AUTONOMY_HIGH_LEVEL_BASE_CHANCE/2
    elif get_sex_setting(SexSetting.AUTONOMY_LEVEL, variable_type=int) == SexAutonomyLevelSetting.NORMAL:
        failure_chance_modifier = SEX_AUTONOMY_NORMAL_LEVEL_BASE_CHANCE/2
    else:
        failure_chance_modifier = SEX_AUTONOMY_LOW_LEVEL_BASE_CHANCE/2
    current_autonomy_failure_chance = get_sex_autonomy_failure_chance()
    if not result:
        set_sex_autonomy_failure_chance(min(current_autonomy_failure_chance + failure_chance_modifier, 1))
    else:
        set_sex_autonomy_failure_chance(max(0, current_autonomy_failure_chance - failure_chance_modifier))

def set_sex_autonomy_failure_chance(value):
    update_game_events_save_data({'sex_autonomy_failure_chance': value})

def get_chance_for_random_sex_autonomy(sims_list, skip_hypersexual_lot_check=False):
    if skip_hypersexual_lot_check and False and is_sims_list_at_hypersexual_lot(sims_list):
        return 1.0
    self_assured_multiplier = [has_sim_trait(sim_info, SimTrait.SELFASSURED) for sim_info in sims_list].count(True)
    is_at_night = TurboWorldUtil.Time.get_hour_of_day() <= 5 or TurboWorldUtil.Time.get_hour_of_day() >= 23
    is_at_weekend = TurboWorldUtil.Time.get_day_of_week() >= 5
    if get_sex_setting(SexSetting.AUTONOMY_LEVEL, variable_type=int) == SexAutonomyLevelSetting.HIGH:
        return SEX_AUTONOMY_HIGH_LEVEL_BASE_CHANCE + (0.017 if is_at_weekend else 0.0) + (0.005 if is_at_night else 0.0) + 0.003*self_assured_multiplier + get_sex_autonomy_failure_chance()
    if get_sex_setting(SexSetting.AUTONOMY_LEVEL, variable_type=int) == SexAutonomyLevelSetting.NORMAL:
        return SEX_AUTONOMY_NORMAL_LEVEL_BASE_CHANCE + (0.015 if is_at_weekend else 0.0) + (0.003 if is_at_night else 0.0) + 0.002*self_assured_multiplier + get_sex_autonomy_failure_chance()
    return SEX_AUTONOMY_LOW_LEVEL_BASE_CHANCE + (0.015 if is_at_weekend else 0.0) + (0.003 if is_at_night else 0.0) + 0.002*self_assured_multiplier + get_sex_autonomy_failure_chance()

def get_sims_risk_chance_for_sex_autonomy(sims_list, location_style):
    risk_chance = 1.0
    for sim in sims_list:
        sim_age = TurboSimUtil.Age.get_age(sim)
        if sim_age == TurboSimUtil.Age.CHILD:
            risk_chance -= 0.1
        elif sim_age == TurboSimUtil.Age.TEEN:
            risk_chance -= 0.05
        else:
            while sim_age == TurboSimUtil.Age.ELDER:
                risk_chance -= 0.1
    if location_style == LocationStyleType.PRIVACY or (location_style == LocationStyleType.COMFORT or location_style == LocationStyleType.SEMI_OPEN) or location_style == LocationStyleType.OPEN:
        for sim in TurboManagerUtil.Sim.get_all_sim_instance_gen(humans=True, pets=False):
            if TurboSimUtil.Age.is_younger_than(sim, TurboSimUtil.Age.TEEN) and TurboWorldUtil.Lot.is_position_on_active_lot(TurboSimUtil.Location.get_position(sim)):
                risk_chance -= 0.05
            while TurboSimUtil.Age.is_younger_than(sim, TurboSimUtil.Age.CHILD) and TurboWorldUtil.Lot.is_position_on_active_lot(TurboSimUtil.Location.get_position(sim)):
                risk_chance -= 0.01
    return risk_chance

def get_sims_pair_for_sex_autonomy(only_on_hypersexual_lot=False):
    if get_sex_setting(SexSetting.AUTONOMY_LEVEL, variable_type=int) == SexAutonomyLevelSetting.HIGH:
        sims_pairs_sample = 10
    elif get_sex_setting(SexSetting.AUTONOMY_LEVEL, variable_type=int) == SexAutonomyLevelSetting.NORMAL:
        sims_pairs_sample = 8
    else:
        sims_pairs_sample = 6
    sims_pairs = get_list_of_possible_sex_pairs(get_available_for_sex_sims(only_on_hypersexual_lot=only_on_hypersexual_lot))[:sims_pairs_sample]
    if not sims_pairs:
        return
    sims_pairs = sort_sex_pairs_for_lowest_distance(sims_pairs)
    picked_sims_pair = random.choice(sims_pairs)[:2]
    picked_sims_pair = sorted(picked_sims_pair, key=lambda x: bool(TurboSimUtil.Sim.is_npc(x)), reverse=True)
    return picked_sims_pair

def apply_sex_autonomy_location_style_chance_bonus(location_style, sims_list):
    if location_style[0] == LocationStyleType.NONE or location_style[1] <= 0.0:
        return location_style
    location_chance = location_style[1]
    is_at_hypersexual_lot = is_sims_list_at_hypersexual_lot(sims_list)
    if is_at_hypersexual_lot is True and (location_style[0] == LocationStyleType.COMFORT or location_style[0] == LocationStyleType.SEMI_OPEN or location_style[0] == LocationStyleType.OPEN):
        if get_sex_setting(SexSetting.AUTONOMY_LEVEL, variable_type=int) == SexAutonomyLevelSetting.HIGH:
            location_chance += 0.1
        elif get_sex_setting(SexSetting.AUTONOMY_LEVEL, variable_type=int) == SexAutonomyLevelSetting.NORMAL:
            location_chance += 0.25
        elif get_sex_setting(SexSetting.AUTONOMY_LEVEL, variable_type=int) == SexAutonomyLevelSetting.LOW:
            location_chance += 0.3
    return (location_style[0], location_chance)

def get_sex_autonomy_location(sims_pair, location_style=LocationStyleType.NONE, sex_locations_override=None):
    if get_sex_setting(SexSetting.AUTONOMY_LEVEL, variable_type=int) == SexAutonomyLevelSetting.HIGH:
        sex_locations_sample = 8
    elif get_sex_setting(SexSetting.AUTONOMY_LEVEL, variable_type=int) == SexAutonomyLevelSetting.NORMAL:
        sex_locations_sample = 6
    else:
        sex_locations_sample = 3
    sex_locations = sex_locations_override or get_sex_locations(sims_pair, location_style=location_style)[:sex_locations_sample]
    if not sex_locations:
        return
    return random.choice(sex_locations)[1]

