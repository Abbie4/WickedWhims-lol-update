from cnutils.CNSimUtils import CNSimUtils
from enums.buffs_enum import SimBuff
from enums.motives_enum import SimMotive
from enums.situations_enum import SimSituation
from enums.traits_enum import SimTrait, LotTrait
from turbolib.manager_util import TurboManagerUtil
from turbolib.math_util import TurboMathUtil
from turbolib.resource_util import TurboResourceUtil
from turbolib.sim_util import TurboSimUtil
from turbolib.world_util import TurboWorldUtil
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.relationships.relationship_utils import get_sim_preferenced_genders
from wickedwhims.sex.autonomy.disabled_locations_handler import is_autonomy_sex_locations_disabled
from wickedwhims.sex.pregnancy.birth_control.birth_control_handler import is_sim_birth_control_safe
from wickedwhims.sex.pregnancy.native_pregnancy_handler import can_sim_get_pregnant
from wickedwhims.sex.pregnancy.pregnancy_interface import get_sim_current_pregnancy_chance
from wickedwhims.sex.relationship_handler import get_test_relationship_score, get_sim_relationship_sims, get_relationship_sex_acceptance_threshold
from wickedwhims.sex.settings.sex_settings import SexSetting, get_sex_setting, SexAutonomyLevelSetting, PregnancyModeSetting
from wickedwhims.sex.utils.sex_init import get_age_limits_for_sex
from wickedwhims.sxex_bridge.relationships import is_true_family_relationship
from wickedwhims.utils_autonomy import is_sim_allowed_for_autonomy
from wickedwhims.utils_buffs import has_sim_buffs
from wickedwhims.utils_motives import get_sim_motive_value
from wickedwhims.utils_sims import is_sim_available
from wickedwhims.utils_situations import has_sim_situations
from wickedwhims.utils_traits import has_sim_traits, has_sim_trait, has_current_lot_trait

def get_list_of_possible_sex_pairs(sims_list):
    checked_sims_pairs = list()
    relationships_list = list()
    for sim in sims_list:
        for target_sim in sims_list:
            if sim is target_sim:
                continue
            sims_pair = {TurboManagerUtil.Sim.get_sim_id(sim), TurboManagerUtil.Sim.get_sim_id(target_sim)}
            if sims_pair in checked_sims_pairs:
                continue
            checked_sims_pairs.append(sims_pair)
            sex_pair_score = get_sex_pair_score(sim, target_sim)
            if sex_pair_score >= get_relationship_sex_acceptance_threshold():
                relationships_list.append((sim, target_sim, sex_pair_score))
    return sorted(relationships_list, key=lambda x: x[2], reverse=True)


def is_sims_possible_sex_pair(sim_a, sim_b):
    sex_pair_score = get_sex_pair_score(sim_a, sim_b)
    if sex_pair_score >= get_relationship_sex_acceptance_threshold():
        return True
    return False


def get_sex_pair_score(sim_identifier, target_sim_identifier):
    if sim_identifier is target_sim_identifier:
        return -1
    age_limit = get_age_limits_for_sex((sim_identifier, target_sim_identifier))
    if TurboSimUtil.Age.is_younger_than(sim_identifier, age_limit[0]) or TurboSimUtil.Age.is_older_than(sim_identifier, age_limit[1]):
        return -1
    if TurboSimUtil.Age.is_younger_than(target_sim_identifier, age_limit[0]) or TurboSimUtil.Age.is_older_than(target_sim_identifier, age_limit[1]):
        return -1
    if TurboSimUtil.Gender.get_gender(sim_identifier) not in get_sim_preferenced_genders(target_sim_identifier):
        return -1
    if TurboSimUtil.Gender.get_gender(target_sim_identifier) not in get_sim_preferenced_genders(sim_identifier):
        return -1
    if is_true_family_relationship(sim_identifier, target_sim_identifier):
        return -1
    if not has_sim_trait(sim_identifier, SimTrait.WW_POLYAMOROUS) and not has_sim_trait(sim_identifier, SimTrait.COMMITMENTISSUES):
        sim_significant_relationships = get_sim_relationship_sims(sim_identifier)
        if sim_significant_relationships and TurboManagerUtil.Sim.get_sim_id(target_sim_identifier) not in sim_significant_relationships:
            return -1
    if get_sex_setting(SexSetting.AUTONOMY_RELATIONSHIP_AWARENESS, variable_type=bool) and not has_sim_trait(target_sim_identifier, SimTrait.WW_POLYAMOROUS) and not has_sim_trait(target_sim_identifier, SimTrait.COMMITMENTISSUES):
        target_significant_relationships = get_sim_relationship_sims(target_sim_identifier)
        if target_significant_relationships and TurboManagerUtil.Sim.get_sim_id(sim_identifier) not in target_significant_relationships:
            return -1
    relationship_score = get_test_relationship_score((sim_identifier, target_sim_identifier), skip_always_accept=True)
    return relationship_score


