'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''import randomfrom turbolib.manager_util import TurboManagerUtilfrom turbolib.sim_util import TurboSimUtilfrom turbolib.wrappers.commands import register_game_command, TurboCommandType
@register_game_command('ww.gender_preference', command_type=TurboCommandType.LIVE)
def _wickedwhims_command_sim_gender_preference(*args, output=None):
    if len(args) != 1 and len(args) != 3:
        output('ww.gender_preference <hetero/homo/bi/none> [<sim_first_name> <sim_last_name>]')
        return
    sim_preference = str(args[0]).lower()
    if sim_preference != 'hetero' and (sim_preference != 'homo' and sim_preference != 'bi') and sim_preference != 'none':
        output("Incorrect hetero/homo/bi/none> variable. '" + sim_preference + "' is not a gender type. Must be 'hetero', 'homo', 'bi' or 'none'.")
        return
    if len(args) == 3:
        sim = TurboManagerUtil.Sim.get_sim_info_with_name(str(args[1]), str(args[2]))
        output("Sim with name '" + str(args[1]) + ' ' + str(args[2]) + "' was not found!")
        return
    else:
        sim = TurboManagerUtil.Sim.get_active_sim()
    if sim_preference == 'hetero':
        if TurboSimUtil.Gender.is_male(sim):
            TurboSimUtil.Gender.set_gender_preference(sim, TurboSimUtil.Gender.MALE, 0)
            TurboSimUtil.Gender.set_gender_preference(sim, TurboSimUtil.Gender.FEMALE, 100)
        else:
            TurboSimUtil.Gender.set_gender_preference(sim, TurboSimUtil.Gender.MALE, 100)
            TurboSimUtil.Gender.set_gender_preference(sim, TurboSimUtil.Gender.FEMALE, 0)
    elif sim_preference == 'homo':
        if TurboSimUtil.Gender.is_male(sim):
            TurboSimUtil.Gender.set_gender_preference(sim, TurboSimUtil.Gender.MALE, 100)
            TurboSimUtil.Gender.set_gender_preference(sim, TurboSimUtil.Gender.FEMALE, 0)
        else:
            TurboSimUtil.Gender.set_gender_preference(sim, TurboSimUtil.Gender.MALE, 0)
            TurboSimUtil.Gender.set_gender_preference(sim, TurboSimUtil.Gender.FEMALE, 100)
    elif sim_preference == 'bi':
        TurboSimUtil.Gender.set_gender_preference(sim, TurboSimUtil.Gender.MALE, 100)
        TurboSimUtil.Gender.set_gender_preference(sim, TurboSimUtil.Gender.FEMALE, 100)
    elif sim_preference == 'none':
        TurboSimUtil.Gender.set_gender_preference(sim, TurboSimUtil.Gender.MALE, 0)
        TurboSimUtil.Gender.set_gender_preference(sim, TurboSimUtil.Gender.FEMALE, 0)
    output("Sim '" + ' '.join(TurboSimUtil.Name.get_name(sim)) + "' gender preference has been changed.")

@register_game_command('ww.preference_hetero', command_type=TurboCommandType.LIVE)
def _wickedwhims_command_sims_preference_hetero(*args, output=None):
    if len(args) != 2:
        output('ww.preference_hetero <percentage> <all/male/female>')
        return
    try:
        percentage = int(args[0])
    except ValueError:
        output('Incorrect <percentage> variable. Must be integer.')
        return
    if percentage <= 0:
        output('Incorrect <percentage> variable. Must be higher than zero.')
        return
    if percentage > 100:
        percentage = 100
    sims_gender = str(args[1]).lower()
    if sims_gender != 'all' and sims_gender != 'male' and sims_gender != 'female':
        output("Incorrect <all/male/female> variable. '" + sims_gender + "' is not a gender type. Must be 'all', 'male' or 'female'.")
        return
    sims_list = list()
    for sim_info in TurboManagerUtil.Sim.get_all_sim_info_gen(humans=True, pets=False):
        while (sims_gender == 'all' or sims_gender == 'male') and (TurboSimUtil.Gender.is_male(sim_info) or sims_gender == 'female') and TurboSimUtil.Gender.is_female(sim_info):
            sims_list.append(sim_info)
    sims_list = random.sample(sims_list, int(percentage/100*len(sims_list)))
    for sim_info in sims_list:
        if TurboSimUtil.Gender.is_male(sim_info):
            TurboSimUtil.Gender.set_gender_preference(sim_info, TurboSimUtil.Gender.MALE, 0)
            TurboSimUtil.Gender.set_gender_preference(sim_info, TurboSimUtil.Gender.FEMALE, 100)
        else:
            TurboSimUtil.Gender.set_gender_preference(sim_info, TurboSimUtil.Gender.MALE, 100)
            TurboSimUtil.Gender.set_gender_preference(sim_info, TurboSimUtil.Gender.FEMALE, 0)
    output('Made ' + str(len(sims_list)) + ' (' + str(percentage) + '%) of ' + sims_gender + ' Sims purely heterosexual.')

