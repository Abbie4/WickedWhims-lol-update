'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''from enums.buffs_enum import SimBufffrom enums.traits_enum import SimTraitfrom turbolib.manager_util import TurboManagerUtilfrom turbolib.world_util import TurboWorldUtilfrom wickedwhims.main.sim_ev_handler import sim_evfrom wickedwhims.sex.enums.sex_type import SexCategoryTypefrom wickedwhims.sex.pregnancy.native_pregnancy_handler import can_sim_get_pregnant, can_sim_impregnatefrom wickedwhims.sex.settings.sex_settings import get_sex_setting, SexSetting, PregnancyModeSettingfrom wickedwhims.sxex_bridge.statistics import increase_sim_ww_statisticfrom wickedwhims.utils_buffs import has_sim_buff, add_sim_buff, remove_sim_bufffrom wickedwhims.utils_interfaces import display_notificationfrom wickedwhims.utils_inventory import add_object_to_sim_inventory, get_object_amount_in_sim_inventory, remove_object_from_sim_inventoryfrom wickedwhims.utils_traits import has_sim_traitCONDOM_WRAPPER_OBJECT_ID = 11033454205624062315
def get_condom_wrapper_object_id():
    return CONDOM_WRAPPER_OBJECT_ID

def try_to_take_and_use_condoms(sim_identifier, silent_failure=False):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    (result, amount) = _try_to_take_and_use_condoms(sim_info)
    if sim_ev(sim_info).active_sex_handler is not None and not sim_ev(sim_info).active_sex_handler.is_npc_only():
        if result:
            if amount == 1:
                display_notification(text=4082674743, text_tokens=(sim_info,), title=1873179704, secondary_icon=sim_info)
            else:
                display_notification(text=2429963938, text_tokens=(str(amount), sim_info), title=1873179704, secondary_icon=sim_info)
                if silent_failure is False:
                    display_notification(text=3990632821, title=1873179704, secondary_icon=sim_info)
        elif silent_failure is False:
            display_notification(text=3990632821, title=1873179704, secondary_icon=sim_info)
    return result

def _try_to_take_and_use_condoms(sim_identifier):
    sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
    if sim is None:
        return (False, 0)
    if sim_ev(sim).active_sex_handler is None:
        return (False, 0)
    sims_that_can_impregnate_list = list()
    for actor_sim in sim_ev(sim).active_sex_handler.get_actors_sim_info_gen():
        while sim_ev(actor_sim).has_condom_on is False and has_sim_trait(actor_sim, SimTrait.GENDEROPTIONS_PREGNANCY_CANIMPREGNATE):
            sims_that_can_impregnate_list.append(actor_sim)
    if not sims_that_can_impregnate_list:
        return (False, 0)
    condoms_count = get_object_amount_in_sim_inventory(sim, CONDOM_WRAPPER_OBJECT_ID)
    if condoms_count < len(sims_that_can_impregnate_list):
        return (False, condoms_count)
    if not remove_object_from_sim_inventory(sim, CONDOM_WRAPPER_OBJECT_ID, len(sims_that_can_impregnate_list)):
        return (False, len(sims_that_can_impregnate_list))
    for actor_sim in sims_that_can_impregnate_list:
        sim_ev(actor_sim).has_condom_on = True
        _update_sim_condom_status_buff(actor_sim)
        increase_sim_ww_statistic(actor_sim, 'times_used_contraception')
    return (True, len(sims_that_can_impregnate_list))

