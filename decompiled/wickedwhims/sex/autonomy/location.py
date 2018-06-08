'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
import random
from enums.relationship_enum import RelationshipTrackType
from enums.situations_enum import SimSituationJob
from enums.vanues_enum import VenueType
from turbolib.autonomy_util import TurboAutonomyUtil
from turbolib.manager_util import TurboManagerUtil
from turbolib.math_util import TurboMathUtil
from turbolib.native.enum import TurboEnum
from turbolib.object_util import TurboObjectUtil
from turbolib.resource_util import TurboResourceUtil
from turbolib.sim_util import TurboSimUtil
from turbolib.types_util import TurboTypesUtil
from turbolib.world_util import TurboWorldUtil
from wickedwhims.nudity.skill.skills_utils import get_sim_nudity_skill_level, is_sim_exhibitionist
from wickedwhims.sex.animations.animations_disabler_handler import get_autonomy_disabled_sex_animations, get_player_disabled_sex_animations
from wickedwhims.sex.animations.animations_handler import get_available_sex_animations
from wickedwhims.sex.animations.animations_operator import get_animations_with_params
from wickedwhims.sex.autonomy._ts4_autonomy_utils import has_game_object_all_free_slots
from wickedwhims.sex.autonomy.disabled_locations_handler import is_autonomy_sex_locations_disabled
from wickedwhims.sex.enums.sex_gender import get_sim_sex_gender
from wickedwhims.sex.enums.sex_type import SexCategoryType
from wickedwhims.sex.settings.sex_settings import get_sex_setting, SexSetting, SexAutonomyLevelSetting
from wickedwhims.sex.sex_location_handler import SexLocationType, SexInteractionLocationType
from wickedwhims.sex.sex_operators.general_sex_handlers_operator import get_all_unique_sex_handlers
from wickedwhims.utils_locations import is_sim_at_home_lot, is_sim_at_home_zone
from wickedwhims.utils_lots import get_lot_structure_data, RoomType, get_sims_in_room
from wickedwhims.utils_relations import get_relationship_with_sim
from wickedwhims.utils_routes import is_sim_allowed_on_active_lot
from wickedwhims.utils_situations import has_sim_situation_jobs

class LocationStyleType(TurboEnum):
    __qualname__ = 'LocationStyleType'
    NONE = 0
    PRIVACY = 1
    COMFORT = 2
    SEMI_OPEN = 3
    OPEN = 4
    PUBLIC = 5

