'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
import random
from enums.buffs_enum import SimBuff
from enums.traits_enum import SimTrait
from turbolib.manager_util import TurboManagerUtil
from turbolib.sim_util import TurboSimUtil
from turbolib.special.custom_exception_watcher import exception_watch
from turbolib.world_util import TurboWorldUtil
from turbolib.wrappers.commands import register_game_command, TurboCommandType
from wickedwhims.main.basemental_handler import is_sim_on_basemental_drugs, is_basemental_drugs_installed
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.sex.pregnancy.native_pregnancy_handler import can_sim_impregnate, can_sim_get_pregnant
from wickedwhims.sex.settings.sex_settings import PregnancyModeSetting, SexSetting, get_sex_setting, MenstrualCycleDurationSetting
from wickedwhims.utils_buffs import add_sim_buff, remove_sim_buff, has_sim_buff
from wickedwhims.utils_traits import has_sim_trait
ABSOLUTE_DAYS_OFFSET = 31415

def update_period_related_buffs(sim_identifier):
    clear_period_related_buffs(sim_identifier)
    if get_sex_setting(SexSetting.PREGNANCY_MODE, variable_type=int) != PregnancyModeSetting.MENSTRUAL_CYCLE:
        return
    if not can_sim_have_period(sim_identifier):
        return
    if TurboSimUtil.Pregnancy.is_pregnant(sim_identifier):
        return
    apply_period_related_buffs(sim_identifier)

def apply_period_related_buffs(sim_identifier):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    sim_id = TurboManagerUtil.Sim.get_sim_id(sim_info)
    menstrual_cycle_days = get_sim_menstrual_cycle_days(sim_info)
    absolute_days = TurboWorldUtil.Time.get_absolute_days() + ABSOLUTE_DAYS_OFFSET
    cycle_day = absolute_days % menstrual_cycle_days + 1
    cycle_number = max(1, int(absolute_days/menstrual_cycle_days))
    random_inst = random.Random(sim_id/cycle_number)
    (_, _, cramps_duration, period_duration) = get_cycle_durations()
    is_on_birth_control = sim_ev(sim_info).day_used_birth_control_pills == TurboWorldUtil.Time.get_absolute_days()
    if is_on_birth_control is True:
        period_duration = 0
    else:
        period_duration = random_inst.randint(*period_duration)
    if period_duration > 0 and cycle_day <= period_duration:
        if has_sim_trait(sim_info, SimTrait.OCCULTVAMPIRE):
            period_buff = SimBuff.WW_PREGNANCY_PERIOD_VAMPIRE_UNCOMFORTABLE
        else:
            period_buff = random_inst.choice((SimBuff.WW_PREGNANCY_PERIOD_FINE, SimBuff.WW_PREGNANCY_PERIOD_FLIRTY, SimBuff.WW_PREGNANCY_PERIOD_DAZED, SimBuff.WW_PREGNANCY_PERIOD_SAD, SimBuff.WW_PREGNANCY_PERIOD_TENSE, SimBuff.WW_PREGNANCY_PERIOD_UNCOMFORTABLE))
        add_sim_buff(sim_info, period_buff)
    is_using_weed = is_basemental_drugs_installed() and (has_sim_buff(sim_info, SimBuff.BASEMENTAL_WEED_HIGH_ON_AK47) or (has_sim_buff(sim_info, SimBuff.BASEMENTAL_WEED_HIGH_ON_OG_KUSH) or has_sim_buff(sim_info, SimBuff.BASEMENTAL_WEED_HIGH_ON_PURPLE_HAZE)))
    if is_on_birth_control is True or is_using_weed is True:
        cramps_duration = 0
    else:
        cramps_duration = random_inst.randint(*cramps_duration) if random_inst.uniform(0, 1) <= 0.5 else 0
    if cramps_duration > 0 and cycle_day > menstrual_cycle_days - cramps_duration:
        add_sim_buff(sim_info, random_inst.choice((SimBuff.WW_PREGNANCY_CRAMPS_LOW, SimBuff.WW_PREGNANCY_CRAMPS_MEDIUM, SimBuff.WW_PREGNANCY_CRAMPS_HIGH)), reason=2061236478)

