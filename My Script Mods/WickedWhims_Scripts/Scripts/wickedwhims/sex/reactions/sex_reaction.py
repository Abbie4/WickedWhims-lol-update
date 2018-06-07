from enums.buffs_enum import SimBuff
from enums.interactions_enum import SimInteraction
from enums.moods_enum import SimMood
from enums.relationship_enum import RelationshipTrackType, SimRelationshipBit
from enums.situations_enum import SimSituation
from enums.traits_enum import SimTrait
from turbolib.interaction_util import TurboInteractionUtil
from turbolib.manager_util import TurboManagerUtil
from turbolib.math_util import TurboMathUtil
from turbolib.native.enum import TurboEnum
from turbolib.sim_util import TurboSimUtil
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.relationships.relationship_settings import get_relationship_setting, RelationshipSetting
from wickedwhims.sex.enums.sex_type import SexCategoryType
from wickedwhims.sex.settings.sex_settings import SexSetting, get_sex_setting
from wickedwhims.sex.sex_operators.active_sex_handlers_operator import get_active_sex_handlers
from wickedwhims.sxex_bridge.body import BodyState, get_sim_actual_body_state
from wickedwhims.sxex_bridge.reactions import register_sim_reaction_function
from wickedwhims.sxex_bridge.relationships import is_true_family_relationship
from wickedwhims.sxex_bridge.sex import is_sim_going_to_sex, is_sim_in_sex
from wickedwhims.sxex_bridge.statistics import increase_sim_ww_statistic
from wickedwhims.utils_buffs import add_sim_buff, has_sim_buff
from wickedwhims.utils_relations import get_relationship_with_sim, has_relationship_bit_with_sim, change_relationship_with_sim
from wickedwhims.utils_sims import has_sim_mood, is_sim_available
from wickedwhims.utils_situations import has_sim_situations
from wickedwhims.utils_traits import has_sim_trait
JEALOUSY_WOOHOO_REACTION_LIST = (76431, 76433, 76581, 76564, 76566, 76430)


class SexReactionType(TurboEnum):
    __qualname__ = 'SexReactionType'
    NEUTARL = 0
    FRIENDLY = 1
    EXCITED = 2
    FUNNY = 3
    FLIRTY = 4
    SAD = 5
    ANGRY = 6
    CUCK = 7
    HORRIFIED = 8
    JEALOUS = 9

SEX_REACTION_NEUTARL = (SexReactionType.NEUTARL, SimInteraction.WW_SEX_REACTION_NEUTRAL, SimBuff.WW_SEX_REACTION_NEUTRAL)
SEX_REACTION_FRIENDLY = (SexReactionType.FRIENDLY, SimInteraction.WW_SEX_REACTION_FRIENDLY, None)
SEX_REACTION_EXCITED = (SexReactionType.EXCITED, SimInteraction.WW_SEX_REACTION_EXCITED, SimBuff.WW_SEX_REACTION_EXCITED)
SEX_REACTION_FUNNY = (SexReactionType.FUNNY, SimInteraction.WW_SEX_REACTION_FUNNY, SimBuff.WW_SEX_REACTION_FUNNY)
SEX_REACTION_FLIRTY_MALE = (SexReactionType.FLIRTY, SimInteraction.WW_SEX_REACTION_FLIRTY_MALE, SimBuff.WW_SEX_REACTION_FLIRTY)
SEX_REACTION_FLIRTY_FEMALE = (SexReactionType.FLIRTY, SimInteraction.WW_SEX_REACTION_FLIRTY_FEMALE, SimBuff.WW_SEX_REACTION_FLIRTY)
SEX_REACTION_SAD = (SexReactionType.SAD, SimInteraction.WW_SEX_REACTION_SAD, SimBuff.WW_SEX_REACTION_SAD)
SEX_REACTION_ANGRY = (SexReactionType.ANGRY, SimInteraction.WW_SEX_REACTION_ANGRY, SimBuff.WW_SEX_REACTION_ANGRY)
SEX_REACTION_CUCK_MALE = (SexReactionType.CUCK, SimInteraction.WW_SEX_REACTION_FLIRTY_MALE, SimBuff.WW_SEX_REACTION_CUCK)
SEX_REACTION_CUCK_FEMALE = (SexReactionType.CUCK, SimInteraction.WW_SEX_REACTION_FLIRTY_FEMALE, SimBuff.WW_SEX_REACTION_CUCK)
SEX_REACTION_HORRIFIED = (SexReactionType.HORRIFIED, SimInteraction.WW_SEX_REACTION_HORRIFIED, SimBuff.WW_SEX_REACTION_HORRIFIED)
SEX_REACTION_JEALOUS = (SexReactionType.JEALOUS, None, None)