def try_auto_apply_condoms(sex_handler, sims_list):
    if sex_handler.tried_auto_apply_birth_control is True:
        return True
    if get_sex_setting(SexSetting.PREGNANCY_MODE, variable_type=int) == PregnancyModeSetting.DISABLED:
        return False
    if get_sex_setting(SexSetting.PREGNANCY_MODE, variable_type=int) == PregnancyModeSetting.SIMPLE and get_sex_setting(SexSetting.SIMPLE_PREGNANCY_CHANCE, variable_type=int) <= 0 and get_sex_setting(SexSetting.SIMPLE_NPC_PREGNANCY_CHANCE, variable_type=int) <= 0:
        return False
    is_pregnancy_sex = False
    for (actor_id, sim_info) in sims_list:
        if is_pregnancy_sex is True:
            break
        if not can_sim_get_pregnant(sim_info):
            pass
        actions = sex_handler.get_animation_instance().get_actor_received_actions(actor_id)
        for (action_actor_id, action_type, __) in actions:
            if action_type != SexCategoryType.VAGINAL:
                pass
            if actor_id == action_actor_id:
                pass
            actor_sim_id = sex_handler.get_sim_id_by_actor_id(action_actor_id)
            actor_sim_info = TurboManagerUtil.Sim.get_sim_info(actor_sim_id)
            if actor_sim_info is None:
                pass
            if not can_sim_impregnate(actor_sim_info):
                pass
            is_pregnancy_sex = True
            break
        while len(sims_list) == 2 and sex_handler.get_animation_instance().get_sex_category() == SexCategoryType.VAGINAL:
            while True:
                for (action_actor_id, actor_sim_info) in sims_list:
                    if actor_id == action_actor_id:
                        pass
                    if actor_sim_info is sim_info:
                        pass
                    if not can_sim_impregnate(actor_sim_info):
                        pass
                    is_pregnancy_sex = True
                    break
    if is_pregnancy_sex is False:
        return False
    condom_sims = list()
    has_sims_requiring_condom_use = False
    for (_, sim_info) in sims_list:
        condoms_count = get_object_amount_in_sim_inventory(sim_info, CONDOM_WRAPPER_OBJECT_ID)
        if _is_sim_requiring_condom_auto_use(sim_info, condoms_count):
            has_sims_requiring_condom_use = True
        condom_sims.append((sim_info, condoms_count))
    if has_sims_requiring_condom_use is False or not condom_sims:
        return False
    (condom_sim, condoms_count) = sorted(condom_sims, key=lambda x: x[1], reverse=True)[0]
    if condoms_count <= 0:
        return False
    try_to_take_and_use_condoms(condom_sim, silent_failure=True)
    sex_handler.tried_auto_apply_birth_control = True
    return True

def _is_sim_requiring_condom_auto_use(sim_identifier, condoms_count):
    if has_sim_trait(sim_identifier, SimTrait.HATESCHILDREN) and (sim_ev(sim_identifier).has_condom_on is False or sim_ev(sim_identifier).day_used_birth_control_pills != TurboWorldUtil.Time.get_absolute_days()):
        return True
    if get_sex_setting(SexSetting.BIRTH_CONTROL_AUTO_USE, variable_type=bool) and sim_ev(sim_identifier).auto_use_of_condoms is True and condoms_count > 0:
        return True
    return False

def give_sim_condoms(sim_identifier, amount=1):
    sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
    return add_object_to_sim_inventory(sim, CONDOM_WRAPPER_OBJECT_ID, amount=amount)

def update_sim_condom_state(sim_identifier):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    if sim_ev(sim_info).has_condom_on is True and sim_ev(sim_info).active_sex_handler is None and sim_ev(sim_info).active_pre_sex_handler is None:
        sim_ev(sim_info).has_condom_on = False
        _update_sim_condom_status_buff(sim_info)

def _update_sim_condom_status_buff(sim_identifier):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    if sim_ev(sim_info).has_condom_on is True:
        if not has_sim_buff(sim_info, SimBuff.WW_PREGNANCY_IS_WEARING_CONDOM):
            add_sim_buff(sim_info, SimBuff.WW_PREGNANCY_IS_WEARING_CONDOM)
    elif has_sim_buff(sim_info, SimBuff.WW_PREGNANCY_IS_WEARING_CONDOM):
        remove_sim_buff(sim_info, SimBuff.WW_PREGNANCY_IS_WEARING_CONDOM)
