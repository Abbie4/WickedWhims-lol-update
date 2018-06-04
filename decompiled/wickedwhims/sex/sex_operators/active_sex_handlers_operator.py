'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from enums.interactions_enum import SimInteraction
from turbolib.events.buildbuy import register_buildbuy_state_change_event_method
from turbolib.events.core import register_zone_load_event_method, has_game_loaded
from turbolib.events.interactions import register_interaction_queue_event_method, register_interaction_run_event_method
from turbolib.interaction_util import TurboInteractionUtil
from turbolib.manager_util import TurboManagerUtil
from turbolib.resource_util import TurboResourceUtil
from turbolib.sim_util import TurboSimUtil
from turbolib.types_util import TurboTypesUtil
from turbolib.world_util import TurboWorldUtil
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.sex.sex_operators.general_sex_handlers_operator import clear_sim_sex_extra_data
from wickedwhims.sxex_bridge.outfit import dress_up_outfit
from wickedwhims.utils_saves.save_sex_handlers import get_sex_handlers_save_data, update_sex_handlers_save_data
ACTIVE_SEX_HANDLERS_LIST = list()
CHECK_ACTIVE_SEX_HANDLERS_TO_UNREGISTER = True

def get_active_sex_handlers():
    return ACTIVE_SEX_HANDLERS_LIST

def reset_active_sex_handlers():
    global ACTIVE_SEX_HANDLERS_LIST
    ACTIVE_SEX_HANDLERS_LIST = list()

def register_active_sex_handler(active_sex_handler, skip_save_data_update=False):
    if active_sex_handler.is_ready_to_unregister is True:
        return
    if active_sex_handler.is_registered is False:
        ACTIVE_SEX_HANDLERS_LIST.append(active_sex_handler)
    active_sex_handler.is_registered = True
    if skip_save_data_update is False:
        sex_handlers_dict = dict()
        for active_sex_handler in ACTIVE_SEX_HANDLERS_LIST:
            sex_handlers_dict[active_sex_handler.get_identifier()] = active_sex_handler.get_save_dict()
        update_sex_handlers_save_data(sex_handlers_dict)

def queue_unregister_active_sex_handler(active_sex_handler):
    global CHECK_ACTIVE_SEX_HANDLERS_TO_UNREGISTER
    active_sex_handler.is_ready_to_unregister = True
    CHECK_ACTIVE_SEX_HANDLERS_TO_UNREGISTER = True

def unregister_active_sex_handlers():
    global ACTIVE_SEX_HANDLERS_LIST
    if CHECK_ACTIVE_SEX_HANDLERS_TO_UNREGISTER is False:
        return
    new_sex_handlers_list = list()
    new_sex_handlers_save_data = dict()
    for sex_handler in ACTIVE_SEX_HANDLERS_LIST:
        if sex_handler.is_ready_to_unregister is True or not sex_handler.is_valid():
            sex_handler.is_ready_to_unregister = True
            sex_handler.is_registered = False
        else:
            new_sex_handlers_list.append(sex_handler)
            new_sex_handlers_save_data[sex_handler.get_identifier()] = sex_handler.get_save_dict()
    ACTIVE_SEX_HANDLERS_LIST = new_sex_handlers_list
    update_sex_handlers_save_data(new_sex_handlers_save_data)

def register_loaded_active_sex_handlers():
    from wickedwhims.sex.sex_handlers.active.active_sex_handler import ActiveSexInteractionHandler
    reset_active_sex_handlers()
    sex_handlers_save_data = get_sex_handlers_save_data()
    for sex_handler_data in sex_handlers_save_data.values():
        try:
            active_sex_handler = ActiveSexInteractionHandler.load_from_dict(sex_handler_data)
            register_active_sex_handler(active_sex_handler, skip_save_data_update=True)
        except:
            pass

def apply_active_sex_handler_to_sim(sim_identifier):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    sex_handler_identifier = sim_ev(sim_info).active_sex_handler_identifier
    if not sex_handler_identifier or sex_handler_identifier == '-1':
        clear_sim_sex_extra_data(sim_info)
        return
    active_sex_handler = None
    for sex_handler in ACTIVE_SEX_HANDLERS_LIST:
        while sex_handler.get_identifier() == sex_handler_identifier:
            active_sex_handler = sex_handler
            break
    if active_sex_handler is None:
        clear_sim_sex_extra_data(sim_info)
        return
    if TurboWorldUtil.Lot.get_active_lot_id() != active_sex_handler.get_lot_id():
        clear_sim_sex_extra_data(sim_info)
        return
    sim_ev(sim_info).active_sex_handler = active_sex_handler

def update_active_sex_handlers(ticks):
    if not ACTIVE_SEX_HANDLERS_LIST:
        return
    for sex_handler in ACTIVE_SEX_HANDLERS_LIST:
        if not sex_handler.is_valid(skip_actors=True):
            queue_unregister_active_sex_handler(sex_handler)
        if sex_handler.is_ready_to_unregister is True:
            pass
        while sex_handler.is_prepared_to_play is True:
            if sex_handler.is_playing is False:
                sex_handler.pre_update(ticks)
            else:
                sex_handler.update(ticks)

