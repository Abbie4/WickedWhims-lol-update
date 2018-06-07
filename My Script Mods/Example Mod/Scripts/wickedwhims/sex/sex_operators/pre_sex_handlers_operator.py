'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''from enums.interactions_enum import SimInteractionfrom enums.roles_enum import SimRoleStatefrom turbolib.interaction_util import TurboInteractionUtilfrom turbolib.manager_util import TurboManagerUtilfrom turbolib.sim_util import TurboSimUtilfrom turbolib.ui_util import TurboUIUtilfrom turbolib.world_util import TurboWorldUtilfrom wickedwhims.main.sim_ev_handler import sim_evfrom wickedwhims.sex.relationship_handler import get_test_relationship_score, apply_asking_for_woohoo_relations, get_relationship_sex_acceptance_thresholdfrom wickedwhims.sex.settings.sex_settings import SexSetting, get_sex_setting, SexInitiationTypeSettingfrom wickedwhims.sex.sex_operators.general_sex_handlers_operator import clear_sim_sex_extra_datafrom wickedwhims.sex.sex_privileges import is_sim_allowed_for_animation, display_not_allowed_messagefrom wickedwhims.utils_interfaces import display_drama_dialogfrom wickedwhims.utils_rolestates import add_sim_rolestate, remove_sim_rolestatefrom wickedwhims.utils_routes import is_sim_allowed_on_active_lotfrom wickedwhims.utils_situations import create_sim_visit_situation
def start_sex_interaction_from_pre_sex_handler(pre_sex_handler):
    is_instant = get_sex_setting(SexSetting.ALWAYS_ACCEPT_STATE, variable_type=bool) and get_sex_setting(SexSetting.SEX_INITIATION_TYPE, variable_type=int) == SexInitiationTypeSetting.INSTANT_TELEPORT
    if pre_sex_handler.get_sims_amount() == 1:
        if is_instant is True:
            return _start_instant_solo_sex_interaction(pre_sex_handler)
        return _start_solo_sex_interaction(pre_sex_handler)
    else:
        creator_sim = TurboManagerUtil.Sim.get_sim_instance(pre_sex_handler.get_creator_sim_id())
        target_sim = TurboManagerUtil.Sim.get_sim_instance(pre_sex_handler.get_second_sim_id())
        if creator_sim is None or target_sim is None:
            clear_sim_sex_extra_data(TurboManagerUtil.Sim.get_sim_info(pre_sex_handler.get_creator_sim_id()))
            clear_sim_sex_extra_data(TurboManagerUtil.Sim.get_sim_info(pre_sex_handler.get_second_sim_id()))
            return False
        ask_player_to_start = False
        if get_sex_setting(SexSetting.AUTONOMY_PLAYER_ASK_PLAYER_DIALOG_STATE, variable_type=bool) and (pre_sex_handler.is_autonomy_sex() and TurboSimUtil.Sim.is_player(creator_sim)) and TurboSimUtil.Sim.is_player(target_sim):
            ask_player_to_start = True
        elif get_sex_setting(SexSetting.AUTONOMY_NPC_ASK_PLAYER_DIALOG_STATE, variable_type=bool) and TurboSimUtil.Sim.is_npc(creator_sim) and TurboSimUtil.Sim.is_player(target_sim):
            ask_player_to_start = True
        elif get_sex_setting(SexSetting.AUTONOMY_PLAYER_ASK_NPC_DIALOG_STATE, variable_type=bool) and (pre_sex_handler.is_autonomy_sex() and TurboSimUtil.Sim.is_player(creator_sim)) and TurboSimUtil.Sim.is_npc(target_sim):
            ask_player_to_start = True
        if is_instant is True:
            return _start_instant_group_sex_interaction(pre_sex_handler, ask_player_to_start=ask_player_to_start)
        return _start_group_sex_interaction(pre_sex_handler, ask_player_to_start=ask_player_to_start)

def _start_instant_solo_sex_interaction(pre_sex_handler):
    sim_ev(TurboManagerUtil.Sim.get_sim_info(pre_sex_handler.get_creator_sim_id())).active_pre_sex_handler = pre_sex_handler
    pre_sex_handler.start_sex_interaction()
    return True

def _start_solo_sex_interaction(pre_sex_handler):
    creator_sim = TurboManagerUtil.Sim.get_sim_instance(pre_sex_handler.get_creator_sim_id())
    if creator_sim is None:
        clear_sim_sex_extra_data(TurboManagerUtil.Sim.get_sim_info(pre_sex_handler.get_creator_sim_id()))
        return False
    sim_ev(creator_sim).is_in_process_to_sex = True
    for interaction_id in TurboSimUtil.Interaction.get_queued_interactions_ids(creator_sim):
        TurboSimUtil.Interaction.cancel_queued_interaction(creator_sim, interaction_id)
    TurboSimUtil.Interaction.unlock_queue(creator_sim)
    TurboSimUtil.Routing.refresh_portals(creator_sim)
    result = TurboSimUtil.Interaction.push_affordance(creator_sim, SimInteraction.WW_ROUTE_TO_SEX_LOCATION, insert_strategy=TurboInteractionUtil.QueueInsertStrategy.FIRST, run_priority=TurboInteractionUtil.Priority.Critical, priority=TurboInteractionUtil.Priority.Critical)
    if result:
        sim_ev(creator_sim).in_sex_process_interaction = TurboInteractionUtil.get_interaction_from_enqueue_result(result)
    return bool(result)

