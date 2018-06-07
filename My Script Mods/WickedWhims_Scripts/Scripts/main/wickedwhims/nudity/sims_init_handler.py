from turbolib.sim_util import TurboSimUtil
from wickedwhims.main.sim_ev_handler import sim_ev

def init_nudity_sim_ev_data(sim_identifier):
    sim_ev(sim_identifier).nude_outfit_parts = {6: -1, 7: -1, 8: -1, 115: -1}
    sim_ev(sim_identifier).penis_outfit_parts = {'soft': -1, 'hard': -1, 'soft_texture': -1, 'hard_texture': -1}
    sim_ev(sim_identifier).outfit_soft_penis_author = ''
    sim_ev(sim_identifier).outfit_hard_penis_author = ''
    sim_ev(sim_identifier).is_penis_hard = False
    sim_ev(sim_identifier).penis_hard_cooldown = 0
    sim_ev(sim_identifier).is_outfit_update_locked = False
    sim_ev(sim_identifier).has_original_outfit_modifications = False
    sim_ev(sim_identifier).original_outfit_category = -1
    sim_ev(sim_identifier).original_outfit_index = -1
    sim_ev(sim_identifier).current_outfit_category = 0
    sim_ev(sim_identifier).current_outfit_index = 0
    sim_ev(sim_identifier).previous_outfit_category = -1
    sim_ev(sim_identifier).previous_outfit_index = -1
    sim_ev(sim_identifier).underwear_flags = {'top': True if TurboSimUtil.Gender.is_female(sim_identifier) else False, 'bottom': True}
    sim_ev(sim_identifier).underwear_outfits_parts = {'00': [-1, -1], '01': [-1, -1], '02': [-1, -1], '03': [-1, -1], '04': [-1, -1], '10': [-1, -1], '11': [-1, -1], '12': [-1, -1], '13': [-1, -1], '14': [-1, -1], '20': [-1, -1], '21': [-1, -1], '22': [-1, -1], '23': [-1, -1], '24': [-1, -1], '40': [-1, -1], '41': [-1, -1], '42': [-1, -1], '43': [-1, -1], '44': [-1, -1]}
    sim_ev(sim_identifier).is_running_mirror_nudity_skill_interaction = False
    sim_ev(sim_identifier).nudity_skill_influence_score = 0
    sim_ev(sim_identifier).last_nudity_denied_permissions = None
    sim_ev(sim_identifier).last_nudity_autonomy = -1
    sim_ev(sim_identifier).nudity_autonomy_chance = 0.05
    sim_ev(sim_identifier).full_nudity_reaction_cooldown = 0
    sim_ev(sim_identifier).inner_nudity_reaction_cooldown = 0
    sim_ev(sim_identifier).on_toilet_outfit_state = -1
    sim_ev(sim_identifier).on_breast_feeding_outfit_state = -1
    sim_ev(sim_identifier).is_flashing = False

