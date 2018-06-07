'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''from enums.interactions_enum import SimInteractionfrom turbolib.events.core_tick import register_zone_update_event_method, get_current_diff_ticksfrom turbolib.manager_util import TurboManagerUtilfrom turbolib.sim_util import TurboSimUtilfrom wickedwhims.main.sim_ev_handler import sim_evfrom wickedwhims.main.tick_handler import register_on_game_update_methodfrom wickedwhims.relationships.desire_handler import update_sims_high_desirefrom wickedwhims.sex.cas_cum_handler import try_clean_sim_cumfrom wickedwhims.sex.pregnancy.birth_control.birth_control_handler import update_sim_birth_control_statefrom wickedwhims.sex.pregnancy.birth_control.pills import try_auto_apply_birth_control_pillsfrom wickedwhims.sex.pregnancy.menstrual_cycle_handler import update_period_related_buffs, reset_pregnancy_boost_datafrom wickedwhims.sex.pregnancy.miscarriage_handler import update_sim_miscarriagefrom wickedwhims.sex.pregnancy.special_pregnancy_handler import update_sim_coming_pregnancyfrom wickedwhims.sex.sex_operators.active_sex_handlers_operator import unregister_active_sex_handlers, update_active_sex_handlersfrom wickedwhims.sex.sex_operators.pre_sex_handlers_operator import update_sim_to_route_for_sexfrom wickedwhims.utils_interfaces import display_notification
@register_zone_update_event_method(unique_id='WickedWhims')
def _update_sex_handlers_on_zone_update():
    update_active_sex_handlers(get_current_diff_ticks())

@register_on_game_update_method(interval=1500)
def _update_sex_on_game_update():
    unregister_active_sex_handlers()
    for sim in TurboManagerUtil.Sim.get_all_sim_instance_gen(humans=True, pets=False):
        update_sim_to_route_for_sex(sim)
        _test_for_broken_sex_interaction(sim)
        update_sims_high_desire(sim)
    for sim_info in TurboManagerUtil.Sim.get_all_sim_info_gen(humans=True, pets=False):
        try_clean_sim_cum(sim_info)
        update_sim_birth_control_state(sim_info)
        update_sim_coming_pregnancy(sim_info)

@register_on_game_update_method(interval=75000)
def _update_pregnancy_data_on_game_update():
    for sim in TurboManagerUtil.Sim.get_all_sim_instance_gen(humans=True, pets=False):
        try_auto_apply_birth_control_pills(sim)
        update_sim_miscarriage(sim)
    for sim_info in TurboManagerUtil.Sim.get_all_sim_info_gen(humans=True, pets=False):
        update_period_related_buffs(sim_info)
        reset_pregnancy_boost_data(sim_info)

def _test_for_broken_sex_interaction(sim_identifier):
    sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
    if sim_ev(sim).active_sex_handler is None:
        return
    if sim_ev(sim).active_sex_handler.is_playing is True and not TurboSimUtil.Interaction.is_running_interaction(sim, SimInteraction.WW_SEX_ANIMATION_DEFAULT) and not TurboSimUtil.Interaction.has_queued_interaction(sim, SimInteraction.WW_SEX_ANIMATION_DEFAULT):
        if sim_ev(sim).active_sex_handler.one_second_counter > 3:
            display_notification(text=2431239863)
        sim_ev(sim).active_sex_handler.reset()