@register_game_command('ww.preference_homo', command_type=TurboCommandType.LIVE)
def _wickedwhims_command_sims_preference_homo(*args, output=None):
    if len(args) != 2:
        output('ww.preference_homo <percentage> <all/male/female>')
        return
    try:
        percentage = int(args[0])
    except ValueError:
        output('Incorrect <percentage> variable. Must be integer.')
        return
    if percentage <= 0:
        output('Incorrect <percentage> variable. Must be higher than zero.')
        return
    if percentage > 100:
        percentage = 100
    sims_gender = str(args[1]).lower()
    if sims_gender != 'all' and sims_gender != 'male' and sims_gender != 'female':
        output("Incorrect <all/male/female> variable. '" + sims_gender + "' is not a gender type. Must be 'all', 'male' or 'female'.")
        return
    sims_list = list()
    for sim_info in TurboManagerUtil.Sim.get_all_sim_info_gen(humans=True, pets=False):
        while (sims_gender == 'all' or sims_gender == 'male') and (TurboSimUtil.Gender.is_male(sim_info) or sims_gender == 'female') and TurboSimUtil.Gender.is_female(sim_info):
            sims_list.append(sim_info)
    sims_list = random.sample(sims_list, int(percentage/100*len(sims_list)))
    for sim_info in sims_list:
        if TurboSimUtil.Gender.is_male(sim_info):
            TurboSimUtil.Gender.set_gender_preference(sim_info, TurboSimUtil.Gender.MALE, 100)
            TurboSimUtil.Gender.set_gender_preference(sim_info, TurboSimUtil.Gender.FEMALE, 0)
        else:
            TurboSimUtil.Gender.set_gender_preference(sim_info, TurboSimUtil.Gender.MALE, 0)
            TurboSimUtil.Gender.set_gender_preference(sim_info, TurboSimUtil.Gender.FEMALE, 100)
    output('Made ' + str(len(sims_list)) + ' (' + str(percentage) + '%) of ' + sims_gender + ' Sims purely homosexual.')

@register_game_command('ww.preference_bi', command_type=TurboCommandType.LIVE)
def _wickedwhims_command_sims_preference_bi(*args, output=None):
    if len(args) != 2:
        output('ww.preference_bi <percentage> <all/male/female>')
        return
    try:
        percentage = int(args[0])
    except ValueError:
        output('Incorrect <percentage> variable. Must be integer.')
        return
    if percentage <= 0:
        output('Incorrect <percentage> variable. Must be higher than zero.')
        return
    if percentage > 100:
        percentage = 100
    sims_gender = str(args[1]).lower()
    if sims_gender != 'all' and sims_gender != 'male' and sims_gender != 'female':
        output("Incorrect <all/male/female> variable. '" + sims_gender + "' is not a gender type. Must be 'all', 'male' or 'female'.")
        return
    sims_list = list()
    for sim_info in TurboManagerUtil.Sim.get_all_sim_info_gen(humans=True, pets=False):
        while (sims_gender == 'all' or sims_gender == 'male') and (TurboSimUtil.Gender.is_male(sim_info) or sims_gender == 'female') and TurboSimUtil.Gender.is_female(sim_info):
            sims_list.append(sim_info)
    sims_list = random.sample(sims_list, int(percentage/100*len(sims_list)))
    for sim_info in sims_list:
        TurboSimUtil.Gender.set_gender_preference(sim_info, TurboSimUtil.Gender.MALE, 100)
        TurboSimUtil.Gender.set_gender_preference(sim_info, TurboSimUtil.Gender.FEMALE, 100)
    output('Made ' + str(len(sims_list)) + ' (' + str(percentage) + '%) of ' + sims_gender + ' Sims purely bisexual.')

