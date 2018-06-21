import random
from enums.traits_enum import SimTrait
from turbolib.cas_util import TurboCASUtil
from turbolib.manager_util import TurboManagerUtil
from turbolib.sim_util import TurboSimUtil
from turbolib.wrappers.commands import register_game_command, TurboCommandType
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.nudity.skill.skills_utils import set_sim_nudity_skill_level, remove_sim_nudity_skill, apply_nudity_skill_influence
from wickedwhims.nudity.story_progression_handler import trigger_story_progression
from wickedwhims.nudity.underwear.mannequin import open_underwear_mannequin
from wickedwhims.nudity.underwear.operator import get_random_underwear_set, set_sim_underwear_data, has_sim_underwear_data
from wickedwhims.sxex_bridge.nudity import update_nude_body_data, reset_sim_bathing_outfits
from wickedwhims.sxex_bridge.outfit import dress_up_outfit
from wickedwhims.sxex_bridge.penis import set_sim_penis_state
from wickedwhims.utils_cas import set_bodytype_caspart
from wickedwhims.utils_interfaces import display_notification
from wickedwhims.utils_traits import remove_sim_trait, add_sim_trait

@register_game_command('ww.set_nudity_skill', command_type=TurboCommandType.LIVE)
def _wickedwhims_command_set_sim_nudity_skill_level(*args, output=None):
    sim = TurboManagerUtil.Sim.get_active_sim()
    if len(args) < 1:
        output('ww.set_nudity_skill <level>')
        return
    try:
        level = int(args[0])
    except ValueError:
        output('Incorrect <level> variable!')
        return
    if level > 0:
        set_sim_nudity_skill_level(sim, level)
    else:
        remove_sim_nudity_skill(sim)
    output('Sim nudity skill has been set to level ' + str(level) + '.')


@register_game_command('ww.set_global_nudity_skill', command_type=TurboCommandType.LIVE)
def _wickedwhims_command_set_global_nudity_skill_level(*args, output=None):
    if len(args) < 1:
        output('ww.set_global_nudity_skill <level>')
        return
    try:
        level = int(args[0])
    except ValueError:
        output('Incorrect <level> variable!')
        return
    for sim_info in TurboManagerUtil.Sim.get_all_sim_info_gen(humans=True, pets=False):
        if TurboSimUtil.Age.is_younger_than(sim_info, TurboSimUtil.Age.CHILD):
            pass
        if level > 0:
            set_sim_nudity_skill_level(sim_info, level)
        else:
            remove_sim_nudity_skill(sim_info)
    output('Global nudity skill has been set to level ' + str(level) + '.')


@register_game_command('ww.convert_to_exhibitionism', command_type=TurboCommandType.LIVE)
def _wickedwhims_command_set_sim_nudity_skill_level(output=None):
    sim = TurboManagerUtil.Sim.get_active_sim()
    add_sim_trait(sim, SimTrait.WW_EXHIBITIONIST)
    output('Sim Exhibitionist trait has been added.')


@register_game_command('ww.global_convert_to_exhibitionism', command_type=TurboCommandType.LIVE)
def _wickedwhims_command_set_sim_nudity_skill_level(output=None):
    for sim_info in TurboManagerUtil.Sim.get_all_sim_info_gen(humans=True, pets=False):
        if TurboSimUtil.Age.is_younger_than(sim_info, TurboSimUtil.Age.CHILD):
            pass
        add_sim_trait(sim_info, SimTrait.WW_EXHIBITIONIST)
    output('Sim Exhibitionist trait has been added to all Sims.')


@register_game_command('ww.remove_exhibitionist_trait', command_type=TurboCommandType.LIVE)
def _wickedwhims_command_set_sim_nudity_skill_level(output=None):
    sim = TurboManagerUtil.Sim.get_active_sim()
    remove_sim_nudity_skill(sim)
    remove_sim_trait(sim, SimTrait.WW_EXHIBITIONIST)
    output('Sim Exhibitionist trait has been removed.')


@register_game_command('ww.remove_global_exhibitionist_trait', command_type=TurboCommandType.LIVE)
def _wickedwhims_command_set_sim_nudity_skill_level(output=None):
    for sim_info in TurboManagerUtil.Sim.get_all_sim_info_gen(humans=True, pets=False):
        if TurboSimUtil.Age.is_younger_than(sim_info, TurboSimUtil.Age.CHILD):
            pass
        remove_sim_nudity_skill(sim_info)
        remove_sim_trait(sim_info, SimTrait.WW_EXHIBITIONIST)
    output('Sim Exhibitionist trait has been removed from all Sims.')


@register_game_command('ww.simulate_nudity_story_progression', command_type=TurboCommandType.LIVE)
def _wickedwhims_command_simulate_story_progression(output=None):
    for sim_info in TurboManagerUtil.Sim.get_all_sim_info_gen(humans=True, pets=False):
        if TurboSimUtil.Age.is_younger_than(sim_info, TurboSimUtil.Age.CHILD):
            pass
        apply_nudity_skill_influence(sim_info, random.uniform(0, 1)*random.randint(1, 7))
    trigger_story_progression()
    output('Simulated a day of nudity story progression.')


@register_game_command('ww.edit_underwear', command_type=TurboCommandType.LIVE)
def _wickedwhims_command_edit_sim_underwear():
    open_underwear_mannequin()


