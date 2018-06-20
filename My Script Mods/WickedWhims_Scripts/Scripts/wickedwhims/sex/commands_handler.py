'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
import random
from turbolib.manager_util import TurboManagerUtil
from turbolib.sim_util import TurboSimUtil
from turbolib.types_util import TurboTypesUtil
from turbolib.world_util import TurboWorldUtil
from turbolib.wrappers.commands import TurboCommandType, register_game_command
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.relationships.desire_handler import set_sim_desire_level
from wickedwhims.sex.autonomy.location import get_sex_locations, LocationStyleType, get_sex_location_style_and_chance
from wickedwhims.sex.autonomy.sims import get_list_of_possible_sex_pairs, get_available_for_sex_sims
from wickedwhims.sex.autonomy.trigger_random import trigger_random_sex_autonomy
from wickedwhims.sex.autonomy.trigger_solo import trigger_random_solo_sex_autonomy
from wickedwhims.sex.autonomy.triggers_handler import get_sims_risk_chance_for_sex_autonomy, get_chance_for_random_sex_autonomy, get_sex_autonomy_location
from wickedwhims.sex.cas_cum_handler import clean_sim_cum_layers, CumLayerType, get_cum_layer_type_by_name, apply_sim_cum_layer
from wickedwhims.sex.sex_location_handler import SexInteractionLocationType
from wickedwhims.sex.sex_operators.active_sex_handlers_operator import get_active_sex_handlers
from wickedwhims.sex.sex_operators.general_sex_handlers_operator import clear_sim_sex_extra_data
from wickedwhims.utils_interfaces import display_notification
from wickedwhims.utils_inventory import add_object_to_sim_inventory

@register_game_command('ww.force_sex_autonomy', 'ww.forcesexautonomy', command_type=TurboCommandType.LIVE)
def _wickedwhims_command_trigger_sex_autonomy(output=None):
    result = trigger_random_sex_autonomy(force=True)
    output('Forced Sex Autonomy resulted in a ' + ('positive' if result else 'negative') + ' outcome.')


@register_game_command('ww.force_solo_sex_autonomy', command_type=TurboCommandType.LIVE)
def _wickedwhims_command_trigger_solo_sex_autonomy(output=None):
    result = trigger_random_solo_sex_autonomy(force=True)
    output('Forced Solo Sex Autonomy resulted in a ' + ('positive' if result else 'negative') + ' outcome.')