@register_game_command('ww.preference_random', command_type=TurboCommandType.LIVE)
def _wickedwhims_command_sims_preference_random(*args, output=None):
    if len(args) != 2:
        output('ww.preference_random <percentage> <all/male/female>')
        return
    try:
        percentage = int(args[0])
    except ValueError:
        output('Incorrect <percentage> variable. Must be integer.')
        return
    if percentage <= 0:
        output('Incorrect <percentage> variable. Must be higher than zero.')
        return
    if percentage > 100:
        percentage = 100
    sims_gender = str(args[1]).lower()
    if sims_gender != 'all' and sims_gender != 'male' and sims_gender != 'female':
        output("Incorrect <all/male/female> variable. '" + sims_gender + "' is not a gender type. Must be 'all', 'male' or 'female'.")
        return
    sims_list = list()
    for sim_info in TurboManagerUtil.Sim.get_all_sim_info_gen(humans=True, pets=False):
        while (sims_gender == 'all' or sims_gender == 'male') and (TurboSimUtil.Gender.is_male(sim_info) or sims_gender == 'female') and TurboSimUtil.Gender.is_female(sim_info):
            sims_list.append(sim_info)
    sims_list = random.sample(sims_list, int(percentage/100*len(sims_list)))
    for sim_info in sims_list:
        TurboSimUtil.Gender.set_gender_preference(sim_info, TurboSimUtil.Gender.MALE, random.randint(0, 100))
        TurboSimUtil.Gender.set_gender_preference(sim_info, TurboSimUtil.Gender.FEMALE, random.randint(0, 100))
    output('Made ' + str(len(sims_list)) + ' (' + str(percentage) + '%) of ' + sims_gender + ' Sims gender preference random.')

@register_game_command('ww.preference_neutral', command_type=TurboCommandType.LIVE)
def _wickedwhims_command_sims_preference_neutral(*args, output=None):
    if len(args) != 2:
        output('ww.preference_neutral <percentage> <all/male/female>')
        return
    try:
        percentage = int(args[0])
    except ValueError:
        output('Incorrect <percentage> variable. Must be integer.')
        return
    if percentage <= 0:
        output('Incorrect <percentage> variable. Must be higher than zero.')
        return
    if percentage > 100:
        percentage = 100
    sims_gender = str(args[1]).lower()
    if sims_gender != 'all' and sims_gender != 'male' and sims_gender != 'female':
        output("Incorrect <all/male/female> variable. '" + sims_gender + "' is not a gender type. Must be 'all', 'male' or 'female'.")
        return
    sims_list = list()
    for sim_info in TurboManagerUtil.Sim.get_all_sim_info_gen(humans=True, pets=False):
        while (sims_gender == 'all' or sims_gender == 'male') and (TurboSimUtil.Gender.is_male(sim_info) or sims_gender == 'female') and TurboSimUtil.Gender.is_female(sim_info):
            sims_list.append(sim_info)
    sims_list = random.sample(sims_list, int(percentage/100*len(sims_list)))
    for sim_info in sims_list:
        TurboSimUtil.Gender.set_gender_preference(sim_info, TurboSimUtil.Gender.MALE, 0)
        TurboSimUtil.Gender.set_gender_preference(sim_info, TurboSimUtil.Gender.FEMALE, 0)
    output('Reset ' + str(len(sims_list)) + ' (' + str(percentage) + '%) of ' + sims_gender + ' Sims gender preference.')