@register_game_command('ww.random_sims_underwear', command_type=TurboCommandType.LIVE)
def _wickedwhims_command_random_underwear_for_all_npc_sims(output=None):
    for sim_info in TurboManagerUtil.Sim.get_all_sim_info_gen(humans=True, pets=False):
        if TurboSimUtil.Sim.is_player(sim_info):
            pass
        underwear_data = get_random_underwear_set(sim_info)
        for outfit_category in (TurboCASUtil.OutfitCategory.EVERYDAY, TurboCASUtil.OutfitCategory.FORMAL, TurboCASUtil.OutfitCategory.ATHLETIC, TurboCASUtil.OutfitCategory.PARTY, TurboCASUtil.OutfitCategory.HOTWEATHER, TurboCASUtil.OutfitCategory.COLDWEATHER):
            for outfit_index in range(TurboCASUtil.OutfitCategory.get_maximum_outfits_for_outfit_category(outfit_category)):
                while TurboSimUtil.CAS.has_outfit(sim_info, (outfit_category, outfit_index)):
                    if not has_sim_underwear_data(sim_info, (outfit_category, outfit_index)):
                        set_sim_underwear_data(sim_info, underwear_data, (outfit_category, outfit_index))
    output('Random underwear has been set for all NPC Sims.')


@register_game_command('ww.list_sims_underwear', command_type=TurboCommandType.LIVE)
def _wickedwhims_command_list_sims_underwear():
    for sim_info in TurboManagerUtil.Sim.get_all_sim_info_gen(humans=True, pets=False):
        underwear_info_list = ''
        for (outfit_id, underwear_data) in sim_ev(sim_info).underwear_outfits_parts.items():
            underwear_info_list += str(outfit_id) + ' > ' + str(underwear_data) + '\n'
        display_notification(text=underwear_info_list, secondary_icon=sim_info)


@register_game_command('ww.global_revert_outfits', command_type=TurboCommandType.LIVE)
def _wickedwhims_command_global_revert_outfits(output=None):
    for sim_info in TurboManagerUtil.Sim.get_all_sim_info_gen(humans=True, pets=False):
        dress_up_outfit(sim_info)
    output('Every Sim outfit has been reverted!')


@register_game_command('ww.set_cas_part', command_type=TurboCommandType.LIVE)
def _wickedwhims_command_set_current_outfit_cas_part(*args, output=None):
    if len(args) < 2:
        output('ww.set_cas_part <body_type> <cas_part>')
        return
    sim = TurboManagerUtil.Sim.get_active_sim()
    body_type = int(args[0])
    cas_part = int(args[1])
    cas_bodypart = TurboCASUtil.Outfit.get_cas_part_body_type_id(cas_part)
    output('CAS Default Body Part: ' + str(cas_bodypart))
    current_outfit = TurboSimUtil.CAS.get_current_outfit(sim)
    set_bodytype_caspart(sim, current_outfit, body_type, cas_part, remove=cas_part == 0)
    try:
        TurboSimUtil.CAS.refresh_outfit(sim)
    except:
        pass
    output('Outfit has been changed.')


@register_game_command('ww.display_outfit', command_type=TurboCommandType.LIVE)
def _wickedwhims_command_display_current_outfit_cas_parts(output=None):
    sim = TurboManagerUtil.Sim.get_active_sim()
    current_outfit_category_and_index = TurboSimUtil.CAS.get_current_outfit(sim)
    output('-------------- Outfit Parts --------------')
    body_parts = TurboSimUtil.CAS.get_outfit_parts(sim, current_outfit_category_and_index)
    for (body_type, cas_part) in body_parts.items():
        output(str(body_type) + ' -> ' + str(cas_part))
    output('---------- Appearance Modifiers ----------')
    appearance_modifiers = TurboCASUtil.AppearanceModifier.get_sim_appearance_modifiers(sim, TurboCASUtil.AppearanceModifier.AppearanceModifierType.SET_CAS_PART)
    for appearance_modifier in appearance_modifiers:
        cas_part = int(getattr(appearance_modifier, 'cas_part'))
        body_type = TurboCASUtil.Outfit.get_cas_part_body_type_id(cas_part)
        output(str(body_type) + ' -> ' + str(cas_part))
    output('------------------------------------------')


@register_game_command('ww.fix_sim_nude_outfit', 'ww.fix_nude_outfit', command_type=TurboCommandType.LIVE)
def _wickedwhims_command_fix_nude_outfit(output=None):
    sim = TurboManagerUtil.Sim.get_active_sim()
    reset_sim_bathing_outfits(sim, ignore_nudity_assurance_setting=True)
    update_nude_body_data(sim, force_update=True)
    output('Active Sim nude outfit has be reset!')


@register_game_command('ww.fix_all_sims_nude_outfit', command_type=TurboCommandType.LIVE)
def _wickedwhims_command_fix_nude_outfit(output=None):
    output('Started to reset all Sims nude outfit...')
    for sim_info in TurboManagerUtil.Sim.get_all_sim_info_gen(humans=True, pets=False):
        reset_sim_bathing_outfits(sim_info, ignore_nudity_assurance_setting=True)
        update_nude_body_data(sim_info, force_update=True)
    output('Every Sim nude outfit has be reset!')


@register_game_command('ww.give_erection', command_type=TurboCommandType.LIVE)
def _wickedwhims_command_give_sim_erection(output=None):
    sim = TurboManagerUtil.Sim.get_active_sim()
    set_sim_penis_state(sim, True, 10, set_if_nude=True)
    output('Got hard.')


@register_game_command('ww.lose_erection', command_type=TurboCommandType.LIVE)
def _wickedwhims_command_lose_sim_erection(output=None):
    sim = TurboManagerUtil.Sim.get_active_sim()
    set_sim_penis_state(sim, False, 0, set_if_nude=True)
    output('Soften out.')