def get_available_for_sex_sims(only_on_hypersexual_lot=False, forbidden_traits=()):
    sims_list = set()
    for sim in TurboManagerUtil.Sim.get_all_sim_instance_gen(humans=True, pets=False):
        if TurboSimUtil.Age.is_younger_than(sim, TurboSimUtil.Age.CHILD):
            continue
        if not CNSimUtils.teen_sex_is_enabled() and CNSimUtils.is_child_or_teen(sim):
            continue
        if not get_sex_setting(SexSetting.PLAYER_AUTONOMY_STATE, variable_type=bool) and TurboSimUtil.Sim.is_player(sim):
            continue
        object_id = TurboResourceUtil.Resource.get_id(sim)
        if is_autonomy_sex_locations_disabled(object_id):
            continue
        if TurboWorldUtil.Time.get_absolute_ticks() < sim_ev(sim).last_sex_autonomy + get_time_between_sex_autonomy_attempts():
            continue
        if not sim_ev(sim).active_sex_handler is not None:
            if sim_ev(sim).active_pre_sex_handler is not None:
                continue
            if not is_sim_allowed_for_autonomy(sim):
                continue
            if not _is_sim_needs_fine(sim):
                continue
            if _is_sim_fearing_possible_pregnancy(sim):
                continue
            if not is_sim_available(sim):
                continue
            if _has_sim_sex_forbidden_traits(sim, forbidden_traits=forbidden_traits):
                continue
            if _has_sim_sex_forbidden_buffs(sim):
                continue
            if _is_sim_in_sex_forbidden_situation(sim):
                continue
            if only_on_hypersexual_lot is True and not TurboWorldUtil.Lot.is_position_on_active_lot(TurboSimUtil.Location.get_position(sim)):
                continue
            sims_list.add(sim)
    return sims_list


def get_time_between_sex_autonomy_attempts():
    if get_sex_setting(SexSetting.AUTONOMY_LEVEL, variable_type=int) == SexAutonomyLevelSetting.HIGH:
        return 360000
    if get_sex_setting(SexSetting.AUTONOMY_LEVEL, variable_type=int) == SexAutonomyLevelSetting.NORMAL:
        return 720000
    if get_sex_setting(SexSetting.AUTONOMY_LEVEL, variable_type=int) == SexAutonomyLevelSetting.LOW:
        return 1440000
    return 0


def sort_sex_pairs_for_lowest_distance(sims_pairs):
    return sorted(sims_pairs, key=lambda x: TurboMathUtil.Position.get_distance(TurboSimUtil.Location.get_position(x[0]), TurboSimUtil.Location.get_position(x[1])))


def is_sims_list_at_hypersexual_lot(sims_list):
    if has_current_lot_trait(LotTrait.WW_LOTTRAIT_HYPERSEXUAL):
        for sim in sims_list:
            if not TurboWorldUtil.Lot.is_position_on_active_lot(TurboSimUtil.Location.get_position(sim)):
                return False
        return True
    return False


def _has_sim_sex_forbidden_traits(sim_identifier, forbidden_traits=()):
    if has_sim_traits(sim_identifier, (SimTrait.HIDDEN_ISEVENTNPC_CHALLENGE, SimTrait.ISGRIMREAPER, SimTrait.BASEMENTAL_AYAHUASCA_SHAMAN) + forbidden_traits):
        return True
    return False