@register_game_command('ww.test_sex_autonomy', 'ww.testsexautonomy', command_type=TurboCommandType.LIVE)
def _wickedwhims_command_test_sex_autonomy(output=None):
    output('--- Sex Autonomy Test ---')
    output('Looking for sims pairs...')
    available_sims = get_available_for_sex_sims()
    sims_pairs = get_list_of_possible_sex_pairs(available_sims)[:8]
    output('Found ' + str(len(available_sims)) + ' Sims and ' + str(len(sims_pairs)) + ' Sims pairs (top 6):')
    for sims_pair in sims_pairs:
        sim_name = TurboSimUtil.Name.get_name(sims_pair[0])
        target_name = TurboSimUtil.Name.get_name(sims_pair[1])
        output(' > ' + str(sim_name[0]) + ' ' + str(sim_name[1]) + ' + ' + str(target_name[0]) + ' ' + str(target_name[1]) + ' = ' + str(sims_pair[2]))
    if not sims_pairs:
        return
    sims_pair = random.choice(sims_pairs)[:2]
    sim_name = TurboSimUtil.Name.get_name(sims_pair[0])
    target_name = TurboSimUtil.Name.get_name(sims_pair[1])
    output(' ')
    output('Picked sims pair for sex location test: ' + str(sim_name[0]) + ' ' + str(sim_name[1]) + ' + ' + str(target_name[0]) + ' ' + str(target_name[1]))
    output(' ')
    autonomy_chance = get_chance_for_random_sex_autonomy(sims_pair)
    output('Current Base Success Rate: ' + str(autonomy_chance*100) + '%')
    output(' ')
    output('Looking for sex locations...')
    location_style_and_delay = get_sex_location_style_and_chance(sims_pair)
    sims_risk = get_sims_risk_chance_for_sex_autonomy(sims_pair, location_style_and_delay[0])
    output(' ')
    output('Picked Location Style: ' + str(location_style_and_delay[0].name))
    output('Picked Location Success Rate: ' + str(location_style_and_delay[1]*100) + '%')
    output('Sims Risk Success Rate: ' + str(sims_risk*100) + '%')
    sex_locations_cache = dict()
    output(' ')
    for location_style in (LocationStyleType.PRIVACY, LocationStyleType.COMFORT, LocationStyleType.SEMI_OPEN, LocationStyleType.OPEN, LocationStyleType.PUBLIC):
        sex_locations = get_sex_locations(sims_pair, location_style=location_style)
        sex_locations_cache[location_style] = sex_locations
        output('Found ' + str(len(sex_locations)) + " locations of type '" + str(location_style.name) + "' (top 6):")
        for sex_location in sex_locations[:6]:
            output(' > ' + str(SexInteractionLocationType.get_location_identifier(sex_location[1])) + ', score: ' + str(sex_location[0]) + ' [' + str(sex_location[1].__class__) + ']')
    output(' ')
    picked_sex_location = get_sex_autonomy_location(sims_pair, location_style=location_style_and_delay[0], sex_locations_override=sex_locations_cache[location_style_and_delay[0]]) if location_style_and_delay[0] != LocationStyleType.NONE else None
    if picked_sex_location is not None:
        output('Picked Sex Location: ' + str(SexInteractionLocationType.get_location_identifier(picked_sex_location)) + ' [' + str(picked_sex_location.__class__) + ']')
        display_notification(text='Picked Sex Autonomy Location', secondary_icon=picked_sex_location)
    else:
        output('Picked Sex Location: None')
    output(' ')
    output('Autonomy Test Run...')
    sims_test = random.uniform(0, 1) <= sims_risk
    output('Sims Test: ' + str('Positive' if sims_test else 'Negative'))
    autonomy_test = random.uniform(0, 1) <= autonomy_chance
    output('Autonomy Test: ' + str('Positive' if autonomy_test else 'Negative'))
    location_test = random.uniform(0, 1) <= location_style_and_delay[1]
    output('Location Test: ' + str('Positive' if location_test else 'Negative'))
    output(' ')
    output('Test Run Positive.' if autonomy_test and location_test and sims_test else 'Test Run Negative.')


@register_game_command('ww.apply_offset', 'ww.applyoffset', command_type=TurboCommandType.LIVE)
def _wickedwhims_command_apply_offset_to_animation(*args, output=None):
    if len(args) < 4:
        output('Not enough arguments!\nww.apply_offset <sim_first_name> <sim_last_name> <axis> <amount>')
        return
    sim_info = TurboManagerUtil.Sim.get_sim_info_with_name(str(args[0]), str(args[1]))
    if sim_info is None:
        output("Sim with name '" + str(args[0]) + ' ' + str(args[1]) + "' was not found!")
        return
    sim = TurboManagerUtil.Sim.get_sim_instance(sim_info)
    axis_arg = args[2].upper()
    amount_arg = args[3]
    if axis_arg != 'X' and (axis_arg != 'Y' and axis_arg != 'Z') and axis_arg != 'A':
        output(str(axis_arg) + ' is not an axis.')
        return
    try:
        amount = float(amount_arg)
    except ValueError:
        output('Invalid numerical value!')
        return
    active_sex_handler = sim_ev(sim_info).active_sex_handler
    if active_sex_handler is None:
        output('Sim is not in sex!')
        return
    actor_id = active_sex_handler.get_actor_id_by_sim_id(TurboManagerUtil.Sim.get_sim_id(sim))
    actor_data = active_sex_handler.get_animation_instance().get_actor(actor_id)
    if axis_arg == 'X':
        actor_data.temp_x_offset = amount
    elif axis_arg == 'Y':
        actor_data.temp_y_offset = amount
    elif axis_arg == 'Z':
        actor_data.temp_z_offset = amount
    elif axis_arg == 'A':
        actor_data.temp_facing_offset = amount
    TurboWorldUtil.Location.move_object_to(sim, active_sex_handler.get_location(), x_offset=actor_data.temp_x_offset, y_offset=actor_data.temp_y_offset, z_offset=actor_data.temp_z_offset, orientation_offset=actor_data.temp_facing_offset)
    output('Offset applied!')


@register_game_command('ww.restart_sex', command_type=TurboCommandType.LIVE)
def _wickedwhims_command_restart_sex(output=None):
    for sex_handler in get_active_sex_handlers():
        while not sex_handler.is_playing is False:
            if sex_handler.is_ready_to_unregister is True:
                pass
            sex_handler.restart()
    output('All running sex interaction have been restarted.')