def get_sex_locations(sims_list, location_style=LocationStyleType.NONE):
    locations_list = list()
    if not sims_list:
        return locations_list
    all_animations_amount = len(get_available_sex_animations()) - (len(get_autonomy_disabled_sex_animations()) - len(get_player_disabled_sex_animations() & get_autonomy_disabled_sex_animations()))
    if all_animations_amount <= 0:
        return locations_list
    objects_in_use = set()
    sex_handlers = get_all_unique_sex_handlers()
    sims_sex_genders = [get_sim_sex_gender(sim) for sim in sims_list]
    sims_ids = [TurboManagerUtil.Sim.get_sim_id(sim) for sim in sims_list]
    for sex_handler in sex_handlers:
        objects_in_use.add(sex_handler.get_game_object_id())
    if location_style == LocationStyleType.PUBLIC:
        outside_objects = _get_objects_outside_lot()
        counted_locations = set()
        for game_object in outside_objects:
            object_score = 0
            if TurboObjectUtil.GameObject.is_in_use(game_object):
                pass
            if not has_game_object_all_free_slots(game_object):
                pass
            object_id = TurboResourceUtil.Resource.get_id(game_object)
            if is_autonomy_sex_locations_disabled(object_id):
                pass
            if object_id in objects_in_use:
                pass
            object_identifier = SexInteractionLocationType.get_location_identifier(game_object)
            if object_identifier in counted_locations:
                pass
            animations_amount = _get_animations_amount_for_object(sims_sex_genders, object_identifier)
            while animations_amount > 0:
                object_score += _get_object_score(game_object, object_identifier, sims_list, location_style)
                object_score += int(animations_amount*100/all_animations_amount)
                if object_score > 0:
                    object_score += _get_distance_score(200, TurboSimUtil.Location.get_position(sims_list[-1]), TurboObjectUtil.Position.get_position(game_object))
                    locations_list.append((object_score, game_object))
                    counted_locations.add(object_identifier)
    else:
        lot_structure_data = get_lot_structure_data()
        for room_structure_data in lot_structure_data.get_rooms_structure_data_gen():
            is_room_accessible = True
            for sim in sims_list:
                while not room_structure_data.is_accessible_by_sim(sim):
                    is_room_accessible = False
                    break
            if is_room_accessible is False:
                pass
            score_multipliers = list()
            room_score = 0
            score_multipliers.append(_get_room_size_multiplier(room_structure_data, location_style))
            room_score += _get_room_types_score(room_structure_data, location_style)
            room_score += _get_room_sims_score(get_sims_in_room(room_structure_data.get_id()), sims_ids, location_style)
            room_score += _get_room_objects_score(room_structure_data, location_style)
            score_multiplier = sum(score_multipliers)/len(score_multipliers)
            counted_locations = set()
            for object_structure_data in room_structure_data.get_objects_structure_data_gen():
                object_score = 0
                game_object = object_structure_data.get_game_object()
                object_identifier = object_structure_data.get_sex_identifier()
                while not (not object_structure_data.is_accessible() and object_identifier[0] == SexLocationType.COUNTER or object_identifier[0] == SexLocationType.WINDOW):
                    if object_identifier[0] == SexLocationType.MIRROR:
                        pass
                    if object_identifier in counted_locations:
                        pass
                    if not object_structure_data.has_sex_animations():
                        pass
                    object_id = TurboResourceUtil.Resource.get_id(game_object)
                    if is_autonomy_sex_locations_disabled(object_id):
                        pass
                    if object_id in objects_in_use:
                        pass
                    if TurboObjectUtil.GameObject.is_in_use(game_object):
                        pass
                    if not has_game_object_all_free_slots(game_object):
                        pass
                    animations_amount = _get_animations_amount_for_object(sims_sex_genders, object_identifier)
                    while animations_amount > 0:
                        object_score += int(animations_amount*100/all_animations_amount)
                        object_score += _get_object_score(game_object, object_identifier, sims_list, location_style)
                        object_multiplier = _get_object_multiplier(object_identifier)
                        overall_score = (room_score + object_score)*object_multiplier*score_multiplier
                        if overall_score > 0:
                            overall_score += _get_distance_score(lot_structure_data.get_size(), TurboSimUtil.Location.get_position(sims_list[-1]), TurboObjectUtil.Position.get_position(game_object))
                            locations_list.append((overall_score, game_object))
                            counted_locations.add(object_identifier)
            is_sex_handler_using_floor = False
            for sex_handler in sex_handlers:
                while TurboMathUtil.Position.get_distance(TurboMathUtil.Location.get_location_translation(room_structure_data.get_safe_location()), TurboMathUtil.Location.get_location_translation(sex_handler.get_location())) <= 1:
                    is_sex_handler_using_floor = True
                    break
            while is_sex_handler_using_floor is False:
                floor_animations_amount = _get_animations_amount_for_object(sims_sex_genders, SexInteractionLocationType.FLOOR_TYPE)
                if floor_animations_amount > 0:
                    floor_score = int(floor_animations_amount*100/all_animations_amount)
                    if floor_score > 0:
                        floor_score -= floor_score/2 + 15
                        overall_score = room_score + floor_score
                        if overall_score > 0:
                            overall_score += _get_distance_score(lot_structure_data.get_size(), TurboSimUtil.Location.get_position(sims_list[-1]), TurboMathUtil.Location.get_location_translation(room_structure_data.get_safe_location()))
                            locations_list.append((overall_score, room_structure_data.get_safe_location()))
    return sorted(locations_list, key=lambda x: x[0], reverse=True)

