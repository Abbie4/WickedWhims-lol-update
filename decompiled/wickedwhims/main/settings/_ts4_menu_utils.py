'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from sims.household import Household
from sims.outfits.outfit_enums import BodyType
from sims.sim_spawner import SimCreator, SimSpawner
from turbolib.cas_util import TurboCASUtil
from turbolib.manager_util import TurboManagerUtil
from turbolib.sim_util import TurboSimUtil
from wickedwhims.main.tick_handler import register_on_game_update_method
MENU_SIM_ID = None

def get_menu_sim():
    global MENU_SIM_ID
    if MENU_SIM_ID is None:
        household = Household(SimSpawner._get_default_account(), starting_funds=0)
        household.set_to_hidden()
        (sim_info_list, _) = SimSpawner.create_sim_infos((SimCreator(),), household=household, creation_source='WickedWhims Menu')
        if sim_info_list:
            sim_info = sim_info_list[0]
            MENU_SIM_ID = TurboManagerUtil.Sim.get_sim_id(sim_info)
            _prepare_sim_outfit(sim_info)
    if MENU_SIM_ID is not None:
        return TurboManagerUtil.Sim.get_sim_info(MENU_SIM_ID)

def _prepare_sim_outfit(sim_info):
    TurboSimUtil.CAS.set_current_outfit(sim_info, (TurboCASUtil.OutfitCategory.EVERYDAY, 0))
    try:
        outfit_editor = TurboCASUtil.OutfitEditor(sim_info, outfit_category_and_index=(TurboCASUtil.OutfitCategory.EVERYDAY, 0))
    except RuntimeError:
        return
    for body_type in outfit_editor.get_body_types():
        outfit_editor.remove_body_type(body_type)
    outfit_editor.add_cas_part(BodyType.HAT, 11863322015736229112)
    outfit_editor.apply()
    TurboSimUtil.CAS.set_current_outfit(sim_info, (TurboCASUtil.OutfitCategory.EVERYDAY, 0))

def clear_menu_sim():
    global MENU_SIM_ID
    if MENU_SIM_ID is not None:
        sim_info = TurboManagerUtil.Sim.get_sim_info(MENU_SIM_ID)
        if sim_info is not None:
            TurboManagerUtil.Sim.remove_sim_info(sim_info)
        MENU_SIM_ID = None

@register_on_game_update_method(interval=12000)
def _clear_stuck_menu_sim_on_game_update():
    clear_menu_sim()

