from wickedwhims.main.sim_ev_handler import sim_ev

def init_sex_sim_ev_data(sim_info):
    sim_ev(sim_info).gender_recognition = 0
    sim_ev(sim_info).is_ready_to_sex = False
    sim_ev(sim_info).is_in_process_to_sex = False
    sim_ev(sim_info).in_sex_process_interaction = None
    sim_ev(sim_info).has_setup_sex = False
    sim_ev(sim_info).active_pre_sex_handler = None
    sim_ev(sim_info).is_playing_sex = False
    sim_ev(sim_info).active_sex_handler = None
    sim_ev(sim_info).active_sex_handler_identifier = '-1'
    sim_ev(sim_info).sim_sex_state_snapshot = dict()
    sim_ev(sim_info).sim_immutable_sex_state_snapshot = dict()
    sim_ev(sim_info).last_sex_autonomy = -10000000
    sim_ev(sim_info).has_condom_on = False
    sim_ev(sim_info).day_used_birth_control_pills = -1
    sim_ev(sim_info).birth_control_pill_power = 0
    sim_ev(sim_info).auto_use_of_condoms = True
    sim_ev(sim_info).auto_use_of_birth_pills = True
    sim_ev(sim_info).pregnancy_fertility_boost = (0, 1.0)
    sim_ev(sim_info).pregnancy_coming_flag = False
    sim_ev(sim_info).pregnancy_counter = 0
    sim_ev(sim_info).miscarriage_potential = 0
    sim_ev(sim_info).strapon_part_id = -1
    sim_ev(sim_info).is_strapon_allowed = True
    sim_ev(sim_info).full_cum_reaction_cooldown = 0
    sim_ev(sim_info).inner_cum_reaction_cooldown = 0
    sim_ev(sim_info).cum_apply_time = -1
    sim_ev(sim_info).sex_reaction_attempt_cooldown = 0
    sim_ev(sim_info).sex_reaction_cooldown = 0
    sim_ev(sim_info).sex_reaction_handlers_list = list()
    sim_ev(sim_info).watching_sim_id = -1

