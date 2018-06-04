'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
import random
from enums.buffs_enum import SimBuff
from enums.interactions_enum import SimInteraction
from enums.moods_enum import SimMood
from enums.relationship_enum import SimRelationshipBit, RelationshipTrackType
from enums.situations_enum import SimSituation
from enums.traits_enum import SimTrait
from turbolib.interaction_util import TurboInteractionUtil
from turbolib.manager_util import TurboManagerUtil
from turbolib.math_util import TurboMathUtil
from turbolib.sim_util import TurboSimUtil
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.nudity.nudity_settings import NuditySetting, get_nudity_setting
from wickedwhims.nudity.outfit_utils import get_sim_outfit_level, OutfitLevel
from wickedwhims.nudity.permissions.test import has_sim_permission_for_nudity
from wickedwhims.nudity.skill.active_nudity import update_sim_nudity_skill_on_seeing_nudity
from wickedwhims.relationships.relationship_utils import get_sim_preferenced_genders
from wickedwhims.sxex_bridge.penis import set_sim_penis_state
from wickedwhims.sxex_bridge.reactions import register_sim_reaction_function
from wickedwhims.sxex_bridge.relationships import is_true_family_relationship
from wickedwhims.sxex_bridge.sex import is_sim_in_sex, is_sim_going_to_sex
from wickedwhims.sxex_bridge.statistics import increase_sim_ww_statistic
from wickedwhims.utils_buffs import add_sim_buff
from wickedwhims.utils_relations import has_relationship_bit_with_sim, get_relationship_with_sim
from wickedwhims.utils_sims import is_sim_available, has_sim_mood
from wickedwhims.utils_situations import has_sim_situations
from wickedwhims.utils_traits import has_sim_trait

@register_sim_reaction_function(priority=3)
def react_to_sims_nudity(sim):
    if not get_nudity_setting(NuditySetting.REACTION_TO_NUDITY_STATE, variable_type=bool):
        return False
    if TurboSimUtil.Age.is_younger_than(sim, TurboSimUtil.Age.TODDLER, or_equal=True):
        return False
    full_reaction_cooldown = sim_ev(sim).full_nudity_reaction_cooldown
    inner_reaction_cooldown = sim_ev(sim).inner_nudity_reaction_cooldown
    if full_reaction_cooldown > 0:
        pass
    if inner_reaction_cooldown > 0:
        pass
    if full_reaction_cooldown > 0 and inner_reaction_cooldown > 0:
        return False
    if is_sim_in_sex(sim) or is_sim_going_to_sex(sim):
        return False
    if has_sim_situations(sim, (SimSituation.GRIMREAPER, SimSituation.FIRE, SimSituation.BABYBIRTH_HOSPITAL)):
        return False
    sim_outfit_level = get_sim_outfit_level(sim)
    if sim_outfit_level == OutfitLevel.NUDE or sim_outfit_level == OutfitLevel.BATHING:
        return False
    if not is_sim_available(sim):
        return False
    has_permission_to_nudity = None
    line_of_sight = TurboMathUtil.LineOfSight.create(TurboSimUtil.Location.get_routing_surface(sim), TurboSimUtil.Location.get_position(sim), 8.0)
    targets = list()
    for target in TurboManagerUtil.Sim.get_all_sim_instance_gen(humans=True, pets=False):
        if sim is target:
            pass
        if has_relationship_bit_with_sim(sim, target, SimRelationshipBit.WW_JUST_HAD_SEX):
            pass
        if TurboSimUtil.Age.is_younger_than(target, TurboSimUtil.Age.TEEN):
            pass
        if is_sim_in_sex(target):
            pass
        if not TurboSimUtil.Location.is_visible(target):
            pass
        if TurboSimUtil.Spawner.is_leaving(target):
            pass
        target_outfit_level = get_sim_outfit_level(target)
        if target_outfit_level != OutfitLevel.NUDE and target_outfit_level != OutfitLevel.BATHING:
            pass
        if not TurboMathUtil.LineOfSight.test(line_of_sight, TurboSimUtil.Location.get_position(target)):
            pass
        if target_outfit_level == OutfitLevel.BATHING:
            extra_skill_level = 1
        else:
            extra_skill_level = 0
        update_sim_nudity_skill_on_seeing_nudity(sim, target)
        if has_permission_to_nudity is None:
            has_permission_to_nudity = has_sim_permission_for_nudity(sim, extra_skill_level=extra_skill_level)[0]
        if has_permission_to_nudity is True:
            pass
        targets.append(target)
    if targets:
        is_mixer_only = _is_only_mixer_reaction(sim)
        target = random.choice(targets)
        if _nudity_reaction(sim, target, only_mixer=is_mixer_only):
            return True
    return False