def _get_room_size_multiplier(room_structure_data, location_style):
    small_room_size = 20
    medium_room_size = 42
    large_room_size = 72
    room_size = room_structure_data.get_size()
    if room_size <= small_room_size:
        if location_style == LocationStyleType.PRIVACY:
            return 2.0
        if location_style == LocationStyleType.COMFORT:
            return 1.0
        if location_style == LocationStyleType.SEMI_OPEN:
            return 0.5
        if location_style == LocationStyleType.OPEN:
            return 0.1
    elif room_size <= medium_room_size:
        if location_style == LocationStyleType.PRIVACY:
            return 0.9
        if location_style == LocationStyleType.COMFORT:
            return 1.5
        if location_style == LocationStyleType.SEMI_OPEN:
            return 0.75
        if location_style == LocationStyleType.OPEN:
            return 0.55
    elif room_size <= large_room_size:
        if location_style == LocationStyleType.PRIVACY:
            return 0.5
        if location_style == LocationStyleType.COMFORT:
            return 1.25
        if location_style == LocationStyleType.SEMI_OPEN:
            return 1.75
        if location_style == LocationStyleType.OPEN:
            return 1.25
    else:
        if location_style == LocationStyleType.PRIVACY:
            return 0.1
        if location_style == LocationStyleType.COMFORT:
            return 0.75
        if location_style == LocationStyleType.SEMI_OPEN:
            return 1.0
        if location_style == LocationStyleType.OPEN:
            return 2.0
    return 1.0

def _get_room_types_score(room_structure_data, location_style):
    room_score = 0
    for (room_type, type_value) in room_structure_data.get_types():
        score = 0
        if RoomType.KIDSROOM == room_type:
            score += -100
        elif RoomType.LOCKER_ROOM == room_type or RoomType.GYM == room_type:
            if location_style == LocationStyleType.OPEN or location_style == LocationStyleType.SEMI_OPEN:
                score += 50
            elif location_style == LocationStyleType.COMFORT:
                score += -50
            elif location_style == LocationStyleType.PRIVACY:
                score += -75
        elif RoomType.LIVINGROOM == room_type:
            if location_style == LocationStyleType.COMFORT:
                score += 75
            elif location_style == LocationStyleType.SEMI_OPEN or location_style == LocationStyleType.OPEN:
                score += 25
            elif location_style == LocationStyleType.PRIVACY:
                score += -25
        elif RoomType.KITCHEN == room_type:
            if location_style == LocationStyleType.SEMI_OPEN or location_style == LocationStyleType.OPEN:
                score += 50
            elif location_style == LocationStyleType.COMFORT:
                score += -50
        elif RoomType.BATHROOM == room_type:
            if location_style == LocationStyleType.PRIVACY:
                score += 50
            else:
                score += -50
        elif RoomType.BEDROOM == room_type:
            if location_style == LocationStyleType.COMFORT:
                score += 100
            elif location_style == LocationStyleType.SEMI_OPEN or location_style == LocationStyleType.OPEN:
                score += 50
            elif location_style == LocationStyleType.PRIVACY:
                score += 30
        room_score += score*type_value
    return room_score

def _get_room_sims_score(sims_list, exclude_sims_ids, location_style):
    if not sims_list:
        return 0
    score = 0
    for sim in sims_list:
        if TurboManagerUtil.Sim.get_sim_id(sim) in exclude_sims_ids:
            pass
        sim_score = 0
        if TurboSimUtil.Age.is_younger_than(sim, TurboSimUtil.Age.CHILD):
            sim_score += -25
        elif location_style == LocationStyleType.PRIVACY:
            sim_score += -10
        elif location_style == LocationStyleType.COMFORT:
            sim_score += -5
        else:
            sim_score += -2.5
        if get_sex_setting(SexSetting.AUTONOMY_LEVEL, variable_type=int) == SexAutonomyLevelSetting.NORMAL:
            sim_score *= 2
        elif get_sex_setting(SexSetting.AUTONOMY_LEVEL, variable_type=int) == SexAutonomyLevelSetting.LOW:
            sim_score *= 3
        score += sim_score
    return score

