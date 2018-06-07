'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''from turbolib.manager_util import TurboManagerUtilfrom turbolib.sim_util import TurboSimUtilfrom wickedwhims.main.sim_ev_handler import sim_evfrom wickedwhims.utils_saves.save_main import get_save_dir, set_has_save_loading_error, get_save_id, load_json_file, save_json_fileSIMS_SAVE_DATA = dict()
def load_sims_save_data(slot_id=-1):
    global SIMS_SAVE_DATA
    save_id = get_save_id('sim', slot_id=slot_id)
    load_file_path = get_save_dir() + save_id + '.json'
    try:
        SIMS_SAVE_DATA = load_json_file(load_file_path) or dict()
    except:
        set_has_save_loading_error()
        SIMS_SAVE_DATA = dict()

def save_sims_save_data():
    save_id = get_save_id('sim')
    save_file_path = get_save_dir() + save_id + '.json'
    save_json_file(save_file_path, SIMS_SAVE_DATA)

def update_sim_save_data(sim_identifier):
    SIMS_SAVE_DATA[str(TurboManagerUtil.Sim.get_sim_id(sim_identifier))] = _get_sim_save_data(sim_identifier)

def _get_sim_save_data(sim_identifier):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    sim_dict = dict()
    sim_general_dict = dict()
    sim_name = TurboSimUtil.Name.get_name(sim_info)
    sim_general_dict['first_name'] = sim_name[0]
    sim_general_dict['last_name'] = sim_name[1]
    sim_nudity_dict = dict()
    sim_nudity_dict['outfit_soft_penis_author'] = sim_ev(sim_info).outfit_soft_penis_author
    sim_nudity_dict['outfit_hard_penis_author'] = sim_ev(sim_info).outfit_hard_penis_author
    sim_nudity_dict['is_penis_hard'] = sim_ev(sim_info).is_penis_hard
    sim_nudity_dict['penis_hard_cooldown'] = sim_ev(sim_info).penis_hard_cooldown
    sim_original_outfit_data = dict()
    sim_original_outfit_data['has_modifs'] = sim_ev(sim_info).has_original_outfit_modifications
    sim_original_outfit_data['category'] = sim_ev(sim_info).original_outfit_category
    sim_original_outfit_data['index'] = sim_ev(sim_info).original_outfit_index
    sim_nudity_dict['original_outfit_data'] = sim_original_outfit_data
    sim_nudity_dict['underwear_flags'] = sim_ev(sim_info).underwear_flags
    sim_nudity_dict['underwear_matrix'] = sim_ev(sim_info).underwear_outfits_parts
    sim_nudity_dict['nudity_skill_influence_score'] = sim_ev(sim_info).nudity_skill_influence_score
    sim_nudity_dict['last_nudity_autonomy'] = sim_ev(sim_info).last_nudity_autonomy
    sim_nudity_dict['nudity_autonomy_chance'] = sim_ev(sim_info).nudity_autonomy_chance
    sim_nudity_dict['on_toilet_outfit_state'] = sim_ev(sim_info).on_toilet_outfit_state
    sim_nudity_dict['on_breast_feeding_outfit_state'] = sim_ev(sim_info).on_breast_feeding_outfit_state
    sim_nudity_dict['is_flashing'] = sim_ev(sim_info).is_flashing
    sim_sex_dict = dict()
    sim_sex_dict['gender_recognition'] = sim_ev(sim_info).gender_recognition
    sim_sex_dict['is_playing_sex'] = sim_ev(sim_info).is_playing_sex
    sim_sex_dict['active_sex_handler_identifier'] = sim_ev(sim_info).active_sex_handler_identifier
    sim_sex_dict['has_setup_sex'] = sim_ev(sim_info).has_setup_sex
    sim_sex_dict['is_ready_to_sex'] = sim_ev(sim_info).is_ready_to_sex
    sim_sex_dict['is_in_process_to_sex'] = sim_ev(sim_info).is_in_process_to_sex
    sim_sex_dict['sim_sex_state_snapshot'] = sim_ev(sim_info).sim_sex_state_snapshot
    sim_sex_dict['sim_immutable_sex_state_snapshot'] = sim_ev(sim_info).sim_immutable_sex_state_snapshot
    sim_sex_dict['last_sex_autonomy'] = sim_ev(sim_info).last_sex_autonomy
    sim_sex_dict['has_condom_on'] = sim_ev(sim_info).has_condom_on
    sim_sex_dict['day_used_birth_control_pills'] = sim_ev(sim_info).day_used_birth_control_pills
    sim_sex_dict['birth_control_pill_power'] = sim_ev(sim_info).birth_control_pill_power
    sim_sex_dict['auto_use_of_condoms'] = sim_ev(sim_info).auto_use_of_condoms
    sim_sex_dict['auto_use_of_birth_pills'] = sim_ev(sim_info).auto_use_of_birth_pills
    sim_sex_dict['pregnancy_fertility_boost'] = sim_ev(sim_info).pregnancy_fertility_boost
    sim_sex_dict['pregnancy_coming_flag'] = sim_ev(sim_info).pregnancy_coming_flag
    sim_sex_dict['pregnancy_counter'] = sim_ev(sim_info).pregnancy_counter
    sim_sex_dict['miscarriage_potential'] = sim_ev(sim_info).miscarriage_potential
    sim_sex_dict['strapon_part_id'] = sim_ev(sim_info).strapon_part_id
    sim_sex_dict['is_strapon_allowed'] = sim_ev(sim_info).is_strapon_allowed
    sim_sex_dict['cum_apply_time'] = sim_ev(sim_info).cum_apply_time
    sim_pre_sex_handler_dict = dict() if sim_ev(sim_info).active_pre_sex_handler is None or not sim_ev(sim_info).active_pre_sex_handler.is_valid() else sim_ev(sim_info).active_pre_sex_handler.get_save_dict()
    sim_dict['general'] = sim_general_dict
    sim_dict['exhibitionism'] = sim_nudity_dict
    sim_dict['sex'] = sim_sex_dict
    sim_dict['pre_sex_handler'] = sim_pre_sex_handler_dict
    return sim_dict