@register_zone_load_event_method(unique_id='WickedWhims', priority=50, late=True)
def _wickedwhims_restart_sex_handlers_on_first_load():
    if has_game_loaded():
        return
    for sim in TurboManagerUtil.Sim.get_all_sim_instance_gen(humans=True, pets=False):
        while sim_ev(sim).active_sex_handler is not None:
            sim_ev(sim).active_sex_handler.restart()

@register_zone_load_event_method(unique_id='WickedWhims', priority=50, late=True)
def _wickedwhims_neutralize_sims_active_sex_data_on_zone_move():
    if not has_game_loaded():
        return
    for sex_handler in ACTIVE_SEX_HANDLERS_LIST:
        for sim_info in sex_handler.get_actors_sim_info_gen():
            if sim_info is None:
                pass
            clear_sim_sex_extra_data(sim_info)
            dress_up_outfit(sim_info)
    reset_active_sex_handlers()

@register_interaction_run_event_method(unique_id='WickedWhims')
def _wickedwhims_reset_sex_handler_on_sim_stand_posture(interaction_instance):
    interaction_guid = TurboResourceUtil.Resource.get_guid64(interaction_instance)
    if interaction_guid == SimInteraction.SIM_STAND:
        sim = TurboInteractionUtil.get_interaction_sim(interaction_instance)
        if sim_ev(sim).is_ready() and sim_ev(sim).active_sex_handler is not None and sim_ev(sim).active_sex_handler.is_playing is True:
            sim_ev(sim).active_sex_handler.stop(hard_stop=True, is_end=True, stop_reason='On Sim stand posture!')

@register_buildbuy_state_change_event_method(unique_id='WickedWhims', priority=0, on_exit=True)
def _wickedwhims_on_buildbuy_exit_reset_sex_interactions():
    for sim in TurboManagerUtil.Sim.get_all_sim_instance_gen(humans=True, pets=False):
        while sim_ev(sim).is_ready():
            if sim_ev(sim).active_sex_handler is not None and not TurboSimUtil.Interaction.is_running_interaction(sim, SimInteraction.WW_SEX_ANIMATION_DEFAULT):
                sim_ev(sim).active_sex_handler.reset()

ALLOWED_PRE_SEX_INTERACTIONS = (SimInteraction.SIM_STAND, SimInteraction.SIM_STAND_EXCLUSIVE, SimInteraction.SIM_SWIM, SimInteraction.WW_SEX_ANIMATION_DEFAULT, SimInteraction.WW_ROUTE_TO_SEX_LOCATION, SimInteraction.WW_WAIT_FOR_SEX_PARTNER)
ALLOWED_ACTIVE_SEX_INTERACTIONS = (SimInteraction.SIM_STAND, SimInteraction.SIM_STAND_EXCLUSIVE, SimInteraction.SIM_SWIM, SimInteraction.WW_SEX_ANIMATION_DEFAULT, SimInteraction.WW_SEX_REACTION_NEUTRAL, SimInteraction.WW_SEX_REACTION_FRIENDLY, SimInteraction.WW_SEX_REACTION_EXCITED, SimInteraction.WW_SEX_REACTION_FUNNY, SimInteraction.WW_SEX_REACTION_FLIRTY_MALE, SimInteraction.WW_SEX_REACTION_FLIRTY_FEMALE, SimInteraction.WW_SEX_REACTION_SAD, SimInteraction.WW_SEX_REACTION_ANGRY, SimInteraction.WW_SEX_REACTION_HORRIFIED, SimInteraction.WW_SEX_WATCH_DEFAULT, 76431, 77427, 76433, 77429, 76581, 77430, 76564, 77426, 76566, 77425, 76430, SimInteraction.WW_STOP_SEX)

@register_interaction_queue_event_method(unique_id='WickedWhims')
def _wickedwhims_block_sim_interaction_queue_during_sex(interaction_instance):
    interaction_guid = TurboResourceUtil.Resource.get_guid64(interaction_instance)
    sim = TurboInteractionUtil.get_interaction_sim(interaction_instance)
    target = TurboInteractionUtil.get_interaction_target(interaction_instance) if TurboTypesUtil.Sims.is_sim(TurboInteractionUtil.get_interaction_target(interaction_instance)) else None
    if _block_sim_interactions_during_sex(sim, interaction_guid) is False or _block_sim_interactions_during_sex(target, interaction_guid) is False:
        return False
    return True

def _block_sim_interactions_during_sex(sim, interaction_guid):
    if sim is None or not sim_ev(sim).is_ready():
        return True
    if sim_ev(sim).active_sex_handler is not None:
        if interaction_guid not in ALLOWED_ACTIVE_SEX_INTERACTIONS:
            return False
        return True
    if sim_ev(sim).active_pre_sex_handler is not None and sim_ev(sim).is_in_process_to_sex is True:
        if interaction_guid not in ALLOWED_PRE_SEX_INTERACTIONS:
            return False
        return True
    return True