def _start_instant_group_sex_interaction(pre_sex_handler, ask_player_to_start=False):
    if ask_player_to_start is True:
        creator_sim = TurboManagerUtil.Sim.get_sim_instance(pre_sex_handler.get_creator_sim_id())
        target_sim = TurboManagerUtil.Sim.get_sim_instance(pre_sex_handler.get_second_sim_id())

        def ask_for_sex_callback(dialog):
            if TurboUIUtil.DramaDialog.get_response_result(dialog):
                _start_group_sex_interaction(pre_sex_handler, ask_player_to_start=False)
            else:
                for pre_sim_info in pre_sex_handler.get_actors_sim_info_gen():
                    clear_sim_sex_extra_data(pre_sim_info)
            return True

        display_drama_dialog(target_sim, creator_sim, text=1638454846, text_tokens=(creator_sim, target_sim), ok_text=3398494028, cancel_text=3364226930, callback=ask_for_sex_callback)
        return False
    for sim_info in pre_sex_handler.get_actors_sim_info_gen():
        sim_ev(sim_info).active_pre_sex_handler = pre_sex_handler
        prepare_npc_sim_to_sex(sim_info)
    pre_sex_handler.start_sex_interaction()
    return True

def _start_group_sex_interaction(pre_sex_handler, ask_player_to_start=False):
    creator_sim = TurboManagerUtil.Sim.get_sim_instance(pre_sex_handler.get_creator_sim_id())
    target_sim = TurboManagerUtil.Sim.get_sim_instance(pre_sex_handler.get_second_sim_id())
    for pre_sim_info in pre_sex_handler.get_actors_sim_info_gen():
        sim_ev(pre_sim_info).active_pre_sex_handler = pre_sex_handler
        prepare_npc_sim_to_sex(pre_sim_info)
        for interaction_id in TurboSimUtil.Interaction.get_queued_interactions_ids(pre_sim_info):
            TurboSimUtil.Interaction.cancel_queued_interaction(pre_sim_info, interaction_id)
    if ask_player_to_start is True:
        result = TurboSimUtil.Interaction.push_affordance(creator_sim, SimInteraction.WW_TRIGGER_SOCIAL_AUTONOMY_ASK_FOR_SEX_DEFAULT, target=target_sim, skip_if_running=True)
        return bool(result)
    result = TurboSimUtil.Interaction.push_affordance(creator_sim, SimInteraction.WW_TRIGGER_SOCIAL_ASK_FOR_SEX_DEFAULT, target=target_sim)
    return bool(result)

def join_sex_interaction_from_pre_sex_handler(pre_sex_handler, join_sims_list, ask_player_to_join=False, ignore_relationship_check=False, flip_relationship_check=False):
    creator_sim_info = TurboManagerUtil.Sim.get_sim_info(pre_sex_handler.get_creator_sim_id())
    can_sims_join = True
    for join_sim in join_sims_list:
        is_sex_allowed = is_sim_allowed_for_animation(tuple(pre_sex_handler.get_actors_sim_info_gen()), pre_sex_handler.get_interaction_type(), is_joining=True)
        if not is_sex_allowed:
            display_not_allowed_message(is_sex_allowed)
            can_sims_join = False
            break
        while ignore_relationship_check is False:
            relationship_score = get_test_relationship_score((creator_sim_info, join_sim))
            if relationship_score < get_relationship_sex_acceptance_threshold():
                if flip_relationship_check is True:
                    apply_asking_for_woohoo_relations(join_sim, creator_sim_info, False)
                else:
                    apply_asking_for_woohoo_relations(creator_sim_info, join_sim, False)
                can_sims_join = False
                break
    if can_sims_join is False:
        for join_sim in join_sims_list:
            clear_sim_sex_extra_data(join_sim, only_pre_active_data=True)
        return
    if ask_player_to_join is True:

        def ask_for_sex_callback(dialog):
            if TurboUIUtil.DramaDialog.get_response_result(dialog):
                _join_sex_interaction_from_pre_handler(pre_sex_handler, join_sims_list)
            else:
                active_sex_handler = sim_ev(pre_sex_handler.get_creator_sim_id()).active_sex_handler
                for sim in join_sims_list:
                    clear_sim_sex_extra_data(sim)
                    sim_id = TurboManagerUtil.Sim.get_sim_id(sim)
                    while sim_id not in active_sex_handler.ignore_autonomy_join_sims:
                        active_sex_handler.ignore_autonomy_join_sims.append(sim_id)
            return True

        display_drama_dialog(creator_sim_info, join_sims_list[0], text=3899042444, text_tokens=(join_sims_list[0], creator_sim_info), ok_text=3398494028, cancel_text=3364226930, callback=ask_for_sex_callback)
        return
    _join_sex_interaction_from_pre_handler(pre_sex_handler, join_sims_list)