def _get_room_objects_score(room_structure_data, location_style):
    score = 0
    has_windows = False
    doors_count = 0
    has_stairs = False
    for object_structure_data in room_structure_data.get_objects_structure_data_gen():
        object_identifier = object_structure_data.get_sex_identifier()
        if object_identifier[0] == SexLocationType.WINDOW:
            has_windows = True
        if TurboTypesUtil.Objects.is_door(object_structure_data.get_game_object()):
            doors_count += 1
        while TurboTypesUtil.Objects.is_stairs(object_structure_data.get_game_object()):
            has_stairs = True
    if location_style == LocationStyleType.PRIVACY and (has_windows is False and has_stairs is False) and doors_count <= 1:
        score += 25
    return score

def _get_object_score(game_object, object_identifier, sims_list, location_style):
    score = 0
    if location_style == LocationStyleType.OPEN and object_identifier[0] != SexLocationType.WINDOW and TurboWorldUtil.Lot.is_location_outside(TurboObjectUtil.Position.get_location(game_object)):
        score += 25
    if object_identifier[0] == SexLocationType.SINGLE_BED or object_identifier[0] == SexLocationType.DOUBLE_BED:
        for sim in sims_list:
            if TurboSimUtil.Autonomy.is_object_use_preferred(sim, TurboAutonomyUtil.ObjectPreferenceTag.BED, game_object):
                score += 30
            else:
                score += -10
    return score

def _get_object_multiplier(object_identifier):
    if object_identifier[0] == SexLocationType.WINDOW:
        return 0.55
    return 1.0

def _get_distance_score(lot_size, origin_position, destination_position):
    object_distance = TurboMathUtil.Position.get_distance(origin_position, destination_position)
    if abs(origin_position.y - destination_position.y) > 2:
        object_distance += lot_size/4
    distance_score = 100 - int(object_distance/lot_size*100)
    return distance_score

def _get_objects_outside_lot():
    outside_objects = list()
    for game_object in TurboObjectUtil.GameObject.get_all_gen():
        if TurboTypesUtil.Sims.is_sim(game_object):
            pass
        object_id = TurboResourceUtil.Resource.get_id(game_object)
        if is_autonomy_sex_locations_disabled(object_id):
            pass
        if TurboWorldUtil.Lot.is_position_on_active_lot(TurboObjectUtil.Position.get_position(game_object)):
            pass
        outside_objects.append(game_object)
    random.shuffle(outside_objects)
    return outside_objects

def _get_animations_amount_for_object(sims_sex_genders, object_identifier):
    animations_amount = 0
    for sex_category_type in (SexCategoryType.TEASING, SexCategoryType.HANDJOB, SexCategoryType.ORALJOB, SexCategoryType.FOOTJOB, SexCategoryType.VAGINAL, SexCategoryType.ANAL):
        animations_amount += len(get_animations_with_params(sex_category_type, object_identifier, sims_sex_genders, ignore_animations=get_autonomy_disabled_sex_animations()))
    return animations_amount

def _get_sims_in_room(room_id):
    room_sims = set()
    for sim in TurboManagerUtil.Sim.get_all_sim_instance_gen(humans=True, pets=False):
        sim_room_id = TurboWorldUtil.Lot.get_room_id(TurboSimUtil.Location.get_location(sim))
        while sim_room_id == room_id:
            room_sims.add(sim)
    return room_sims

