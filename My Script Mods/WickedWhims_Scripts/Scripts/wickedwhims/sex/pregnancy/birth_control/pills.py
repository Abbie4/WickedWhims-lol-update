'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
import random
from enums.buffs_enum import SimBuff
from turbolib.manager_util import TurboManagerUtil
from turbolib.sim_util import TurboSimUtil
from turbolib.world_util import TurboWorldUtil
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.sex.settings.sex_settings import get_sex_setting, SexSetting, NPCBirthControlModeSetting, PregnancyModeSetting
from wickedwhims.sxex_bridge.statistics import increase_sim_ww_statistic
from wickedwhims.utils_buffs import has_sim_buff, add_sim_buff, remove_sim_buff
from wickedwhims.utils_interfaces import display_notification
from wickedwhims.utils_inventory import get_object_amount_in_sim_inventory, remove_object_from_sim_inventory, add_object_to_sim_inventory
BIRTH_CONTROL_PILL_OBJECT_ID = 14744913713073164047

def get_birth_control_pill_object_id():
    return BIRTH_CONTROL_PILL_OBJECT_ID


def take_birth_control_pill(sim_identifier, no_inventory=False):
    if no_inventory is False:
        sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
        if sim is None:
            return False
        if get_object_amount_in_sim_inventory(sim, BIRTH_CONTROL_PILL_OBJECT_ID) <= 0:
            return False
        if not remove_object_from_sim_inventory(sim, BIRTH_CONTROL_PILL_OBJECT_ID, 1):
            return False
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    sim_ev(sim_info).day_used_birth_control_pills = TurboWorldUtil.Time.get_absolute_days()
    sim_ev(sim_info).birth_control_pill_power = 1
    update_sim_birth_control_status_buff(sim_info)
    increase_sim_ww_statistic(sim_info, 'times_used_contraception')
    if TurboSimUtil.Sim.is_player(sim_info):
        display_notification(text=949418969, text_tokens=(sim_info,), title=1873179704, secondary_icon=sim_info)
    return True


def try_auto_apply_birth_control_pills(sim_identifier):
    if not get_sex_setting(SexSetting.BIRTH_CONTROL_AUTO_USE, variable_type=bool):
        return False
    if sim_ev(sim_identifier).auto_use_of_birth_pills is False:
        return False
    if get_sex_setting(SexSetting.PREGNANCY_MODE, variable_type=int) == PregnancyModeSetting.DISABLED:
        return False
    if get_sex_setting(SexSetting.PREGNANCY_MODE, variable_type=int) == PregnancyModeSetting.SIMPLE and get_sex_setting(SexSetting.SIMPLE_PREGNANCY_CHANCE, variable_type=int) <= 0 and get_sex_setting(SexSetting.SIMPLE_NPC_PREGNANCY_CHANCE, variable_type=int) <= 0:
        return False
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    if sim_ev(sim_info).day_used_birth_control_pills == TurboWorldUtil.Time.get_absolute_days():
        return True
    if not take_birth_control_pill(sim_identifier):
        return False
    return True


def give_sim_birth_control_pills(sim_identifier, amount=1):
    sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
    return add_object_to_sim_inventory(sim, BIRTH_CONTROL_PILL_OBJECT_ID, amount=amount)


def update_sim_birth_control_status_buff(sim_identifier):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    if sim_ev(sim_info).day_used_birth_control_pills == TurboWorldUtil.Time.get_absolute_days():
        if not has_sim_buff(sim_info, SimBuff.WW_PREGNANCY_IS_ON_BIRTH_CONTROL):
            add_sim_buff(sim_info, SimBuff.WW_PREGNANCY_IS_ON_BIRTH_CONTROL)
    elif has_sim_buff(sim_info, SimBuff.WW_PREGNANCY_IS_ON_BIRTH_CONTROL):
        remove_sim_buff(sim_info, SimBuff.WW_PREGNANCY_IS_ON_BIRTH_CONTROL)


def is_sim_allowed_for_free_birth_control(sim_identifier):
    random_inst = random.Random(TurboManagerUtil.Sim.get_sim_id(sim_identifier)/max(1, TurboWorldUtil.Time.get_absolute_days()))
    if get_sex_setting(SexSetting.NPC_BIRTH_CONTROL_MODE, variable_type=int) == NPCBirthControlModeSetting.SAFE:
        if random_inst.uniform(0, 1) > 0.1:
            return True
    elif get_sex_setting(SexSetting.NPC_BIRTH_CONTROL_MODE, variable_type=int) == NPCBirthControlModeSetting.MODERATE and random_inst.uniform(0, 1) > 0.38:
        return True
    return False


def update_sim_birth_control_power(sim_identifier):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    if sim_ev(sim_info).birth_control_pill_power > 0:
        birth_control_use_diff = TurboWorldUtil.Time.get_absolute_days() - sim_ev(sim_info).day_used_birth_control_pills
        if birth_control_use_diff > 0:
            power_difference = birth_control_use_diff*2.5
            birth_control_power = 1/power_difference
            if birth_control_power <= 0.15:
                birth_control_power = 0.0
            sim_ev(sim_info).birth_control_pill_power = birth_control_power