def clear_period_related_buffs(sim_identifier):
    remove_sim_buff(sim_identifier, SimBuff.WW_PREGNANCY_PERIOD_FINE)
    remove_sim_buff(sim_identifier, SimBuff.WW_PREGNANCY_PERIOD_FLIRTY)
    remove_sim_buff(sim_identifier, SimBuff.WW_PREGNANCY_PERIOD_DAZED)
    remove_sim_buff(sim_identifier, SimBuff.WW_PREGNANCY_PERIOD_SAD)
    remove_sim_buff(sim_identifier, SimBuff.WW_PREGNANCY_PERIOD_TENSE)
    remove_sim_buff(sim_identifier, SimBuff.WW_PREGNANCY_PERIOD_UNCOMFORTABLE)
    remove_sim_buff(sim_identifier, SimBuff.WW_PREGNANCY_PERIOD_VAMPIRE_UNCOMFORTABLE)
    remove_sim_buff(sim_identifier, SimBuff.WW_PREGNANCY_CRAMPS_LOW)
    remove_sim_buff(sim_identifier, SimBuff.WW_PREGNANCY_CRAMPS_MEDIUM)
    remove_sim_buff(sim_identifier, SimBuff.WW_PREGNANCY_CRAMPS_HIGH)

def can_sim_have_period(sim_identifier):
    if TurboSimUtil.Age.is_younger_than(sim_identifier, TurboSimUtil.Age.CHILD):
        return False
    if TurboSimUtil.Age.is_older_than(sim_identifier, TurboSimUtil.Age.ELDER, or_equal=True):
        return False
    if not get_sex_setting(SexSetting.TEENS_SEX_STATE, variable_type=bool) and (TurboSimUtil.Age.get_age(sim_identifier) == TurboSimUtil.Age.TEEN or TurboSimUtil.Age.get_age(sim_identifier) == TurboSimUtil.Age.CHILD):
        return False
    if not has_sim_trait(sim_identifier, SimTrait.GENDEROPTIONS_PREGNANCY_CANBEIMPREGNATED):
        return False
    if has_sim_trait(sim_identifier, SimTrait.WW_INFERTILE):
        return False
    if has_sim_trait(sim_identifier, SimTrait.PLANTSIM):
        return False
    return True

def is_sim_on_period(sim_identifier):
    sim_id = TurboManagerUtil.Sim.get_sim_id(sim_identifier)
    menstrual_cycle_days = get_sim_menstrual_cycle_days(sim_identifier)
    absolute_days = TurboWorldUtil.Time.get_absolute_days() + ABSOLUTE_DAYS_OFFSET
    cycle_day = absolute_days % menstrual_cycle_days + 1
    cycle_number = max(1, int(absolute_days/menstrual_cycle_days))
    random_int = random.Random(sim_id/cycle_number)
    (_, _, _, period_duration) = get_cycle_durations()
    period_duration = random_int.randint(*period_duration)
    return cycle_day <= period_duration

def apply_pregnancy_boost_data(sim_identifier):
    absolute_days = TurboWorldUtil.Time.get_absolute_days() + ABSOLUTE_DAYS_OFFSET
    sim_ev(sim_identifier).pregnancy_fertility_boost = (absolute_days, random.uniform(1.5, 2.5))

def reset_pregnancy_boost_data(sim_identifier):
    absolute_days = TurboWorldUtil.Time.get_absolute_days() + ABSOLUTE_DAYS_OFFSET
    menstrual_cycle_days = get_sim_menstrual_cycle_days(sim_identifier)
    if absolute_days > sim_ev(sim_identifier).pregnancy_fertility_boost[0] + menstrual_cycle_days:
        sim_ev(sim_identifier).pregnancy_fertility_boost = (0, 1.0)

def get_sim_current_menstrual_pregnancy_chance(sim_identifier):
    if has_sim_trait(sim_identifier, SimTrait.WW_INFERTILE):
        return 0.0
    if has_sim_trait(sim_identifier, SimTrait.GENDEROPTIONS_PREGNANCY_CANBEIMPREGNATED):
        return _get_sim_current_menstrual_pregnancy_chance(sim_identifier)
    if has_sim_trait(sim_identifier, SimTrait.GENDEROPTIONS_PREGNANCY_CANIMPREGNATE):
        return _get_sim_current_menstrual_impregnation_chance(sim_identifier)
    return 0.0

def _get_sim_current_menstrual_impregnation_chance(sim_identifier):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    if not can_sim_impregnate(sim_info):
        return 0.0
    sim_age = TurboSimUtil.Age.get_age(sim_info)
    result = 0.0
    if sim_age == TurboSimUtil.Age.CHILD:
        result = 0.8
    if sim_age == TurboSimUtil.Age.TEEN:
        result = 0.9
    elif sim_age == TurboSimUtil.Age.YOUNGADULT:
        result = 0.91
    elif sim_age == TurboSimUtil.Age.ADULT:
        result = 0.85
    elif sim_age == TurboSimUtil.Age.ELDER:
        result = 0.75
    if has_sim_trait(sim_info, SimTrait.FERTILE):
        result += result*0.2
    if is_sim_on_basemental_drugs(sim_info, skip_weed=True):
        result -= result*0.25
    return result