@register_game_command('ww.stop_sex', 'ww.stopsex', command_type=TurboCommandType.LIVE)
def _wickedwhims_command_stop_all_sex(output=None):
    for sim_info in TurboManagerUtil.Sim.get_all_sim_info_gen(humans=True, pets=False):
        pre_sex_handler = sim_ev(sim_info).active_pre_sex_handler
        active_sex_handler = sim_ev(sim_info).active_sex_handler
        clear_sim_sex_extra_data(sim_info)
        if pre_sex_handler is not None:
            for sim in pre_sex_handler.get_actors_sim_instance_gen():
                if sim is None:
                    pass
                TurboSimUtil.Interaction.unlock_queue(sim)
                TurboSimUtil.Sim.reset_sim(sim, hard_reset_on_exception=True)
        try:
            while active_sex_handler is not None:
                active_sex_handler.stop(hard_stop=True, is_end=True, stop_reason='On stop sex command.')
        except:
            pass
    output('Sex was stopped. Sad.')


@register_game_command('ww.give_condom', command_type=TurboCommandType.LIVE)
def _wickedwhims_command_give_condom(output=None):
    sim = TurboManagerUtil.Sim.get_active_sim()
    add_object_to_sim_inventory(sim, 11033454205624062315)
    output('Condom was added to the sim inventory.')


@register_game_command('ww.give_condoms_box', command_type=TurboCommandType.LIVE)
def _wickedwhims_command_give_condoms_box(output=None):
    sim = TurboManagerUtil.Sim.get_active_sim()
    add_object_to_sim_inventory(sim, 11891109332024626718)
    output('Condom box was added to the sim inventory.')


@register_game_command('ww.give_birth_pill', command_type=TurboCommandType.LIVE)
def _wickedwhims_command_give_birth_control_pill(output=None):
    sim = TurboManagerUtil.Sim.get_active_sim()
    add_object_to_sim_inventory(sim, 14744913713073164047)
    output('Birth control pill was added to the sim inventory.')


@register_game_command('ww.give_birth_pills_box', command_type=TurboCommandType.LIVE)
def _wickedwhims_command_give_birth_control_pills_box(output=None):
    sim = TurboManagerUtil.Sim.get_active_sim()
    add_object_to_sim_inventory(sim, 16840089604155629431)
    output('Birth control pills box was added to the sim inventory.')


@register_game_command('ww.apply_cum', command_type=TurboCommandType.LIVE)
def _wickedwhims_command_clear_cum(*args, output=None):
    args_len = len(args)
    sim = None
    if args_len == 0:
        output('Missing cum type and/or sim name! (ww.apply_cum <face/chest/back/vagina/butt/feet> [<first_name> <last_name>])')
        return
    if args_len == 1:
        sim = TurboManagerUtil.Sim.get_active_sim()
    elif args_len >= 3:
        sim_info = TurboManagerUtil.Sim.get_sim_info_with_name(str(args[1]), str(args[2]))
        if sim_info is None:
            output("Sim with name '" + str(args[1]) + ' ' + str(args[2]) + "' was not found!")
            return
        sim = TurboManagerUtil.Sim.get_sim_instance(sim_info)
    if sim is None:
        output('No Sim found!')
        return
    cum_layer = get_cum_layer_type_by_name(str(args[0]))
    if cum_layer == CumLayerType.NONE:
        output("Cum layer with name '" + str(args[0]) + "' does not exist!")
        return
    apply_sim_cum_layer(sim, (cum_layer,))
    output('Cum applied!')


@register_game_command('ww.clear_cum', 'ww.clearcum', command_type=TurboCommandType.LIVE)
def _wickedwhims_command_clear_cum(output=None):
    sim = TurboManagerUtil.Sim.get_active_sim()
    clean_sim_cum_layers(sim)
    output('Cleard cum.')


@register_game_command('ww.set_desire', 'ww.setdesire', command_type=TurboCommandType.LIVE)
def _wickedwhims_command_set_desire_level(*args, output=None):
    sim = TurboManagerUtil.Sim.get_active_sim()
    args_len = len(args)
    if args_len != 1:
        return
    try:
        amount = int(args[0])
    except ValueError:
        return
    set_sim_desire_level(sim, amount)
    output('Desire level of active sim set to: ' + str(amount))

