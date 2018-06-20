import random
from enums.buffs_enum import SimBuff
from enums.moods_enum import SimMood
from enums.relationship_enum import RelationshipTrackType, SimRelationshipBit
from enums.skills_enum import SimSkill
from enums.traits_enum import SimTrait
from enums.vanues_enum import VenueType
from turbolib.manager_util import TurboManagerUtil
from turbolib.native.enum import TurboEnum
from turbolib.resource_util import TurboResourceUtil
from turbolib.sim_util import TurboSimUtil
from turbolib.world_util import TurboWorldUtil
from turbolib.wrappers.commands import register_game_command, TurboCommandType
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.sex._ts4_sex_buffs import set_buff_timeout
from wickedwhims.sex.reactions.sex_reaction import SexReactionType, get_reaction_type
from wickedwhims.sex.sex_handlers.sex_handler_utils import get_sim_sex_state_snapshot
from wickedwhims.utils_buffs import add_sim_buff, remove_sim_buff
from wickedwhims.utils_relations import get_relationship_with_sim, has_relationship_bit_with_sim
from wickedwhims.utils_skills import get_sim_skill_level
from wickedwhims.utils_traits import has_sim_trait
POSITIVE_MOODS = (SimMood.CONFIDENT, SimMood.FLIRTY, SimMood.ENERGIZED, SimMood.FOCUSED, SimMood.HAPPY, SimMood.PLAYFUL, SimMood.INSPIRED)
NEGATIVE_MOODS = (SimMood.STRESSED, SimMood.EMBARRASSED, SimMood.ANGRY, SimMood.UNCOMFORTABLE, SimMood.SAD)
POSITIVE_REACTIONS = (SexReactionType.FRIENDLY, SexReactionType.EXCITED, SexReactionType.FLIRTY)
NEGATIVE_REACTIONS = (SexReactionType.SAD, SexReactionType.ANGRY, SexReactionType.HORRIFIED, SexReactionType.JEALOUS)
AGE_INDEX = (TurboSimUtil.Age.TEEN, TurboSimUtil.Age.YOUNGADULT, TurboSimUtil.Age.ADULT, TurboSimUtil.Age.ELDER)

class SexSatisfactionType(TurboEnum):
    __qualname__ = 'SexSatisfactionType'
    STRANGER_SEX = 1
    YOUNG_SEX = 2
    PUBLIC_SEX = 3
    AUDIENCE = 4
    FAMILY_SEX = 10
    GHOST_SEX = 11
    GROUP_SEX = 98
    GENERIC = 99

SEX_SATISFACTION_BUFFS = {SexSatisfactionType.STRANGER_SEX: SimBuff.WW_SEX_SATISFACTION_STRANGER_SEX, SexSatisfactionType.YOUNG_SEX: SimBuff.WW_SEX_SATISFACTION_YOUNG_SEX, SexSatisfactionType.PUBLIC_SEX: SimBuff.WW_SEX_SATISFACTION_PUBLIC_SEX, SexSatisfactionType.AUDIENCE: SimBuff.WW_SEX_SATISFACTION_AUDIENCE, SexSatisfactionType.FAMILY_SEX: SimBuff.WW_SEX_SATISFACTION_FAMILY_SEX, SexSatisfactionType.GHOST_SEX: SimBuff.WW_SEX_SATISFACTION_GHOST_SEX, SexSatisfactionType.GROUP_SEX: SimBuff.WW_SEX_SATISFACTION_GROUP_SEX, SexSatisfactionType.GENERIC: SimBuff.WW_SEX_SATISFACTION_GENERIC}

class SexUnsatisfactionType(TurboEnum):
    __qualname__ = 'SexUnsatisfactionType'
    BAD_EXPERIENICE = 1
    BAD_PERFORMANCE = 2
    GENERIC = 99

SEX_UNSATISFACTION_BUFFS = {SexUnsatisfactionType.BAD_EXPERIENICE: SimBuff.WW_SEX_UNSATISFACTION_BAD_EXPERIENCE, SexUnsatisfactionType.BAD_PERFORMANCE: SimBuff.WW_SEX_UNSATISFACTION_BAD_PERFORMANCE, SexUnsatisfactionType.GENERIC: SimBuff.WW_SEX_UNSATISFACTION_GENERIC}

