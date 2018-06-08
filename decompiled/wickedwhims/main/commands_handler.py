'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from sims.outfits.outfit_enums import BodyType
from enums.buffs_enum import SimBuff
from enums.relationship_enum import SimRelationshipBit
from turbolib.cas_util import TurboCASUtil
from turbolib.manager_util import TurboManagerUtil
from turbolib.sim_util import TurboSimUtil
from turbolib.world_util import TurboWorldUtil
from turbolib.wrappers.commands import register_game_command, TurboCommandType
from wickedwhims.main.settings.main_settings import open_main_settings
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.nudity.sims_init_handler import init_nudity_sim_ev_data
from wickedwhims.sex.animations.animations_disabler_handler import apply_disabled_sex_animations_from_dict
from wickedwhims.sex.sex_handlers.active.utils.satisfaction import clear_all_satifaction_data
from wickedwhims.sex.sex_operators.general_sex_handlers_operator import clear_sim_sex_extra_data
from wickedwhims.sex.sex_operators.pre_sex_handlers_operator import unprepare_npc_sim_from_sex
from wickedwhims.sex.sims_init_handler import init_sex_sim_ev_data
from wickedwhims.sxex_bridge.body import update_sim_body_flags
from wickedwhims.sxex_bridge.nudity import update_nude_body_data
from wickedwhims.sxex_bridge.penis import reset_penis_data
from wickedwhims.sxex_bridge.statistics import display_global_statistics_dialog, display_sim_statistics_dialog
from wickedwhims.sxex_bridge.underwear import update_sim_underwear_data
from wickedwhims.utils_buffs import remove_sim_buff
from wickedwhims.utils_cas import get_sim_outfit_parts
from wickedwhims.utils_lots import get_lot_structure_data
from wickedwhims.utils_relations import get_sim_ids_with_relationsip_bit, remove_relationsip_bit_with_sim
from wickedwhims.utils_saves.save_disabled_animations import update_disabled_animations_save_data

@register_game_command('ww.settings', command_type=TurboCommandType.LIVE)
def _wickedwhims_command_open_main_settings():
    open_main_settings()

@register_game_command('ww.stats', command_type=TurboCommandType.LIVE)
def _wickedwhims_command_display_global_statistics():
    display_global_statistics_dialog()

@register_game_command('ww.sim_stats', command_type=TurboCommandType.LIVE)
def _wickedwhims_command_display_sim_statistics():
    sim = TurboManagerUtil.Sim.get_active_sim()
    display_sim_statistics_dialog(sim)

@register_game_command('ww.list_rooms', command_type=TurboCommandType.LIVE)
def _wickedwhims_command_display_rooms_list(output=None):
    lot_structure_data = get_lot_structure_data()
    output(str(lot_structure_data))
    for room_structure_data in lot_structure_data.get_rooms_structure_data_gen():
        output(str(room_structure_data))
        for object_structure_data in room_structure_data.get_objects_structure_data_gen():
            output(str(object_structure_data))

@register_game_command('ww.force_fix', command_type=TurboCommandType.LIVE)
def _wickedwhims_command_force_fix_everything(output=None):
    _fix_sex_related_issues(output)
    _fix_pregnancy_related_issues(output)
    _force_fix_nudity_related_issues(output)
    _fix_nudity_related_issues(output)
    _force_fix_sex_related_issues(output)
    _force_fix_general_related_issues(output)
    _clean_sims_moodlets(output)
    output('Force fixing finished!')
    output('Only save your game if everything is running correctly!')

@register_game_command('ww.fix', command_type=TurboCommandType.LIVE)
def _wickedwhims_command_fix_everything(output=None):
    _fix_sex_related_issues(output)
    _fix_pregnancy_related_issues(output)
    _fix_nudity_related_issues(output)
    _fix_other_issues(output)
    output('Fixing finished!')
    output('Only save your game if everything is running correctly!')

def _fix_other_issues(output):
    output('Fixing other issues...')
    sims_list = list(TurboManagerUtil.Sim.get_all_sim_info_gen(humans=True, pets=False))
    for sim_info in sims_list:
        body_parts = get_sim_outfit_parts(sim_info)
        while BodyType.HAT in body_parts and body_parts[BodyType.HAT] == 11863322015736229112:
            TurboManagerUtil.Sim.remove_sim_info(sim_info)
    output('Fixed other issues.')

def _fix_nudity_related_issues(output):
    output('Fixing nudity related issues...')
    for sim_info in TurboManagerUtil.Sim.get_all_sim_info_gen(humans=True, pets=False):
        while TurboSimUtil.CAS.get_current_outfit(sim_info)[0] == TurboCASUtil.OutfitCategory.SPECIAL:
            if not TurboSimUtil.CAS.has_outfit(sim_info, (TurboCASUtil.OutfitCategory.EVERYDAY, 0)):
                TurboSimUtil.CAS.generate_outfit(sim_info, (TurboCASUtil.OutfitCategory.EVERYDAY, 0))
            TurboSimUtil.CAS.set_current_outfit(sim_info, (TurboCASUtil.OutfitCategory.EVERYDAY, 0))
            TurboSimUtil.Sim.reset_sim(sim_info)
    output('Fixed nudity related issues.')

