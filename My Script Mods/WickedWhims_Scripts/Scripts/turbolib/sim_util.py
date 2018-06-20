'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
import inspect
import build_buy
import routing
import routing.connectivity
import services
from animation.posture_manifest import Hand
from autonomy.content_sets import get_valid_aops_gen
from autonomy.settings import AutonomyState
from buffs.buff import Buff
from cas.cas import get_tags_from_outfit
from interactions.aop import AffordanceObjectPair
from interactions.context import InteractionContext, QueueInsertStrategy
from interactions.interaction_finisher import FinishingType
from interactions.priority import Priority
from interactions.si_state import SIState
from objects import HiddenReasonFlag
from objects.object_enums import ResetReason
from postures import posture_graph
from postures.posture_specs import get_origin_spec, PostureSpecVariable
from postures.posture_state import PostureState
from protocolbuffers import S4Common_pb2, Outfits_pb2, PersistenceBlobs_pb2
from sims.aging.aging_tuning import AgeSpeeds
from sims.occult.occult_enums import OccultType
from sims.sim_info_types import Gender, Age, Species
from situations.situation_goal_targeted_sim import SituationGoalTargetedSim
from turbolib.cas_util import TurboCASUtil
from turbolib.components_util import TurboComponentUtil
from turbolib.manager_util import TurboManagerUtil
from turbolib.math_util import TurboMathUtil
from turbolib.object_util import TurboObjectUtil
from turbolib.resource_util import TurboResourceUtil