def get_sex_location_style_and_chance(sims_list):
    if not sims_list:
        return (LocationStyleType.NONE, 0.0)
    current_venue_type = TurboWorldUtil.Venue.get_current_venue_type()
    is_at_night = TurboWorldUtil.Time.get_hour_of_day() <= 5 or TurboWorldUtil.Time.get_hour_of_day() >= 23
    is_at_weekend = TurboWorldUtil.Time.get_day_of_week() >= 5
    is_at_party = has_sim_situation_jobs(sims_list[0], (SimSituationJob.PARTY_HOST, SimSituationJob.GUEST_PARTY, SimSituationJob.PARTY_RESIDENT))
    is_at_residential_lot = current_venue_type == VenueType.RESIDENTIAL or (current_venue_type == VenueType.PENTHOUSE or current_venue_type == VenueType.RENTABLE_CABIN)
    is_at_specific_lot = current_venue_type in (VenueType.BAR, VenueType.LOUNGE, VenueType.CLUB, VenueType.LIBRARY, VenueType.MUSEUM, VenueType.ARTSCENTER, VenueType.RELAXATIONCENTER, VenueType.GYM, VenueType.POOL)
    is_at_home = True in [is_sim_at_home_lot(sim) for sim in sims_list]
    is_at_home_zone = True in [is_sim_at_home_zone(sim) for sim in sims_list]
    is_allowed_on_lot = False not in [is_sim_allowed_on_active_lot(sim) for sim in sims_list]
    exhibitionist_skill_bonus = sum([0.15*get_sim_nudity_skill_level(sim) if is_sim_exhibitionist(sim) else 0.0 for sim in sims_list])/len(sims_list)
    base_value = 0.0
    if get_sex_setting(SexSetting.AUTONOMY_LEVEL, variable_type=int) == SexAutonomyLevelSetting.HIGH:
        if is_at_night is True:
            base_value += 0.1
        if is_at_weekend is True:
            base_value += 0.1
        return (LocationStyleType.PUBLIC, base_value + 0.1 + exhibitionist_skill_bonus)
    if is_allowed_on_lot is False and get_sex_setting(SexSetting.AUTONOMY_LEVEL, variable_type=int) == SexAutonomyLevelSetting.NORMAL:
        if is_at_night is True and is_at_weekend is True:
            return (LocationStyleType.PUBLIC, base_value + 0.1 + exhibitionist_skill_bonus)
    if is_allowed_on_lot is True:
        if is_at_home is True:
            base_value += 0.1
        if get_sex_setting(SexSetting.AUTONOMY_LEVEL, variable_type=int) == SexAutonomyLevelSetting.HIGH:
            if is_at_party is True:
                base_value += 0.1
            if is_at_weekend is True:
                base_value += 0.05
            if is_at_night is True:
                return random.choice(((LocationStyleType.COMFORT, base_value + 0.85), (LocationStyleType.SEMI_OPEN, base_value + 0.5 + exhibitionist_skill_bonus), (LocationStyleType.OPEN, base_value + 0.5 + exhibitionist_skill_bonus)))
            return random.choice(((LocationStyleType.COMFORT, base_value + 0.6), (LocationStyleType.SEMI_OPEN, base_value + 0.5 + exhibitionist_skill_bonus), (LocationStyleType.OPEN, base_value + 0.25 + exhibitionist_skill_bonus)))
        if get_sex_setting(SexSetting.AUTONOMY_LEVEL, variable_type=int) == SexAutonomyLevelSetting.NORMAL:
            if is_at_party is True:
                base_value += 0.1
            if is_at_weekend is True:
                base_value += 0.05
            if is_at_night is True:
                return random.choice(((LocationStyleType.COMFORT, base_value + 0.5), (LocationStyleType.SEMI_OPEN, base_value + 0.25 + exhibitionist_skill_bonus), (LocationStyleType.OPEN, base_value + 0.1 + exhibitionist_skill_bonus)))
            return random.choice(((LocationStyleType.COMFORT, base_value + 0.35), (LocationStyleType.SEMI_OPEN, base_value + 0.15 + exhibitionist_skill_bonus)))
        if is_at_home_zone is True and get_sex_setting(SexSetting.AUTONOMY_LEVEL, variable_type=int) == SexAutonomyLevelSetting.LOW:
            if is_at_party is True:
                base_value += 0.2
            if is_at_weekend is True:
                base_value += 0.1
            if is_at_night is True:
                return (LocationStyleType.COMFORT, base_value + 0.3)
            return (LocationStyleType.COMFORT, base_value + 0.2)
        if is_at_residential_lot is True and is_at_home is False:
            zone_household = TurboWorldUtil.Household.get_current_zone_household()
            if zone_household is not None:
                household_relationship_score_sum = 0
                zone_household_sims = TurboWorldUtil.Household.get_household_sims(zone_household)
                for household_sim in zone_household_sims:
                    relationship_score_sum = 0
                    for sim in sims_list:
                        relationship_score_sum += get_relationship_with_sim(household_sim, sim, RelationshipTrackType.FRIENDSHIP)
                    household_relationship_score_sum += relationship_score_sum/len(sims_list)
                household_relationship_score_sum /= len(zone_household_sims)
                if 0 < household_relationship_score_sum < 50:
                    if get_sex_setting(SexSetting.AUTONOMY_LEVEL, variable_type=int) == SexAutonomyLevelSetting.HIGH:
                        return random.choice(((LocationStyleType.COMFORT, base_value + 0.35), (LocationStyleType.SEMI_OPEN, base_value + 0.15 + exhibitionist_skill_bonus)))
                    if get_sex_setting(SexSetting.AUTONOMY_LEVEL, variable_type=int) == SexAutonomyLevelSetting.NORMAL:
                        return random.choice(((LocationStyleType.PRIVACY, base_value + 0.25), (LocationStyleType.COMFORT, base_value + 0.2)))
                        if household_relationship_score_sum >= 50:
                            if get_sex_setting(SexSetting.AUTONOMY_LEVEL, variable_type=int) == SexAutonomyLevelSetting.HIGH:
                                return random.choice(((LocationStyleType.PRIVACY, base_value + 0.7), (LocationStyleType.COMFORT, base_value + 0.6), (LocationStyleType.SEMI_OPEN, base_value + 0.5 + exhibitionist_skill_bonus), (LocationStyleType.OPEN, base_value + 0.25 + exhibitionist_skill_bonus)))
                            if get_sex_setting(SexSetting.AUTONOMY_LEVEL, variable_type=int) == SexAutonomyLevelSetting.NORMAL:
                                return random.choice(((LocationStyleType.PRIVACY, base_value + 0.5), (LocationStyleType.COMFORT, base_value + 0.4)))
                            if get_sex_setting(SexSetting.AUTONOMY_LEVEL, variable_type=int) == SexAutonomyLevelSetting.LOW:
                                return (LocationStyleType.PRIVACY, base_value + 0.25)
                elif household_relationship_score_sum >= 50:
                    if get_sex_setting(SexSetting.AUTONOMY_LEVEL, variable_type=int) == SexAutonomyLevelSetting.HIGH:
                        return random.choice(((LocationStyleType.PRIVACY, base_value + 0.7), (LocationStyleType.COMFORT, base_value + 0.6), (LocationStyleType.SEMI_OPEN, base_value + 0.5 + exhibitionist_skill_bonus), (LocationStyleType.OPEN, base_value + 0.25 + exhibitionist_skill_bonus)))
                    if get_sex_setting(SexSetting.AUTONOMY_LEVEL, variable_type=int) == SexAutonomyLevelSetting.NORMAL:
                        return random.choice(((LocationStyleType.PRIVACY, base_value + 0.5), (LocationStyleType.COMFORT, base_value + 0.4)))
                    if get_sex_setting(SexSetting.AUTONOMY_LEVEL, variable_type=int) == SexAutonomyLevelSetting.LOW:
                        return (LocationStyleType.PRIVACY, base_value + 0.25)
        if get_sex_setting(SexSetting.AUTONOMY_LEVEL, variable_type=int) == SexAutonomyLevelSetting.HIGH:
            if is_at_party is True:
                base_value += 0.1
            if is_at_weekend is True:
                base_value += 0.05
            return random.choice(((LocationStyleType.COMFORT, base_value + 0.2), (LocationStyleType.SEMI_OPEN, base_value + 0.4 + exhibitionist_skill_bonus), (LocationStyleType.OPEN, base_value + 0.2 + exhibitionist_skill_bonus)))
        if get_sex_setting(SexSetting.AUTONOMY_LEVEL, variable_type=int) == SexAutonomyLevelSetting.NORMAL:
            if is_at_party is True:
                base_value += 0.1
            if is_at_weekend is True:
                base_value += 0.05
            return random.choice(((LocationStyleType.PRIVACY, base_value + 0.45), (LocationStyleType.SEMI_OPEN, base_value + 0.2 + exhibitionist_skill_bonus)))
        if is_at_specific_lot is True and is_at_night is True and get_sex_setting(SexSetting.AUTONOMY_LEVEL, variable_type=int) == SexAutonomyLevelSetting.LOW:
            if is_at_party is True:
                base_value += 0.05
            if is_at_weekend is True:
                base_value += 0.05
            return random.choice(((LocationStyleType.PRIVACY, base_value + 0.2), (LocationStyleType.SEMI_OPEN, base_value + 0.1 + exhibitionist_skill_bonus)))
        if is_at_night is True:
            if get_sex_setting(SexSetting.AUTONOMY_LEVEL, variable_type=int) == SexAutonomyLevelSetting.HIGH:
                if is_at_party is True:
                    base_value += 0.1
                if is_at_weekend is True:
                    base_value += 0.1
                return random.choice(((LocationStyleType.SEMI_OPEN, base_value + 0.4 + exhibitionist_skill_bonus), (LocationStyleType.OPEN, base_value + 0.35 + exhibitionist_skill_bonus), (LocationStyleType.PUBLIC, base_value + 0.2 + exhibitionist_skill_bonus)))
            if get_sex_setting(SexSetting.AUTONOMY_LEVEL, variable_type=int) == SexAutonomyLevelSetting.NORMAL:
                if is_at_party is True:
                    base_value += 0.05
                if is_at_weekend is True:
                    base_value += 0.1
                return random.choice(((LocationStyleType.PRIVACY, base_value + 0.5), (LocationStyleType.SEMI_OPEN, base_value + 0.3 + exhibitionist_skill_bonus)))
            if get_sex_setting(SexSetting.AUTONOMY_LEVEL, variable_type=int) == SexAutonomyLevelSetting.LOW:
                return random.choice(((LocationStyleType.PRIVACY, base_value + 0.25), (LocationStyleType.SEMI_OPEN, base_value + 0.1 + exhibitionist_skill_bonus)))
                if get_sex_setting(SexSetting.AUTONOMY_LEVEL, variable_type=int) == SexAutonomyLevelSetting.HIGH:
                    if is_at_party is True:
                        base_value += 0.05
                    if is_at_weekend is True:
                        base_value += 0.1
                    return random.choice(((LocationStyleType.PRIVACY, base_value + 0.4), (LocationStyleType.SEMI_OPEN, base_value + 0.3 + exhibitionist_skill_bonus), (LocationStyleType.OPEN, base_value + 0.2 + exhibitionist_skill_bonus)))
                if get_sex_setting(SexSetting.AUTONOMY_LEVEL, variable_type=int) == SexAutonomyLevelSetting.NORMAL:
                    if is_at_party is True:
                        base_value += 0.05
                    if is_at_weekend is True:
                        base_value += 0.05
                    return random.choice(((LocationStyleType.PRIVACY, base_value + 0.35), (LocationStyleType.SEMI_OPEN, base_value + 0.2 + exhibitionist_skill_bonus)))
                if get_sex_setting(SexSetting.AUTONOMY_LEVEL, variable_type=int) == SexAutonomyLevelSetting.LOW:
                    return (LocationStyleType.PRIVACY, base_value + 0.2)
        else:
            if get_sex_setting(SexSetting.AUTONOMY_LEVEL, variable_type=int) == SexAutonomyLevelSetting.HIGH:
                if is_at_party is True:
                    base_value += 0.05
                if is_at_weekend is True:
                    base_value += 0.1
                return random.choice(((LocationStyleType.PRIVACY, base_value + 0.4), (LocationStyleType.SEMI_OPEN, base_value + 0.3 + exhibitionist_skill_bonus), (LocationStyleType.OPEN, base_value + 0.2 + exhibitionist_skill_bonus)))
            if get_sex_setting(SexSetting.AUTONOMY_LEVEL, variable_type=int) == SexAutonomyLevelSetting.NORMAL:
                if is_at_party is True:
                    base_value += 0.05
                if is_at_weekend is True:
                    base_value += 0.05
                return random.choice(((LocationStyleType.PRIVACY, base_value + 0.35), (LocationStyleType.SEMI_OPEN, base_value + 0.2 + exhibitionist_skill_bonus)))
            if get_sex_setting(SexSetting.AUTONOMY_LEVEL, variable_type=int) == SexAutonomyLevelSetting.LOW:
                return (LocationStyleType.PRIVACY, base_value + 0.2)
    return (LocationStyleType.NONE, 0.0)