def _force_fix_nudity_related_issues(output):
    for sim_info in TurboManagerUtil.Sim.get_all_sim_info_gen(humans=True, pets=False):
        init_nudity_sim_ev_data(sim_info)
        update_nude_body_data(sim_info, force_update=True)
        update_sim_body_flags(sim_info, update_nude_outfit_data=False)
        update_sim_underwear_data(sim_info)
    output('Force fixed nudity related issues.')

def _fix_pregnancy_related_issues(output):
    output('Fixing pregnancy related issues...')
    for sim_info in TurboManagerUtil.Sim.get_all_sim_info_gen(humans=True, pets=False):
        sim_ev(sim_info).has_condom_on = False
        sim_ev(sim_info).day_used_birth_control_pills = -1
        sim_ev(sim_info).birth_control_pill_power = 0
        sim_ev(sim_info).pregnancy_coming_flag = False
        sim_ev(sim_info).pregnancy_counter = 0
        partners_ids_list = get_sim_ids_with_relationsip_bit(sim_info, SimRelationshipBit.WW_POTENTIAL_PREGNANCY_PARENT)
        for partner_sim_id in partners_ids_list:
            partner_sim_info = TurboManagerUtil.Sim.get_sim_info(partner_sim_id)
            while partner_sim_info is not None:
                remove_relationsip_bit_with_sim(sim_info, partner_sim_info, SimRelationshipBit.WW_POTENTIAL_PREGNANCY_PARENT)
    output('Fixed pregnancy related issues.')

def _fix_sex_related_issues(output):
    output('Fixing sex related issues...')
    for sim_info in TurboManagerUtil.Sim.get_all_sim_info_gen(humans=True, pets=False):
        pre_sex_handler = sim_ev(sim_info).active_pre_sex_handler
        active_sex_handler = sim_ev(sim_info).active_sex_handler
        if active_sex_handler is not None:
            try:
                while active_sex_handler is not None:
                    active_sex_handler.stop(hard_stop=True, is_end=True, stop_reason='On fix everything command.')
            except:
                pass
        TurboSimUtil.Interaction.unlock_queue(sim_info)
        unprepare_npc_sim_from_sex(sim_info)
        if active_sex_handler is not None or pre_sex_handler is not None:
            TurboSimUtil.Sim.reset_sim(sim_info, hard_reset_on_exception=True)
        clear_sim_sex_extra_data(sim_info)
    output('Fixed sex related issues.')

def _force_fix_sex_related_issues(output):
    reset_penis_data()
    empty_animations = {'disabled_animations': list()}
    apply_disabled_sex_animations_from_dict(empty_animations)
    update_disabled_animations_save_data(empty_animations)
    for sim_info in TurboManagerUtil.Sim.get_all_sim_info_gen(humans=True, pets=False):
        init_sex_sim_ev_data(sim_info)
    output('Force fixed sex related issues.')

def _force_fix_general_related_issues(output):
    for sim_info in TurboManagerUtil.Sim.get_all_sim_info_gen(humans=True, pets=False):
        sim_ev(sim_info).outfit_parts_cache = dict()
        TurboSimUtil.CAS.set_current_outfit(sim_info, TurboSimUtil.CAS.get_current_outfit(sim_info), dirty=True)
    output('Force fixed general issues and refreshed current outfit.')

def _clean_sims_moodlets(output):
    for sim_info in TurboManagerUtil.Sim.get_all_sim_info_gen(humans=True, pets=False):
        clear_all_satifaction_data(sim_info)
        remove_sim_buff(sim_info, SimBuff.WW_NUDITY_IS_NAKED_LOW)
        remove_sim_buff(sim_info, SimBuff.WW_NUDITY_HAS_FLASHED)
        remove_sim_buff(sim_info, SimBuff.WW_DESIRE_POSITIVE)
        remove_sim_buff(sim_info, SimBuff.WW_DESIRE_NEGATIVE)
        remove_sim_buff(sim_info, SimBuff.WW_CUM_ON_BODY_POSITIVE)
        remove_sim_buff(sim_info, SimBuff.WW_CUM_ON_BODY_NEGATIVE)
        remove_sim_buff(sim_info, SimBuff.WW_SEX_REACTION_NEUTRAL)
        remove_sim_buff(sim_info, SimBuff.WW_SEX_REACTION_FUNNY)
        remove_sim_buff(sim_info, SimBuff.WW_SEX_REACTION_ANGRY)
        remove_sim_buff(sim_info, SimBuff.WW_SEX_REACTION_EXCITED)
        remove_sim_buff(sim_info, SimBuff.WW_SEX_REACTION_SAD)
        remove_sim_buff(sim_info, SimBuff.WW_SEX_REACTION_FRIENDLY)
        remove_sim_buff(sim_info, SimBuff.WW_SEX_REACTION_FLIRTY)
        remove_sim_buff(sim_info, SimBuff.WW_SEX_REACTION_HORRIFIED)
    output('Cleared moodlets from sims.')

@register_game_command('ww.save_time', command_type=TurboCommandType.LIVE)
def _wickedwhims_command_display_save_time(output=None):
    output('This save is ' + str(TurboWorldUtil.Time.get_absolute_days()) + ' days old.')

