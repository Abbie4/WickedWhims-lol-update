'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from enums.relationship_enum import SimRelationshipBit
from turbolib.manager_util import TurboManagerUtil
from turbolib.resources.affordances import AffordanceRegistration, register_affordance_class
from turbolib.sim_util import TurboSimUtil
from turbolib.special.custom_exception_watcher import exception_watch
from turbolib.types_util import TurboTypesUtil
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.utils_interfaces import display_ok_dialog
from wickedwhims.utils_relations import has_relationship_bit_with_sim
GLOBAL_WW_STATISTICS = dict()

def display_global_statistics_dialog():
    values = list()
    values.extend('' for _ in range(150))
    values[10] = ''
    display_ok_dialog(text=2093939627, text_tokens=values, title=3778116009)

def set_global_ww_statistic(statistic_name, value):
    GLOBAL_WW_STATISTICS[statistic_name] = value

def increase_global_ww_statistic(statistic_name, add=1):
    value = 0
    if statistic_name in GLOBAL_WW_STATISTICS:
        value = GLOBAL_WW_STATISTICS[statistic_name]
    GLOBAL_WW_STATISTICS[statistic_name] = value + add

def get_global_ww_statistic(statistic_name):
    if statistic_name in GLOBAL_WW_STATISTICS:
        return GLOBAL_WW_STATISTICS[statistic_name]
    return 0

def set_global_ww_statistics(value):
    global GLOBAL_WW_STATISTICS
    GLOBAL_WW_STATISTICS = value

def get_global_ww_statistics():
    return GLOBAL_WW_STATISTICS

@exception_watch()
def display_sim_statistics_dialog(sim_identifier):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    _update_sim_statistics(sim_info)
    values = list()
    values.append(sim_info)
    values.extend('' for _ in range(150))
    values[10] = str(get_sim_ww_statistic(sim_info, 'times_had_sex'))
    values[11] = str(_get_percentage(get_sim_ww_statistic(sim_info, 'times_had_incest_sex'), get_sim_ww_statistic(sim_info, 'times_had_sex')))
    values[12] = str(get_sim_ww_statistic(sim_info, 'times_had_solo_sex'))
    values[13] = str(get_sim_ww_statistic(sim_info, 'times_been_seen_in_sex'))
    values[14] = str(get_sim_ww_statistic(sim_info, 'times_reacted_to_sex'))
    sex_ask_overall = get_sim_ww_statistic(sim_info, 'times_sex_got_accepted') + get_sim_ww_statistic(sim_info, 'times_sex_got_rejected')
    values[15] = str(sex_ask_overall)
    values[16] = str(_get_percentage(get_sim_ww_statistic(sim_info, 'times_sex_got_accepted'), sex_ask_overall))
    values[17] = str(_get_percentage(get_sim_ww_statistic(sim_info, 'times_sex_got_rejected'), sex_ask_overall))
    sex_time_overall = get_sim_ww_statistic(sim_info, 'time_spent_on_sex_teasing') + get_sim_ww_statistic(sim_info, 'time_spent_on_sex_handjob') + get_sim_ww_statistic(sim_info, 'time_spent_on_sex_footjob') + get_sim_ww_statistic(sim_info, 'time_spent_on_sex_oraljob') + get_sim_ww_statistic(sim_info, 'time_spent_on_sex_vaginal') + get_sim_ww_statistic(sim_info, 'time_spent_on_sex_anal') + get_sim_ww_statistic(sim_info, 'time_spent_on_sex_climax')
    values[21] = str('%.2f' % (sex_time_overall/60))
    values[22] = str(_get_percentage(get_sim_ww_statistic(sim_info, 'time_spent_on_sex_teasing'), sex_time_overall))
    values[23] = str(_get_percentage(get_sim_ww_statistic(sim_info, 'time_spent_on_sex_handjob'), sex_time_overall))
    values[24] = str(_get_percentage(get_sim_ww_statistic(sim_info, 'time_spent_on_sex_footjob'), sex_time_overall))
    values[25] = str(_get_percentage(get_sim_ww_statistic(sim_info, 'time_spent_on_sex_oraljob'), sex_time_overall))
    values[26] = str(_get_percentage(get_sim_ww_statistic(sim_info, 'time_spent_on_sex_vaginal'), sex_time_overall))
    values[27] = str(_get_percentage(get_sim_ww_statistic(sim_info, 'time_spent_on_sex_anal'), sex_time_overall))
    values[28] = str(_get_percentage(get_sim_ww_statistic(sim_info, 'time_spent_on_sex_climax'), sex_time_overall))
    sex_unique_partners_overall = get_sim_ww_statistic(sim_info, 'unique_sex_partners')
    values[30] = str(sex_unique_partners_overall)
    values[31] = str(_get_percentage(get_sim_ww_statistic(sim_info, 'unique_sex_partner_teen'), sex_unique_partners_overall))
    values[32] = str(_get_percentage(get_sim_ww_statistic(sim_info, 'unique_sex_partner_youngadult'), sex_unique_partners_overall))
    values[33] = str(_get_percentage(get_sim_ww_statistic(sim_info, 'unique_sex_partner_adult'), sex_unique_partners_overall))
    values[34] = str(_get_percentage(get_sim_ww_statistic(sim_info, 'unique_sex_partner_elder'), sex_unique_partners_overall))
    sex_cum_received_overall = get_sim_ww_statistic(sim_info, 'times_received_cum_face') + get_sim_ww_statistic(sim_info, 'times_received_cum_chest') + get_sim_ww_statistic(sim_info, 'times_received_cum_back') + get_sim_ww_statistic(sim_info, 'times_received_cum_vagina') + get_sim_ww_statistic(sim_info, 'times_received_cum_butt') + get_sim_ww_statistic(sim_info, 'times_received_cum_feet')
    values[40] = str(sex_cum_received_overall)
    values[41] = str(_get_percentage(get_sim_ww_statistic(sim_info, 'times_received_cum_face'), sex_cum_received_overall))
    values[42] = str(_get_percentage(get_sim_ww_statistic(sim_info, 'times_received_cum_chest'), sex_cum_received_overall))
    values[43] = str(_get_percentage(get_sim_ww_statistic(sim_info, 'times_received_cum_back'), sex_cum_received_overall))
    values[44] = str(_get_percentage(get_sim_ww_statistic(sim_info, 'times_received_cum_vagina'), sex_cum_received_overall))
    values[45] = str(_get_percentage(get_sim_ww_statistic(sim_info, 'times_received_cum_butt'), sex_cum_received_overall))
    values[46] = str(_get_percentage(get_sim_ww_statistic(sim_info, 'times_received_cum_feet'), sex_cum_received_overall))
    values[50] = str('%.2f' % (get_sim_ww_statistic(sim_info, 'time_spent_nude')/60))
    values[51] = str(get_sim_ww_statistic(sim_info, 'times_been_seen_nude'))
    values[52] = str(get_sim_ww_statistic(sim_info, 'times_reacted_to_nudity'))
    values[53] = str(get_sim_ww_statistic(sim_info, 'times_talked_exhibitionism'))
    flashed_times_overall = get_sim_ww_statistic(sim_info, 'times_flashed_top') + get_sim_ww_statistic(sim_info, 'times_flashed_bottom') + get_sim_ww_statistic(sim_info, 'times_flashed_full')
    values[60] = str(flashed_times_overall)
    values[61] = str(_get_percentage(get_sim_ww_statistic(sim_info, 'times_flashed_top'), flashed_times_overall))
    values[62] = str(_get_percentage(get_sim_ww_statistic(sim_info, 'times_flashed_bottom'), flashed_times_overall))
    values[63] = str(_get_percentage(get_sim_ww_statistic(sim_info, 'times_flashed_full'), flashed_times_overall))
    values[100] = str(get_sim_ww_statistic(sim_info, 'times_impregnated'))
    values[101] = str(get_sim_ww_statistic(sim_info, 'times_got_pregnant'))
    values[102] = str(get_sim_ww_statistic(sim_info, 'times_terminated_pregnancy'))
    values[103] = str(get_sim_ww_statistic(sim_info, 'times_used_contraception'))
    display_ok_dialog(text=863853338, text_tokens=values, title=1561155736, title_tokens=(sim_info,))