@register_sim_reaction_function(priority=1)
def _react_to_sims_sex(sim):
    if not get_sex_setting(SexSetting.REACTION_TO_SEX_STATE, variable_type=bool):
        return False
    if TurboSimUtil.Age.is_younger_than(sim, TurboSimUtil.Age.BABY, or_equal=True):
        return False
    registered_sex_handlers = get_active_sex_handlers()
    if not registered_sex_handlers:
        return False
    try_to_react = True
    if sim_ev(sim).sex_reaction_attempt_cooldown > 0:
        try_to_react = False
    if sim_ev(sim).sex_reaction_cooldown > 0:
        try_to_react = False
    if try_to_react is False:
        return False
    if is_sim_in_sex(sim) or is_sim_going_to_sex(sim):
        return False
    if has_sim_situations(sim, (SimSituation.GRIMREAPER, SimSituation.FIRE, SimSituation.BABYBIRTH_HOSPITAL)):
        return False
    if not is_sim_available(sim):
        return False
    for interaction_id in TurboSimUtil.Interaction.get_running_interactions_ids(sim):
        while interaction_id == SimInteraction.WW_STOP_SEX:
            return True
    line_of_sight = TurboMathUtil.LineOfSight.create(TurboSimUtil.Location.get_routing_surface(sim), TurboSimUtil.Location.get_position(sim), 8.0)
    for sex_handler in registered_sex_handlers:
        if not sex_handler.is_playing is False:
            if sex_handler.is_ready_to_unregister is True:
                pass
            if sex_handler.get_identifier() in sim_ev(sim).sex_reaction_handlers_list:
                pass
            if sex_handler.get_creator_sim_id() == TurboManagerUtil.Sim.get_sim_id(sim):
                pass
            sex_interaction_los_position = sex_handler.get_los_position()
            if not TurboMathUtil.LineOfSight.test(line_of_sight, sex_interaction_los_position):
                pass
            sim_ev(sim).sex_reaction_attempt_cooldown = 2
            if _jealousy_from_sex_reaction(sim, sex_handler):
                return True
            if _general_sex_reaction(sim, sex_handler):
                return True
            return False