def apply_after_sex_satisfaction(sims_list, sex_handler):
    if len(sims_list) == 1:
        return
    for (_, sim_info) in sims_list:
        satisfaction_level = _get_sex_satisfaction_level(sim_info, sims_list, sex_handler=sex_handler)
        satisfaction_type = _get_sim_satisfaction_type(sim_info, sims_list, satisfaction_level, sex_handler=sex_handler)
        _apply_sim_sex_satisfaction_moodlet(sim_info, satisfaction_type, satisfaction_level)


def _get_sex_satisfaction_level(sim_info, sims_list, sex_handler=None):
    sim_state_snapshot = sim_ev(sim_info).sim_immutable_sex_state_snapshot
    satisfaction_threshold = 0.0
    for (_, target_sim_info) in sims_list:
        if sim_info is target_sim_info:
            pass
        sim_satisfaction_threshold = 1.0
        if (get_relationship_with_sim(sim_info, target_sim_info, RelationshipTrackType.FRIENDSHIP) + get_relationship_with_sim(sim_info, target_sim_info, RelationshipTrackType.ROMANCE))/2 >= 40:
            sim_satisfaction_threshold = 0.85
            if has_relationship_bit_with_sim(sim_info, target_sim_info, SimRelationshipBit.WW_KNOWS_SEX_FANTASY):
                sim_satisfaction_threshold = 0.75
        if has_relationship_bit_with_sim(sim_info, target_sim_info, SimRelationshipBit.ROMANTICCOMBO_SOULMATES) or has_relationship_bit_with_sim(sim_info, target_sim_info, SimRelationshipBit.ROMANTICCOMBO_LOVERS) or has_relationship_bit_with_sim(sim_info, target_sim_info, SimRelationshipBit.ROMANTICCOMBO_SWEETHEARTS):
            sim_satisfaction_threshold = 0.6
            if has_sim_trait(sim_info, SimTrait.ROMANTIC) or has_sim_trait(sim_info, SimTrait.JEALOUS) or has_relationship_bit_with_sim(sim_info, target_sim_info, SimRelationshipBit.WW_KNOWS_SEX_FANTASY):
                sim_satisfaction_threshold = 0.55
        if has_relationship_bit_with_sim(sim_info, target_sim_info, SimRelationshipBit.ROMANTIC_ENGAGED) or (has_relationship_bit_with_sim(sim_info, target_sim_info, SimRelationshipBit.ROMANTIC_GETTINGMARRIED) or has_relationship_bit_with_sim(sim_info, target_sim_info, SimRelationshipBit.ROMANTIC_MARRIED)) or has_relationship_bit_with_sim(sim_info, target_sim_info, SimRelationshipBit.ROMANTIC_SIGNIFICANT_OTHER):
            sim_satisfaction_threshold = 0.5
            if has_sim_trait(sim_info, SimTrait.FAMILYORIENTED) or has_sim_trait(sim_info, SimTrait.FAMILYSIM):
                sim_satisfaction_threshold = 0.45
        if has_sim_trait(sim_info, SimTrait.COMMITMENTISSUES) and sim_satisfaction_threshold <= 0.55:
            sim_satisfaction_threshold = 0.55
        satisfaction_threshold += sim_satisfaction_threshold
    satisfaction_threshold /= max(1, len(sims_list) - 1)
    satisfaction_value = 0.0
    for (_, target_sim_info) in sims_list:
        if sim_info is target_sim_info:
            pass
        target_state_snapshot = sim_ev(target_sim_info).sim_immutable_sex_state_snapshot
        if 'motive_hygiene' in target_state_snapshot:
            hygiene_motive_snapshot = target_state_snapshot['motive_hygiene']
            if not has_sim_trait(sim_info, SimTrait.SLOB):
                satisfaction_value += 0.25
            if has_sim_trait(sim_info, SimTrait.NEAT) and hygiene_motive_snapshot >= 90:
                satisfaction_value += 0.4
            elif hygiene_motive_snapshot >= 50:
                satisfaction_value += 0.25
            elif hygiene_motive_snapshot <= -55:
                satisfaction_value += -0.15 if not has_sim_trait(sim_info, SimTrait.NEAT) and not has_sim_trait(sim_info, SimTrait.SQUEAMISH) else -0.2
        if 'motive_energy' in target_state_snapshot:
            energy_motive_snapshot = target_state_snapshot['motive_energy']
            if energy_motive_snapshot >= 90:
                satisfaction_value += 0.25
            elif energy_motive_snapshot >= 50:
                satisfaction_value += 0.2
            elif energy_motive_snapshot <= -55:
                satisfaction_value += -0.05
        sim_mood = sim_state_snapshot['mood'] if 'mood' in sim_state_snapshot else TurboResourceUtil.Resource.get_guid64(TurboSimUtil.Mood.get_mood(sim_info))
        target_mood = target_state_snapshot['mood'] if 'mood' in target_state_snapshot else TurboResourceUtil.Resource.get_guid64(TurboSimUtil.Mood.get_mood(target_sim_info))
        if target_mood in POSITIVE_MOODS:
            if sim_mood in POSITIVE_MOODS:
                satisfaction_value += 0.4
            elif sim_mood in NEGATIVE_MOODS:
                satisfaction_value += 0.5
        elif target_mood in NEGATIVE_MOODS:
            if sim_mood in POSITIVE_MOODS and has_sim_trait(sim_info, SimTrait.MEAN):
                satisfaction_value += 0.3
            elif has_sim_trait(sim_info, SimTrait.GOOD) or has_sim_trait(sim_info, SimTrait.CHEERFUL):
                satisfaction_value += 0.15
            elif has_sim_trait(sim_info, SimTrait.EVIL):
                satisfaction_value += 0.4
            else:
                satisfaction_value += -0.1
        sims_age_difference = AGE_INDEX.index(TurboSimUtil.Age.get_age(sim_info)) - AGE_INDEX.index(TurboSimUtil.Age.get_age(target_sim_info))
        if TurboSimUtil.Gender.is_male(sim_info):
            if sims_age_difference > 0:
                satisfaction_value += 0.075*(sims_age_difference + 1)
            elif sims_age_difference == 0 or sims_age_difference == -1:
                satisfaction_value += 0.1
        elif sims_age_difference == 0:
            satisfaction_value += 0.1
        elif abs(sims_age_difference) == 1:
            satisfaction_value += 0.15
        if TurboSimUtil.Gender.is_female(sim_info) and TurboSimUtil.Gender.is_male(target_sim_info):
            target_sim_age = TurboSimUtil.Age.get_age(target_sim_info)
            if target_sim_age == TurboSimUtil.Age.TEEN and random.uniform(0, 1) < 0.25:
                satisfaction_value += -0.05
            elif target_sim_age == TurboSimUtil.Age.YOUNGADULT and random.uniform(0, 1) < 0.1:
                satisfaction_value += -0.1
            elif target_sim_age == TurboSimUtil.Age.ADULT and random.uniform(0, 1) < 0.1:
                satisfaction_value += -0.1
            elif target_sim_age == TurboSimUtil.Age.ELDER and random.uniform(0, 1) < 0.3:
                satisfaction_value += -0.05
        if has_sim_trait(target_sim_info, SimTrait.LAZY):
            satisfaction_value += -0.05
        if has_sim_trait(target_sim_info, SimTrait.CHILDISH):
            satisfaction_value += -0.05
        if has_sim_trait(target_sim_info, SimTrait.CLUMSY) and random.uniform(0, 1) <= 0.25:
            satisfaction_value += -0.05
        if has_sim_trait(target_sim_info, SimTrait.ACTIVE):
            satisfaction_value += 0.05
        if has_sim_trait(target_sim_info, SimTrait.DANCEMACHINE):
            satisfaction_value += 0.05
        if has_sim_trait(target_sim_info, SimTrait.GOOFBALL) and random.uniform(0, 1) <= 0.25:
            satisfaction_value += 0.1
        if has_sim_trait(sim_info, SimTrait.SNOB) and has_sim_trait(target_sim_info, SimTrait.SNOB):
            satisfaction_value += 0.1
        if has_sim_trait(sim_info, SimTrait.BRO) and has_sim_trait(target_sim_info, SimTrait.BRO):
            satisfaction_value += 0.1
        if has_sim_trait(sim_info, SimTrait.ROMANTIC) and has_sim_trait(target_sim_info, SimTrait.ALLURING):
            satisfaction_value += 0.05
        while get_sim_skill_level(target_sim_info, SimSkill.FITNESS) >= 7:
            satisfaction_value += 0.05
    satisfaction_value /= max(1, len(sims_list) - 1)
    if 'motive_energy' in sim_state_snapshot:
        energy_motive_snapshot = sim_state_snapshot['motive_energy']
        if energy_motive_snapshot >= 90:
            satisfaction_value += 0.15
        elif energy_motive_snapshot >= 50:
            satisfaction_value += 0.1
        elif energy_motive_snapshot <= -55:
            satisfaction_value += -0.05
    if 'motive_bladder' in sim_state_snapshot:
        bladder_motive_snapshot = sim_state_snapshot['motive_bladder']
        if bladder_motive_snapshot >= -50 and bladder_motive_snapshot < -25:
            satisfaction_value += 0.1
    if has_sim_trait(sim_info, SimTrait.OUTGOING) and len(sims_list) > 2:
        satisfaction_value += 0.1
    if has_sim_trait(sim_info, SimTrait.WW_EXHIBITIONIST) and (sex_handler is not None and TurboWorldUtil.Venue.get_current_venue_type() not in (VenueType.RESIDENTIAL, VenueType.PENTHOUSE, VenueType.RENTABLE_CABIN)) and not TurboWorldUtil.Lot.is_sim_on_home_lot(sim_info):
        satisfaction_value += 0.1
    if has_sim_trait(sim_info, SimTrait.LOVESOUTDOORS) and (sex_handler is not None and TurboWorldUtil.Lot.is_location_outside(sex_handler.get_location())) and TurboWorldUtil.Lot.is_sim_on_home_lot(sim_info):
        satisfaction_value += 0.05
    if has_sim_trait(sim_info, SimTrait.INSANE) and random.uniform(0, 1) <= 0.3:
        if random.uniform(0, 1) <= 0.5:
            satisfaction_value += 0.25
        else:
            satisfaction_value += -0.25
    if 'has_positive_desire_buff' in sim_state_snapshot and sim_state_snapshot['has_positive_desire_buff'] is True:
        satisfaction_value += 0.2
    if sex_handler is not None and sex_handler.has_reacted_sims_list:
        reactions_satisfaction_value = 0.0
        for reacted_sim_id in sex_handler.has_reacted_sims_list:
            reacted_sim_info = TurboManagerUtil.Sim.get_sim_info(reacted_sim_id)
            while reacted_sim_info is not None:
                (sex_reaction_data, _, _) = get_reaction_type(reacted_sim_info, sex_handler, allow_special_types=True)
                if sex_reaction_data[0] in POSITIVE_REACTIONS:
                    reactions_satisfaction_value += 0.05 if not has_sim_trait(sim_info, SimTrait.WW_EXHIBITIONIST) else 0.1
                elif sex_reaction_data[0] == SexReactionType.CUCK:
                    reactions_satisfaction_value += 0.15
                elif sex_reaction_data[0] == SexReactionType.JEALOUS:
                    reactions_satisfaction_value += -0.1
                elif sex_reaction_data[0] in NEGATIVE_REACTIONS and not has_sim_trait(sim_info, SimTrait.WW_EXHIBITIONIST):
                    reactions_satisfaction_value += -0.05
        satisfaction_value += reactions_satisfaction_value/len(sex_handler.has_reacted_sims_list)
    satisfaction_level_value = satisfaction_value/satisfaction_threshold
    if satisfaction_level_value <= 0.0:
        return 0.0
    if satisfaction_level_value < 1.0:
        if random.uniform(0, 1) <= satisfaction_level_value:
            return 1.0
        return 0.0
    return round(satisfaction_level_value)