def force_nudity_reaction(sim, target):
    sim_ev(sim).full_nudity_reaction_cooldown = 0
    sim_ev(sim).inner_nudity_reaction_cooldown = 0
    _nudity_reaction(sim, target, force=True)

def _nudity_reaction(sim, target, only_mixer=False, force=False):
    increase_sim_ww_statistic(sim, 'times_reacted_to_nudity')
    increase_sim_ww_statistic(target, 'times_been_seen_nude')
    if _is_positive_to_sim_nudity(sim, target):
        positive_reaction_affordance = random.choice((SimInteraction.WW_NUDITY_REACTION_POSITIVE_1, SimInteraction.WW_NUDITY_REACTION_POSITIVE_2, SimInteraction.WW_NUDITY_REACTION_POSITIVE_3))
        si_result = TurboSimUtil.Interaction.push_affordance(sim, positive_reaction_affordance, target=target, interaction_context=TurboInteractionUtil.InteractionContext.SOURCE_SCRIPT, insert_strategy=TurboInteractionUtil.QueueInsertStrategy.NEXT if force is False else TurboInteractionUtil.QueueInsertStrategy.FIRST, priority=TurboInteractionUtil.Priority.High if force is False else TurboInteractionUtil.Priority.Critical, run_priority=TurboInteractionUtil.Priority.High if force is False else TurboInteractionUtil.Priority.Critical) if only_mixer is False else None
    else:
        si_result = TurboSimUtil.Interaction.push_affordance(sim, SimInteraction.WW_NUDITY_REACTION_SHOCK, target=target, interaction_context=TurboInteractionUtil.InteractionContext.SOURCE_SCRIPT, insert_strategy=TurboInteractionUtil.QueueInsertStrategy.NEXT if force is False else TurboInteractionUtil.QueueInsertStrategy.FIRST, priority=TurboInteractionUtil.Priority.High if force is False else TurboInteractionUtil.Priority.Critical, run_priority=TurboInteractionUtil.Priority.High if force is False else TurboInteractionUtil.Priority.Critical) if only_mixer is False else None
    if not si_result and (si_result is None or TurboInteractionUtil.can_interaction_fallback_to_mixer_interaction(sim, si_result.execute_result.interaction)):
        si_result = TurboSimUtil.Interaction.push_affordance(sim, SimInteraction.WW_NUDITY_REACTION_MIXER, target=target, interaction_context=TurboInteractionUtil.InteractionContext.SOURCE_REACTION, insert_strategy=TurboInteractionUtil.QueueInsertStrategy.NEXT)
    if si_result:
        if TurboSimUtil.Age.get_age(sim) == TurboSimUtil.Age.CHILD:
            add_sim_buff(sim, SimBuff.PRIVACY_EMBARRASSED)
        cooldown_offset = random.randint(-1, 2)
        sim_ev(sim).full_nudity_reaction_cooldown = 12 + cooldown_offset
        sim_ev(sim).inner_nudity_reaction_cooldown = 6 + cooldown_offset
        set_sim_penis_state(sim, True, 8, set_if_nude=True)
        return True
    return False