def _general_sex_reaction(sim, sex_handler):
    skip_reaction = False
    if sex_handler.get_actors_amount() == 1 and sex_handler.get_animation_instance().get_sex_category() == SexCategoryType.TEASING:
        target = next(iter(sex_handler.get_actors_sim_instance_gen()))
        if target is not None:
            skip_reaction = True
            if TurboSimUtil.Gender.is_female(target) and get_sim_actual_body_state(target, 6) == BodyState.NUDE or get_sim_actual_body_state(target, 7) == BodyState.NUDE:
                skip_reaction = False
    if skip_reaction is True:
        return False
    sex_creator_sim = TurboManagerUtil.Sim.get_sim_instance(sex_handler.get_creator_sim_id())
    if sex_creator_sim is None:
        return False
    (sex_reaction_data, sex_reaction_should_left, sex_reaction_target_override) = get_reaction_type(sim, sex_handler)
    if not get_sex_setting(SexSetting.PRIVACY_STATE, variable_type=bool):
        sex_reaction_should_left = False
    sim_id = TurboManagerUtil.Sim.get_sim_id(sim)
    if sex_reaction_should_left is True:
        if sim_id in sex_handler.go_away_sims_list:
            go_away_reaction_result = TurboSimUtil.Interaction.push_affordance(sim, SimInteraction.WW_GO_AWAY_FROM_SEX, target=sex_creator_sim, interaction_context=TurboInteractionUtil.InteractionContext.SOURCE_SCRIPT, insert_strategy=TurboInteractionUtil.QueueInsertStrategy.NEXT, must_run_next=True, priority=TurboInteractionUtil.Priority.High, run_priority=TurboInteractionUtil.Priority.High)
            return bool(go_away_reaction_result)
        sex_handler.go_away_sims_list.add(sim_id)
    else:
        sim_ev(sim).sex_reaction_handlers_list.append(sex_handler.get_identifier())
    if sim_id in sex_handler.has_reacted_sims_list:
        reaction_result = TurboSimUtil.Interaction.push_affordance(sim, sex_reaction_data[1], target=sex_reaction_target_override if sex_reaction_target_override is not None else sex_creator_sim, insert_strategy=TurboInteractionUtil.QueueInsertStrategy.NEXT, priority=TurboInteractionUtil.Priority.High, run_priority=TurboInteractionUtil.Priority.High, skip_if_running=True)
    else:
        reaction_result = TurboSimUtil.Interaction.push_affordance(sim, sex_reaction_data[1], target=sex_reaction_target_override if sex_reaction_target_override is not None else sex_creator_sim, insert_strategy=TurboInteractionUtil.QueueInsertStrategy.FIRST, must_run_next=True, priority=TurboInteractionUtil.Priority.Critical, run_priority=TurboInteractionUtil.Priority.Critical, skip_if_running=True)
    if reaction_result:
        increase_sim_ww_statistic(sim, 'times_reacted_to_sex')
        increase_sim_ww_statistic(sex_creator_sim, 'times_been_seen_in_sex')
        if sex_reaction_data[2] is not None:
            add_sim_buff(sim, sex_reaction_data[2])
        if sex_reaction_should_left is True:
            sim_ev(sim).sex_reaction_attempt_cooldown = 0
        sex_handler.has_reacted_sims_list.add(sim_id)
        return True
    return False


