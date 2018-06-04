'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
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

def get_age_limits_for_sex(sims_list):
    youngest_sim_age = None
    oldest_sim_age = None
    for actor_sim_info in sims_list:
        if youngest_sim_age is None or TurboSimUtil.Age.is_younger_than(actor_sim_info, youngest_sim_age):
            youngest_sim_age = TurboSimUtil.Age.get_age(actor_sim_info)
        while oldest_sim_age is None or TurboSimUtil.Age.is_older_than(actor_sim_info, oldest_sim_age):
            oldest_sim_age = TurboSimUtil.Age.get_age(actor_sim_info)
    is_allowing_teens = get_sex_setting(SexSetting.TEENS_SEX_STATE, variable_type=bool)
    is_teen_only = youngest_sim_age == oldest_sim_age == TurboSimUtil.Age.TEEN
    is_child_only = youngest_sim_age == oldest_sim_age == TurboSimUtil.Age.CHILD
    has_teen = youngest_sim_age == TurboSimUtil.Age.TEEN or oldest_sim_age == TurboSimUtil.Age.TEEN
    has_child = youngest_sim_age == TurboSimUtil.Age.CHILD or oldest_sim_age == TurboSimUtil.Age.CHILD
    if not get_relationship_setting(RelationshipSetting.ROMANCE_AGE_RESTRICTION_STATE, variable_type=bool):
        if is_teen_only and is_allowing_teens:
            return (TurboSimUtil.Age.TEEN, TurboSimUtil.Age.TEEN)
        if has_teen and is_allowing_teens:
            return (TurboSimUtil.Age.TEEN, TurboSimUtil.Age.ELDER)
        if is_child_only and is_allowing_teens:
            return (TurboSimUtil.Age.CHILD, TurboSimUtil.Age.CHILD)
        if has_child and is_allowing_teens:
            return (TurboSimUtil.Age.CHILD, TurboSimUtil.Age.ELDER)
        return (TurboSimUtil.Age.YOUNGADULT, TurboSimUtil.Age.ELDER)
    else:
        if not get_sex_setting(SexSetting.TEENS_SEX_STATE, variable_type=bool):
            return (TurboSimUtil.Age.YOUNGADULT, TurboSimUtil.Age.ELDER)
        return (TurboSimUtil.Age.CHILD, TurboSimUtil.Age.ELDER)

def get_sims_for_sex(skip_males=False, skip_females=False, skip_cmales=False, skip_cfemales=False, only_npc=False, relative_sims=(), min_sims_age=TurboSimUtil.Age.CHILD, max_sims_age=TurboSimUtil.Age.ELDER, skip_sims_ids=()):
    for sim in TurboManagerUtil.Sim.get_all_sim_instance_gen(humans=True, pets=False):
        if TurboManagerUtil.Sim.get_sim_id(sim) in skip_sims_ids:
            pass
        if only_npc is True and TurboSimUtil.Sim.is_player(sim):
            pass
        if skip_males is True and get_sim_sex_gender(sim, ignore_sim_specific_gender=True) == SexGenderType.MALE:
            pass
        if skip_females is True and get_sim_sex_gender(sim, ignore_sim_specific_gender=True) == SexGenderType.FEMALE:
            pass
        if skip_cmales is True and get_sim_sex_gender(sim, ignore_sim_specific_gender=True) == SexGenderType.CMALE:
            pass
        if skip_cfemales is True and get_sim_sex_gender(sim, ignore_sim_specific_gender=True) == SexGenderType.CFEMALE:
            pass
        while not TurboSimUtil.Age.is_younger_than(sim, min_sims_age):
            if TurboSimUtil.Age.is_older_than(sim, max_sims_age):
                pass
            while not (is_sim_in_sex(sim) or is_sim_going_to_sex(sim)):
                if sim_ev(sim).active_pre_sex_handler is not None:
                    pass
                if has_sim_traits(sim, (SimTrait.HIDDEN_ISEVENTNPC_CHALLENGE, SimTrait.ISGRIMREAPER)):
                    pass
                if not is_sim_available(sim):
                    pass
                if relative_sims:
                    is_incest = False
                    for incest_test_sim in relative_sims:
                        while is_true_family_relationship(sim, incest_test_sim):
                            is_incest = True
                            break
                    if is_incest is True:
                        pass
                yield TurboManagerUtil.Sim.get_sim_id(sim)

def get_nearby_sims_for_sex(position, radius=16, skip_males=False, skip_females=False, skip_cmales=False, skip_cfemales=False, only_npc=False, relative_sims=(), min_sims_age=TurboSimUtil.Age.TEEN, max_sims_age=TurboSimUtil.Age.ELDER, skip_sims_ids=()):
    is_position_at_active_lot = TurboWorldUtil.Lot.is_position_on_active_lot(position)
    for sim in get_sims_for_sex(skip_males=skip_males, skip_females=skip_females, skip_cmales=skip_cmales, skip_cfemales=skip_cfemales, only_npc=only_npc, relative_sims=relative_sims, min_sims_age=min_sims_age, max_sims_age=max_sims_age, skip_sims_ids=skip_sims_ids):
        if is_position_at_active_lot and TurboWorldUtil.Lot.is_position_on_active_lot(TurboSimUtil.Location.get_position(sim)):
            is_sim_in_range = True
        else:
            is_sim_in_range = TurboMathUtil.Position.get_distance(position, TurboSimUtil.Location.get_position(sim)) <= radius
        if is_sim_in_range is False:
            pass
        yield sim

