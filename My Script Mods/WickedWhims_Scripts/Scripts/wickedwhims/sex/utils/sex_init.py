from enums.traits_enum import SimTrait
from turbolib.manager_util import TurboManagerUtil
from turbolib.math_util import TurboMathUtil
from turbolib.sim_util import TurboSimUtil
from turbolib.world_util import TurboWorldUtil
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.relationships.relationship_settings import get_relationship_setting, RelationshipSetting
from wickedwhims.sex.enums.sex_gender import SexGenderType, get_sim_sex_gender
from wickedwhims.sex.settings.sex_settings import get_sex_setting, SexSetting
from wickedwhims.sxex_bridge.relationships import is_true_family_relationship
from wickedwhims.sxex_bridge.sex import is_sim_in_sex, is_sim_going_to_sex
from wickedwhims.utils_sims import is_sim_available
from wickedwhims.utils_traits import has_sim_traits
from turbolib.special.custom_exception_watcher import log_message


def get_age_limits_for_sex(sims_list):
    youngest_sim_age = None
    oldest_sim_age = None
    for actor_sim_info in sims_list:
        if actor_sim_info is None:
            continue
        if youngest_sim_age is None or TurboSimUtil.Age.is_younger_than(actor_sim_info, youngest_sim_age):
            youngest_sim_age = TurboSimUtil.Age.get_age(actor_sim_info)
        if oldest_sim_age is None or TurboSimUtil.Age.is_older_than(actor_sim_info, oldest_sim_age):
            oldest_sim_age = TurboSimUtil.Age.get_age(actor_sim_info)
    is_allowing_teens = get_sex_setting(SexSetting.TEENS_SEX_STATE, variable_type=bool)
    is_child_only = youngest_sim_age == oldest_sim_age == TurboSimUtil.Age.CHILD
    is_teen_only = youngest_sim_age == oldest_sim_age == TurboSimUtil.Age.TEEN
    has_teen = youngest_sim_age == TurboSimUtil.Age.TEEN or oldest_sim_age == TurboSimUtil.Age.TEEN
    has_child = youngest_sim_age == TurboSimUtil.Age.CHILD or oldest_sim_age == TurboSimUtil.Age.CHILD
    if not get_relationship_setting(RelationshipSetting.ROMANCE_AGE_RESTRICTION_STATE, variable_type=bool):
        if is_child_only and is_allowing_teens:
            return (TurboSimUtil.Age.CHILD, TurboSimUtil.Age.CHILD)
        if is_teen_only and is_allowing_teens:
            return (TurboSimUtil.Age.TEEN, TurboSimUtil.Age.TEEN)
        if has_child and is_allowing_teens:
            return (TurboSimUtil.Age.CHILD, TurboSimUtil.Age.ELDER)
        if has_teen and is_allowing_teens:
            return (TurboSimUtil.Age.TEEN, TurboSimUtil.Age.ELDER)
        return (TurboSimUtil.Age.YOUNGADULT, TurboSimUtil.Age.ELDER)
    else:
        if not get_sex_setting(SexSetting.TEENS_SEX_STATE, variable_type=bool):
            return (TurboSimUtil.Age.YOUNGADULT, TurboSimUtil.Age.ELDER)
        return (TurboSimUtil.Age.CHILD, TurboSimUtil.Age.ELDER)


def get_sims_for_sex(skip_males=False, skip_females=False, skip_cmales=False, skip_cfemales=False, only_npc=False, relative_sims=(), min_sims_age=TurboSimUtil.Age.CHILD, max_sims_age=TurboSimUtil.Age.ELDER, skip_sims_ids=()):
    log_message("Is skipping males: " + str(skip_males))
    log_message("Is skipping females: " + str(skip_females))
    log_message("Is skipping cmales: " + str(skip_cmales))
    log_message("Is skipping cfemales: " + str(skip_cfemales))
    log_message("Min age: " + str(min_sims_age))
    log_message("Max age: " + str(max_sims_age))
    for sim in TurboManagerUtil.Sim.get_all_sim_instance_gen(humans=True, pets=False):
        if TurboManagerUtil.Sim.get_sim_id(sim) in skip_sims_ids:
            continue
        if only_npc is True and TurboSimUtil.Sim.is_player(sim):
            continue
        if skip_cmales is True and get_sim_sex_gender(sim, ignore_sim_specific_gender=True) == SexGenderType.CMALE:
            continue
        if skip_males is True and get_sim_sex_gender(sim, ignore_sim_specific_gender=True) == SexGenderType.MALE:
            continue
        if skip_cfemales is True and get_sim_sex_gender(sim, ignore_sim_specific_gender=True) == SexGenderType.CFEMALE:
            continue
        if skip_females is True and get_sim_sex_gender(sim, ignore_sim_specific_gender=True) == SexGenderType.FEMALE:
            continue
        if not TurboSimUtil.Age.is_younger_than(sim, min_sims_age) and not TurboSimUtil.Age.is_older_than(sim, max_sims_age):
            if not (is_sim_in_sex(sim) or is_sim_going_to_sex(sim)):
                if sim_ev(sim).active_pre_sex_handler is not None:
                    log_message("No active_pre_sex_handler")
                    continue
                if has_sim_traits(sim, (SimTrait.HIDDEN_ISEVENTNPC_CHALLENGE, SimTrait.ISGRIMREAPER)):
                    continue
                if not is_sim_available(sim):
                    sim_name = TurboSimUtil.Name.get_name(sim)
                    log_message("Sim is not available " + sim_name[0] + " " + sim_name[1])
                    continue
                if relative_sims:
                    log_message("Sim is relative")
                    is_incest = False
                    for incest_test_sim in relative_sims:
                        log_message("Testing incest")
                        if is_true_family_relationship(sim, incest_test_sim):
                            log_message("Is true family relationship")
                            is_incest = True
                            break
                    if is_incest is True:
                        log_message("Is incest")
                        continue
                yield TurboManagerUtil.Sim.get_sim_id(sim)


def get_nearby_sims_for_sex(position, radius=16, skip_males=False, skip_females=False, skip_cmales=False, skip_cfemales=False, only_npc=False, relative_sims=(), min_sims_age=TurboSimUtil.Age.CHILD, max_sims_age=TurboSimUtil.Age.ELDER, skip_sims_ids=()):
    is_position_at_active_lot = TurboWorldUtil.Lot.is_position_on_active_lot(position)
    for sim in get_sims_for_sex(skip_males=skip_males, skip_females=skip_females, skip_cmales=skip_cmales, skip_cfemales=skip_cfemales, only_npc=only_npc, relative_sims=relative_sims, min_sims_age=min_sims_age, max_sims_age=max_sims_age, skip_sims_ids=skip_sims_ids):
        if is_position_at_active_lot and TurboWorldUtil.Lot.is_position_on_active_lot(TurboSimUtil.Location.get_position(sim)):
            is_sim_in_range = True
        else:
            is_sim_in_range = TurboMathUtil.Position.get_distance(position, TurboSimUtil.Location.get_position(sim)) <= radius
        if is_sim_in_range is False:
            continue
        yield sim

