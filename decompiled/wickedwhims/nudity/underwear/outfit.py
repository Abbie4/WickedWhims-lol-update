'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from turbolib.events.core import register_zone_load_event_method, is_game_loading
from turbolib.events.sims import register_sim_info_instance_init_event_method
from turbolib.manager_util import TurboManagerUtil
from turbolib.sim_util import TurboSimUtil
from wickedwhims.nudity.outfit_utils import is_sim_in_towel_outfit
from wickedwhims.sxex_bridge.underwear import set_sim_bottom_underwear_state, set_sim_top_underwear_state

@register_sim_info_instance_init_event_method(unique_id='WickedWhims', priority=1, late=True)
def _wickedwhims_register_towel_outfit_change_callback_on_new_sim(sim_info):
    if is_game_loading():
        return
    if TurboSimUtil.Species.is_human(sim_info):
        TurboSimUtil.CAS.register_for_outfit_changed_callback(sim_info, _on_sim_towel_outfit_change)

@register_zone_load_event_method(unique_id='WickedWhims', priority=40, late=True)
def _wickedwhims_register_towel_outfit_change_callback():
    for sim_info in TurboManagerUtil.Sim.get_all_sim_info_gen(humans=True, pets=False):
        TurboSimUtil.CAS.register_for_outfit_changed_callback(sim_info, _on_sim_towel_outfit_change)

def _on_sim_towel_outfit_change(sim_info, _):
    if is_sim_in_towel_outfit(sim_info):
        set_sim_top_underwear_state(sim_info, False)
        set_sim_bottom_underwear_state(sim_info, False)

