'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''import randomfrom enums.relationship_enum import SimRelationshipBitfrom turbolib.manager_util import TurboManagerUtilfrom turbolib.sim_util import TurboSimUtilfrom turbolib.world_util import TurboWorldUtilfrom turbolib.wrappers.interactions import TurboImmediateSuperInteraction, TurboInteractionStartMixinfrom wickedwhims.debug.debug_controller import is_main_debug_flag_enabledfrom wickedwhims.main.sim_ev_handler import sim_evfrom wickedwhims.sex.pregnancy.menstrual_cycle_handler import get_sim_menstrual_cycle_days, get_sim_days_till_ovulation, apply_period_related_buffs, get_fertility_days_data, get_cycle_durations, get_sim_menstrual_pregnancy_chance_matrixfrom wickedwhims.sex.pregnancy.native_pregnancy_handler import get_sim_pregnancy_discovery_statefrom wickedwhims.sex.pregnancy.pregnancy_interface import get_sim_current_pregnancy_chancefrom wickedwhims.utils_interfaces import display_notificationfrom wickedwhims.utils_relations import get_sim_ids_with_relationsip_bit
class DebugPregnancyInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'DebugPregnancyInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return is_main_debug_flag_enabled()

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        sim = cls.get_interaction_target(interaction_instance)
        sim_id = TurboManagerUtil.Sim.get_sim_id(sim)
        pregnancy_debug_info = ''
        absolute_days = TurboWorldUtil.Time.get_absolute_days() + 31415
        menstrual_cycle_days = get_sim_menstrual_cycle_days(sim)
        (before_fertile_window_start, fertile_window_start, most_fertile_window_start, ovulation_day) = get_fertility_days_data(menstrual_cycle_days)
        cycle_day = absolute_days % menstrual_cycle_days + 1
        cycle_number = max(1, int(absolute_days/menstrual_cycle_days))
        random_int = random.Random(sim_id/cycle_number)
        (_, _, cramps_duration, period_duration) = get_cycle_durations()
        period_duration = random_int.randint(*period_duration)
        cramps_duration = random_int.randint(*cramps_duration) if random_int.uniform(0, 1) <= 0.5 else 0
        pregnancy_matrix = get_sim_menstrual_pregnancy_chance_matrix(sim)
        pregnancy_debug_info += 'Menstrual Cycle Days:\n'
        pregnancy_debug_info += '  Before Fertile Window Day: ' + str(before_fertile_window_start) + '\n'
        pregnancy_debug_info += '  Fertile Window Day: ' + str(fertile_window_start) + '\n'
        pregnancy_debug_info += '  Most Fertile Window Day: ' + str(most_fertile_window_start) + '\n'
        pregnancy_debug_info += '  Ovulation Day: ' + str(ovulation_day) + '\n'
        pregnancy_debug_info += 'Menstrual Cycle:\n'
        pregnancy_debug_info += '  Menstrual Cycle Duration: ' + str(menstrual_cycle_days) + '\n'
        pregnancy_debug_info += '  Menstrual Cycle Day: ' + str(cycle_day) + '\n'
        pregnancy_debug_info += '  Menstrual Cycle Number: ' + str(cycle_number) + '\n'
        pregnancy_debug_info += '  Days Till Ovulation: ' + str(get_sim_days_till_ovulation(sim)) + '\n'
        pregnancy_debug_info += '  Current Cramps Duration: ' + str(cramps_duration) + '\n'
        pregnancy_debug_info += '  Has Cramps: ' + str(True if cramps_duration > 0 and cycle_day > menstrual_cycle_days - cramps_duration else False) + '\n'
        pregnancy_debug_info += '  Current Period Duration: ' + str(period_duration) + '\n'
        pregnancy_debug_info += '  Is On Period: ' + str(cycle_day <= period_duration) + '\n'
        pregnancy_debug_info += 'Pregnancy:\n'
        pregnancy_debug_info += '  Pregnancy Discovery State: ' + str(get_sim_pregnancy_discovery_state(sim)) + '\n'
        pregnancy_debug_info += '  Is Native Pregnant: ' + str(TurboSimUtil.Pregnancy.is_pregnant(sim)) + '\n'
        pregnancy_debug_info += '  Pregnancy Chance: ' + str(get_sim_current_pregnancy_chance(sim)) + '\n'
        pregnancy_debug_info += '  Pregnancy Boost: ' + str(sim_ev(sim).pregnancy_fertility_boost) + '\n'
        pregnancy_debug_info += '  Pregnancy Coming Flag: ' + str(sim_ev(sim).pregnancy_coming_flag) + '\n'
        pregnancy_debug_info += '  Pregnancy Counter: ' + str(sim_ev(sim).pregnancy_counter) + '\n'
        pregnancy_debug_info += '  Pregnancy Partners: ' + str(get_sim_ids_with_relationsip_bit(sim, SimRelationshipBit.WW_POTENTIAL_PREGNANCY_PARENT)) + '\n'
        pregnancy_debug_info += '  Miscarriage Potential: ' + str(sim_ev(sim).miscarriage_potential) + '\n'
        pregnancy_debug_info += 'Birth Control:\n'
        pregnancy_debug_info += '  Has Condom On: ' + str(sim_ev(sim).has_condom_on) + '\n'
        pregnancy_debug_info += '  Is On Birth Control: ' + str(sim_ev(sim).day_used_birth_control_pills == TurboWorldUtil.Time.get_absolute_days()) + '\n'
        pregnancy_debug_info += '  Day Used Birth Control Pill: ' + str(sim_ev(sim).day_used_birth_control_pills) + '\n'
        pregnancy_debug_info += '  Birth Control Pill Power: ' + str(sim_ev(sim).birth_control_pill_power) + '\n'
        pregnancy_debug_info += 'Pregnancy Chances Matrix:\n'
        for (key, value) in pregnancy_matrix.items():
            pregnancy_debug_info += '  Day ' + str(key) + ': ' + str(value) + '\n'
        display_notification(text=pregnancy_debug_info, title=str(TurboSimUtil.Name.get_name(sim)[0]) + ' ' + str(TurboSimUtil.Name.get_name(sim)[1]) + ' Pregnancy Debug', secondary_icon=sim)
        apply_period_related_buffs(sim)
