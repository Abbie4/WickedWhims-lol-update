from buffs.buff_ops import BuffOp
from event_testing.test_variants import UserRunningInteractionTest
from turbolib.sim_util import TurboSimUtil
try:
    from sims.sim_info_tests import SimInfoTest, MatchType
except:
    from event_testing.test_variants import SimInfoTest, MatchType
from filters.tunable import AgeFilterTerm
from interactions import ParticipantType
from relationships.relationship_tests import RelationshipTestEvents, RelationshipTest
from sims.phone_tuning import PhoneTuning
from sims4.collections import ListSet
from sims4.localization import TunableLocalizedStringFactory
from sims4.tuning.tunable import TunedInterval
from whims.whims_tracker import WhimsTracker
from turbolib.resource_util import TurboResourceUtil

class TurboTunableUtil:
    __qualname__ = 'TurboTunableUtil'

    class ParticipantType:
        __qualname__ = 'TurboTunableUtil.ParticipantType'

        def _get_participant_type(*args):
            try:
                return ParticipantType(args[0])
            except:
                return ParticipantType.Invalid

        Invalid = _get_participant_type(0)
        Actor = _get_participant_type(1)
        Object = _get_participant_type(2)
        TargetSim = _get_participant_type(4)
        Listeners = _get_participant_type(8)
        All = _get_participant_type(16)
        AllSims = _get_participant_type(32)
        Lot = _get_participant_type(64)
        CraftingProcess = _get_participant_type(128)
        JoinTarget = _get_participant_type(256)
        CarriedObject = _get_participant_type(512)
        Affordance = _get_participant_type(1024)
        InteractionContext = _get_participant_type(2048)
        CustomSim = _get_participant_type(4096)
        AllRelationships = _get_participant_type(8192)
        CraftingObject = _get_participant_type(16384)
        ActorSurface = _get_participant_type(32768)
        ObjectChildren = _get_participant_type(65536)
        LotOwners = _get_participant_type(131072)
        CreatedObject = _get_participant_type(262144)
        PickedItemId = _get_participant_type(524288)
        StoredSim = _get_participant_type(1048576)
        PickedObject = _get_participant_type(2097152)
        SocialGroup = _get_participant_type(4194304)
        OtherSimsInteractingWithTarget = _get_participant_type(8388608)
        PickedSim = _get_participant_type(16777216)
        ObjectParent = _get_participant_type(33554432)
        SignificantOtherActor = _get_participant_type(67108864)
        SignificantOtherTargetSim = _get_participant_type(134217728)
        OwnerSim = _get_participant_type(268435456)
        StoredSimOnActor = _get_participant_type(536870912)
        Unlockable = _get_participant_type(1073741824)
        LiveDragActor = _get_participant_type(2147483648)
        LiveDragTarget = _get_participant_type(4294967296)
        PickedZoneId = _get_participant_type(8589934592)
        SocialGroupSims = _get_participant_type(17179869184)
        PregnancyPartnerActor = _get_participant_type(34359738368)
        PregnancyPartnerTargetSim = _get_participant_type(68719476736)
        SocialGroupAnchor = _get_participant_type(137438953472)
        TargetSurface = _get_participant_type(274877906944)
        ActiveHousehold = _get_participant_type(549755813888)
        ActorPostureTarget = _get_participant_type(1099511627776)
        InventoryObjectStack = _get_participant_type(2199023255552)
        AllOtherInstancedSims = _get_participant_type(4398046511104)
        CareerEventSim = _get_participant_type(8796093022208)
        StoredSimOnPickedObject = _get_participant_type(17592186044416)
        SavedActor1 = _get_participant_type(35184372088832)
        SavedActor2 = _get_participant_type(70368744177664)
        SavedActor3 = _get_participant_type(140737488355328)
        SavedActor4 = _get_participant_type(281474976710656)
        LotOwnerSingleAndInstanced = _get_participant_type(562949953421312)
        LinkedPostureSim = _get_participant_type(1125899906842624)
        AssociatedClub = _get_participant_type(2251799813685248)
        AssociatedClubMembers = _get_participant_type(4503599627370496)
        AssociatedClubLeader = _get_participant_type(9007199254740992)
        AssociatedClubGatheringMembers = _get_participant_type(18014398509481984)
        ActorEnsemble = _get_participant_type(36028797018963968)
        TargetEnsemble = _get_participant_type(72057594037927936)
        TargetSimPostureTarget = _get_participant_type(144115188075855872)
        ActorEnsembleSansActor = _get_participant_type(288230376151711744)
        ActorDiningGroupMembers = _get_participant_type(576460752303423488)
        TableDiningGroupMembers = _get_participant_type(1152921504606846976)
        StoredSimOrNameData = _get_participant_type(2305843009213693952)
        TargetDiningGroupMembers = _get_participant_type(4611686018427387904)
        LinkedObjects = _get_participant_type(9223372036854775808)

    class Whims:
        __qualname__ = 'TurboTunableUtil.Whims'

        class WhimAwardTypes:
            __qualname__ = 'TurboTunableUtil.Whims.WhimAwardTypes'

            def _get_whim_award_type(*args):
                try:
                    return WhimsTracker.WhimAwardTypes(args[0])
                except:
                    return

            MONEY = _get_whim_award_type(0)
            BUFF = _get_whim_award_type(1)
            OBJECT = _get_whim_award_type(2)
            TRAIT = _get_whim_award_type(3)
            CASPART = _get_whim_award_type(4)

        @staticmethod
        def get_whims_tracker_satisfaction_store_items():
            return WhimsTracker.SATISFACTION_STORE_ITEMS

        @staticmethod
        def set_whims_tracker_satisfaction_store_items(new_satisfaction_store_items):
            WhimsTracker.SATISFACTION_STORE_ITEMS = new_satisfaction_store_items

    class Filters:
        __qualname__ = 'TurboTunableUtil.Filters'

        class AgeFilterTerm:
            __qualname__ = 'TurboTunableUtil.Filters.AgeFilterTerm'

            @staticmethod
            def is_age_filter_term(age_filter_term):
                return isinstance(age_filter_term, AgeFilterTerm)

            @staticmethod
            def get_age_filter_term(minimum_filter_score=None, invert_score=None, min_value=None, max_value=None, ideal_value=None, copy_age_filter_term=None):
                if minimum_filter_score is None:
                    minimum_filter_score = copy_age_filter_term.minimum_filter_score
                if invert_score is None:
                    invert_score = copy_age_filter_term.invert_score
                if min_value is None:
                    invert_score = copy_age_filter_term.min_value
                if max_value is None:
                    max_value = copy_age_filter_term.max_value
                if copy_age_filter_term is not None and ideal_value is None:
                    ideal_value = copy_age_filter_term.ideal_value
                return AgeFilterTerm(minimum_filter_score=minimum_filter_score, invert_score=invert_score, min_value=min_value, max_value=max_value, ideal_value=ideal_value)

    class Tests:
        __qualname__ = 'TurboTunableUtil.Tests'

        class Relationship:
            __qualname__ = 'TurboTunableUtil.Tests.Relationship'

            @staticmethod
            def get_relationship_test(subject=None, target_sim=None, required_relationship_bits=None, prohibited_relationship_bits=None, track=None, relationship_score_interval=None, test_incest=None, num_relations=None, test_event=None, copy_relationship_test=None):
                class_args_list = list(None for _ in range(len(RelationshipTest.__slots__) - 1))
                if len(class_args_list) >= 1:
                    if subject:
                        class_args_list[0] = subject
                    elif copy_relationship_test is not None:
                        class_args_list[0] = copy_relationship_test.subject
                    else:
                        class_args_list[0] = TurboTunableUtil.ParticipantType.Actor
                if len(class_args_list) >= 2:
                    if target_sim:
                        class_args_list[1] = target_sim
                    elif copy_relationship_test is not None:
                        class_args_list[1] = copy_relationship_test.target_sim
                    else:
                        class_args_list[1] = TurboTunableUtil.ParticipantType.TargetSim
                if len(class_args_list) >= 3:
                    if required_relationship_bits:
                        immutable_slots_class = TurboResourceUtil.Collections.get_immutable_slots_class(list(required_relationship_bits.keys()))
                        class_args_list[2] = immutable_slots_class(required_relationship_bits)
                    elif copy_relationship_test is not None:
                        class_args_list[2] = copy_relationship_test.required_relationship_bits
                    else:
                        immutable_slots_class = TurboResourceUtil.Collections.get_immutable_slots_class(['match_all', 'match_any'])
                        class_args_list[2] = immutable_slots_class(dict(match_all=frozenset(), match_any=frozenset()))
                if len(class_args_list) >= 4:
                    if prohibited_relationship_bits:
                        immutable_slots_class = TurboResourceUtil.Collections.get_immutable_slots_class(list(prohibited_relationship_bits.keys()))
                        class_args_list[3] = immutable_slots_class(prohibited_relationship_bits)
                    elif copy_relationship_test is not None:
                        class_args_list[3] = copy_relationship_test.prohibited_relationship_bits
                    else:
                        immutable_slots_class = TurboResourceUtil.Collections.get_immutable_slots_class(['match_all', 'match_any'])
                        class_args_list[3] = immutable_slots_class(dict(match_all=frozenset(), match_any=frozenset()))
                if len(class_args_list) >= 5:
                    if track:
                        class_args_list[4] = track
                    elif copy_relationship_test is not None:
                        class_args_list[4] = copy_relationship_test.track
                if len(class_args_list) >= 6:
                    if relationship_score_interval:
                        class_args_list[5] = relationship_score_interval
                    elif copy_relationship_test is not None:
                        class_args_list[5] = copy_relationship_test.relationship_score_interval
                    else:
                        class_args_list[5] = TunedInterval(lower_bound=-100.0, upper_bound=100.0)
                if len(class_args_list) >= 7:
                    if test_incest:
                        class_args_list[6] = test_incest
                    elif copy_relationship_test is not None:
                        class_args_list[6] = copy_relationship_test.test_incest
                if len(class_args_list) >= 8:
                    if num_relations:
                        class_args_list[7] = num_relations
                    elif copy_relationship_test is not None:
                        class_args_list[7] = copy_relationship_test.num_relations
                    else:
                        class_args_list[7] = 0
                if len(class_args_list) >= 9:
                    if test_event:
                        class_args_list[8] = test_event
                    elif copy_relationship_test is not None:
                        class_args_list[8] = copy_relationship_test.test_event
                    else:
                        class_args_list[8] = RelationshipTestEvents.AllRelationshipEvents
                return RelationshipTest(*class_args_list)

        class SimInfo:
            __qualname__ = 'TurboTunableUtil.Tests.SimInfo'

            @staticmethod
            def is_sim_info_test(sim_info_test):
                return isinstance(sim_info_test, SimInfoTest)

            @staticmethod
            def is_age_test(sim_info_test):
                return bool(sim_info_test.ages)

            @staticmethod
            def get_ages_from_sim_info_test(sim_info_test):
                if not isinstance(sim_info_test, SimInfoTest) or not sim_info_test.ages:
                    return list()
                return list(sim_info_test.ages)

            @staticmethod
            def get_who_from_sim_info_test(sim_info_test):
                return sim_info_test.who

            @staticmethod
            def get_sim_info_test(who=None, gender=None, ages=None, species=None, can_age_up=None, npc=None, has_been_played=None, is_active_sim=None, match_type=None, copy_sim_info_test=None):
                try:
                    sim_info_test = SimInfoTest()
                except:
                    sim_info_test = SimInfoTest(*list(None for _ in range(len(SimInfoTest.__slots__))))
                if who is not None:
                    sim_info_test.who = who
                elif copy_sim_info_test is not None:
                    sim_info_test.who = copy_sim_info_test.who
                else:
                    sim_info_test.who = ParticipantType.Actor
                if gender is not None:
                    sim_info_test.gender = gender
                elif copy_sim_info_test is not None:
                    sim_info_test.gender = copy_sim_info_test.gender
                else:
                    sim_info_test.gender = None
                if ages is not None:
                    sim_info_test.ages = frozenset(ages)
                elif copy_sim_info_test is not None:
                    sim_info_test.ages = copy_sim_info_test.ages
                else:
                    sim_info_test.ages = (TurboSimUtil.Age.TEEN, TurboSimUtil.Age.YOUNGADULT, TurboSimUtil.Age.ADULT, TurboSimUtil.Age.ELDER)
                if species is not None:
                    sim_info_test.species = frozenset(species) if species else None
                elif copy_sim_info_test is not None:
                    sim_info_test.species = copy_sim_info_test.species
                else:
                    sim_info_test.species = None
                if can_age_up is not None:
                    sim_info_test.can_age_up = can_age_up
                elif copy_sim_info_test is not None:
                    sim_info_test.can_age_up = copy_sim_info_test.can_age_up
                else:
                    sim_info_test.can_age_up = None
                if npc is not None:
                    sim_info_test.npc = npc
                elif copy_sim_info_test is not None:
                    sim_info_test.npc = copy_sim_info_test.npc
                else:
                    sim_info_test.npc = False
                if has_been_played is not None:
                    sim_info_test.has_been_played = has_been_played
                elif copy_sim_info_test is not None:
                    sim_info_test.has_been_played = copy_sim_info_test.has_been_played
                else:
                    sim_info_test.has_been_played = False
                if is_active_sim is not None:
                    sim_info_test.is_active_sim = is_active_sim
                elif copy_sim_info_test is not None:
                    sim_info_test.is_active_sim = copy_sim_info_test.is_active_sim
                else:
                    sim_info_test.is_active_sim = True
                if match_type is not None:
                    sim_info_test.match_type = match_type
                elif copy_sim_info_test is not None:
                    sim_info_test.match_type = copy_sim_info_test.match_type
                else:
                    sim_info_test.match_type = MatchType.MATCH_ALL
                return sim_info_test

    class Loot:
        __qualname__ = 'TurboTunableUtil.Loot'

        @staticmethod
        def is_buff_operation(buff_operation):
            return isinstance(buff_operation, BuffOp)

    class Phone:
        __qualname__ = 'TurboTunableUtil.Phone'

        @staticmethod
        def register_disabled_affordances(affordances_list):
            affordance_manager = TurboResourceUtil.Services.get_instance_manager(TurboResourceUtil.ResourceTypes.INTERACTION)
            valid_affordances = set()
            for affordance_id in affordances_list:
                affordance_instance = TurboResourceUtil.Services.get_instance_from_manager(affordance_manager, affordance_id)
                while affordance_instance is not None:
                    valid_affordances.add(affordance_instance)
            interactions_test = UserRunningInteractionTest(participant=ParticipantType.Actor, affordances=valid_affordances, affordance_lists=list(), test_for_not_running=False, all_participants_running=False)
            immutable_slots_class = TurboResourceUtil.Collections.get_immutable_slots_class(['test', 'tooltip'])
            immutable_slots = immutable_slots_class(dict(test=interactions_test, tooltip=TunableLocalizedStringFactory._Wrapper(3956250692)))
            items_list = list(PhoneTuning.DISABLE_PHONE_TESTS)
            items_list.append(immutable_slots)
            PhoneTuning.DISABLE_PHONE_TESTS = ListSet(items_list)