def _update_sim_statistics(sim_identifier):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    set_sim_ww_statistic(sim_info, 'unique_sex_partners', 0)
    set_sim_ww_statistic(sim_info, 'unique_sex_partner_teen', 0)
    set_sim_ww_statistic(sim_info, 'unique_sex_partner_youngadult', 0)
    set_sim_ww_statistic(sim_info, 'unique_sex_partner_adult', 0)
    set_sim_ww_statistic(sim_info, 'unique_sex_partner_elder', 0)
    for target_sim_info in TurboManagerUtil.Sim.get_all_sim_info_gen(humans=True, pets=False):
        while sim_info is not target_sim_info and has_relationship_bit_with_sim(sim_info, target_sim_info, SimRelationshipBit.ROMANTIC_HAVEDONEWOOHOO):
            increase_sim_ww_statistic(sim_info, 'unique_sex_partners')
            if TurboSimUtil.Age.get_age(target_sim_info) == TurboSimUtil.Age.TEEN:
                increase_sim_ww_statistic(sim_info, 'unique_sex_partner_teen')
            elif TurboSimUtil.Age.get_age(target_sim_info) == TurboSimUtil.Age.YOUNGADULT:
                increase_sim_ww_statistic(sim_info, 'unique_sex_partner_youngadult')
            elif TurboSimUtil.Age.get_age(target_sim_info) == TurboSimUtil.Age.ADULT:
                increase_sim_ww_statistic(sim_info, 'unique_sex_partner_adult')
            elif TurboSimUtil.Age.get_age(target_sim_info) == TurboSimUtil.Age.ELDER:
                increase_sim_ww_statistic(sim_info, 'unique_sex_partner_elder')

def set_sim_ww_statistic(sim_identifier, statistic_name, value):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    sim_ev(sim_info).special_statistics[statistic_name] = value

def increase_sim_ww_statistic(sim_identifier, statistic_name, add=1):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    value = 0
    if statistic_name in sim_ev(sim_info).special_statistics:
        value = sim_ev(sim_info).special_statistics[statistic_name]
    sim_ev(sim_info).special_statistics[statistic_name] = value + add

def get_sim_ww_statistic(sim_identifier, statistic_name):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    if statistic_name in sim_ev(sim_info).special_statistics:
        return sim_ev(sim_info).special_statistics[statistic_name]
    return 0

def _get_percentage(amount, overall_amount):
    if overall_amount <= 0:
        return 0
    return '%.2f' % (amount/overall_amount*100)

@register_affordance_class()
class MainAffordanceRegisterClass(AffordanceRegistration):
    __qualname__ = 'MainAffordanceRegisterClass'

    def get_affordance_references(self):
        return (17491222577090633016,)

    def is_script_object(self, script_object):
        return TurboTypesUtil.Sims.is_sim(script_object) and TurboSimUtil.Species.is_human(script_object)