def _has_sim_sex_forbidden_buffs(sim_identifier):
    if has_sim_buffs(sim_identifier, (SimBuff.GETTINGMARRIED, SimBuff.DRAINED, SimBuff.PREGNANCY_INLABOR, SimBuff.WEDDINGARCH_FANTASIZE_COMMITMENTISSUES, SimBuff.WEDDINGARCH_FANTASIZEANGRY, SimBuff.WEDDINGARCH_FANTASIZEFLIRTY, SimBuff.WEDDINGARCH_FANTASIZEHAPPY, SimBuff.OBJECT_FITNESS_VERYFATIGUED, SimBuff.ROLE_IMPRISONED, SimBuff.CAREER_14_PRINCIPALSSPEECH, SimBuff.CAREER_22_CHEESYSPEECH, SimBuff.GRIMREAPER_ROLE, SimBuff.MOTIVES_PEEDSELF)):
        return True
    return False


def _is_sim_running_sex_forbidden_interactions(sim_identifier):
    forbidden_interactions = (106223,)
    for interaction_id in TurboSimUtil.Interaction.get_running_interactions_ids(sim_identifier):
        if interaction_id in forbidden_interactions:
            return True
    for interaction_id in TurboSimUtil.Interaction.get_queued_interactions_ids(sim_identifier):
        if interaction_id in forbidden_interactions:
            return True
    return False


def _is_sim_needs_fine(sim_identifier):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    is_sim_vampire = has_sim_trait(sim_info, SimTrait.OCCULTVAMPIRE)
    is_sim_plant = has_sim_trait(sim_info, SimTrait.PLANTSIM)
    is_sim_normal = not is_sim_vampire and not is_sim_plant
    hygiene_motive = get_sim_motive_value(sim_info, SimMotive.HYGIENE)
    if hygiene_motive < -89:
        return False
    if is_sim_normal is True:
        bladder_motive = get_sim_motive_value(sim_info, SimMotive.BLADDER)
        if bladder_motive < -59:
            return False
    if is_sim_normal or is_sim_plant:
        hunger_motive = get_sim_motive_value(sim_info, SimMotive.HUNGER)
        if hunger_motive < -59:
            return False
    if is_sim_normal or is_sim_plant:
        energy_motive = get_sim_motive_value(sim_info, SimMotive.ENERGY)
        if energy_motive < -51:
            return False
    if is_sim_vampire:
        power_motive = get_sim_motive_value(sim_info, SimMotive.VAMPIRE_POWER)
        if power_motive < -91:
            return False
    if is_sim_vampire:
        thirst_motive = get_sim_motive_value(sim_info, SimMotive.VAMPIRE_THIRST)
        if thirst_motive < -59:
            return False
    if is_sim_plant:
        water_motive = get_sim_motive_value(sim_info, SimMotive.PLANTSIM_WATER)
        if water_motive < -59:
            return False
    return True


def _is_sim_fearing_possible_pregnancy(sim_identifier):
    if TurboSimUtil.Sim.is_player(sim_identifier):
        return False
    if not can_sim_get_pregnant(sim_identifier):
        return False
    if is_sim_birth_control_safe(sim_identifier, allow_potentially=True):
        return False
    if get_sex_setting(SexSetting.AUTONOMY_NPC_PREGNANCY_AWARENESS, variable_type=bool) and get_sex_setting(SexSetting.PREGNANCY_MODE, variable_type=bool) == PregnancyModeSetting.MENSTRUAL_CYCLE and get_sim_current_pregnancy_chance(sim_identifier) > 0:
        return True
    return False