def get_reaction_type(sim, sex_handler, allow_special_types=False):
    sex_reaction_data = SEX_REACTION_NEUTARL
    sex_reaction_should_left = True
    sex_reaction_target_override = None
    for target in sex_handler.get_actors_sim_instance_gen():
        if target is None:
            pass
        if allow_special_types is True and (SEX_REACTION_JEALOUS[0] > sex_reaction_data[0] and (get_relationship_setting(RelationshipSetting.JEALOUSY_STATE, variable_type=bool) and (sex_handler.get_actors_amount() > 1 and not has_sim_trait(sim, SimTrait.WW_POLYAMOROUS)))) and not has_sim_trait(sim, SimTrait.WW_CUCKOLD):
            (found_lovers, found_non_lovers) = _get_jealousy_sims_from_sex_handler(sim, sex_handler)
            if found_lovers and found_non_lovers:
                sex_reaction_data = SEX_REACTION_JEALOUS
                sex_reaction_should_left = True
        if SEX_REACTION_HORRIFIED[0] > sex_reaction_data[0] and (TurboSimUtil.Age.is_younger_than(sim, TurboSimUtil.Age.TEEN) or is_true_family_relationship(sim, target)):
            sex_reaction_data = SEX_REACTION_HORRIFIED
            sex_reaction_should_left = True
        if SEX_REACTION_CUCK_MALE[0] > sex_reaction_data[0] and has_sim_trait(sim, SimTrait.WW_CUCKOLD):
            (found_lovers, found_non_lovers) = _get_jealousy_sims_from_sex_handler(sim, sex_handler)
            if found_lovers and found_non_lovers:
                if TurboSimUtil.Gender.is_male(sim):
                    sex_reaction_data = SEX_REACTION_CUCK_MALE
                else:
                    sex_reaction_data = SEX_REACTION_CUCK_FEMALE
                sex_reaction_should_left = False
                sex_reaction_target_override = found_lovers[0]
        if SEX_REACTION_ANGRY[0] > sex_reaction_data[0] and (get_relationship_with_sim(sim, target, RelationshipTrackType.FRIENDSHIP) <= -15 or has_sim_mood(sim, SimMood.STRESSED)):
            sex_reaction_data = SEX_REACTION_ANGRY
            sex_reaction_should_left = True
        if SEX_REACTION_SAD[0] > sex_reaction_data[0] and has_relationship_bit_with_sim(sim, target, SimRelationshipBit.ROMANTIC_BROKEN_UP) and has_relationship_bit_with_sim(sim, target, SimRelationshipBit.ROMANTIC_HAVEDONEWOOHOO):
            sex_reaction_data = SEX_REACTION_SAD
            sex_reaction_should_left = True
        if SEX_REACTION_FLIRTY_MALE[0] > sex_reaction_data[0] and (has_sim_mood(sim, SimMood.FLIRTY) or get_relationship_with_sim(sim, target, RelationshipTrackType.ROMANCE) >= 40):
            if TurboSimUtil.Gender.is_male(sim):
                sex_reaction_data = SEX_REACTION_FLIRTY_MALE
            else:
                sex_reaction_data = SEX_REACTION_FLIRTY_FEMALE
            sex_reaction_should_left = False
        if SEX_REACTION_FUNNY[0] > sex_reaction_data[0] and (has_sim_trait(sim, SimTrait.CHILDISH) or has_sim_trait(sim, SimTrait.GOOFBALL)):
            sex_reaction_data = SEX_REACTION_FUNNY
            sex_reaction_should_left = True
        if SEX_REACTION_EXCITED[0] > sex_reaction_data[0] and (has_sim_mood(sim, SimMood.ENERGIZED) or has_sim_mood(sim, SimMood.CONFIDENT) or has_sim_trait(sim, SimTrait.BRO) and has_sim_trait(target, SimTrait.BRO)):
            sex_reaction_data = SEX_REACTION_EXCITED
            sex_reaction_should_left = False
        if SEX_REACTION_FRIENDLY[0] > sex_reaction_data[0] and get_relationship_with_sim(sim, target, RelationshipTrackType.FRIENDSHIP) > 40:
            sex_reaction_data = SEX_REACTION_FRIENDLY
            sex_reaction_should_left = True
        while sex_reaction_data == SEX_REACTION_NEUTARL:
            if has_relationship_bit_with_sim(sim, target, SimRelationshipBit.ROMANTICCOMBO_SOULMATES) or (has_relationship_bit_with_sim(sim, target, SimRelationshipBit.ROMANTICCOMBO_SWEETHEARTS) or (has_relationship_bit_with_sim(sim, target, SimRelationshipBit.ROMANTICCOMBO_ROMANTICINTEREST) or (has_relationship_bit_with_sim(sim, target, SimRelationshipBit.ROMANTIC_SIGNIFICANT_OTHER) or (has_relationship_bit_with_sim(sim, target, SimRelationshipBit.FRIENDSHIP_BFF) or has_relationship_bit_with_sim(sim, target, SimRelationshipBit.FRIENDSHIP_BFF_BROMANTICPARTNER))))) or has_relationship_bit_with_sim(sim, target, SimRelationshipBit.ROMANTIC_HAVEDONEWOOHOO):
                sex_reaction_should_left = False
    return (sex_reaction_data, sex_reaction_should_left, sex_reaction_target_override)


