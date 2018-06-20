'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
import random
from enums.buffs_enum import SimBuff
from enums.moods_enum import SimMood
from enums.motives_enum import SimMotive
from enums.relationship_enum import RelationshipTrackType, ShortTermRelationshipTrackType, SimRelationshipBit
from enums.situations_enum import SimSituationJob
from enums.skills_enum import SimSkill
from enums.statistics_enum import SimCommodity
from enums.traits_enum import SimTrait
from turbolib.manager_util import TurboManagerUtil
from turbolib.sim_util import TurboSimUtil
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.relationships.desire_handler import get_sim_desire_level
from wickedwhims.relationships.relationship_settings import get_relationship_setting, RelationshipSetting
from wickedwhims.relationships.relationship_utils import get_sim_preferenced_genders
from wickedwhims.sex.settings.sex_settings import SexSetting, get_sex_setting, SexAutonomyLevelSetting
from wickedwhims.sex.utils.sex_init import get_age_limits_for_sex
from wickedwhims.sxex_bridge.relationships import is_true_family_relationship
from wickedwhims.sxex_bridge.statistics import increase_sim_ww_statistic
from wickedwhims.utils_buffs import add_sim_buff, has_sim_buff
from wickedwhims.utils_interfaces import display_notification
from wickedwhims.utils_motives import get_sim_motive_value, set_sim_motive_value
from wickedwhims.utils_relations import change_relationship_with_sim, get_relationship_with_sim, add_relationsip_bit_with_sim, has_relationship_bit_with_sim, get_sim_ids_with_relationsip_bit
from wickedwhims.utils_sims import has_sim_mood
from wickedwhims.utils_situations import has_sim_situation_job
from wickedwhims.utils_skills import get_sim_skill_level
from wickedwhims.utils_statistics import change_sim_statistic_value
from wickedwhims.utils_traits import has_sim_trait
RELATIONSHIP_SEX_ACCEPTANCE_THRESHOLD = 15

def get_relationship_sex_acceptance_threshold():
    return RELATIONSHIP_SEX_ACCEPTANCE_THRESHOLD


def get_test_relationship_score(sims_list, skip_always_accept=False):
    if not sims_list:
        return 0
    overall_score = 0
    for sim in sims_list:
        for target in sims_list:
            if sim is target:
                pass
            overall_score += get_relationship_score(sim, target, skip_always_accept=skip_always_accept)
    relationship_score = overall_score/len(sims_list)
    return relationship_score


