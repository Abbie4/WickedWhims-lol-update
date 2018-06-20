'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
import random
from enums.interactions_enum import SimInteraction
from enums.relationship_enum import SimRelationshipBit
from enums.situations_enum import SimSituation
from turbolib.interaction_util import TurboInteractionUtil
from turbolib.manager_util import TurboManagerUtil
from turbolib.math_util import TurboMathUtil
from turbolib.sim_util import TurboSimUtil
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.sex.cas_cum_handler import get_cum_layer_cas_id, CumLayerType
from wickedwhims.sex.settings.sex_settings import SexSetting, get_sex_setting
from wickedwhims.sxex_bridge.body import BodyState, get_sim_actual_body_state
from wickedwhims.sxex_bridge.nudity import update_nude_body_data
from wickedwhims.sxex_bridge.reactions import register_sim_reaction_function
from wickedwhims.sxex_bridge.sex import is_sim_in_sex, is_sim_going_to_sex
from wickedwhims.utils_cas import has_sim_cas_part_id
from wickedwhims.utils_relations import has_relationship_bit_with_sim
from wickedwhims.utils_sims import is_sim_available
from wickedwhims.utils_situations import has_sim_situations

@register_sim_reaction_function(priority=4)
def _reaction_to_sims_cum(sim):
    if not get_sex_setting(SexSetting.REACTION_TO_CUM_STATE, variable_type=bool):
        return False
    if TurboSimUtil.Age.is_younger_than(sim, TurboSimUtil.Age.TODDLER, or_equal=True):
        return False
    full_reaction_cooldown = sim_ev(sim).full_cum_reaction_cooldown
    inner_reaction_cooldown = sim_ev(sim).inner_cum_reaction_cooldown
    if full_reaction_cooldown > 0:
        pass
    if inner_reaction_cooldown > 0:
        pass
    if full_reaction_cooldown > 0 and inner_reaction_cooldown > 0:
        return False
    if is_sim_in_sex(sim) or is_sim_going_to_sex(sim):
        return False
    if not is_sim_available(sim):
        return False
    if has_sim_situations(sim, (SimSituation.GRIMREAPER, SimSituation.FIRE, SimSituation.BABYBIRTH_HOSPITAL)):
        return False
    if _has_sim_visible_cum(sim):
        return False
    line_of_sight = TurboMathUtil.LineOfSight.create(TurboSimUtil.Location.get_routing_surface(sim), TurboSimUtil.Location.get_position(sim), 2.5)
    targets = list()
    for target in TurboManagerUtil.Sim.get_all_sim_instance_gen(humans=True, pets=False):
        if sim is target:
            pass
        if TurboSimUtil.Age.is_younger_than(target, TurboSimUtil.Age.TEEN):
            pass
        if has_relationship_bit_with_sim(sim, target, SimRelationshipBit.WW_JUST_HAD_SEX):
            pass
        if not _has_sim_visible_cum(target):
            pass
        if not TurboSimUtil.Location.is_visible(target):
            pass
        if TurboSimUtil.Spawner.is_leaving(target):
            pass
        if not TurboMathUtil.LineOfSight.test(line_of_sight, TurboSimUtil.Location.get_position(target)):
            pass
        targets.append(target)
    if targets:
        is_mixer_only = _is_only_mixer_reaction(sim)
        target = random.choice(targets)
        if _cum_reaction(sim, target, only_mixer=is_mixer_only):
            return True
    return False


