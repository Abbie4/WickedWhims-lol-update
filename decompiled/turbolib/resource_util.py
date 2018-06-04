'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
import services
import sims4.collections
from sims4.collections import FrozenAttributeDict
from sims4.resources import get_resource_key, Types, ResourceLoader

class TurboResourceUtil:
    __qualname__ = 'TurboResourceUtil'

    class Client:
        __qualname__ = 'TurboResourceUtil.Client'

        @staticmethod
        def get_current_client_id():
            client = services.client_manager().get_first_client()
            if client is None:
                return 0
            return client.id

    class ResourceTypes:
        __qualname__ = 'TurboResourceUtil.ResourceTypes'

        def _get_resource_type(*args):
            try:
                return Types(args[0])
            except:
                return Types.INVALID

        INVALID = _get_resource_type(4294967295)
        MODEL = _get_resource_type(23466547)
        RIG = _get_resource_type(2393838558)
        FOOTPRINT = _get_resource_type(3548561239)
        SLOT = _get_resource_type(3540272417)
        OBJECTDEFINITION = _get_resource_type(3235601127)
        OBJCATALOG = _get_resource_type(832458525)
        MAGAZINECOLLECTION = _get_resource_type(1946487583)
        GPINI = _get_resource_type(2249506521)
        PNG = _get_resource_type(796721156)
        TGA = _get_resource_type(796721158)
        STATEMACHINE = _get_resource_type(47570707)
        PROPX = _get_resource_type(968010314)
        VP6 = _get_resource_type(929579223)
        BC_CACHE = _get_resource_type(479834948)
        AC_CACHE = _get_resource_type(3794048034)
        XML = _get_resource_type(53690476)
        TRACKMASK = _get_resource_type(53633251)
        CLIP = _get_resource_type(1797309683)
        CLIP_HEADER = _get_resource_type(3158986820)
        OBJDEF = _get_resource_type(3625704905)
        SIMINFO = _get_resource_type(39769844)
        CASPART = _get_resource_type(55242443)
        SKINTONE = _get_resource_type(55867754)
        COMBINED_TUNING = _get_resource_type(1659456824)
        PLAYLIST = _get_resource_type(1415235194)
        DDS = _get_resource_type(11720834)
        WALKSTYLE = _get_resource_type(666901909)
        HOUSEHOLD_DESCRIPTION = _get_resource_type(1923050575)
        REGION_DESCRIPTION = _get_resource_type(3596464121)
        WORLD_DESCRIPTION = _get_resource_type(2793466443)
        LOT_DESCRIPTION = _get_resource_type(26488364)
        FRIEZE = _get_resource_type(2690089244)
        BLOCK = _get_resource_type(127102176)
        CEILING_RAILING = _get_resource_type(1057772186)
        FENCE = _get_resource_type(68746794)
        FLOOR_TRIM = _get_resource_type(2227319321)
        FLOOR_PATTERN = _get_resource_type(3036111561)
        POOL_TRIM = _get_resource_type(2782919923)
        ROOF = _get_resource_type(2448276798)
        ROOF_TRIM = _get_resource_type(2956008719)
        ROOF_PATTERN = _get_resource_type(4058889606)
        STAIRS = _get_resource_type(2585840924)
        RAILING = _get_resource_type(471658999)
        STYLE = _get_resource_type(2673671952)
        WALL = _get_resource_type(2438063804)
        WALL_PATTERN = _get_resource_type(3589339425)
        GENERIC_MTX = _get_resource_type(2885921078)
        TRAY_METADATA = _get_resource_type(713711138)
        HALFWALL_TRIM = _get_resource_type(2851789917)
        TUNING = _get_resource_type(62078431)
        POSTURE = _get_resource_type(2909789983)
        SLOT_TYPE = _get_resource_type(1772477092)
        STATIC_COMMODITY = _get_resource_type(1359443523)
        RELATIONSHIP_BIT = _get_resource_type(151314192)
        OBJECT_STATE = _get_resource_type(1526890910)
        RECIPE = _get_resource_type(3952605219)
        GAME_RULESET = _get_resource_type(3779558936)
        STATISTIC = _get_resource_type(865846717)
        MOOD = _get_resource_type(3128647864)
        BUFF = _get_resource_type(1612179606)
        TRAIT = _get_resource_type(3412057543)
        SLOT_TYPE_SET = _get_resource_type(1058419973)
        PIE_MENU_CATEGORY = _get_resource_type(65657188)
        ASPIRATION = _get_resource_type(683034229)
        ASPIRATION_CATEGORY = _get_resource_type(3813727192)
        ASPIRATION_TRACK = _get_resource_type(3223387309)
        OBJECTIVE = _get_resource_type(6899006)
        TUTORIAL = _get_resource_type(3762955427)
        TUTORIAL_TIP = _get_resource_type(2410930353)
        CAREER = _get_resource_type(1939434475)
        SNIPPET = _get_resource_type(2113017500)
        INTERACTION = _get_resource_type(3900887599)
        ACHIEVEMENT = _get_resource_type(2018877086)
        ACHIEVEMENT_CATEGORY = _get_resource_type(609337601)
        ACHIEVEMENT_COLLECTION = _get_resource_type(80917605)
        SERVICE_NPC = _get_resource_type(2629964386)
        VENUE = _get_resource_type(3871070174)
        REWARD = _get_resource_type(1873057832)
        TEST_BASED_SCORE = _get_resource_type(1332976878)
        LOT_TUNING = _get_resource_type(3632270694)
        REGION = _get_resource_type(1374134669)
        STREET = _get_resource_type(4142189312)
        WALK_BY = _get_resource_type(1070998590)
        OBJECT = _get_resource_type(3055412916)
        ANIMATION = _get_resource_type(3994535597)
        BALLOON = _get_resource_type(3966406598)
        ACTION = _get_resource_type(209137191)
        OBJECT_PART = _get_resource_type(1900520272)
        SITUATION = _get_resource_type(4223905515)
        SITUATION_JOB = _get_resource_type(2617738591)
        SITUATION_GOAL = _get_resource_type(1502554343)
        SITUATION_GOAL_SET = _get_resource_type(2649944562)
        STRATEGY = _get_resource_type(1646578134)
        SIM_FILTER = _get_resource_type(1846401695)
        TOPIC = _get_resource_type(1938713686)
        SIM_TEMPLATE = _get_resource_type(212125579)
        SUBROOT = _get_resource_type(3086978965)
        SOCIAL_GROUP = _get_resource_type(776446212)
        TAG_SET = _get_resource_type(1228493570)
        TEMPLATE_CHOOSER = _get_resource_type(1220728301)
        ZONE_DIRECTOR = _get_resource_type(4183335058)
        ROLE_STATE = _get_resource_type(239932923)
        CAREER_LEVEL = _get_resource_type(745582072)
        CAREER_TRACK = _get_resource_type(1221024995)
        CAREER_EVENT = _get_resource_type(2487354146)
        BROADCASTER = _get_resource_type(3736796019)
        AWAY_ACTION = _get_resource_type(2947394632)
        ROYALTY = _get_resource_type(938421991)
        NOTEBOOK_ENTRY = _get_resource_type(2567109238)
        DETECTIVE_CLUE = _get_resource_type(1400130038)
        BUCKS_PERK = _get_resource_type(3963461902)
        STORY_PROGRESSION_ACTION = _get_resource_type(3187939130)
        CLUB_SEED = _get_resource_type(794407991)
        CLUB_INTERACTION_GROUP = _get_resource_type(4195351092)
        DRAMA_NODE = _get_resource_type(626258997)
        ENSEMBLE = _get_resource_type(3112702240)
        BUSINESS = _get_resource_type(1977092083)
        OPEN_STREET_DIRECTOR = _get_resource_type(1265622724)
        ZONE_MODIFIER = _get_resource_type(1008568217)
        USER_INTERFACE_INFO = _get_resource_type(3099531875)
        CALL_TO_ACTION = _get_resource_type(4114068192)
        TUNING_DESCRIPTION = _get_resource_type(2519486516)

        @staticmethod
        def get_resource_key(instance_type, instance_id):
            return get_resource_key(instance_id, instance_type)

    class Services:
        __qualname__ = 'TurboResourceUtil.Services'

        @staticmethod
        def get_instance(resource_type, instance_id):
            instance_manager = services.get_instance_manager(resource_type)
            resource_key = TurboResourceUtil.ResourceTypes.get_resource_key(resource_type, instance_id)
            return instance_manager.get(resource_key)

        @staticmethod
        def get_instance_manager(resource_type):
            return services.get_instance_manager(resource_type)

        @staticmethod
        def get_all_instances_from_manager(instance_manager):
            return instance_manager.types.items()

        @staticmethod
        def get_instance_from_manager(instance_manager, instance_id):
            resource_key = TurboResourceUtil.ResourceTypes.get_resource_key(instance_manager.TYPE, instance_id)
            return instance_manager.get(resource_key)

    class Resource:
        __qualname__ = 'TurboResourceUtil.Resource'

        @staticmethod
        def get_icon(obj):
            return obj.icon

        @staticmethod
        def get_id(obj):
            if not hasattr(obj, 'id'):
                return -1
            return obj.id

        @staticmethod
        def get_guid(obj):
            if not hasattr(obj, 'guid'):
                return -1
            return obj.guid

        @staticmethod
        def get_guid64(obj):
            if not hasattr(obj, 'guid64'):
                return -1
            return int(obj.guid64)

        @staticmethod
        def load_bytes(resource_key, silent_fail=True):
            resource_loader = ResourceLoader(resource_key)
            return resource_loader.load(silent_fail=silent_fail)

    class Persistance:
        __qualname__ = 'TurboResourceUtil.Persistance'

        @staticmethod
        def get_save_guid():
            return services.get_persistence_service().get_save_slot_proto_guid()

        @staticmethod
        def get_save_slot_id():
            return services.get_persistence_service().get_save_slot_proto_buff().slot_id

        @staticmethod
        def get_save_id_data():
            persistance_service = services.get_persistence_service()
            save_guid = persistance_service.get_save_slot_proto_guid()
            slot_id = persistance_service.get_save_slot_proto_buff().slot_id
            return (save_guid, slot_id)

        @staticmethod
        def get_save_id():
            hash_value = 3430008
            for item in TurboResourceUtil.Persistance.get_save_id_data():
                hash_value = eval(hex(1000003*hash_value & 4294967295)[:-1]) ^ item
            hash_value ^= 3
            return abs(hash_value)

    class Collections:
        __qualname__ = 'TurboResourceUtil.Collections'

        @staticmethod
        def get_immutable_slots_class(slots):
            return sims4.collections.make_immutable_slots_class(slots)

        @staticmethod
        def get_frozen_attribute_dict(dictionary):
            return FrozenAttributeDict(dictionary)