def _get_sim_current_menstrual_pregnancy_chance(sim_identifier):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    if not can_sim_get_pregnant(sim_info):
        return 0.0
    pregnancy_matrix = get_sim_menstrual_pregnancy_chance_matrix(sim_info)
    menstrual_cycle_days = get_sim_menstrual_cycle_days(sim_info)
    cycle_day = (TurboWorldUtil.Time.get_absolute_days() + ABSOLUTE_DAYS_OFFSET) % menstrual_cycle_days + 1
    if cycle_day not in pregnancy_matrix:
        return 0.0
    pregnancy_chance = pregnancy_matrix[cycle_day]
    if is_sim_on_basemental_drugs(sim_info, skip_weed=True):
        pregnancy_chance -= pregnancy_chance*0.25
    pregnancy_chance *= max(1, sim_ev(sim_info).pregnancy_fertility_boost[1])
    return min(pregnancy_chance, 1.0)

def get_sim_menstrual_cycle_days(sim_identifier):
    sim_id = TurboManagerUtil.Sim.get_sim_id(sim_identifier)
    random_int = random.Random(sim_id)
    (adult_cycle, teen_cycle, _, _) = get_cycle_durations()
    if TurboSimUtil.Age.get_age(sim_identifier) == TurboSimUtil.Age.TEEN or TurboSimUtil.Age.get_age(sim_identifier) == TurboSimUtil.Age.CHILD:
        menstrual_cycle_days = random_int.randint(*teen_cycle)
    else:
        menstrual_cycle_days = random_int.randint(*adult_cycle)
    return menstrual_cycle_days

def get_sim_days_till_ovulation(sim_identifier):
    menstrual_cycle_days = get_sim_menstrual_cycle_days(sim_identifier)
    (_, _, _, ovulation_day) = get_fertility_days_data(menstrual_cycle_days)
    absolute_days = TurboWorldUtil.Time.get_absolute_days() + ABSOLUTE_DAYS_OFFSET
    current_menstrual_cycle_day = absolute_days % menstrual_cycle_days + 1
    target_day = ovulation_day - current_menstrual_cycle_day
    if target_day >= 0:
        return target_day
    return menstrual_cycle_days + target_day

def get_sim_menstrual_pregnancy_chance_matrix(sim_identifier):
    menstrual_cycle_days = get_sim_menstrual_cycle_days(sim_identifier)
    (before_fertile_window_start, fertile_window_start, most_fertile_window_start, ovulation_day) = get_fertility_days_data(menstrual_cycle_days)
    (before_fertile_window_chance, fertile_window_chance, most_fertile_window_chance, ovulation_day_chance) = get_fertility_chances_data()
    sim_id = TurboManagerUtil.Sim.get_sim_id(sim_identifier)
    absolute_days = max(1, TurboWorldUtil.Time.get_absolute_days() + ABSOLUTE_DAYS_OFFSET)
    random_int = random.Random(sim_id/absolute_days)
    fertility_bonus = has_sim_trait(sim_identifier, SimTrait.FERTILE)
    pregnancy_matrix = dict()
    for day in range(menstrual_cycle_days):
        while not day > ovulation_day:
            if day < before_fertile_window_start:
                pass
            if day == ovulation_day:
                pregnancy_matrix[day] = random_int.uniform(*ovulation_day_chance)
            elif day >= most_fertile_window_start:
                pregnancy_matrix[day] = random_int.uniform(*most_fertile_window_chance)
            elif day >= fertile_window_start:
                pregnancy_matrix[day] = random_int.uniform(*fertile_window_chance)
            elif day >= before_fertile_window_start:
                pregnancy_matrix[day] = random_int.uniform(*before_fertile_window_chance)
            while fertility_bonus is True:
                pregnancy_matrix[day] += pregnancy_matrix[day]*0.2
    return pregnancy_matrix

def get_fertility_chances_data():
    before_fertile_window_chance = (0.0, 0.1)
    fertile_window_chance = (0.15, 0.21)
    most_fertile_window_chance = (0.31, 0.36)
    ovulation_day_chance = (0.49, 0.84)
    return (before_fertile_window_chance, fertile_window_chance, most_fertile_window_chance, ovulation_day_chance)