def get_relationship_score(sim_identifier, target_sim_identifier, skip_always_accept=False):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    target_sim_info = TurboManagerUtil.Sim.get_sim_info(target_sim_identifier)
    is_npc_exclusive = TurboSimUtil.Sim.is_npc(sim_info) and TurboSimUtil.Sim.is_npc(target_sim_info)
    if get_sex_setting(SexSetting.ALWAYS_ACCEPT_STATE, variable_type=bool) and is_npc_exclusive is False and skip_always_accept is False:
        return 1000
    if has_sim_trait(sim_info, SimTrait.WW_SEXUALLY_ABSTINENT):
        return -1000
    if has_sim_trait(sim_info, SimTrait.BASEMENTAL_IS_A_DRUG_DEALER) and (has_sim_buff(target_sim_info, SimBuff.BASEMENTAL_COCAINE_SEX_PAYMENT_HIDDEN) or has_sim_buff(target_sim_info, SimBuff.BASEMENTAL_AMPHETAMINE_SEX_PAYMENT_HIDDEN) or has_sim_buff(target_sim_info, SimBuff.BASEMENTAL_MDMA_SEX_PAYMENT_HIDDEN)):
        return 1000
    if has_sim_trait(sim_info, SimTrait.BASEMENTAL_IS_A_COCAINE_DRUG_DEALER) and has_sim_buff(target_sim_info, SimBuff.BASEMENTAL_COCAINE_SEX_PAYMENT_HIDDEN):
        return 1000
    if has_sim_trait(sim_info, SimTrait.BASEMENTAL_IS_A_AMPHETAMINE_DRUG_DEALER) and has_sim_buff(target_sim_info, SimBuff.BASEMENTAL_AMPHETAMINE_SEX_PAYMENT_HIDDEN):
        return 1000
    if has_relationship_bit_with_sim(sim_info, target_sim_info, SimRelationshipBit.BASEMENTAL_DEALER_COCAINE_COMPANION) and has_relationship_bit_with_sim(target_sim_info, sim_info, SimRelationshipBit.BASEMENTAL_DEALER_COCAINE_COMPANION):
        return 1000
    score = 0
    if is_npc_exclusive:
        pre_sex_handler = sim_ev(sim_info).active_pre_sex_handler or sim_ev(target_sim_info).active_pre_sex_handler
        if pre_sex_handler is not None and (pre_sex_handler.is_manual_sex() or pre_sex_handler.is_autonomy_sex()):
            return 1000
        if get_sex_setting(SexSetting.AUTONOMY_LEVEL, variable_type=int) == SexAutonomyLevelSetting.LOW:
            score += 3
        elif get_sex_setting(SexSetting.AUTONOMY_LEVEL, variable_type=int) == SexAutonomyLevelSetting.NORMAL:
            score += 6
        elif get_sex_setting(SexSetting.AUTONOMY_LEVEL, variable_type=int) == SexAutonomyLevelSetting.HIGH:
            score += 20
        age_limit = get_age_limits_for_sex((sim_info,))
        if TurboSimUtil.Age.is_younger_than(target_sim_info, age_limit[0]) or TurboSimUtil.Age.is_older_than(target_sim_info, age_limit[1]):
            return -1000
        preferred_genders = get_sim_preferenced_genders(sim_info)
        if TurboSimUtil.Gender.get_gender(target_sim_info) in preferred_genders:
            score += 5
        else:
            score += -5
    if is_true_family_relationship(sim_info, target_sim_info):
        score += -50
    current_charisma_skill_level = get_sim_skill_level(sim_info, SimSkill.ADULTMAJOR_CHARISMA)
    if 1 <= current_charisma_skill_level <= 2:
        score += 2
    if 3 <= current_charisma_skill_level <= 4:
        score += 3
    if 5 <= current_charisma_skill_level <= 6:
        score += 6
    if 7 <= current_charisma_skill_level <= 8:
        score += 8
    if 9 <= current_charisma_skill_level <= 10:
        score += 12
    if has_sim_trait(sim_info, SimTrait.ALLURING):
        score += 4
    if get_relationship_setting(RelationshipSetting.JEALOUSY_STATE, variable_type=bool) and not has_sim_trait(sim_info, SimTrait.WW_POLYAMOROUS):
        current_significant_sims = get_sim_relationship_sims(sim_info)
        if current_significant_sims:
            if TurboManagerUtil.Sim.get_sim_id(target_sim_info) in current_significant_sims:
                score += 6 if not has_sim_trait(sim_info, SimTrait.COMMITMENTISSUES) else 3
            else:
                score += -10 if not has_sim_trait(sim_info, SimTrait.COMMITMENTISSUES) else -5
    if has_relationship_bit_with_sim(sim_info, target_sim_info, SimRelationshipBit.SOCIALCONTEXT_ROMANCE_STEAMY):
        score += 12
    if has_relationship_bit_with_sim(sim_info, target_sim_info, SimRelationshipBit.SOCIALCONTEXT_ROMANCE_AMOROUS):
        score += 7
    if has_relationship_bit_with_sim(sim_info, target_sim_info, SimRelationshipBit.FRIENDSHIP_BFF_BROMANTICPARTNER):
        score += 6
    if has_relationship_bit_with_sim(sim_info, target_sim_info, SimRelationshipBit.FRIENDSHIP_BFF):
        score += 5
    if has_relationship_bit_with_sim(sim_info, target_sim_info, SimRelationshipBit.FRIENDSHIP_BFF_EVIL):
        score += 4
    if has_relationship_bit_with_sim(sim_info, target_sim_info, SimRelationshipBit.SOCIALCONTEXT_ROMANCE_SUGGESTIVE):
        score += 5
    if has_relationship_bit_with_sim(sim_info, target_sim_info, SimRelationshipBit.SOCIALCONTEXT_FRIENDSHIP_FRIENDLY):
        score += 4
    if has_relationship_bit_with_sim(sim_info, target_sim_info, SimRelationshipBit.SOCIALCONTEXT_FUN_FUNNY):
        score += 4
    if has_relationship_bit_with_sim(sim_info, target_sim_info, SimRelationshipBit.SOCIALCONTEXT_FUN_HILARIOUS):
        score += 4
    if has_relationship_bit_with_sim(sim_info, target_sim_info, SimRelationshipBit.SOCIALCONTEXT_RETAIL_MILDLYINTERESTED):
        score += 1
    if has_relationship_bit_with_sim(sim_info, target_sim_info, SimRelationshipBit.SOCIALCONTEXT_RETAIL_UNINTERESTED):
        score += 1
    if has_relationship_bit_with_sim(sim_info, target_sim_info, SimRelationshipBit.SOCIALCONTEXT_RETAIL_VERYINTERESTED):
        score += 1
    if has_relationship_bit_with_sim(sim_info, target_sim_info, SimRelationshipBit.SOCIALCONTEXT_FRIENDSHIP_DISTASTEFUL):
        score += -5
    if has_relationship_bit_with_sim(sim_info, target_sim_info, SimRelationshipBit.SOCIALCONTEXT_FUN_BORING):
        score += -5
    if has_relationship_bit_with_sim(sim_info, target_sim_info, SimRelationshipBit.SOCIALCONTEXT_FUN_TEDIOUS):
        score += -8
    if has_relationship_bit_with_sim(sim_info, target_sim_info, SimRelationshipBit.SOCIALCONTEXT_FUN_INSUFFERABLYTEDIOUS):
        score += -15
    if has_relationship_bit_with_sim(sim_info, target_sim_info, SimRelationshipBit.SOCIALCONTEXT_FRIENDSHIP_OFFENSIVE):
        score += -20
    if has_relationship_bit_with_sim(sim_info, target_sim_info, SimRelationshipBit.SOCIALCONTEXT_AWKWARDNESS_AWKWARD):
        score += -23
    if has_relationship_bit_with_sim(sim_info, target_sim_info, SimRelationshipBit.SOCIALCONTEXT_AWKWARDNESS_VERYAWKWARD):
        score += -23
    if has_relationship_bit_with_sim(sim_info, target_sim_info, SimRelationshipBit.SOCIALCONTEXT_FRIENDSHIP_ABHORRENT):
        score += -25
    current_desire_level = get_sim_desire_level(sim_info)
    if current_desire_level >= 85:
        score += 10
    elif current_desire_level >= 50:
        score += 7
    current_friendship_rel_amount = get_relationship_with_sim(sim_info, target_sim_info, RelationshipTrackType.FRIENDSHIP)
    if -100 <= current_friendship_rel_amount <= -70:
        score += -10
    if -70 <= current_friendship_rel_amount <= -30:
        score += -5
    if -30 <= current_friendship_rel_amount <= -15:
        score += -2
    if -15 <= current_friendship_rel_amount <= 25:
        score += 4
    if 25 <= current_friendship_rel_amount <= 60:
        score += 8
    if 60 <= current_friendship_rel_amount <= 100:
        score += 10
    current_romantic_rel_amount = get_relationship_with_sim(sim_info, target_sim_info, RelationshipTrackType.ROMANCE)
    if -100 <= current_romantic_rel_amount <= -50:
        score += -6
    if -50 <= current_romantic_rel_amount <= 0:
        score += -3
    if 25 <= current_romantic_rel_amount <= 50:
        score += 10
    if 50 <= current_romantic_rel_amount <= 100:
        score += 25
    if has_sim_mood(sim_info, SimMood.FLIRTY):
        score += 7
    if has_sim_mood(sim_info, SimMood.DAZED):
        score += 7
    if has_sim_mood(sim_info, SimMood.CONFIDENT):
        score += 4
    if has_sim_mood(sim_info, SimMood.HAPPY):
        score += 4
    if has_sim_mood(sim_info, SimMood.PLAYFUL):
        score += 3
    if has_sim_mood(sim_info, SimMood.ENERGIZED):
        score += 2
    if has_sim_mood(sim_info, SimMood.FINE):
        score += 2
    if has_sim_mood(sim_info, SimMood.INSPIRED):
        score += 2
    if has_sim_mood(sim_info, SimMood.FOCUSED):
        score += 2
    if has_sim_mood(sim_info, SimMood.INSPIRED):
        score += 2
    if has_sim_mood(sim_info, SimMood.ANGRY):
        score += -3
    if has_sim_mood(sim_info, SimMood.STRESSED):
        score += -5
    if has_sim_mood(sim_info, SimMood.UNCOMFORTABLE):
        score += -5
    if has_sim_mood(sim_info, SimMood.BORED):
        score += -6
    if has_sim_mood(sim_info, SimMood.SAD):
        score += -10
    if has_sim_mood(sim_info, SimMood.EMBARRASSED):
        score += -13
    if has_sim_trait(sim_info, SimTrait.WW_SEXUALLY_ALLURING) and has_relationship_bit_with_sim(sim_info, target_sim_info, SimRelationshipBit.HAS_MET):
        score += 50
    if has_sim_trait(sim_info, SimTrait.EVIL) and get_sim_relationship_sims(target_sim_info):
        score += 4
    if has_sim_trait(sim_info, SimTrait.LONER):
        score += 3
    if has_sim_trait(sim_info, SimTrait.BRO) and has_sim_trait(target_sim_info, SimTrait.BRO):
        score += 1
    if has_sim_buff(sim_info, SimBuff.MOODHIDDEN_PASSIONATE):
        score += 10
    if has_sim_buff(sim_info, SimBuff.CLUBS_PERKS_SOCIALBONUS_ROMANTIC):
        score += 10
    if has_sim_buff(sim_info, SimBuff.MOODHIDDEN_FEARLESS):
        score += 5
    if has_sim_buff(sim_info, SimBuff.MOODHIDDEN_ELATED):
        score += 5
    if has_sim_buff(sim_info, SimBuff.FESTIVAL_BLOSSOM_TEAGLOW_SAKURA):
        score += 5
    if has_sim_buff(sim_info, SimBuff.BASEMENTAL_MDMA_HIGH_ON_SUPER_QUALITY) or (has_sim_buff(sim_info, SimBuff.BASEMENTAL_MDMA_HIGH_ON_HIGH_QUALITY) or has_sim_buff(sim_info, SimBuff.BASEMENTAL_MDMA_HIGH_ON_GOOD_1_QUALITY)) or has_sim_buff(sim_info, SimBuff.BASEMENTAL_MDMA_HIGH_ON_GOOD_2_QUALITY):
        score += 3
    if has_sim_buff(sim_info, SimBuff.BASEMENTAL_COCAINE_HIGH_ON_HIGH_QUALITY) or has_sim_buff(sim_info, SimBuff.BASEMENTAL_COCAINE_HIGH_ON_MEDIUM_QUALITY):
        score += 3
    if has_sim_buff(sim_info, SimBuff.BASEMENTAL_MDMA_HIGH_ON_MEDIUM_QUALITY) or has_sim_buff(sim_info, SimBuff.BASEMENTAL_MDMA_HIGH_ON_LOW_QUALITY):
        score += 2
    if has_sim_buff(sim_info, SimBuff.BASEMENTAL_COCAINE_VERY_HIGH_ON_HIGH_QUALITY) or has_sim_buff(sim_info, SimBuff.BASEMENTAL_COCAINE_VERY_HIGH_ON_MEDIUM_QUALITY):
        score += 3
    if has_sim_buff(sim_info, SimBuff.BASEMENTAL_ALCOHOL_TIPSY):
        score += 1
    elif has_sim_buff(sim_info, SimBuff.BASEMENTAL_ALCOHOL_DRUNK):
        score += 2
    elif has_sim_buff(sim_info, SimBuff.BASEMENTAL_ALCOHOL_WASTED):
        score += 3
    if has_sim_buff(sim_info, SimBuff.MOODHIDDEN_HUMILIATED) or has_sim_buff(sim_info, SimBuff.MOODHIDDEN_MORTIFIED):
        score += 1
    if has_sim_buff(sim_info, SimBuff.MOODHIDDEN_PUMPED):
        score += 1
    if has_sim_buff(sim_info, SimBuff.MOODHIDDEN_INTHEZONE):
        score += 1
    if has_sim_buff(sim_info, SimBuff.MOODHIDDEN_IMAGINATIVE) or has_sim_buff(sim_info, SimBuff.MOODHIDDEN_MUSER_TRAITREPLACEMENT) or has_sim_buff(sim_info, SimBuff.MOODHIDDEN_MUSERER_TRAITREPLACEMENT):
        score += 1
    if has_sim_buff(sim_info, SimBuff.MOODHIDDEN_SILLY) or has_sim_buff(sim_info, SimBuff.MOODHIDDEN_HYSTERICAL):
        score += 1
    if has_sim_buff(sim_info, SimBuff.MOODHIDDEN_DEPRESSED) or has_sim_buff(sim_info, SimBuff.MOODHIDDEN_GLOOMIER):
        score += -5
    if has_sim_buff(sim_info, SimBuff.MOODHIDDEN_STRESSED):
        score += -5
    if has_sim_buff(sim_info, SimBuff.MOODHIDDEN_MISERABLE):
        score += -5
    if has_sim_buff(sim_info, SimBuff.MOODHIDDEN_ENRAGED) or (has_sim_buff(sim_info, SimBuff.MOODHIDDEN_FURIOUS) or has_sim_buff(sim_info, SimBuff.MOODHIDDEN_HOTHEAD2)) or has_sim_buff(sim_info, SimBuff.MOODHIDDEN_HOTHEAD3):
        score += -5
    if has_sim_buff(target_sim_info, SimBuff.OBJECT_DRINK_FLIRTY):
        score += 10
    if has_sim_buff(target_sim_info, SimBuff.BROKENUPORDIVORCED_HIDDEN):
        score += -5
    if has_relationship_bit_with_sim(sim_info, target_sim_info, SimRelationshipBit.ROMANTIC_HASBEENUNFAITHFUL):
        score += -8
    if len(get_sim_ids_with_relationsip_bit(sim_info, SimRelationshipBit.SHORTTERM_JUSTBROKEUPORDIVORCED)) > 0:
        score += -18
    if has_sim_situation_job(sim_info, SimSituationJob.RESTAURANTDINER_SUB_NPC_BADDATE_ANGRYSIM):
        score += -25
    current_higiene_motive = get_sim_motive_value(sim_info, SimMotive.HYGIENE)
    if current_higiene_motive <= -50:
        score += -12
    if current_higiene_motive == -100:
        score += -8
    return score