def _get_sim_satisfaction_type(sim_info, sims_list, satisfaction_level, sex_handler=None):
    sim_state_snapshot = sim_ev(sim_info).sim_immutable_sex_state_snapshot
    if satisfaction_level <= 0:
        satisfaction_type = SexUnsatisfactionType.GENERIC
        if SexUnsatisfactionType.BAD_EXPERIENICE < satisfaction_type:
            sim_mood = sim_state_snapshot['mood'] if 'mood' in sim_state_snapshot else TurboResourceUtil.Resource.get_guid64(TurboSimUtil.Mood.get_mood(sim_info))
            for (_, target_sim_info) in sims_list:
                if sim_info is target_sim_info:
                    pass
                if (sim_mood == SimMood.FLIRTY or has_sim_trait(sim_info, SimTrait.ROMANTIC) or has_sim_trait(sim_info, SimTrait.JEALOUS)) and (get_relationship_with_sim(sim_info, target_sim_info, RelationshipTrackType.FRIENDSHIP) + get_relationship_with_sim(sim_info, target_sim_info, RelationshipTrackType.ROMANCE))/2 >= 40:
                    satisfaction_type = SexUnsatisfactionType.BAD_EXPERIENICE
                    break
                while has_sim_trait(sim_info, SimTrait.FAMILYORIENTED) or has_sim_trait(sim_info, SimTrait.FAMILYSIM):
                    if has_relationship_bit_with_sim(sim_info, target_sim_info, SimRelationshipBit.ROMANTIC_ENGAGED) or (has_relationship_bit_with_sim(sim_info, target_sim_info, SimRelationshipBit.ROMANTIC_GETTINGMARRIED) or has_relationship_bit_with_sim(sim_info, target_sim_info, SimRelationshipBit.ROMANTIC_MARRIED)) or has_relationship_bit_with_sim(sim_info, target_sim_info, SimRelationshipBit.ROMANTIC_SIGNIFICANT_OTHER):
                        satisfaction_type = SexUnsatisfactionType.BAD_EXPERIENICE
                        break
        if SexUnsatisfactionType.BAD_PERFORMANCE < satisfaction_type:
            if has_sim_trait(sim_info, SimTrait.ACTIVE) or get_sim_skill_level(sim_info, SimSkill.FITNESS) >= 7:
                satisfaction_type = SexUnsatisfactionType.BAD_PERFORMANCE
    else:
        satisfaction_type = SexSatisfactionType.GENERIC
        if not (SexSatisfactionType.STRANGER_SEX < satisfaction_type and has_sim_trait(sim_info, SimTrait.LONER)):
            while True:
                for (_, target_sim_info) in sims_list:
                    if sim_info is target_sim_info:
                        pass
                    friendship_track_score = get_relationship_with_sim(sim_info, target_sim_info, RelationshipTrackType.FRIENDSHIP)
                    romance_track_score = get_relationship_with_sim(sim_info, target_sim_info, RelationshipTrackType.ROMANCE)
                    while friendship_track_score < 30 and romance_track_score < 10:
                        satisfaction_type = SexSatisfactionType.STRANGER_SEX
                        break
        if SexSatisfactionType.YOUNG_SEX < satisfaction_type:
            for (_, target_sim_info) in sims_list:
                if sim_info is target_sim_info:
                    pass
                while TurboSimUtil.Age.get_age(target_sim_info) < TurboSimUtil.Age.get_age(sim_info) and abs(AGE_INDEX.index(TurboSimUtil.Age.get_age(sim_info)) - AGE_INDEX.index(TurboSimUtil.Age.get_age(target_sim_info))) >= 2:
                    satisfaction_type = SexSatisfactionType.YOUNG_SEX
                    break
        if has_sim_trait(sim_info, SimTrait.WW_EXHIBITIONIST) and TurboWorldUtil.Venue.get_current_venue_type() not in (VenueType.RESIDENTIAL, VenueType.PENTHOUSE, VenueType.RENTABLE_CABIN) and not TurboWorldUtil.Lot.is_sim_on_home_lot(sim_info):
            satisfaction_type = SexSatisfactionType.PUBLIC_SEX
        if SexSatisfactionType.PUBLIC_SEX < satisfaction_type and (has_sim_trait(sim_info, SimTrait.LOVESOUTDOORS) and sex_handler is not None) and random.uniform(0, 1) <= 0.25:
            if TurboWorldUtil.Lot.is_location_outside(sex_handler.get_location()) and not TurboWorldUtil.Lot.is_sim_on_home_lot(sim_info):
                satisfaction_type = SexSatisfactionType.PUBLIC_SEX
        if SexSatisfactionType.AUDIENCE < satisfaction_type and (not has_sim_trait(sim_info, SimTrait.UNFLIRTY) and sex_handler is not None) and sex_handler.has_reacted_sims_list:
            reaction_sims_list = sex_handler.has_reacted_sims_list.difference(sex_handler.go_away_sims_list)
            reactions_count = 0
            for reacted_sim_id in reaction_sims_list:
                reacted_sim_info = TurboManagerUtil.Sim.get_sim_info(reacted_sim_id)
                while reacted_sim_info is not None:
                    (sex_reaction_data, _, _) = get_reaction_type(reacted_sim_info, sex_handler)
                    if sex_reaction_data[0] in POSITIVE_REACTIONS:
                        reactions_count += 1
                    elif sex_reaction_data[0] == SexReactionType.CUCK:
                        reactions_count += 2
                    elif sex_reaction_data[0] == SexReactionType.JEALOUS:
                        reactions_count -= 2
                    elif sex_reaction_data[0] in NEGATIVE_REACTIONS and not has_sim_trait(sim_info, SimTrait.WW_EXHIBITIONIST):
                        reactions_count -= 1
            if reactions_count > 0:
                satisfaction_type = SexSatisfactionType.AUDIENCE
        if SexSatisfactionType.FAMILY_SEX < satisfaction_type and (has_sim_trait(sim_info, SimTrait.FAMILYORIENTED) or has_sim_trait(sim_info, SimTrait.FAMILYSIM)):
            while True:
                for (_, target_sim_info) in sims_list:
                    if sim_info is target_sim_info:
                        pass
                    while has_relationship_bit_with_sim(sim_info, target_sim_info, SimRelationshipBit.ROMANTIC_ENGAGED) or has_relationship_bit_with_sim(sim_info, target_sim_info, SimRelationshipBit.ROMANTIC_GETTINGMARRIED) or has_relationship_bit_with_sim(sim_info, target_sim_info, SimRelationshipBit.ROMANTIC_MARRIED):
                        satisfaction_type = SexSatisfactionType.FAMILY_SEX
                        break
        if SexSatisfactionType.GHOST_SEX < satisfaction_type:
            for (_, target_sim_info) in sims_list:
                if sim_info is target_sim_info:
                    pass
                while TurboSimUtil.Sim.is_npc(target_sim_info) and TurboSimUtil.Occult.is_ghost(target_sim_info):
                    satisfaction_type = SexSatisfactionType.GHOST_SEX
                    break
        if SexSatisfactionType.GROUP_SEX < satisfaction_type and len(sims_list) > 2:
            satisfaction_type = SexSatisfactionType.GROUP_SEX
    return satisfaction_type