def _is_only_mixer_reaction(sim):
    is_ready_for_inner = sim_ev(sim).inner_nudity_reaction_cooldown <= 0
    if is_ready_for_inner is True and has_sim_situations(sim, (SimSituation.BARISTA_VENUE, SimSituation.HIREDNPC_BARISTA, SimSituation.BARBARTENDER, SimSituation.BARTENDER_RESTAURANT, SimSituation.HIREDNPC_BARTENDER, SimSituation.HIREDNPC_CATERER, SimSituation.HIREDNPC_CATERER_VEGETARIAN, SimSituation.HIREDNPC_DJ, SimSituation.HIREDNPC_DJ_LEVEL10, SimSituation.SINGLEJOB_CLUB_DJ, SimSituation.SINGLEJOB_CLUB_DJ_LEVEL10, SimSituation.HIREDNPC_ENTERTAINER_GUITAR, SimSituation.HIREDNPC_ENTERTAINER_MICCOMEDY, SimSituation.HIREDNPC_ENTERTAINER_ORGAN, SimSituation.HIREDNPC_ENTERTAINER_PIANO, SimSituation.HIREDNPC_ENTERTAINER_VIOLIN, SimSituation.BUTLER_SITUATION, SimSituation.GYMTRAINER_VENUE, SimSituation.MAID_SITUATION, SimSituation.MAILMAN_SITUATION, SimSituation.PIZZADELIVERY_NEW, SimSituation.REPAIR_SITUATION, SimSituation.MASSAGETHERAPIST_VENUE, SimSituation.MASSAGETHERAPIST_SERVICECALL, SimSituation.CHEFSITUATION, SimSituation.HOST_1, SimSituation.RESTAURANT_WAITSTAFF, SimSituation.CAREER_DOCTOR_NPC_DOCTOR, SimSituation.CAREER_DOCTOR_NPC_ASSISTANT, SimSituation.CAREER_DOCTOR_NPC_DOCTOR_DIAGNOSER, SimSituation.CAREER_DOCTOR_NPC_NURSE, SimSituation.CAREER_DOCTOR_NPC_PATIENT_ADMITTED, SimSituation.DETECTIVE_APB, SimSituation.DETECTIVE_APBNEUTRAL, SimSituation.CAREER_DETECTIVE_APBPLAYER)):
        return True
    is_ready_for_full = sim_ev(sim).full_nudity_reaction_cooldown <= 0
    if is_ready_for_full is False:
        return True
    return False

def _is_positive_to_sim_nudity(sim, target):
    if TurboSimUtil.Age.is_younger_than(sim, TurboSimUtil.Age.CHILD, or_equal=True):
        return False
    if has_relationship_bit_with_sim(sim, target, SimRelationshipBit.ROMANTIC_HAVEDONEWOOHOO):
        return True
    if has_relationship_bit_with_sim(sim, target, SimRelationshipBit.ROMANTIC_ENGAGED) or has_relationship_bit_with_sim(sim, target, SimRelationshipBit.ROMANTIC_MARRIED) or has_relationship_bit_with_sim(sim, target, SimRelationshipBit.ROMANTIC_SIGNIFICANT_OTHER):
        return True
    if has_relationship_bit_with_sim(sim, target, SimRelationshipBit.FRIENDSHIP_BFF) or has_relationship_bit_with_sim(sim, target, SimRelationshipBit.FRIENDSHIP_BFF_EVIL) or has_relationship_bit_with_sim(sim, target, SimRelationshipBit.FRIENDSHIP_BFF_BROMANTICPARTNER):
        return True
    if is_true_family_relationship(sim, target):
        return False
    if get_relationship_with_sim(sim, target, RelationshipTrackType.FRIENDSHIP) >= 60 or get_relationship_with_sim(sim, target, RelationshipTrackType.FRIENDSHIP) >= 50:
        return True
    if has_sim_trait(sim, SimTrait.UNFLIRTY):
        return False
    if TurboSimUtil.Gender.get_gender(target) not in get_sim_preferenced_genders(sim):
        chance = 0.15
        if TurboSimUtil.Age.get_age(sim) == TurboSimUtil.Age.TEEN:
            chance += 0.05
        if has_sim_mood(sim, SimMood.FLIRTY):
            chance += 0.05
        if has_sim_trait(sim, SimTrait.BRO) and has_sim_trait(target, SimTrait.BRO):
            chance += 0.05
        if has_sim_trait(sim, SimTrait.LONER):
            chance += 0.025
        return chance >= 1.0 or random.Random(TurboManagerUtil.Sim.get_sim_id(sim)).uniform(0, 1) <= chance
    return False