def get_fertility_days_data(menstrual_cycle_days):
    if _get_menstrual_cycle_duration() == MenstrualCycleDurationSetting.VERY_LONG:
        ovulation_day = menstrual_cycle_days - 14
        most_fertile_window_start = ovulation_day - 2
        fertile_window_start = ovulation_day - 5
        before_fertile_window_start = ovulation_day - 6
        return (before_fertile_window_start, fertile_window_start, most_fertile_window_start, ovulation_day)
    if _get_menstrual_cycle_duration() == MenstrualCycleDurationSetting.LONG:
        ovulation_day = menstrual_cycle_days - 8
        most_fertile_window_start = ovulation_day - 2
        fertile_window_start = ovulation_day - 5
        before_fertile_window_start = ovulation_day - 6
        return (before_fertile_window_start, fertile_window_start, most_fertile_window_start, ovulation_day)
    if _get_menstrual_cycle_duration() == MenstrualCycleDurationSetting.NORMAL:
        ovulation_day = menstrual_cycle_days - 1
        most_fertile_window_start = ovulation_day - 1
        fertile_window_start = ovulation_day - 3
        before_fertile_window_start = ovulation_day - 4
        return (before_fertile_window_start, fertile_window_start, most_fertile_window_start, ovulation_day)
    if _get_menstrual_cycle_duration() == MenstrualCycleDurationSetting.SHORT:
        ovulation_day = menstrual_cycle_days - 1
        most_fertile_window_start = ovulation_day - 1
        fertile_window_start = ovulation_day - 2
        before_fertile_window_start = ovulation_day - 3
        return (before_fertile_window_start, fertile_window_start, most_fertile_window_start, ovulation_day)
    return (0, 0, 0, 0)

def get_cycle_durations():
    if _get_menstrual_cycle_duration() == MenstrualCycleDurationSetting.VERY_LONG:
        adult_cycle = (21, 30)
        teen_cycle = (21, 40)
        period_duration = (2, 4)
        cramps_duration = (1, 2)
        return (adult_cycle, teen_cycle, cramps_duration, period_duration)
    if _get_menstrual_cycle_duration() == MenstrualCycleDurationSetting.LONG:
        adult_cycle = (18, 24)
        teen_cycle = (18, 30)
        period_duration = (2, 4)
        cramps_duration = (1, 2)
        return (adult_cycle, teen_cycle, cramps_duration, period_duration)
    if _get_menstrual_cycle_duration() == MenstrualCycleDurationSetting.NORMAL:
        adult_cycle = (8, 10)
        teen_cycle = (8, 15)
        period_duration = (1, 2)
        cramps_duration = (1, 1)
        return (adult_cycle, teen_cycle, cramps_duration, period_duration)
    if _get_menstrual_cycle_duration() == MenstrualCycleDurationSetting.SHORT:
        adult_cycle = (6, 7)
        teen_cycle = (6, 10)
        period_duration = (1, 1)
        cramps_duration = (1, 1)
        return (adult_cycle, teen_cycle, cramps_duration, period_duration)
    return ((0, 0), (0, 0), (0, 0), (0, 0))

@exception_watch()
def _get_menstrual_cycle_duration():
    if get_sex_setting(SexSetting.MENSTRUAL_CYCLE_DURATION, variable_type=int) == MenstrualCycleDurationSetting.AUTO:
        sims_age_speed = TurboSimUtil.Age.get_global_age_speed()
        if sims_age_speed == TurboSimUtil.Age.AgeSpeed.SLOW:
            return MenstrualCycleDurationSetting.LONG
        if sims_age_speed == TurboSimUtil.Age.AgeSpeed.NORMAL:
            return MenstrualCycleDurationSetting.NORMAL
        if sims_age_speed == TurboSimUtil.Age.AgeSpeed.FAST:
            return MenstrualCycleDurationSetting.SHORT
        return MenstrualCycleDurationSetting.NORMAL
    return get_sex_setting(SexSetting.MENSTRUAL_CYCLE_DURATION, variable_type=int)

@register_game_command('ww.shift_menstrual_days', command_type=TurboCommandType.LIVE)
def _wickedwhims_command_shift_menstrual_days(output=None):
    global ABSOLUTE_DAYS_OFFSET
    ABSOLUTE_DAYS_OFFSET += 1
    for sim_info in TurboManagerUtil.Sim.get_all_sim_info_gen(humans=True, pets=False):
        update_period_related_buffs(sim_info)
    output('Menstrual Cycle days have shifted.')