def _is_sim_in_sex_forbidden_situation(sim_identifier):
    if has_sim_situations(sim_identifier, (SimSituation.BARISTA_VENUE, SimSituation.HIREDNPC_BARISTA, SimSituation.BARBARTENDER, SimSituation.BARTENDER_RESTAURANT, SimSituation.HIREDNPC_BARTENDER, SimSituation.HIREDNPC_CATERER, SimSituation.HIREDNPC_CATERER_VEGETARIAN, SimSituation.HIREDNPC_DJ, SimSituation.HIREDNPC_DJ_LEVEL10, SimSituation.SINGLEJOB_CLUB_DJ, SimSituation.SINGLEJOB_CLUB_DJ_LEVEL10, SimSituation.HIREDNPC_ENTERTAINER_GUITAR, SimSituation.HIREDNPC_ENTERTAINER_MICCOMEDY, SimSituation.HIREDNPC_ENTERTAINER_ORGAN, SimSituation.HIREDNPC_ENTERTAINER_PIANO, SimSituation.HIREDNPC_ENTERTAINER_VIOLIN, SimSituation.BUTLER_SITUATION, SimSituation.GARDENER_SERVICE_SITUATION, SimSituation.NANNY_SITUATION, SimSituation.GYMTRAINER_VENUE, SimSituation.LANDLORD, SimSituation.LIBRARYVENUE_LIBRARIAN, SimSituation.MAID_SITUATION, SimSituation.MAILMAN_SITUATION, SimSituation.PIZZADELIVERY_NEW, SimSituation.FORESTRANGER_VACATIONARRIVAL, SimSituation.REFLEXOLOGIST_VENUE, SimSituation.REPAIR_SITUATION, SimSituation.TRAGICCLOWN, SimSituation.YOGAINSTRUCTOR_VENUE, SimSituation.MASSAGETHERAPIST_VENUE, SimSituation.MASSAGETHERAPIST_SERVICECALL, SimSituation.CHEFSITUATION, SimSituation.HOST_1, SimSituation.RESTAURANT_WAITSTAFF, SimSituation.RESTAURANTDINER_SUB_NPC_CRITIC, SimSituation.RESTAURANTDINERBACKGROUND_NPC_CRITIC, SimSituation.RETAILEMPLOYEE_HARDWORKER, SimSituation.RETAILEMPLOYEE_NPCSTORE_HARDWORKER, SimSituation.SINGLEJOB_COWORKER_RETAILEMPLOYEE, SimSituation.HIREDNPC_STALLVENDOR, SimSituation.HIREDNPC_VENDORSTALL, SimSituation.OPENSTREETS_STALLVENDOR, SimSituation.CAREER_DOCTOR_NPC_DOCTOR, SimSituation.CAREER_DOCTOR_NPC_ASSISTANT, SimSituation.CAREER_DOCTOR_NPC_DOCTOR_DIAGNOSER, SimSituation.CAREER_DOCTOR_NPC_NURSE, SimSituation.PATIENTEMERGENCY_COLLAPSEDPATIENT, SimSituation.PATIENTEMERGENCY_DELIVERBABY, SimSituation.PATIENTEMERGENCY_SAMPLEANALYSIS, SimSituation.CAREER_DOCTOR_NPC_PATIENT_ADMITTED, SimSituation.CAREER_DOCTOR_NPC_PATIENT_ADMITTED_RECLINE, SimSituation.CAREER_DOCTOR_AWAYEVENTS_HOUSECALLPATIENT, SimSituation.CAREER_DOCTOR_AWAYEVENTS_OUTBREAKPATIENT, SimSituation.CAREEREVENTSITUATIONS_DOCTOR_UNDERSTAFFED_COLLAPSEDPATIENT, SimSituation.CAREEREVENTSITUATIONS_DOCTORCAREER_ROUNDS_MID_COLLAPSEDPATIENT, SimSituation.CAREEREVENTSITUATIONS_DOCTORCAREER_ROUNDSHIGH_COLLAPSEDPATIENT, SimSituation.HOSPITALPATIENT_LOWLEVEL, SimSituation.HOSPITALPATIENT_LOWLEVEL_ELDER, SimSituation.HOSPITALPATIENT_LOWLEVEL_CHILD, SimSituation.HOSPITALPATIENT_HIGHLEVEL, SimSituation.HOSPITALPATIENT_DIAGNOSED_STARRYEYES, SimSituation.HOSPITALPATIENT_DIAGNOSED_LLAMAFLU, SimSituation.HOSPITALPATIENT_DIAGNOSED_GASANDGIGGLES, SimSituation.HOSPITALPATIENT_DIAGNOSED_BLOATYHEAD, SimSituation.HOSPITALPATIENT_ADMITTED, SimSituation.VET_EMPLOYEE, SimSituation.DETECTIVE_APB, SimSituation.DETECTIVE_APBNEUTRAL, SimSituation.CAREER_DETECTIVE_APBPLAYER, SimSituation.SINGLEJOB_COWORKER_SCIENTIST, SimSituation.SINGLEJOB_COWORKER_SCIENTIST_FRONTDESK, SimSituation.CAREEREVENTSITUATIONS_SCIENTISTCAREER_MAIN, SimSituation.GRIMREAPER, SimSituation.FIRE, SimSituation.BABYBIRTH_HOSPITAL, SimSituation.PARK_CHILDPLAYING, SimSituation.CAREGIVER_TODDLER, SimSituation.WEDDING)):
        return True
    return False

