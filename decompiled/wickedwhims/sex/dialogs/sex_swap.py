'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from turbolib.manager_util import TurboManagerUtil
from turbolib.special.custom_exception_watcher import exception_watch
from turbolib.ui_util import TurboUIUtil
from wickedwhims.sex.utils.sex_swap import is_compatible_actor
from wickedwhims.utils_interfaces import display_sim_picker_dialog, display_ok_dialog

def open_swap_sex_sims_picker_dialog(active_sex_handler, swap_sim):

    @exception_watch()
    def swap_sim_picker_callback(dialog):
        if active_sex_handler is None:
            return False
        if not TurboUIUtil.SimPickerDialog.get_response_result(dialog):
            return False
        selected_sim_id = TurboUIUtil.SimPickerDialog.get_tag_result(dialog)
        if not selected_sim_id:
            return False
        selected_sim_info = TurboManagerUtil.Sim.get_sim_info(int(selected_sim_id))
        if selected_sim_info is None:
            return False
        sim_id = TurboManagerUtil.Sim.get_sim_id(swap_sim)
        if sim_id == selected_sim_id:
            return False
        sim_actor_id = active_sex_handler.get_actor_id_by_sim_id(sim_id)
        target_actor_id = active_sex_handler.get_actor_id_by_sim_id(selected_sim_id)
        if sim_actor_id == -1 or target_actor_id == -1:
            return False
        active_sex_handler.swap_actors(sim_actor_id, target_actor_id)
        return True

    sims_list = list()
    swap_actor_id = active_sex_handler.get_actor_id_by_sim_id(TurboManagerUtil.Sim.get_sim_id(swap_sim))
    swap_actor_data = active_sex_handler.get_animation_instance().get_actor(swap_actor_id)
    if swap_actor_data is None:
        return
    for (actor_id, actor_sim) in active_sex_handler.get_sims_list():
        if actor_id == swap_actor_id:
            pass
        actor_data = active_sex_handler.get_animation_instance().get_actor(actor_id)
        if actor_data is None:
            return
        while is_compatible_actor(actor_sim, actor_data, swap_sim, swap_actor_data):
            sims_list.append(TurboManagerUtil.Sim.get_sim_id(actor_sim))
    if not sims_list:
        display_ok_dialog(text=4051936639, title=465151699, title_tokens=(swap_sim,))
        return
    display_sim_picker_dialog(text=4149247255, text_tokens=(swap_sim,), title=465151699, title_tokens=(swap_sim,), sims_id_list=sims_list, sim=swap_sim, callback=swap_sim_picker_callback)