def apply_sim_save_data(sim_identifier):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    sim_id = TurboManagerUtil.Sim.get_sim_id(sim_identifier)
    if str(sim_id) not in SIMS_SAVE_DATA:
        return
    if 'exhibitionism' in SIMS_SAVE_DATA[str(sim_id)]:
        sim_nudity_dict = SIMS_SAVE_DATA[str(sim_id)]['exhibitionism']
        sim_ev(sim_info).outfit_soft_penis_author = sim_nudity_dict.get('outfit_soft_penis_author', sim_ev(sim_info).outfit_soft_penis_author)
        sim_ev(sim_info).outfit_hard_penis_author = sim_nudity_dict.get('outfit_hard_penis_author', sim_ev(sim_info).outfit_hard_penis_author)
        sim_ev(sim_info).is_penis_hard = sim_nudity_dict.get('is_penis_hard', sim_ev(sim_info).is_penis_hard)
        sim_ev(sim_info).penis_hard_cooldown = sim_nudity_dict.get('penis_hard_cooldown', sim_ev(sim_info).penis_hard_cooldown)
        if 'original_outfit_data' in sim_nudity_dict:
            sim_original_outfit_data = sim_nudity_dict['original_outfit_data']
            sim_ev(sim_info).has_original_outfit_modifications = sim_original_outfit_data.get('has_modifs', sim_ev(sim_info).has_original_outfit_modifications)
            sim_ev(sim_info).original_outfit_category = sim_original_outfit_data.get('category', sim_ev(sim_info).original_outfit_category)
            sim_ev(sim_info).original_outfit_index = sim_original_outfit_data.get('index', sim_ev(sim_info).original_outfit_index)
        sim_ev(sim_info).underwear_flags = sim_nudity_dict.get('underwear_flags', sim_ev(sim_info).underwear_flags)
        sim_ev(sim_info).underwear_outfits_parts = sim_nudity_dict.get('underwear_matrix', sim_ev(sim_info).underwear_outfits_parts)
        sim_ev(sim_info).nudity_skill_influence_score = sim_nudity_dict.get('nudity_skill_influence_score', sim_ev(sim_info).nudity_skill_influence_score)
        sim_ev(sim_info).last_nudity_autonomy = sim_nudity_dict.get('last_nudity_autonomy', sim_ev(sim_info).last_nudity_autonomy)
        sim_ev(sim_info).nudity_autonomy_chance = sim_nudity_dict.get('nudity_autonomy_chance', sim_ev(sim_info).nudity_autonomy_chance)
        sim_ev(sim_info).on_toilet_outfit_state = sim_nudity_dict.get('on_toilet_outfit_state', sim_ev(sim_info).on_toilet_outfit_state)
        sim_ev(sim_info).on_breast_feeding_outfit_state = sim_nudity_dict.get('on_breast_feeding_outfit_state', sim_ev(sim_info).on_breast_feeding_outfit_state)
        sim_ev(sim_info).is_flashing = sim_nudity_dict.get('is_flashing', sim_ev(sim_info).is_flashing)
    if 'sex' in SIMS_SAVE_DATA[str(sim_id)]:
        sim_sex_dict = SIMS_SAVE_DATA[str(sim_id)]['sex']
        sim_ev(sim_info).gender_recognition = sim_sex_dict.get('gender_recognition', sim_ev(sim_info).gender_recognition)
        sim_ev(sim_info).is_playing_sex = sim_sex_dict.get('is_playing_sex', sim_ev(sim_info).is_playing_sex)
        sim_ev(sim_info).active_sex_handler_identifier = sim_sex_dict.get('active_sex_handler_identifier', sim_ev(sim_info).active_sex_handler_identifier)
        sim_ev(sim_info).has_setup_sex = sim_sex_dict.get('has_setup_sex', sim_ev(sim_info).has_setup_sex)
        sim_ev(sim_info).is_ready_to_sex = sim_sex_dict.get('is_ready_to_sex', sim_ev(sim_info).is_ready_to_sex)
        sim_ev(sim_info).is_in_process_to_sex = sim_sex_dict.get('is_going_to_sex_location', sim_ev(sim_info).is_in_process_to_sex)
        sim_ev(sim_info).sim_sex_state_snapshot = sim_sex_dict.get('sim_sex_state_snapshot', sim_ev(sim_info).sim_sex_state_snapshot)
        sim_ev(sim_info).sim_immutable_sex_state_snapshot = sim_sex_dict.get('sim_immutable_sex_state_snapshot', sim_ev(sim_info).sim_sex_state_snapshot)
        sim_ev(sim_info).last_sex_autonomy = sim_sex_dict.get('last_sex_autonomy', sim_ev(sim_info).last_sex_autonomy)
        sim_ev(sim_info).has_condom_on = sim_sex_dict.get('has_condom_on', sim_ev(sim_info).has_condom_on)
        sim_ev(sim_info).day_used_birth_control_pills = sim_sex_dict.get('day_used_birth_control_pills', sim_ev(sim_info).day_used_birth_control_pills)
        sim_ev(sim_info).birth_control_pill_power = sim_sex_dict.get('birth_control_pill_power', sim_ev(sim_info).birth_control_pill_power)
        sim_ev(sim_info).auto_use_of_condoms = sim_sex_dict.get('auto_use_of_condoms', sim_ev(sim_info).auto_use_of_condoms)
        sim_ev(sim_info).auto_use_of_birth_pills = sim_sex_dict.get('auto_use_of_birth_pills', sim_ev(sim_info).auto_use_of_birth_pills)
        sim_ev(sim_info).pregnancy_fertility_boost = sim_sex_dict.get('pregnancy_fertility_boost', sim_ev(sim_info).pregnancy_fertility_boost)
        sim_ev(sim_info).pregnancy_coming_flag = sim_sex_dict.get('pregnancy_coming_flag', sim_ev(sim_info).pregnancy_coming_flag)
        sim_ev(sim_info).pregnancy_counter = sim_sex_dict.get('pregnancy_counter', sim_ev(sim_info).pregnancy_counter)
        sim_ev(sim_info).miscarriage_potential = sim_sex_dict.get('miscarriage_potential', sim_ev(sim_info).miscarriage_potential)
        sim_ev(sim_info).strapon_part_id = sim_sex_dict.get('strapon_part_id', sim_ev(sim_info).strapon_part_id)
        sim_ev(sim_info).is_strapon_allowed = sim_sex_dict.get('is_strapon_allowed', sim_ev(sim_info).is_strapon_allowed)
        sim_ev(sim_info).cum_apply_time = sim_sex_dict.get('cum_apply_time', sim_ev(sim_info).cum_apply_time)
    if 'pre_sex_handler' in SIMS_SAVE_DATA[str(sim_id)]:
        sim_pre_sex_handler_dict = SIMS_SAVE_DATA[str(sim_id)]['pre_sex_handler']
        if sim_pre_sex_handler_dict is not None and len(sim_pre_sex_handler_dict) > 0:
            from wickedwhims.sex.sex_handlers.pre_sex_handler import PreSexInteractionHandler
            sim_ev(sim_info).active_pre_sex_handler = PreSexInteractionHandler.load_from_dict(sim_pre_sex_handler_dict) or sim_ev(sim_info).active_pre_sex_handler