def _join_sex_interaction_from_pre_handler(pre_sex_handler, join_sims_list):
    creator_sim_info = TurboManagerUtil.Sim.get_sim_info(pre_sex_handler.get_creator_sim_id())
    sim_ev(creator_sim_info).active_sex_handler.has_joining_sims = True
    for sim_info in pre_sex_handler.get_actors_sim_info_gen():
        sim_ev(sim_info).active_pre_sex_handler = pre_sex_handler
        while sim_ev(sim_info).active_sex_handler is not None:
            sim_ev(sim_info).is_ready_to_sex = True
    is_instant = get_sex_setting(SexSetting.ALWAYS_ACCEPT_STATE, variable_type=bool) and get_sex_setting(SexSetting.SEX_INITIATION_TYPE, variable_type=int) == SexInitiationTypeSetting.INSTANT_TELEPORT
    for join_sim_info in join_sims_list:
        join_sim_info = TurboManagerUtil.Sim.get_sim_info(join_sim_info)
        prepare_npc_sim_to_sex(join_sim_info)
        while is_instant is False:
            sim_ev(join_sim_info).is_in_process_to_sex = True
            TurboSimUtil.Interaction.unlock_queue(join_sim_info)
            TurboSimUtil.Routing.refresh_portals(join_sim_info)
            result = TurboSimUtil.Interaction.push_affordance(join_sim_info, SimInteraction.WW_ROUTE_TO_SEX_LOCATION, insert_strategy=TurboInteractionUtil.QueueInsertStrategy.FIRST, priority=TurboInteractionUtil.Priority.Critical, run_priority=TurboInteractionUtil.Priority.Critical)
            if result:
                sim_ev(join_sim_info).in_sex_process_interaction = TurboInteractionUtil.get_interaction_from_enqueue_result(result)
    if is_instant is True:
        sim_ev(creator_sim_info).active_sex_handler.stop(hard_stop=True, no_teleport=True, is_joining_stop=True, stop_reason='On join interaction!')
        pre_sex_handler.start_sex_interaction()

def prepare_npc_sim_to_sex(sim_identifier):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    if TurboSimUtil.Sim.is_player(sim_info):
        return
    sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
    if sim is None:
        return
    pre_sex_handler = sim_ev(sim_info).active_pre_sex_handler
    if pre_sex_handler is None:
        return
    is_at_active_lot = TurboWorldUtil.Lot.is_position_on_active_lot(pre_sex_handler.get_route_position())
    if is_at_active_lot is False:
        add_sim_rolestate(sim, SimRoleState.WW_OPEN_STREET_SEX)
        return
    if is_at_active_lot is True and not is_sim_allowed_on_active_lot(sim):
        add_sim_rolestate(sim, SimRoleState.WW_HOUSE_GUEST_SEX)
        create_sim_visit_situation(sim)
        return

def unprepare_npc_sim_from_sex(sim_identifier):
    sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
    if sim is None or TurboSimUtil.Sim.is_player(sim):
        return
    remove_sim_rolestate(sim, SimRoleState.WW_HOUSE_GUEST_SEX)
    remove_sim_rolestate(sim, SimRoleState.WW_OPEN_STREET_SEX)

def update_sim_to_route_for_sex(sim):
    if sim_ev(sim).is_in_process_to_sex is True:
        if sim_ev(sim).active_pre_sex_handler is not None:
            TurboSimUtil.Interaction.unlock_queue(sim)
            TurboSimUtil.Routing.refresh_portals(sim)
            result = TurboSimUtil.Interaction.push_affordance(sim, SimInteraction.WW_ROUTE_TO_SEX_LOCATION, insert_strategy=TurboInteractionUtil.QueueInsertStrategy.FIRST, priority=TurboInteractionUtil.Priority.Critical, run_priority=TurboInteractionUtil.Priority.Critical, skip_if_running=True)
            if result:
                sim_ev(sim).in_sex_process_interaction = TurboInteractionUtil.get_interaction_from_enqueue_result(result)
            else:
                clear_sim_sex_extra_data(sim, only_pre_active_data=True)
                unprepare_npc_sim_from_sex(sim)
        else:
            clear_sim_sex_extra_data(sim, only_pre_active_data=True)
            unprepare_npc_sim_from_sex(sim)