def _cum_reaction(sim, target, only_mixer=False):
    si_result = TurboSimUtil.Interaction.push_affordance(sim, SimInteraction.WW_SEX_CUM_REACTION, target=target, interaction_context=TurboInteractionUtil.InteractionContext.SOURCE_SCRIPT, insert_strategy=TurboInteractionUtil.QueueInsertStrategy.NEXT) if only_mixer is False else None
    if not si_result and (si_result is None or TurboInteractionUtil.can_interaction_fallback_to_mixer_interaction(sim, si_result.execute_result.interaction)):
        si_result = TurboSimUtil.Interaction.push_affordance(sim, SimInteraction.WW_SEX_CUM_REACTION_MIXER, target=target, interaction_context=TurboInteractionUtil.InteractionContext.SOURCE_REACTION, insert_strategy=TurboInteractionUtil.QueueInsertStrategy.NEXT)
    if si_result:
        cooldown_offset = random.randint(-1, 2)
        sim_ev(sim).full_cum_reaction_cooldown = 12 + cooldown_offset
        sim_ev(sim).inner_cum_reaction_cooldown = 6 + cooldown_offset
        return True
    return False


def _is_only_mixer_reaction(sim):
    is_ready_for_inner = sim_ev(sim).inner_cum_reaction_cooldown <= 0
    if is_ready_for_inner is True and has_sim_situations(sim, (SimSituation.BARISTA_VENUE, SimSituation.HIREDNPC_BARISTA, SimSituation.BARBARTENDER, SimSituation.BARTENDER_RESTAURANT, SimSituation.HIREDNPC_BARTENDER, SimSituation.HIREDNPC_CATERER, SimSituation.HIREDNPC_CATERER_VEGETARIAN, SimSituation.HIREDNPC_DJ, SimSituation.HIREDNPC_DJ_LEVEL10, SimSituation.SINGLEJOB_CLUB_DJ, SimSituation.SINGLEJOB_CLUB_DJ_LEVEL10, SimSituation.HIREDNPC_ENTERTAINER_GUITAR, SimSituation.HIREDNPC_ENTERTAINER_MICCOMEDY, SimSituation.HIREDNPC_ENTERTAINER_ORGAN, SimSituation.HIREDNPC_ENTERTAINER_PIANO, SimSituation.HIREDNPC_ENTERTAINER_VIOLIN, SimSituation.BUTLER_SITUATION, SimSituation.GYMTRAINER_VENUE, SimSituation.MAID_SITUATION, SimSituation.MAILMAN_SITUATION, SimSituation.PIZZADELIVERY_NEW, SimSituation.REPAIR_SITUATION, SimSituation.MASSAGETHERAPIST_VENUE, SimSituation.MASSAGETHERAPIST_SERVICECALL, SimSituation.CHEFSITUATION, SimSituation.HOST_1, SimSituation.RESTAURANT_WAITSTAFF, SimSituation.CAREER_DOCTOR_NPC_DOCTOR, SimSituation.CAREER_DOCTOR_NPC_ASSISTANT, SimSituation.CAREER_DOCTOR_NPC_DOCTOR_DIAGNOSER, SimSituation.CAREER_DOCTOR_NPC_NURSE, SimSituation.CAREER_DOCTOR_NPC_PATIENT_ADMITTED, SimSituation.DETECTIVE_APB, SimSituation.DETECTIVE_APBNEUTRAL, SimSituation.CAREER_DETECTIVE_APBPLAYER)):
        return True
    is_ready_for_full = sim_ev(sim).full_cum_reaction_cooldown <= 0
    if is_ready_for_full is False:
        return True
    return False


def _has_sim_visible_cum(sim):
    if has_sim_cas_part_id(sim, get_cum_layer_cas_id(CumLayerType.FACE)):
        return True
    update_nude_body_data(sim)
    if has_sim_cas_part_id(sim, get_cum_layer_cas_id(CumLayerType.CHEST)) or has_sim_cas_part_id(sim, get_cum_layer_cas_id(CumLayerType.BACK)):
        top_state = get_sim_actual_body_state(sim, 6)
        if top_state == BodyState.NUDE or top_state == BodyState.UNDERWEAR:
            return True
    if has_sim_cas_part_id(sim, get_cum_layer_cas_id(CumLayerType.BUTT)) or has_sim_cas_part_id(sim, get_cum_layer_cas_id(CumLayerType.VAGINA)):
        bottom_state = get_sim_actual_body_state(sim, 7)
        if bottom_state == BodyState.NUDE:
            return True
    return False