def _jealousy_from_sex_reaction(sim, sex_handler):
    if not get_relationship_setting(RelationshipSetting.JEALOUSY_STATE, variable_type=bool):
        return False
    if sex_handler.get_actors_amount() <= 1:
        return False
    if TurboSimUtil.Age.is_younger_than(sim, TurboSimUtil.Age.TEEN):
        return False
    if has_sim_trait(sim, SimTrait.WW_POLYAMOROUS) or has_sim_trait(sim, SimTrait.WW_CUCKOLD):
        return False
    (found_lovers, found_non_lovers) = _get_jealousy_sims_from_sex_handler(sim, sex_handler)
    if found_lovers and found_non_lovers:
        for target in found_non_lovers:
            relationship_amount_modifier = -3 if not has_sim_trait(sim, SimTrait.JEALOUS) else -6
            change_relationship_with_sim(sim, target, RelationshipTrackType.FRIENDSHIP, relationship_amount_modifier)
            while get_relationship_with_sim(sim, target, RelationshipTrackType.ROMANCE) > 0:
                change_relationship_with_sim(sim, target, RelationshipTrackType.ROMANCE, relationship_amount_modifier)
        for target in found_lovers:
            jealousy_success = False
            for jealousy_interaction in JEALOUSY_WOOHOO_REACTION_LIST:
                result = TurboSimUtil.Interaction.push_affordance(sim, jealousy_interaction, target=target, interaction_context=TurboInteractionUtil.InteractionContext.SOURCE_SCRIPT, insert_strategy=TurboInteractionUtil.QueueInsertStrategy.NEXT, must_run_next=True, priority=TurboInteractionUtil.Priority.High, run_priority=TurboInteractionUtil.Priority.High)
                while result:
                    jealousy_success = True
                    break
            if has_sim_buff(sim, SimBuff.JEALOUSY_CHEATER):
                current_romance_rel_amount = get_relationship_with_sim(sim, target, RelationshipTrackType.ROMANCE)
                if current_romance_rel_amount >= 30 and has_relationship_bit_with_sim(sim, target, SimRelationshipBit.ROMANTIC_ENGAGED) or (has_relationship_bit_with_sim(sim, target, SimRelationshipBit.ROMANTIC_MARRIED) or has_relationship_bit_with_sim(sim, target, SimRelationshipBit.ROMANTIC_GETTINGMARRIED)) or has_relationship_bit_with_sim(sim, target, SimRelationshipBit.ROMANTIC_SIGNIFICANT_OTHER):
                    add_sim_buff(sim, SimBuff.JEALOUSY_HIDDEN_WITNESSEDCHEATING)
            while jealousy_success is True:
                sim_ev(sim).sex_reaction_cooldown = 5
                return True
    return False


def _get_jealousy_sims_from_sex_handler(sim, sex_handler):
    found_lovers = list()
    found_non_lovers = list()
    for target in sex_handler.get_actors_sim_instance_gen():
        if target is None:
            pass
        if has_sim_trait(target, SimTrait.PLAYER):
            pass
        current_romance_rel_amount = get_relationship_with_sim(sim, target, RelationshipTrackType.ROMANCE)
        if has_relationship_bit_with_sim(sim, target, SimRelationshipBit.ROMANTIC_ENGAGED) or has_relationship_bit_with_sim(sim, target, SimRelationshipBit.ROMANTIC_MARRIED) or has_relationship_bit_with_sim(sim, target, SimRelationshipBit.ROMANTIC_GETTINGMARRIED):
            found_lovers.append(target)
        if current_romance_rel_amount > 0 and (has_relationship_bit_with_sim(sim, target, SimRelationshipBit.ROMANTICCOMBO_SOULMATES) or (has_relationship_bit_with_sim(sim, target, SimRelationshipBit.ROMANTICCOMBO_SWEETHEARTS) or has_relationship_bit_with_sim(sim, target, SimRelationshipBit.ROMANTICCOMBO_ROMANTICINTEREST)) or has_relationship_bit_with_sim(sim, target, SimRelationshipBit.ROMANTIC_SIGNIFICANT_OTHER)):
            found_lovers.append(target)
        if current_romance_rel_amount > 10 and has_relationship_bit_with_sim(sim, target, SimRelationshipBit.ROMANTICCOMBO_AWKWARDLOVERS):
            found_lovers.append(target)
        if current_romance_rel_amount > 10 and has_relationship_bit_with_sim(sim, target, SimRelationshipBit.ROMANTICCOMBO_ENEMIESWITHBENEFITS):
            found_lovers.append(target)
        if current_romance_rel_amount >= 75:
            found_lovers.append(target)
        found_non_lovers.append(target)
    return (found_lovers, found_non_lovers)

