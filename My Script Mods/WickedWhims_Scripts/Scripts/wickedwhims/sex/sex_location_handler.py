'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from collections import OrderedDict
from enums.tags_enum import GameTag
from turbolib.object_util import TurboObjectUtil
from turbolib.types_util import TurboTypesUtil

class SexLocationType:
    __qualname__ = 'SexLocationType'
    FLOOR = 'FLOOR'
    POOL = 'POOL'
    TABLE_DINING_SHORT = 'TABLE_DINING_SHORT'
    TABLE_DINING_LONG = 'TABLE_DINING_LONG'
    TABLE_TV_STAND = 'TABLE_TV_STAND'
    TABLE_COFFEE = 'TABLE_COFFEE'
    TABLE_ACCENT = 'TABLE_ACCENT'
    TABLE_PICNIC = 'TABLE_PICNIC'
    TABLE_OUTDOOR = 'TABLE_OUTDOOR'
    TABLE_OUTDOOR_UMBRELLA = 'TABLE_OUTDOOR_UMBRELLA'
    DESK = 'DESK'
    BAR = 'BAR'
    COUNTER = 'COUNTER'
    SOFA = 'SOFA'
    LOVESEAT = 'LOVESEAT'
    BENCH_OUTDOOR = 'BENCH_OUTDOOR'
    WORKOUT_MACHINE = 'WORKOUT_MACHINE'
    CHAIR_LIVING = 'CHAIR_LIVING'
    CHAIR_DINING = 'CHAIR_DINING'
    CHAIR_STOOL = 'CHAIR_STOOL'
    CHAIR_DESK = 'CHAIR_DESK'
    TOILET = 'TOILET'
    DOUBLE_BED = 'DOUBLE_BED'
    SINGLE_BED = 'SINGLE_BED'
    OTTOMAN = 'OTTOMAN'
    HOTTUB = 'HOTTUB'
    SHOWER_TUB = 'SHOWER_TUB'
    SHOWER = 'SHOWER'
    BATHTUB = 'BATHTUB'
    SAUNA = 'SAUNA'
    YOGA_MAT = 'YOGA_MAT'
    MASSAGE_TABLE = 'MASSAGE_TABLE'
    WINDOW = 'WINDOW'
    MIRROR = 'MIRROR'
    TABLE_DNING_LONG = 'TABLE_DNING_LONG'
    TABLE_OUTDOOR_UNBRELLA = 'TABLE_OUTDOOR_UNBRELLA'

    @staticmethod
    def get_user_name(sex_location_type):
        if sex_location_type == SexLocationType.FLOOR:
            return 'Floor'
        if sex_location_type == SexLocationType.POOL:
            return 'Pool'
        if sex_location_type == SexLocationType.TABLE_DINING_SHORT:
            return 'Short Dining Table'
        if sex_location_type == SexLocationType.TABLE_DINING_LONG:
            return 'Long Dining Table'
        if sex_location_type == SexLocationType.TABLE_TV_STAND:
            return 'TV Stand'
        if sex_location_type == SexLocationType.TABLE_COFFEE:
            return 'Coffee Table'
        if sex_location_type == SexLocationType.TABLE_ACCENT:
            return 'Accent Table'
        if sex_location_type == SexLocationType.TABLE_PICNIC:
            return 'Picnic Table'
        if sex_location_type == SexLocationType.TABLE_OUTDOOR:
            return 'Outdoor Table'
        if sex_location_type == SexLocationType.TABLE_OUTDOOR_UMBRELLA:
            return 'Outdoor Umbrella Table'
        if sex_location_type == SexLocationType.DESK:
            return 'Desk'
        if sex_location_type == SexLocationType.BAR:
            return 'Bar'
        if sex_location_type == SexLocationType.COUNTER:
            return 'Counter'
        if sex_location_type == SexLocationType.SOFA:
            return 'Sofa'
        if sex_location_type == SexLocationType.LOVESEAT:
            return 'Loveseat'
        if sex_location_type == SexLocationType.BENCH_OUTDOOR:
            return 'Bench'
        if sex_location_type == SexLocationType.WORKOUT_MACHINE:
            return 'Workout Machine'
        if sex_location_type == SexLocationType.CHAIR_LIVING:
            return 'Living Room Chair'
        if sex_location_type == SexLocationType.CHAIR_DINING:
            return 'Dining Room Chair'
        if sex_location_type == SexLocationType.CHAIR_STOOL:
            return 'Stool'
        if sex_location_type == SexLocationType.CHAIR_DESK:
            return 'Desk Chair'
        if sex_location_type == SexLocationType.TOILET:
            return 'Toilet'
        if sex_location_type == SexLocationType.DOUBLE_BED:
            return 'Double Bed'
        if sex_location_type == SexLocationType.SINGLE_BED:
            return 'Single Bed'
        if sex_location_type == SexLocationType.OTTOMAN:
            return 'Ottoman'
        if sex_location_type == SexLocationType.HOTTUB:
            return 'Hot Tub'
        if sex_location_type == SexLocationType.SHOWER_TUB:
            return 'Shower Tub'
        if sex_location_type == SexLocationType.SHOWER:
            return 'Shower'
        if sex_location_type == SexLocationType.BATHTUB:
            return 'Bathtub'
        if sex_location_type == SexLocationType.SAUNA:
            return 'Steam Room'
        if sex_location_type == SexLocationType.YOGA_MAT:
            return 'Yoga Mat'
        if sex_location_type == SexLocationType.MASSAGE_TABLE:
            return 'Massage Table'
        if sex_location_type == SexLocationType.WINDOW:
            return 'Window'
        if sex_location_type == SexLocationType.MIRROR:
            return 'Mirror'
        return str(sex_location_type)