def apply_asking_for_woohoo_relations(sim_identifier, target_sim_identifier, status, display_message=True):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    target_sim_info = TurboManagerUtil.Sim.get_sim_info(target_sim_identifier)
    if sim_info is None or target_sim_info is None:
        return
    set_sim_motive_value(sim_info, SimMotive.SOCIAL, get_sim_motive_value(sim_info, SimMotive.SOCIAL) + 8, skip_disabled=True)
    set_sim_motive_value(target_sim_info, SimMotive.SOCIAL, get_sim_motive_value(target_sim_info, SimMotive.SOCIAL) + 8, skip_disabled=True)
    if has_sim_trait(sim_info, SimTrait.EVIL) and has_sim_trait(sim_info, SimTrait.GOOD) or has_sim_trait(sim_info, SimTrait.GOOD) and has_sim_trait(sim_info, SimTrait.EVIL):
        if random.uniform(0, 1) <= 0.05:
            add_sim_buff(sim_info, SimBuff.GOODVSEVIL_ANGRY)
        if random.uniform(0, 1) <= 0.05:
            add_sim_buff(target_sim_info, SimBuff.GOODVSEVIL_ANGRY)
        if random.uniform(0, 1) <= 0.05:
            add_sim_buff(sim_info, SimBuff.GOODVSEVIL_SAD)
        if random.uniform(0, 1) <= 0.05:
            add_sim_buff(target_sim_info, SimBuff.GOODVSEVIL_SAD)
        change_sim_statistic_value(sim_info, 50, SimCommodity.TRAIT_ROMANTIC_AFFECTION)
    if status is True:
        TurboSimUtil.Gender.set_gender_preference(sim_info, TurboSimUtil.Gender.get_gender(target_sim_info), TurboSimUtil.Gender.get_gender_preference(sim_info, TurboSimUtil.Gender.get_gender(target_sim_info)) + 10)
        change_sim_statistic_value(sim_info, 10, SimCommodity.BUFF_SOCIAL_FLIRTYCONVERSATION)
        change_sim_statistic_value(target_sim_info, 10, SimCommodity.BUFF_SOCIAL_FLIRTYCONVERSATION)
        change_sim_statistic_value(sim_info, -10, SimCommodity.BUFF_SOCIAL_ANGRYCONVERSATION)
        change_sim_statistic_value(target_sim_info, -10, SimCommodity.BUFF_SOCIAL_ANGRYCONVERSATION)
        change_sim_statistic_value(sim_info, -10, SimCommodity.BUFF_SOCIAL_EMBARRASSINGCONVERSATION)
        change_sim_statistic_value(target_sim_info, -10, SimCommodity.BUFF_SOCIAL_EMBARRASSINGCONVERSATION)
        change_sim_statistic_value(sim_info, -10, SimCommodity.BUFF_SOCIAL_BORINGCONVERSATION)
        change_sim_statistic_value(target_sim_info, -10, SimCommodity.BUFF_SOCIAL_BORINGCONVERSATION)
        change_sim_statistic_value(sim_info, -10, SimCommodity.BUFF_SOCIAL_HAPPYCONVERSATION)
        change_sim_statistic_value(target_sim_info, -10, SimCommodity.BUFF_SOCIAL_HAPPYCONVERSATION)
        change_sim_statistic_value(sim_info, -10, SimCommodity.BUFF_SOCIAL_PLAYFULCONVERSATION)
        change_sim_statistic_value(target_sim_info, -10, SimCommodity.BUFF_SOCIAL_PLAYFULCONVERSATION)
        change_relationship_with_sim(sim_info, target_sim_info, ShortTermRelationshipTrackType.ROMANCE, 5)
        change_relationship_with_sim(target_sim_info, sim_info, ShortTermRelationshipTrackType.ROMANCE, 5)
        current_fun_short_rel_amount = get_relationship_with_sim(sim_info, target_sim_info, ShortTermRelationshipTrackType.FUN)
        short_fun_rel_gain_amount = 0
        if -100 <= current_fun_short_rel_amount <= -50:
            short_fun_rel_gain_amount += 20
        elif -50 <= current_fun_short_rel_amount <= -15:
            short_fun_rel_gain_amount += 10
        elif 15 <= current_fun_short_rel_amount <= 50:
            short_fun_rel_gain_amount += -10
        elif 50 <= current_fun_short_rel_amount <= 100:
            short_fun_rel_gain_amount += -20
        change_relationship_with_sim(sim_info, target_sim_info, ShortTermRelationshipTrackType.FUN, short_fun_rel_gain_amount)
        change_relationship_with_sim(target_sim_info, sim_info, ShortTermRelationshipTrackType.FUN, short_fun_rel_gain_amount)
        current_friendship_short_rel_amount = get_relationship_with_sim(sim_info, target_sim_info, ShortTermRelationshipTrackType.FRIENDSHIP)
        short_friendship_rel_gain_amount = 0
        if -100 <= current_friendship_short_rel_amount <= -50:
            short_friendship_rel_gain_amount += 20
        elif -50 <= current_friendship_short_rel_amount <= -15:
            short_friendship_rel_gain_amount += 10
        elif 15 <= current_friendship_short_rel_amount <= 50:
            short_friendship_rel_gain_amount += 5
        change_relationship_with_sim(sim_info, target_sim_info, ShortTermRelationshipTrackType.FRIENDSHIP, short_friendship_rel_gain_amount)
        change_relationship_with_sim(target_sim_info, sim_info, ShortTermRelationshipTrackType.FRIENDSHIP, short_friendship_rel_gain_amount)
        current_awkwardness_short_rel_amount = get_relationship_with_sim(sim_info, target_sim_info, ShortTermRelationshipTrackType.AWKWARDNESS)
        short_awkwardness_rel_gain_amount = 0
        if -100 <= current_awkwardness_short_rel_amount <= -50:
            short_awkwardness_rel_gain_amount += 20
        elif -50 <= current_awkwardness_short_rel_amount <= -15:
            short_awkwardness_rel_gain_amount += 10
        change_relationship_with_sim(sim_info, target_sim_info, ShortTermRelationshipTrackType.AWKWARDNESS, short_friendship_rel_gain_amount)
        change_relationship_with_sim(target_sim_info, sim_info, ShortTermRelationshipTrackType.AWKWARDNESS, short_friendship_rel_gain_amount)
        increase_sim_ww_statistic(sim_info, 'times_sex_got_accepted')
    else:
        change_relationship_with_sim(sim_info, target_sim_info, ShortTermRelationshipTrackType.AWKWARDNESS, -10)
        change_relationship_with_sim(target_sim_info, sim_info, ShortTermRelationshipTrackType.AWKWARDNESS, -10)
        current_romance_short_rel_amount = get_relationship_with_sim(sim_info, target_sim_info, ShortTermRelationshipTrackType.ROMANCE)
        short_romance_rel_gain_amount = 0
        if -100 <= current_romance_short_rel_amount <= -50:
            short_romance_rel_gain_amount += 20
        elif -50 <= current_romance_short_rel_amount <= -15:
            short_romance_rel_gain_amount += 10
        elif 15 <= current_romance_short_rel_amount <= 50:
            short_romance_rel_gain_amount += -10
        elif 50 <= current_romance_short_rel_amount <= 100:
            short_romance_rel_gain_amount += -20
        change_relationship_with_sim(sim_info, target_sim_info, ShortTermRelationshipTrackType.ROMANCE, short_romance_rel_gain_amount)
        change_relationship_with_sim(target_sim_info, sim_info, ShortTermRelationshipTrackType.ROMANCE, short_romance_rel_gain_amount)
        current_friendship_short_rel_amount = get_relationship_with_sim(sim_info, target_sim_info, ShortTermRelationshipTrackType.FRIENDSHIP)
        short_friendship_rel_gain_amount = 0
        if -100 <= current_friendship_short_rel_amount <= -50:
            short_friendship_rel_gain_amount += 20
        elif -50 <= current_friendship_short_rel_amount <= -15:
            short_friendship_rel_gain_amount += 10
        elif 15 <= current_friendship_short_rel_amount <= 50:
            short_friendship_rel_gain_amount += -10
        elif 50 <= current_friendship_short_rel_amount <= 100:
            short_friendship_rel_gain_amount += -20
        change_relationship_with_sim(sim_info, target_sim_info, ShortTermRelationshipTrackType.FRIENDSHIP, short_friendship_rel_gain_amount)
        change_relationship_with_sim(target_sim_info, sim_info, ShortTermRelationshipTrackType.FRIENDSHIP, short_friendship_rel_gain_amount)
        current_fun_short_rel_amount = get_relationship_with_sim(sim_info, target_sim_info, ShortTermRelationshipTrackType.FUN)
        short_fun_rel_gain_amount = 0
        if -50 <= current_fun_short_rel_amount <= -15:
            short_fun_rel_gain_amount += 10
        if 15 <= current_fun_short_rel_amount <= 50:
            short_fun_rel_gain_amount += -10
        elif 50 <= current_fun_short_rel_amount <= 100:
            short_fun_rel_gain_amount += -20
        change_relationship_with_sim(sim_info, target_sim_info, ShortTermRelationshipTrackType.FUN, short_fun_rel_gain_amount)
        change_relationship_with_sim(target_sim_info, sim_info, ShortTermRelationshipTrackType.FUN, short_fun_rel_gain_amount)
        current_friendship_rel_amount = get_relationship_with_sim(sim_info, target_sim_info, RelationshipTrackType.FRIENDSHIP)
        friendship_rel_gain_amount = 0
        if -100 <= current_friendship_rel_amount <= -40:
            friendship_rel_gain_amount += -2
        elif -40 <= current_friendship_rel_amount <= 0:
            friendship_rel_gain_amount += -2
        elif 0 <= current_friendship_rel_amount <= 20:
            friendship_rel_gain_amount += -2
        elif 20 <= current_friendship_rel_amount <= 40:
            friendship_rel_gain_amount += -2
        elif 40 <= current_friendship_rel_amount <= 80:
            friendship_rel_gain_amount += -3
        elif 80 <= current_friendship_rel_amount <= 100:
            friendship_rel_gain_amount += -4
        if has_sim_trait(sim_info, SimTrait.LONER) and sim_ev(sim_info).active_sex_handler is None and random.uniform(0, 1) <= 0.2:
            add_sim_buff(sim_info, SimBuff.EMBARRASSED_LONER)
        current_romance_rel_amount = get_relationship_with_sim(sim_info, target_sim_info, RelationshipTrackType.ROMANCE)
        romance_rel_gain_amount = 0
        if -100 <= current_romance_rel_amount <= -40:
            romance_rel_gain_amount += -2
        elif -40 <= current_romance_rel_amount <= 0:
            romance_rel_gain_amount += -2
        elif 0 <= current_romance_rel_amount <= 20:
            romance_rel_gain_amount += -2
        elif 20 <= current_romance_rel_amount <= 40:
            romance_rel_gain_amount += -2
        elif 40 <= current_romance_rel_amount <= 80:
            romance_rel_gain_amount += -2
        elif 80 <= current_romance_rel_amount <= 100:
            romance_rel_gain_amount += -2
        change_sim_statistic_value(sim_info, -20, SimCommodity.BUFF_SOCIAL_FLIRTYCONVERSATION)
        change_sim_statistic_value(target_sim_info, -20, SimCommodity.BUFF_SOCIAL_FLIRTYCONVERSATION)
        change_sim_statistic_value(sim_info, -20, SimCommodity.BUFF_SOCIAL_ANGRYCONVERSATION)
        change_sim_statistic_value(target_sim_info, -20, SimCommodity.BUFF_SOCIAL_ANGRYCONVERSATION)
        if has_sim_trait(sim_info, SimTrait.LONER):
            embarrassing_conversation_commodity_amount = 40
        else:
            embarrassing_conversation_commodity_amount = 20
        if sim_ev(sim_info).active_sex_handler is None:
            change_sim_statistic_value(sim_info, embarrassing_conversation_commodity_amount, SimCommodity.BUFF_SOCIAL_EMBARRASSINGCONVERSATION)
        change_sim_statistic_value(sim_info, -20, SimCommodity.BUFF_SOCIAL_BORINGCONVERSATION)
        change_sim_statistic_value(target_sim_info, -20, SimCommodity.BUFF_SOCIAL_BORINGCONVERSATION)
        change_sim_statistic_value(sim_info, -20, SimCommodity.BUFF_SOCIAL_HAPPYCONVERSATION)
        change_sim_statistic_value(target_sim_info, -20, SimCommodity.BUFF_SOCIAL_HAPPYCONVERSATION)
        change_sim_statistic_value(sim_info, -20, SimCommodity.BUFF_SOCIAL_PLAYFULCONVERSATION)
        change_sim_statistic_value(target_sim_info, -20, SimCommodity.BUFF_SOCIAL_PLAYFULCONVERSATION)
        add_relationsip_bit_with_sim(sim_info, target_sim_info, SimRelationshipBit.SHORTTERM_RECENTNEGATIVESOCIAL)
        if display_message is True and (TurboSimUtil.Sim.is_player(sim_info) or TurboSimUtil.Sim.is_player(target_sim_info)):
            display_notification(text=215847180, text_tokens=(target_sim_info, sim_info), title=0, secondary_icon=target_sim_info)
        increase_sim_ww_statistic(sim_info, 'times_sex_got_rejected')


def get_sim_relationship_sims(sim_identifier):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    return get_sim_ids_with_relationsip_bit(sim_info, SimRelationshipBit.ROMANTIC_MARRIED) or (get_sim_ids_with_relationsip_bit(sim_info, SimRelationshipBit.ROMANTIC_GETTINGMARRIED) or (get_sim_ids_with_relationsip_bit(sim_info, SimRelationshipBit.ROMANTIC_ENGAGED) or get_sim_ids_with_relationsip_bit(sim_info, SimRelationshipBit.ROMANTIC_SIGNIFICANT_OTHER)))