class TurboSimUtil:
    __qualname__ = 'TurboSimUtil'

    class Sim:
        __qualname__ = 'TurboSimUtil.Sim'

        @staticmethod
        def is_npc(sim_identifier):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
            return sim_info.is_npc

        @staticmethod
        def is_player(sim_identifier):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
            return not sim_info.is_npc

        @staticmethod
        def reset_sim(sim_identifier, hard_reset=False, hard_reset_on_exception=False):
            '''
            Soft resets Sim instance.
            Sim Interaction Queue and Super Interaction State is being reset and/or recreated.
            Do not use hard reset if not necessary since it's common for the game to not be able to handle these without errors.
            :param sim_identifier: int or SimInfo or Sim -> sim identifier
            :param hard_reset: bool -> skip soft reset and make a full reset
            :param hard_reset_on_exception: bool -> make a full reset if soft reset throws an exception
            :return: bool -> if reset process was successful
            '''
            sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
            if sim is None:
                return False
            if hard_reset is True:
                try:
                    sim.reset(ResetReason.RESET_EXPECTED)
                    return True
                except:
                    return False
            try:
                if sim.queue is not None:
                    sim.queue.on_reset()
                    sim.queue.unlock()
                if sim.si_state is not None:
                    try:
                        sim.si_state.on_reset()
                    except:
                        sim._si_state = SIState(sim)
                        sim.si_state.on_reset()
                else:
                    sim._si_state = SIState(sim)
                    sim.si_state.on_reset()
                if sim.ui_manager is not None:
                    sim.ui_manager.remove_all_interactions()
                sim.socials_locked = False
                sim.last_affordance = None
                sim.two_person_social_transforms.clear()
                if sim.posture_state is not None:
                    sim.posture_state.on_reset(ResetReason.RESET_EXPECTED)
                sim._stop_animation_interaction()
                sim._start_animation_interaction()
                if build_buy.is_location_pool(services.current_zone_id(), sim.position, sim.location.level):
                    posture_type = posture_graph.SIM_SWIM_POSTURE_TYPE
                else:
                    posture_type = posture_graph.SIM_DEFAULT_POSTURE_TYPE
                sim.posture_state = PostureState(sim, None, get_origin_spec(posture_type), {PostureSpecVariable.HAND: (Hand.LEFT,)})
                sim._posture_target_refs.clear()
                return True
            except:
                if hard_reset_on_exception is True:
                    return TurboSimUtil.Sim.reset_sim(sim, hard_reset=True)
            return False

    class Name:
        __qualname__ = 'TurboSimUtil.Name'

        @staticmethod
        def has_name(sim_identifier):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier, allow_base_wrapper=True)
            return sim_info.first_name and sim_info.last_name

        @staticmethod
        def get_name(sim_identifier):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier, allow_base_wrapper=True)
            return (sim_info.first_name, sim_info.last_name)

        @staticmethod
        def get_full_name_key(sim_identifier):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier, allow_base_wrapper=True)
            return sim_info.full_name_key

    class Age:
        __qualname__ = 'TurboSimUtil.Age'
        BABY = Age(1)
        TODDLER = Age(2)
        CHILD = Age(4)
        TEEN = Age(8)
        YOUNGADULT = Age(16)
        ADULT = Age(32)
        ELDER = Age(64)

        class AgeSpeed:
            __qualname__ = 'TurboSimUtil.Age.AgeSpeed'
            FAST = AgeSpeeds(0)
            NORMAL = AgeSpeeds(1)
            SLOW = AgeSpeeds(2)

        @staticmethod
        def get_age(sim_identifier):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier, allow_base_wrapper=True)
            return sim_info.age

        @staticmethod
        def is_younger_than(sim_identifier, age, or_equal=False):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier, allow_base_wrapper=True)
            if or_equal is False:
                return sim_info.age < age
            return sim_info.age <= age

        @staticmethod
        def is_older_than(sim_identifier, age, or_equal=False):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier, allow_base_wrapper=True)
            if or_equal is False:
                return sim_info.age > age
            return sim_info.age >= age

        @staticmethod
        def get_global_age_speed():
            try:
                age_service = services.get_aging_service()
            except:
                age_service = services.get_age_service()
            return int(age_service.aging_speed)

        @staticmethod
        def set_global_age_speed(age_speed):
            try:
                age_service = services.get_aging_service()
            except:
                age_service = services.get_age_service()
            age_service.set_aging_speed(age_speed)

    class Gender:
        __qualname__ = 'TurboSimUtil.Gender'
        MALE = Gender.MALE
        FEMALE = Gender.FEMALE

        @staticmethod
        def get_gender(sim_identifier):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier, allow_base_wrapper=True)
            return sim_info.gender

        @staticmethod
        def is_male(sim_identifier):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier, allow_base_wrapper=True)
            return sim_info.gender == Gender.MALE

        @staticmethod
        def is_female(sim_identifier):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier, allow_base_wrapper=True)
            return sim_info.gender == Gender.FEMALE

        @staticmethod
        def is_male_frame(sim_identifier):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier, allow_base_wrapper=True)
            for trait in TurboSimUtil.Trait.get_all_traits_gen(sim_info):
                while TurboResourceUtil.Resource.get_guid64(trait) == 136877:
                    return True
            return False

        @staticmethod
        def is_female_frame(sim_identifier):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier, allow_base_wrapper=True)
            for trait in TurboSimUtil.Trait.get_all_traits_gen(sim_info):
                while TurboResourceUtil.Resource.get_guid64(trait) == 136878:
                    return True
            return False

        @staticmethod
        def set_gender_preference(sim_identifier, gender, value):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
            sim_info.get_gender_preference(gender).set_value(value)

        @staticmethod
        def get_gender_preference(sim_identifier, gender):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
            return sim_info.get_gender_preference(gender).get_value()

    class Species:
        __qualname__ = 'TurboSimUtil.Species'

        def _get_species(*args):
            try:
                return Species(args[0])
            except:
                return Species.HUMAN

        HUMAN = _get_species(1)
        DOG = _get_species(2)
        CAT = _get_species(3)

        @staticmethod
        def get_species(sim_identifier):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier, allow_base_wrapper=True)
            return sim_info.species

        @staticmethod
        def is_human(sim_identifier):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier, allow_base_wrapper=True)
            return sim_info.species == TurboSimUtil.Species.HUMAN

        @staticmethod
        def is_pet(sim_identifier):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier, allow_base_wrapper=True)
            return sim_info.species != TurboSimUtil.Species.HUMAN

    class Occult:
        __qualname__ = 'TurboSimUtil.Occult'

        def _get_occult_type(*args):
            try:
                return OccultType(args[0])
            except:
                return OccultType.HUMAN

        HUMAN = _get_occult_type(1)
        ALIEN = _get_occult_type(2)
        VAMPIRE = _get_occult_type(4)

        @staticmethod
        def is_ghost(sim_identifier):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
            for trait in TurboSimUtil.Trait.get_all_traits_gen(sim_info):
                while trait.is_ghost_trait:
                    return True
            return False

        @staticmethod
        def get_current_occult_type(sim_identifier):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
            return sim_info.current_occult_types

        @staticmethod
        def get_occult_types(sim_identifier):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
            for occult in OccultType:
                while sim_info.occult_tracker.has_occult_type(occult):
                    yield occult

        @staticmethod
        def get_all_sim_info_occults(sim_identifier):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
            if sim_info is None:
                return (sim_identifier,)
            sim_current_occult_typ = sim_info.current_occult_types
            sim_info_list = [sim_info]
            for occult in OccultType:
                if occult == sim_current_occult_typ:
                    pass
                while sim_info.occult_tracker.has_occult_type(occult):
                    occult_sim_info = sim_info.occult_tracker.get_occult_sim_info(occult)
                    if occult_sim_info is None:
                        pass
                    sim_info_list.append(occult_sim_info)
            return sim_info_list

    class Household:
        __qualname__ = 'TurboSimUtil.Household'

        @staticmethod
        def get_household(sim_identifier):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
            return sim_info.household

        @staticmethod
        def is_same_household(sim_identifier, target_sim_identifier):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
            if sim_info.household is None:
                return False
            target_sim_info = TurboManagerUtil.Sim.get_sim_info(target_sim_identifier)
            if target_sim_info.household is None:
                return False
            return sim_info.household is target_sim_info.household

    class Relationship:
        __qualname__ = 'TurboSimUtil.Relationship'

        @staticmethod
        def get_relationship_score(sim_identifier, target_sim_identifier, relationship_track_instance):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
            target_sim_info = TurboManagerUtil.Sim.get_sim_info(target_sim_identifier)
            return sim_info.relationship_tracker.get_relationship_score(target_sim_info.sim_id, relationship_track_instance)

        @staticmethod
        def set_relationship_score(sim_identifier, target_sim_identifier, relationship_track_instance, amount):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
            target_sim_info = TurboManagerUtil.Sim.get_sim_info(target_sim_identifier)
            sim_info.relationship_tracker.set_relationship_score(target_sim_info.sim_id, amount, relationship_track_instance)

        @staticmethod
        def change_relationship_score(sim_identifier, target_sim_identifier, relationship_track_instance, amount):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
            target_sim_info = TurboManagerUtil.Sim.get_sim_info(target_sim_identifier)
            sim_info.relationship_tracker.add_relationship_score(target_sim_info.sim_id, amount, relationship_track_instance)

        @staticmethod
        def add_relationship_bit(sim_identifier, target_sim_identifier, relationship_bit_instance, force_add=False):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
            target_sim_info = TurboManagerUtil.Sim.get_sim_info(target_sim_identifier)
            sim_info.relationship_tracker.add_relationship_bit(target_sim_info.sim_id, relationship_bit_instance, force_add=force_add)

        @staticmethod
        def remove_relationship_bit(sim_identifier, target_sim_identifier, relationship_bit_instance):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
            target_sim_info = TurboManagerUtil.Sim.get_sim_info(target_sim_identifier)
            sim_info.relationship_tracker.remove_relationship_bit(target_sim_info.sim_id, relationship_bit_instance)

        @staticmethod
        def has_relationship_bit(sim_identifier, target_sim_identifier, relationship_bit_instance):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
            target_sim_info = TurboManagerUtil.Sim.get_sim_info(target_sim_identifier)
            return sim_info.relationship_tracker.has_bit(target_sim_info.sim_id, relationship_bit_instance)

        @staticmethod
        def get_target_ids_with_relationship_bit(sim_identifier, relationship_bit_instance):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
            sims_ids = list()
            for target_sim_info in TurboManagerUtil.Sim.get_all_sim_info_gen(humans=True, pets=False):
                if sim_info is target_sim_info:
                    pass
                while sim_info.relationship_tracker.has_bit(target_sim_info.sim_id, relationship_bit_instance):
                    sims_ids.append(target_sim_info.sim_id)
            return sims_ids

        @staticmethod
        def create_relationship(sim_identifier, target_sim_identifier, relationship_track_instance):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
            target_sim_info = TurboManagerUtil.Sim.get_sim_info(target_sim_identifier)
            relationship = sim_info.relationship_tracker.create_relationship(target_sim_info.sim_id)
            relationship.relationship_track_tracker.add_statistic(relationship_track_instance)

        @staticmethod
        def is_family(sim_identifier, target_sim_identifier):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
            target_sim_info = TurboManagerUtil.Sim.get_sim_info(target_sim_identifier)
            sim_info_family_data = set(sim_info.get_family_sim_ids(include_self=True))
            target_sim_info_family_data = set(target_sim_info.get_family_sim_ids(include_self=True))
            families_union = sim_info_family_data & target_sim_info_family_data
            if None in families_union:
                families_union.remove(None)
            if families_union:
                return True
            return False

    class Statistic:
        __qualname__ = 'TurboSimUtil.Statistic'

        @staticmethod
        def add_tracked_statistic(sim_identifier, statistic_instance, value):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
            if not TurboSimUtil.Component.has_component(sim_info, TurboComponentUtil.ComponentType.STATISTIC):
                return
            statistics_tracker = sim_info.get_tracker(statistic_instance)
            statistic = statistics_tracker.add_statistic(statistic_instance)
            if value is not None:
                statistic.set_value(value)

        @staticmethod
        def get_tracked_statistic(sim_identifier, statistic_instance, add=False):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
            if not TurboSimUtil.Component.has_component(sim_info, TurboComponentUtil.ComponentType.STATISTIC):
                return
            statistic_tracker = sim_info.get_tracker(statistic_instance)
            if statistic_tracker:
                return statistic_tracker.get_statistic(statistic_instance, add=add)

        @staticmethod
        def has_tracked_statistic(sim_identifier, statistic_instance):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
            if not TurboSimUtil.Component.has_component(sim_info, TurboComponentUtil.ComponentType.STATISTIC):
                return False
            statistic_tracker = sim_info.get_tracker(statistic_instance)
            if statistic_tracker:
                return statistic_tracker.has_statistic(statistic_instance)
            return False

        @staticmethod
        def remove_tracked_statistic(sim_identifier, statistic_instance):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
            if not TurboSimUtil.Component.has_component(sim_info, TurboComponentUtil.ComponentType.STATISTIC):
                return
            return sim_info.remove_statistic(statistic_instance)

        @staticmethod
        def set_statistic_value(sim_identifier, statistic_instance, value, add=True):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
            if not TurboSimUtil.Component.has_component(sim_info, TurboComponentUtil.ComponentType.STATISTIC):
                return
            statistic_tracker = sim_info.get_tracker(statistic_instance)
            if statistic_tracker:
                statistic_tracker.set_value(statistic_instance, value, add=add)

        @staticmethod
        def get_statistic_value(sim_identifier, statistic_instance, add=False):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
            if not TurboSimUtil.Component.has_component(sim_info, TurboComponentUtil.ComponentType.STATISTIC):
                return statistic_instance.get_initial_value()
            statistic_tracker = sim_info.get_tracker(statistic_instance)
            if statistic_tracker:
                return statistic_tracker.get_value(statistic_instance, add=add)
            return statistic_instance.get_initial_value()

        @staticmethod
        def get_statistic_initial_value(statistic_instance):
            return statistic_instance.get_initial_value()

        @staticmethod
        def get_statistic_min_value(statistic_instance):
            return statistic_instance.min_value

        @staticmethod
        def get_statistic_max_value(statistic_instance):
            return statistic_instance.max_value

        @staticmethod
        def change_tracker_statistic(sim_identifier, statistic_instance, value, add=True):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
            if not TurboSimUtil.Component.has_component(sim_info, TurboComponentUtil.ComponentType.STATISTIC):
                return
            statistic_tracker = sim_info.get_tracker(statistic_instance)
            if statistic_tracker:
                statistic_tracker.set_value(statistic_instance, statistic_tracker.get_value(statistic_instance, add=add) + value, add=add)

    class Motive:
        __qualname__ = 'TurboSimUtil.Motive'

        @staticmethod
        def is_motive_disabled(sim_identifier, motive_instance, add=True):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
            motive_tracker = sim_info.get_tracker(motive_instance)
            if motive_instance.continuous:
                tracked_motive = motive_tracker.get_statistic(motive_instance, add=add)
                if tracked_motive and (tracked_motive.get_decay_rate_modifier() == 0 or sim_info.is_locked(tracked_motive)):
                    return True
            return False

    class Skill:
        __qualname__ = 'TurboSimUtil.Skill'

        @staticmethod
        def has_skill(sim_identifier, skill_instance):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
            skill_tracker = sim_info.get_tracker(skill_instance)
            if skill_tracker:
                return skill_tracker.has_statistic(skill_instance)
            return False

        @staticmethod
        def remove_skill(sim_identifier, skill_instance):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
            skill_tracker = sim_info.get_tracker(skill_instance)
            if skill_tracker:
                return skill_tracker.remove_statistic(skill_instance)
            return False

        @staticmethod
        def get_skill_value(sim_identifier, skill_instance):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
            skill_tracker = sim_info.get_tracker(skill_instance)
            if skill_tracker:
                tracked_skill = skill_tracker.get_statistic(skill_instance, add=False)
                if tracked_skill:
                    return tracked_skill.get_value()
            return 0

        @staticmethod
        def set_skill_value(sim_identifier, skill_instance, value):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
            skill_tracker = sim_info.get_tracker(skill_instance)
            if skill_tracker:
                tracked_skill = skill_tracker.get_statistic(skill_instance, add=True)
                if value > 0:
                    tracked_skill.set_value(value)

        @staticmethod
        def get_value_for_next_level(sim_identifier, skill_instance):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
            skill_tracker = sim_info.get_tracker(skill_instance)
            if skill_tracker:
                tracked_skill = skill_tracker.get_statistic(skill_instance, add=True)
                if tracked_skill:
                    current_level = tracked_skill.get_user_value()
                    amount_for_prev_level = tracked_skill.get_skill_value_for_level(current_level)
                    amount_for_next_level = tracked_skill.get_skill_value_for_level(current_level + 1) - amount_for_prev_level
                    return amount_for_next_level
            return 0

        @staticmethod
        def get_value_for_level(sim_identifier, skill_instance, skill_level):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
            skill_tracker = sim_info.get_tracker(skill_instance)
            if skill_tracker:
                tracked_skill = skill_tracker.get_statistic(skill_instance, add=True)
                if tracked_skill:
                    return tracked_skill.get_skill_value_for_level(skill_level)
            return 0

        @staticmethod
        def get_skill_level(sim_identifier, skill_instance):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
            skill_tracker = sim_info.get_tracker(skill_instance)
            if skill_tracker:
                tracked_skill = skill_tracker.get_statistic(skill_instance, add=False)
                if tracked_skill:
                    return tracked_skill.get_user_value()
            return 0

        @staticmethod
        def set_skill_level(sim_identifier, skill_instance, value):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
            skill_tracker = sim_info.get_tracker(skill_instance)
            if skill_tracker:
                tracked_skill = skill_tracker.get_statistic(skill_instance, add=True)
                return tracked_skill.set_user_value(value)

        @staticmethod
        def has_reached_max_level(sim_identifier, skill_instance):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
            skill_tracker = sim_info.get_tracker(skill_instance)
            if skill_tracker:
                tracked_skill = skill_tracker.get_statistic(skill_instance, add=False)
                if tracked_skill:
                    return tracked_skill.reached_max_level
            return False

    class Trait:
        __qualname__ = 'TurboSimUtil.Trait'

        @staticmethod
        def add(sim_identifier, trait_instance):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier, allow_base_wrapper=True)
            return sim_info.add_trait(trait_instance)

        @staticmethod
        def remove(sim_identifier, trait_instance):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier, allow_base_wrapper=True)
            return sim_info.remove_trait(trait_instance)

        @staticmethod
        def get_all_traits_gen(sim_identifier):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier, allow_base_wrapper=True)
            for trait in sim_info.get_traits():
                yield trait

    class Buff:
        __qualname__ = 'TurboSimUtil.Buff'

        @staticmethod
        def add(sim_identifier, buff_instance, buff_reason=None):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
            if not TurboSimUtil.Component.has_component(sim_info, TurboComponentUtil.ComponentType.BUFF):
                return False
            return sim_info.get_component(TurboComponentUtil.ComponentType.BUFF).add_buff_from_op(buff_instance, buff_reason=buff_reason)

        @staticmethod
        def remove(sim_identifier, buff_instance):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
            if not TurboSimUtil.Component.has_component(sim_info, TurboComponentUtil.ComponentType.BUFF):
                return
            sim_info.get_component(TurboComponentUtil.ComponentType.BUFF).remove_buff_by_type(buff_instance)

        @staticmethod
        def has(sim_identifier, buff_instance):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
            if not TurboSimUtil.Component.has_component(sim_info, TurboComponentUtil.ComponentType.BUFF):
                return False
            return sim_info.get_component(TurboComponentUtil.ComponentType.BUFF).has_buff(buff_instance)

        @staticmethod
        def get_all_buffs_gen(sim_identifier):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
            if not TurboSimUtil.Component.has_component(sim_info, TurboComponentUtil.ComponentType.BUFF):
                return tuple()
            for buff in tuple(sim_info.get_component(TurboComponentUtil.ComponentType.BUFF)):
                while not buff is None:
                    if not isinstance(buff, Buff):
                        pass
                    yield buff

        @staticmethod
        def register_for_buff_added_callback(sim_identifier, callback):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
            if not TurboSimUtil.Component.has_component(sim_info, TurboComponentUtil.ComponentType.BUFF):
                return
            if callback not in sim_info.get_component(TurboComponentUtil.ComponentType.BUFF).on_buff_added:
                sim_info.get_component(TurboComponentUtil.ComponentType.BUFF).on_buff_added.append(callback)

        @staticmethod
        def unregister_for_buff_added_callback(sim_identifier, callback):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
            if not TurboSimUtil.Component.has_component(sim_info, TurboComponentUtil.ComponentType.BUFF):
                return
            if callback in sim_info.get_component(TurboComponentUtil.ComponentType.BUFF).on_buff_added:
                sim_info.get_component(TurboComponentUtil.ComponentType.BUFF).on_buff_added.remove(callback)

        @staticmethod
        def register_for_buff_removed_callback(sim_identifier, callback):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
            if not TurboSimUtil.Component.has_component(sim_info, TurboComponentUtil.ComponentType.BUFF):
                return
            if callback not in sim_info.get_component(TurboComponentUtil.ComponentType.BUFF).on_buff_removed:
                sim_info.get_component(TurboComponentUtil.ComponentType.BUFF).on_buff_removed.append(callback)

        @staticmethod
        def unregister_for_buff_removed_callback(sim_identifier, callback):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
            if not TurboSimUtil.Component.has_component(sim_info, TurboComponentUtil.ComponentType.BUFF):
                return
            if callback in sim_info.get_component(TurboComponentUtil.ComponentType.BUFF).on_buff_removed:
                sim_info.get_component(TurboComponentUtil.ComponentType.BUFF).on_buff_removed.remove(callback)

    class Whim:
        __qualname__ = 'TurboSimUtil.Whim'

        @staticmethod
        def has_whim_tracker(sim_identifier):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
            return sim_info.whim_tracker is not None

        @staticmethod
        def yield_whims(sim_identifier):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
            for whim_data in sim_info.whim_tracker.get_active_whim_data():
                while whim_data.whim is not None:
                    yield whim_data.whim

        @staticmethod
        def complete_whim(whim_instance, target_sim_identifier=None):
            target_sim_info = TurboManagerUtil.Sim.get_sim_info(target_sim_identifier)
            if target_sim_info is None:
                return False
            if isinstance(whim_instance, SituationGoalTargetedSim) and whim_instance.get_required_target_sim_info() is not None and whim_instance.get_required_target_sim_info() is not target_sim_info:
                return False
            whim_instance.force_complete(target_sim=target_sim_info)
            return True

    class Situation:
        __qualname__ = 'TurboSimUtil.Situation'

        @staticmethod
        def create_visit_situation(sim_identifier):
            sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
            if sim is None:
                return False
            services.get_zone_situation_manager().create_visit_situation(sim)
            return True

        @staticmethod
        def get_active_situations(sim_identifier):
            sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
            if sim is None:
                return False
            return services.get_zone_situation_manager().get_situations_sim_is_in(sim)

    class Mood:
        __qualname__ = 'TurboSimUtil.Mood'

        @staticmethod
        def get_mood(sim_identifier):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
            return sim_info.get_mood()

    class Interaction:
        __qualname__ = 'TurboSimUtil.Interaction'

        @staticmethod
        def get_queue_status(sim_identifier):
            sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
            if sim is None:
                return False
            if sim.queue is not None:
                return sim.queue.locked
            return False

        @staticmethod
        def lock_queue(sim_identifier):
            sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
            if sim is None:
                return False
            if sim.queue is not None:
                sim.queue.lock()
                return True
            return False

        @staticmethod
        def unlock_queue(sim_identifier):
            sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
            if sim is None:
                return False
            if sim.queue is not None:
                sim.queue.unlock()
                return True
            return False

        @staticmethod
        def is_running_interaction(sim_identifier, affordance_id):
            sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
            if sim is None:
                return False
            if sim.si_state is not None:
                for si in sim.si_state:
                    while hasattr(si, 'guid64') and si.guid64 == affordance_id:
                        return True
            return False

        @staticmethod
        def get_running_interactions_ids(sim_identifier):
            sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
            affordance_list = list()
            if sim is None:
                return affordance_list
            if sim.si_state is not None:
                for si in sim.si_state:
                    while hasattr(si, 'guid64'):
                        affordance_list.append(int(si.guid64))
            return affordance_list

        @staticmethod
        def get_running_interactions(sim_identifier):
            sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
            if sim.si_state is not None:
                return list(sim.si_state)
            return list()

        @staticmethod
        def cancel_running_interaction(sim_identifier, affordance_id, finishing_type=FinishingType.NATURAL):
            sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
            if sim is None:
                return False
            if sim.si_state is not None:
                for si in sim.si_state:
                    while hasattr(si, 'guid64') and si.guid64 == affordance_id:
                        si.cancel(finishing_type, 'TurboSimUtil.Interaction.cancel_running_interaction')

        @staticmethod
        def kill_running_interaction(sim_identifier, affordance_id):
            sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
            if sim is None:
                return False
            if sim.si_state is not None:
                for si in list(sim.si_state):
                    while hasattr(si, 'guid64') and si.guid64 == affordance_id:
                        si.kill()
            return True

        @staticmethod
        def has_queued_interaction(sim_identifier, affordance_id):
            sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
            if sim is None:
                return False
            if sim.queue is not None:
                for si in sim.queue:
                    while hasattr(si, 'guid64') and si.guid64 == affordance_id:
                        return True
            return False

        @staticmethod
        def get_queued_interactions_ids(sim_identifier):
            sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
            affordance_list = list()
            if sim is None:
                return affordance_list
            if sim.queue is not None:
                for si in sim.queue:
                    while hasattr(si, 'guid64'):
                        affordance_list.append(int(si.guid64))
            return affordance_list

        @staticmethod
        def get_queued_interactions(sim_identifier):
            sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
            if sim.queue is not None:
                return list(sim.queue)
            return list()

        @staticmethod
        def cancel_queued_interaction(sim_identifier, affordance_id, finishing_type=FinishingType.NATURAL):
            sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
            if sim is None:
                return False
            if sim.queue is not None:
                queue_lock_status = TurboSimUtil.Interaction.get_queue_status(sim)
                for si in sim.queue:
                    while hasattr(si, 'guid64') and si.guid64 == affordance_id:
                        si.cancel(finishing_type, 'TurboSimUtil.Interaction.cancel_queued_interaction')
                if queue_lock_status is False:
                    TurboSimUtil.Interaction.unlock_queue(sim)
                else:
                    TurboSimUtil.Interaction.lock_queue(sim)
                return True
            return False

        @staticmethod
        def kill_queued_interaction(sim_identifier, affordance_id):
            sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
            if sim is None:
                return False
            if sim.queue is not None:
                for si in list(sim.queue):
                    while hasattr(si, 'guid64') and si.guid64 == affordance_id:
                        si.kill()
            return False

        @staticmethod
        def push_affordance(sim_identifier, affordance_id, social_super_affordance_id=None, target=None, interaction_context=InteractionContext.SOURCE_SCRIPT_WITH_USER_INTENT, priority=Priority.High, run_priority=Priority.High, insert_strategy=QueueInsertStrategy.NEXT, must_run_next=False, skip_if_running=False):
            sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
            if sim is None or (sim.si_state is None or (sim.queue is None or sim.posture_state is None)) or sim.posture is None:
                return
            affordance_instance = TurboResourceUtil.Services.get_instance(TurboResourceUtil.ResourceTypes.INTERACTION, affordance_id)
            if affordance_instance is None:
                return
            if skip_if_running:
                for si in sim.si_state:
                    while si.super_affordance == affordance_instance:
                        return
                for si in sim.queue:
                    while si.super_affordance == affordance_instance:
                        return
            if affordance_instance.is_super:
                return TurboSimUtil.Interaction.push_super_affordance(sim, affordance_instance, target=target, interaction_context=interaction_context, priority=priority, run_priority=run_priority, insert_strategy=insert_strategy, must_run_next=must_run_next)
            if affordance_instance.is_social:
                return TurboSimUtil.Interaction.push_social_affordance(sim, social_super_affordance_id, affordance_id, target=target, interaction_context=interaction_context, priority=priority, run_priority=run_priority, insert_strategy=insert_strategy, must_run_next=must_run_next)
            return TurboSimUtil.Interaction.push_mixer_affordance(sim, affordance_id, target=target, interaction_context=interaction_context, priority=priority, run_priority=run_priority, insert_strategy=insert_strategy, must_run_next=must_run_next)

        @staticmethod
        def push_super_affordance(sim_identifier, affordance, target=None, interaction_context=InteractionContext.SOURCE_SCRIPT_WITH_USER_INTENT, priority=Priority.High, run_priority=Priority.High, insert_strategy=QueueInsertStrategy.NEXT, must_run_next=False):
            sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
            affordance_instance = affordance if not isinstance(affordance, int) else TurboResourceUtil.Services.get_instance(TurboResourceUtil.ResourceTypes.INTERACTION, affordance)
            if affordance_instance is None:
                return
            context = InteractionContext(sim, interaction_context, priority, run_priority=run_priority, insert_strategy=insert_strategy, must_run_next=must_run_next)
            result = sim.push_super_affordance(affordance_instance, target, context, picked_object=target)
            return result

        @staticmethod
        def push_social_affordance(sim_identifier, social_super_affordance, mixer_affordance, target=None, interaction_context=InteractionContext.SOURCE_SCRIPT_WITH_USER_INTENT, priority=Priority.High, run_priority=Priority.High, insert_strategy=QueueInsertStrategy.NEXT, must_run_next=False):
            if social_super_affordance is not None and mixer_affordance is None:
                return TurboSimUtil.Interaction.push_super_affordance(sim_identifier, social_super_affordance, target=target, interaction_context=interaction_context, priority=priority, run_priority=run_priority, insert_strategy=insert_strategy, must_run_next=must_run_next)
            sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
            super_affordance_instance = social_super_affordance if not isinstance(social_super_affordance, int) else TurboResourceUtil.Services.get_instance(TurboResourceUtil.ResourceTypes.INTERACTION, social_super_affordance)
            if super_affordance_instance is None:
                return
            mixer_affordance_instance = mixer_affordance if not isinstance(mixer_affordance, int) else TurboResourceUtil.Services.get_instance(TurboResourceUtil.ResourceTypes.INTERACTION, mixer_affordance)
            if mixer_affordance_instance is None:
                return

            def _get_existing_ssi(si_iter):
                for si in si_iter:
                    while si.super_affordance == super_affordance_instance:
                        target_sim = TurboManagerUtil.Sim.get_sim_instance(target)
                        if si.social_group is None:
                            pass
                        if target_sim is not None and target_sim not in si.social_group:
                            pass
                        return si.super_interaction

            super_interaction = _get_existing_ssi(sim.si_state) or _get_existing_ssi(sim.queue)
            if super_interaction is None:
                si_context = InteractionContext(sim, interaction_context, priority, run_priority=run_priority, insert_strategy=insert_strategy, must_run_next=must_run_next)
                si_result = sim.push_super_affordance(super_affordance_instance, target, si_context, picked_object=target)
                if not si_result:
                    return
                super_interaction = si_result.interaction
            pick = super_interaction.context.pick
            preferred_objects = super_interaction.context.preferred_objects
            context = super_interaction.context.clone_for_continuation(super_interaction, insert_strategy=insert_strategy, source_interaction_id=super_interaction.id, source_interaction_sim_id=TurboManagerUtil.Sim.get_sim_id(sim), pick=pick, preferred_objects=preferred_objects, must_run_next=must_run_next)
            aop = AffordanceObjectPair(mixer_affordance_instance, target, super_affordance_instance, super_interaction, picked_object=target, push_super_on_prepare=True)
            return aop.test_and_execute(context)

        @staticmethod
        def push_mixer_affordance(sim_identifier, affordance, target=None, interaction_context=InteractionContext.SOURCE_SCRIPT_WITH_USER_INTENT, priority=Priority.High, run_priority=Priority.High, insert_strategy=QueueInsertStrategy.NEXT, must_run_next=False):
            sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
            affordance_instance = affordance if not isinstance(affordance, int) else TurboResourceUtil.Services.get_instance(TurboResourceUtil.ResourceTypes.INTERACTION, affordance)
            if affordance_instance is None:
                return
            source_interaction = sim.posture.source_interaction
            if source_interaction is None:
                return
            sim_specific_lockout = affordance_instance.lock_out_time.target_based_lock_out if affordance_instance.lock_out_time else False
            if sim_specific_lockout and sim.is_sub_action_locked_out(affordance_instance):
                return
            super_affordance_instance = source_interaction.super_affordance
            context = InteractionContext(sim, interaction_context, priority, run_priority=run_priority, insert_strategy=insert_strategy, must_run_next=must_run_next)
            for (aop, test_result) in get_valid_aops_gen(target, affordance_instance, super_affordance_instance, source_interaction, context, False, push_super_on_prepare=False):
                interaction_constraint = aop.constraint_intersection(sim=sim, posture_state=None)
                posture_constraint = sim.posture_state.posture_constraint_strict
                constraint_intersection = interaction_constraint.intersect(posture_constraint)
                while constraint_intersection.valid:
                    return aop.execute(context)

    class Location:
        __qualname__ = 'TurboSimUtil.Location'

        @staticmethod
        def is_visible(sim_identifier):
            sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
            if sim.is_hidden() or sim.opacity == 0:
                return False
            return True

        @staticmethod
        def is_at_rabbit_hole(sim_identifier):
            sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
            if sim is None:
                return False
            return sim.has_hidden_flags(HiddenReasonFlag.RABBIT_HOLE)

        @staticmethod
        def get_head_position(sim_identifier):
            sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
            if TurboSimUtil.Age.get_age(sim) == TurboSimUtil.Age.TODDLER:
                sim_height = 0.885
            elif TurboSimUtil.Age.get_age(sim) == TurboSimUtil.Age.CHILD:
                sim_height = 1.285
            else:
                sim_height = 1.875
            return TurboMathUtil.Position.get_vector3(sim.position.x, sim.position.y + sim_height, sim.position.z)

        @staticmethod
        def get_position(sim_identifier):
            sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
            return sim.position

        @staticmethod
        def get_location(sim_identifier):
            sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
            return sim.location

        @staticmethod
        def get_level(sim_identifier):
            sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
            return sim.routing_surface.secondary_id

        @staticmethod
        def get_routing_surface(sim_identifier):
            sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
            return sim.routing_surface

    class Component:
        __qualname__ = 'TurboSimUtil.Component'

        @staticmethod
        def has_component(sim_or_sim_info, component_type):
            if component_type is None:
                return False
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_or_sim_info)
            if sim_info is not None and TurboComponentUtil.has_component(sim_info, component_type):
                return True
            sim_instance = TurboManagerUtil.Sim.get_sim_instance(sim_or_sim_info)
            if sim_instance is not None and TurboComponentUtil.has_component(sim_instance, component_type):
                return True
            return False

    class Autonomy:
        __qualname__ = 'TurboSimUtil.Autonomy'

        @staticmethod
        def is_in_full_autonomy(sim_identifier):
            sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
            if sim is None:
                return False
            return sim.get_component(TurboComponentUtil.ComponentType.AUTONOMY).get_autonomy_state_setting() == AutonomyState.FULL

        @staticmethod
        def get_time_until_next_update(sim_identifier):
            sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
            if sim is None:
                return -1
            return sim.get_component(TurboComponentUtil.ComponentType.AUTONOMY).get_time_until_next_update().in_ticks()

        @staticmethod
        def is_object_scoring_preferred(sim_identifier, object_preference_tag, game_object):
            sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
            if sim is None:
                return False
            return sim.is_object_scoring_preferred(object_preference_tag, game_object)

        @staticmethod
        def is_object_use_preferred(sim_identifier, object_preference_tag, game_object):
            sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
            if sim is None:
                return False
            return sim.is_object_use_preferred(object_preference_tag, game_object)

        @staticmethod
        def get_active_roles(sim_identifier):
            sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
            if sim is None:
                return ()
            return tuple(sim.get_component(TurboComponentUtil.ComponentType.AUTONOMY).active_roles())

        @staticmethod
        def add_rolestate(sim_identifier, rolestate_instance):
            sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
            if sim is None:
                return False
            return sim.get_component(TurboComponentUtil.ComponentType.AUTONOMY).add_role(rolestate_instance)

        @staticmethod
        def remove_rolestate(sim_identifier, rolestate_instance):
            sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
            if sim is None:
                return False
            return sim.get_component(TurboComponentUtil.ComponentType.AUTONOMY).remove_role_of_type(rolestate_instance)

    class Inventory:
        __qualname__ = 'TurboSimUtil.Inventory'

        @staticmethod
        def add_object(sim_identifier, game_object):
            sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
            if sim is None:
                return False
            if not TurboSimUtil.Component.has_component(sim, TurboComponentUtil.ComponentType.INVENTORY):
                return False
            return sim.get_component(TurboComponentUtil.ComponentType.INVENTORY).player_try_add_object(game_object)

        @staticmethod
        def remove_object_by_definition(sim_identifier, object_definition, amount=1):
            sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
            if sim is None:
                return False
            if not TurboSimUtil.Component.has_component(sim, TurboComponentUtil.ComponentType.INVENTORY):
                return False
            inventory_component = sim.get_component(TurboComponentUtil.ComponentType.INVENTORY)
            for inventory_object in inventory_component:
                while inventory_object.definition == object_definition:
                    if not inventory_component.try_remove_object_by_id(inventory_object.id, count=amount):
                        pass
                    else:
                        return True
            return False

        @staticmethod
        def remove_object_by_id(sim_identifier, object_id, amount=1):
            sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
            if sim is None:
                return False
            if not TurboSimUtil.Component.has_component(sim, TurboComponentUtil.ComponentType.INVENTORY):
                return False
            inventory_component = sim.get_component(TurboComponentUtil.ComponentType.INVENTORY)
            for inventory_object in inventory_component:
                while inventory_object.id == object_id:
                    return inventory_component.try_remove_object_by_id(inventory_object.id, count=amount)
            return False

        @staticmethod
        def count_objects(sim_identifier, object_definition):
            sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
            if sim is None:
                return 0
            if not TurboSimUtil.Component.has_component(sim, TurboComponentUtil.ComponentType.INVENTORY):
                return 0
            return sim.get_component(TurboComponentUtil.ComponentType.INVENTORY).get_count(object_definition)

    class Pregnancy:
        __qualname__ = 'TurboSimUtil.Pregnancy'

        @staticmethod
        def is_pregnant(sim_identifier):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
            pregnancy_tracker = sim_info.pregnancy_tracker
            if pregnancy_tracker is None:
                return False
            return pregnancy_tracker.is_pregnant

        @staticmethod
        def get_partner(sim_identifier):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
            pregnancy_tracker = sim_info.pregnancy_tracker
            if pregnancy_tracker is None:
                return
            return pregnancy_tracker.get_partner()

        @staticmethod
        def start_pregnancy(sim_identifier, partner_sim_identifier):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
            partner_sim_info = TurboManagerUtil.Sim.get_sim_info(partner_sim_identifier)
            pregnancy_tracker = sim_info.pregnancy_tracker
            if pregnancy_tracker is None:
                return False
            if sim_info.household.free_slot_count <= 0:
                return False
            pregnancy_tracker.start_pregnancy(sim_info, partner_sim_info)
            pregnancy_tracker.clear_pregnancy_visuals()
            pregnancy_commodity = TurboResourceUtil.Services.get_instance(TurboResourceUtil.ResourceTypes.STATISTIC, 16640)
            TurboSimUtil.Statistic.set_statistic_value(sim_info, pregnancy_commodity, 1)
            return True

        @staticmethod
        def clear_pregnancy(sim_identifier):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
            sim_info.pregnancy_tracker.clear_pregnancy()
            return True

    class CAS:
        __qualname__ = 'TurboSimUtil.CAS'

        @staticmethod
        def get_current_outfit(sim_identifier):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier, allow_base_wrapper=True)
            return sim_info.get_current_outfit()

        @staticmethod
        def get_previous_outfit(sim_identifier):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier, allow_base_wrapper=True)
            return sim_info.get_previous_outfit()

        @staticmethod
        def has_outfit(sim_identifier, outfit_category_and_index):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier, allow_base_wrapper=True)
            try:
                return sim_info.has_outfit(outfit_category_and_index)
            except:
                return False

        @staticmethod
        def set_current_outfit(sim_identifier, outfit_category_and_index, dirty=False):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier, allow_base_wrapper=True)
            if dirty is True:
                sim_info.set_outfit_dirty(outfit_category_and_index[0])
            sim_info.set_current_outfit(outfit_category_and_index)

        @staticmethod
        def set_outfit_category_dirty(sim_identifier, outfit_category, state):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier, allow_base_wrapper=True)
            if state:
                sim_info.set_outfit_dirty(outfit_category)
            else:
                sim_info.clear_outfit_dirty(outfit_category)

        @staticmethod
        def get_change_outfit_element(sim_identifier, outfit_category_and_index, do_spin=False, interaction=None, dirty_outfit=False):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier, allow_base_wrapper=True)
            if dirty_outfit is True:
                TurboSimUtil.CAS.set_outfit_category_dirty(sim_info, outfit_category_and_index[0], True)
            if interaction is not None and 'interaction' in inspect.getargspec(sim_info.get_change_outfit_element).args:
                return sim_info.get_change_outfit_element(outfit_category_and_index, do_spin=do_spin, interaction=interaction)
            return sim_info.get_change_outfit_element(outfit_category_and_index, do_spin=do_spin)

        @staticmethod
        def update_previous_outfit(sim_identifier):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier, allow_base_wrapper=True)
            sim_info.set_previous_outfit(None, force=True)

        @staticmethod
        def generate_outfit(sim_identifier, outfit_category_and_index):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier, allow_base_wrapper=True)
            sim_info.generate_outfit(outfit_category_and_index[0], outfit_category_and_index[1])

        @staticmethod
        def register_for_outfit_changed_callback(sim_identifier, callback):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier, allow_base_wrapper=True)
            sim_info.register_for_outfit_changed_callback(callback)

        @staticmethod
        def unregister_for_outfit_changed_callback(sim_identifier, callback):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier, allow_base_wrapper=True)
            sim_info.unregister_for_outfit_changed_callback(callback)

        @staticmethod
        def register_for_appearance_tracker_changed_callback(sim_identifier, callback):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier, allow_base_wrapper=True)
            if callback not in sim_info.appearance_tracker_changed:
                sim_info.appearance_tracker_changed.append(callback)

        @staticmethod
        def unregister_for_appearance_tracker_changed_callback(sim_identifier, callback):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier, allow_base_wrapper=True)
            if callback in sim_info.appearance_tracker_changed:
                sim_info.appearance_tracker_changed.remove(callback)

        @staticmethod
        def reset_appearance_modifiers_owner(sim_identifier):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier, allow_base_wrapper=True)
            sim_info.appearance_tracker.appearance_override_sim_info = None

        @staticmethod
        def evaluate_appearance_modifiers(sim_identifier):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier, allow_base_wrapper=True)
            sim_info.appearance_tracker.evaluate_appearance_modifiers()

        @staticmethod
        def get_outfit_data(sim_identifier, outfit_category_and_index):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier, allow_base_wrapper=True)
            return sim_info.get_outfit(outfit_category_and_index[0], outfit_category_and_index[1])

        @staticmethod
        def get_outfit_parts(sim_identifier, outfit_category_and_index):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier, allow_base_wrapper=True)
            outfit_data = TurboSimUtil.CAS.get_outfit_data(sim_info, outfit_category_and_index)
            if outfit_data is None:
                return dict()
            return TurboCASUtil.Special.pack_outfit(outfit_data.body_types, outfit_data.part_ids)

        @staticmethod
        def set_outfit_parts(sim_identifier, outfit_category_and_index, outfit_parts):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier, allow_base_wrapper=True)
            outfit_data = sim_info.get_outfit(outfit_category_and_index[0], outfit_category_and_index[1])
            if outfit_data is None:
                return
            outfit_body_types = list()
            outfit_part_ids = list()
            for (bodytype, cas_id) in outfit_parts.items():
                while not bodytype == -1:
                    if cas_id == -1:
                        pass
                    outfit_body_types.append(int(bodytype))
                    outfit_part_ids.append(int(cas_id))
            outfits_msg = sim_info.save_outfits()
            for outfit in outfits_msg.outfits:
                while int(outfit.category) == int(outfit_category_and_index[0]) and outfit.outfit_id == outfit_data.outfit_id:
                    outfit.parts = S4Common_pb2.IdList()
                    outfit.parts.ids.extend(outfit_part_ids)
                    outfit.body_types_list = Outfits_pb2.BodyTypesList()
                    outfit.body_types_list.body_types.extend(outfit_body_types)
            sim_info._base.outfits = outfits_msg.SerializeToString()
            sim_info.resend_outfits()

        @staticmethod
        def resend_outfit_data(sim_identifier):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier, allow_base_wrapper=True)
            sim_info.resend_outfits()

        @staticmethod
        def refresh_outfit(sim_identifier):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier, allow_base_wrapper=True)
            sim_info.on_outfit_changed(sim_info, sim_info.get_current_outfit())
            sim_info.resend_physical_attributes()
            sim_info.resend_outfits()
            sim_info.appearance_tracker.evaluate_appearance_modifiers()

        @staticmethod
        def get_outfit_tags(sim_identifier, outfit_category, outfit_index):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier, allow_base_wrapper=True)
            try:
                return get_tags_from_outfit(sim_info._base, outfit_category, outfit_index)
            except:
                return dict()

    class AppearanceAttributes:
        __qualname__ = 'TurboSimUtil.AppearanceAttributes'

        @staticmethod
        def set_appearance_attribute(sim_identifier, key, value, remove=False):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier, allow_base_wrapper=True)
            sim_appearance_attributes = PersistenceBlobs_pb2.BlobSimFacialCustomizationData()
            sim_appearance_attributes.ParseFromString(sim_info.facial_attributes)
            if remove is False:
                appearance_attribute_set = False
                for modifier in sim_appearance_attributes.body_modifiers:
                    while modifier.key == key:
                        modifier.amount = value
                        appearance_attribute_set = True
                new_modifier = sim_appearance_attributes.body_modifiers.add()
                new_modifier.key = key
                new_modifier.amount = value
            else:
                for modifier in sim_appearance_attributes.body_modifiers:
                    while modifier.key == key:
                        sim_appearance_attributes.body_modifiers.remove(modifier)
                        break
            sim_info.facial_attributes = sim_appearance_attributes.SerializeToString()
            sim_info.resend_physical_attributes()

    class Routing:
        __qualname__ = 'TurboSimUtil.Routing'

        @staticmethod
        def has_location_connectivity(sim_identifier, location, sim_route_location=None):
            sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
            if sim is None:
                return False
            if sim_route_location is not None:
                sim_route_location = routing.Location(TurboMathUtil.Location.get_location_translation(sim_route_location), TurboMathUtil.Location.get_location_orientation(sim_route_location), TurboMathUtil.Location.get_location_routing_surface(sim_route_location))
            else:
                sim_route_location = routing.Location(sim.transform.translation, TurboMathUtil.Orientation.get_quaternion_identity(), sim.routing_surface)
            target_route_location = routing.Location(TurboMathUtil.Location.get_location_translation(location), TurboMathUtil.Location.get_location_orientation(location), TurboMathUtil.Location.get_location_routing_surface(location))
            return bool(routing.test_connectivity_pt_pt(sim_route_location, target_route_location, sim.routing_context))

        @staticmethod
        def is_routable_position(sim_identifier, position):
            sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
            if sim is None:
                return False
            route_location = routing.Location(position, TurboMathUtil.Orientation.get_quaternion_identity(), sim.routing_surface)
            return bool(routing.test_connectivity_permissions_for_handle(routing.connectivity.Handle(route_location), sim.routing_context))

        @staticmethod
        def register_on_location_changed_callback(sim_identifier, callback):
            sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
            if not TurboSimUtil.Component.has_component(sim, TurboComponentUtil.ComponentType.ROUTING):
                return
            sim.register_on_location_changed(callback)

        @staticmethod
        def unregister_on_location_changed_callback(sim_identifier, callback):
            sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
            if not TurboSimUtil.Component.has_component(sim, TurboComponentUtil.ComponentType.ROUTING):
                return
            sim.unregister_on_location_changed(callback)

        @staticmethod
        def has_permission_for_door(sim_identifier, portal_object):
            sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
            if sim is None:
                return False
            return not bool(portal_object.test_lock(sim))

        @staticmethod
        def refresh_portals(sim_identifier):
            sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
            if sim is None:
                return False
            for portal_object in TurboObjectUtil.Portal.get_all_doors_gen():
                if TurboSimUtil.Routing.has_permission_for_door(sim, portal_object):
                    for portal_pair in portal_object.get_portal_pairs():
                        sim.routing_context.unlock_portal(portal_pair.there)
                        sim.routing_context.unlock_portal(portal_pair.back)
                else:
                    for portal_pair in portal_object.get_portal_pairs():
                        sim.routing_context.lock_portal(portal_pair.there)
                        sim.routing_context.lock_portal(portal_pair.back)
            return True

    class Spawner:
        __qualname__ = 'TurboSimUtil.Spawner'

        @staticmethod
        def is_leaving(sim_identifier):
            sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
            if sim is None:
                return False
            return services.sim_spawner_service().sim_is_leaving(sim)