class SexInteractionLocationType:
    __qualname__ = 'SexInteractionLocationType'
    LOCATION_TYPES = OrderedDict()
    LOCATION_TYPES[SexLocationType.FLOOR] = (-1,)
    LOCATION_TYPES[SexLocationType.POOL] = (-1,)
    LOCATION_TYPES[SexLocationType.TABLE_DINING_SHORT] = (int(GameTag.BUYCATSS_DININGTABLESHORT),)
    LOCATION_TYPES[SexLocationType.TABLE_DINING_LONG] = (int(GameTag.BUYCATSS_DININGTABLELONG),)
    LOCATION_TYPES[SexLocationType.TABLE_TV_STAND] = (int(GameTag.BUYCATSS_COFFEETABLE), int(GameTag.BUYCATEE_TVSTAND))
    LOCATION_TYPES[SexLocationType.TABLE_COFFEE] = (int(GameTag.BUYCATSS_COFFEETABLE),)
    LOCATION_TYPES[SexLocationType.TABLE_ACCENT] = (int(GameTag.BUYCATSS_ACCENTTABLE),)
    LOCATION_TYPES[SexLocationType.TABLE_PICNIC] = (int(GameTag.FUNC_PICNICTABLE),)
    LOCATION_TYPES[SexLocationType.TABLE_OUTDOOR] = (int(GameTag.BUYCATSS_OUTDOORTABLE),)
    LOCATION_TYPES[SexLocationType.TABLE_OUTDOOR_UMBRELLA] = (int(GameTag.BUYCATSS_OUTDOORTABLE), int(GameTag.FUNC_TABLEDININGUMBRELLA))
    LOCATION_TYPES[SexLocationType.DESK] = (int(GameTag.BUYCATSS_DESK),)
    LOCATION_TYPES[SexLocationType.BAR] = (int(GameTag.FUNC_BAR),)
    LOCATION_TYPES[SexLocationType.COUNTER] = (int(GameTag.BUYCATSS_COUNTER),)
    LOCATION_TYPES[SexLocationType.SOFA] = (int(GameTag.BUYCATSS_SOFA),)
    LOCATION_TYPES[SexLocationType.LOVESEAT] = (int(GameTag.BUYCATSS_LOVESEAT),)
    LOCATION_TYPES[SexLocationType.BENCH_OUTDOOR] = (int(GameTag.VENUE_OBJECT_BENCH),)
    LOCATION_TYPES[SexLocationType.WORKOUT_MACHINE] = (int(GameTag.FUNC_WORKOUTMACHINE),)
    LOCATION_TYPES[SexLocationType.CHAIR_LIVING] = (int(GameTag.BUYCATSS_LIVINGCHAIR),)
    LOCATION_TYPES[SexLocationType.CHAIR_DINING] = (int(GameTag.FUNC_DININGCHAIR),)
    LOCATION_TYPES[SexLocationType.CHAIR_STOOL] = (int(GameTag.BUYCATSS_BARSTOOL),)
    LOCATION_TYPES[SexLocationType.CHAIR_DESK] = (int(GameTag.BUYCATSS_DESKCHAIR),)
    LOCATION_TYPES[SexLocationType.TOILET] = (int(GameTag.BUYCATPA_TOILET), int(GameTag.FUNC_BLADDER))
    LOCATION_TYPES[SexLocationType.DOUBLE_BED] = (int(GameTag.FUNC_DOUBLEBED),)
    LOCATION_TYPES[SexLocationType.SINGLE_BED] = (int(GameTag.FUNC_SINGLEBED),)
    LOCATION_TYPES[SexLocationType.OTTOMAN] = (int(GameTag.FUNC_OTTOMAN),)
    LOCATION_TYPES[SexLocationType.HOTTUB] = (int(GameTag.FUNC_HOTTUB),)
    LOCATION_TYPES[SexLocationType.SHOWER_TUB] = (int(GameTag.BUYCATPA_SHOWER), int(GameTag.BUYCATPA_TUB))
    LOCATION_TYPES[SexLocationType.SHOWER] = (int(GameTag.BUYCATPA_SHOWER),)
    LOCATION_TYPES[SexLocationType.BATHTUB] = (int(GameTag.BUYCATPA_TUB),)
    LOCATION_TYPES[SexLocationType.SAUNA] = (int(GameTag.FUNC_SAUNA),)
    LOCATION_TYPES[SexLocationType.YOGA_MAT] = (int(GameTag.FUNC_YOGAMAT),)
    LOCATION_TYPES[SexLocationType.MASSAGE_TABLE] = (int(GameTag.FUNC_MASSAGETABLE),)
    LOCATION_TYPES[SexLocationType.WINDOW] = (int(GameTag.BUILD_WINDOW),)
    LOCATION_TYPES[SexLocationType.MIRROR] = (int(GameTag.BUYCATLD_MIRROR),)
    FLOOR_TYPE = (SexLocationType.FLOOR, -1)
    POOL_TYPE = (SexLocationType.POOL, -1)
    LOCATION_TYPES[SexLocationType.TABLE_DNING_LONG] = (int(GameTag.BUYCATSS_DININGTABLELONG),)
    LOCATION_TYPES[SexLocationType.TABLE_OUTDOOR_UNBRELLA] = (int(GameTag.BUYCATSS_OUTDOORTABLE), int(GameTag.FUNC_TABLEDININGUMBRELLA))

    @staticmethod
    def verify_location_type(name):
        name = name.upper()
        for location_type in SexInteractionLocationType.LOCATION_TYPES:
            while location_type == name:
                return name

    @staticmethod
    def get_location_identifier(location_object):
        if TurboTypesUtil.Data.is_location(location_object) or TurboTypesUtil.Objects.is_terrain(location_object):
            return SexInteractionLocationType.FLOOR_TYPE
        object_tags = TurboObjectUtil.GameObject.get_game_tags(location_object)
        object_wwid = TurboObjectUtil.Special.get_object_unique_id(location_object)
        for (location_type, location_tags) in SexInteractionLocationType.LOCATION_TYPES.items():
            tags_count = 0
            for object_tag in object_tags:
                for location_tag in location_tags:
                    while location_tag == object_tag:
                        tags_count += 1
                        break
                while tags_count == len(location_tags):
                    return (location_type, object_wwid)
        return (None, object_wwid)