def _apply_sim_sex_satisfaction_moodlet(sim_info, satisfaction_type, satisfaction_level):
    satisfaction_moodlet_timeout = 60*max(1, satisfaction_level)
    satisfaction_moodlet = None
    if satisfaction_level <= 0:
        if satisfaction_type in SEX_UNSATISFACTION_BUFFS:
            satisfaction_moodlet = SEX_UNSATISFACTION_BUFFS[satisfaction_type]
    elif satisfaction_type in SEX_SATISFACTION_BUFFS:
        satisfaction_moodlet = SEX_SATISFACTION_BUFFS[satisfaction_type]
    if satisfaction_moodlet is None:
        return
    clear_all_satifaction_data(sim_info)
    if set_buff_timeout(satisfaction_moodlet, satisfaction_moodlet_timeout):
        add_sim_buff(sim_info, satisfaction_moodlet, reason=4052013031)
    set_buff_timeout(satisfaction_moodlet, 600)


def clear_all_satifaction_data(sim_identifier):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    for buff_id in SEX_SATISFACTION_BUFFS.values():
        remove_sim_buff(sim_info, buff_id)
    for buff_id in SEX_UNSATISFACTION_BUFFS.values():
        remove_sim_buff(sim_info, buff_id)


@register_game_command('ww.test_sex_satisfaction', command_type=TurboCommandType.LIVE)
def test_sex_satifaction_outcome(output=None):
    sims_count = 0
    sims_pairs = 0
    satisfaction_levels = dict()
    satisfaction_positive_types = dict()
    satisfaction_negative_types = dict()
    for sim_info in TurboManagerUtil.Sim.get_all_sim_info_gen(humans=True, pets=False):
        if TurboSimUtil.Age.is_younger_than(sim_info, TurboSimUtil.Age.TEEN):
            pass
        sims_count += 1
        for target_sim_info in TurboManagerUtil.Sim.get_all_sim_info_gen(humans=True, pets=False):
            if sim_info is target_sim_info:
                pass
            if TurboSimUtil.Age.is_younger_than(target_sim_info, TurboSimUtil.Age.TEEN):
                pass
            sims_pairs += 1
            sim_ev(sim_info).sim_immutable_sex_state_snapshot = get_sim_sex_state_snapshot(sim_info)
            sim_ev(sim_info).sim_immutable_sex_state_snapshot['mood'] = int(SimMood.HAPPY)
            sim_ev(sim_info).sim_immutable_sex_state_snapshot['motive_energy'] = 100
            sim_ev(sim_info).sim_immutable_sex_state_snapshot['motive_hygiene'] = 100
            sim_ev(sim_info).sim_immutable_sex_state_snapshot['motive_bladder'] = 100
            sim_ev(target_sim_info).sim_immutable_sex_state_snapshot = get_sim_sex_state_snapshot(target_sim_info)
            sim_ev(target_sim_info).sim_immutable_sex_state_snapshot['mood'] = int(SimMood.HAPPY)
            sim_ev(target_sim_info).sim_immutable_sex_state_snapshot['motive_energy'] = 100
            sim_ev(target_sim_info).sim_immutable_sex_state_snapshot['motive_hygiene'] = 100
            sim_ev(target_sim_info).sim_immutable_sex_state_snapshot['motive_bladder'] = 100
            sims_list = ((0, sim_info), (1, target_sim_info))
            satisfaction_level = _get_sex_satisfaction_level(sim_info, sims_list)
            satisfaction_type = _get_sim_satisfaction_type(sim_info, sims_list, satisfaction_level)
            satisfaction_levels_count = 1 if satisfaction_level not in satisfaction_levels else satisfaction_levels[satisfaction_level] + 1
            satisfaction_levels[satisfaction_level] = satisfaction_levels_count
            if satisfaction_level > 0:
                positive_satisfaction_count = 1 if satisfaction_type not in satisfaction_positive_types else satisfaction_positive_types[satisfaction_type] + 1
                satisfaction_positive_types[satisfaction_type] = positive_satisfaction_count
            else:
                negative_satisfaction_count = 1 if satisfaction_type not in satisfaction_negative_types else satisfaction_negative_types[satisfaction_type] + 1
                satisfaction_negative_types[satisfaction_type] = negative_satisfaction_count
    output('Testing {} possible pairs from {} Sims.'.format(str(sims_pairs), str(sims_count)))
    output('')
    output('Satisfaction Levels:')
    for (level, count) in satisfaction_levels.items():
        output('Level {}: {} times'.format(str(level), str(count)))
    output('')
    output('Positive Satisfaction Types:')
    for (satisfaction_type, count) in satisfaction_positive_types.items():
        output('Type {}: {} times'.format(str(satisfaction_type.name), str(count)))
    output('')
    output('Negative Satisfaction Types:')
    for (satisfaction_type, count) in satisfaction_negative_types.items():
        output('Type {}: {} times'.format(str(satisfaction_type.name), str(count)))


@register_game_command('ww.test_sex_satisfaction_moodlets', command_type=TurboCommandType.LIVE)
def test_sex_satifaction_moodlets(output=None):
    sim = TurboManagerUtil.Sim.get_active_sim()
    for buff_id in SEX_SATISFACTION_BUFFS.values():
        while set_buff_timeout(buff_id, 60):
            add_sim_buff(sim, buff_id, reason=4052013031)
            set_buff_timeout(buff_id, 600)
    for buff_id in SEX_UNSATISFACTION_BUFFS.values():
        while set_buff_timeout(buff_id, 60):
            add_sim_buff(sim, buff_id, reason=4052013031)
            set_buff_timeout(buff_id, 600)
    output('Sex Satisfaction moodlets applied.')

