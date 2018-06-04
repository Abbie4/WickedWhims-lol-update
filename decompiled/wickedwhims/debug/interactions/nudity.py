'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from enums.statistics_enum import SimCommodity
from turbolib.sim_util import TurboSimUtil
from turbolib.wrappers.interactions import TurboImmediateSuperInteraction, TurboInteractionStartMixin
from wickedwhims.debug.debug_controller import is_main_debug_flag_enabled
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.nudity.skill.skills_utils import is_sim_naturist, is_sim_exhibitionist, get_sim_nudity_skill_level, get_sim_nudity_skill_progress
from wickedwhims.sxex_bridge.body import get_sim_body_state, get_sim_additional_body_state, get_sim_actual_body_state, has_sim_outfit_top, has_sim_outfit_bottom, is_sim_outfit_fullbody
from wickedwhims.utils_interfaces import display_notification
from wickedwhims.utils_statistics import get_sim_statistic_value

class DebugNudityInfoInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'DebugNudityInfoInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return is_main_debug_flag_enabled()

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        sim = cls.get_interaction_target(interaction_instance)
        nudity_debug_info = ''
        nudity_debug_info += 'Body States:\
'
        nudity_debug_info += '  Top: ' + str(get_sim_body_state(sim, 6)) + '\
'
        nudity_debug_info += '  Bottom: ' + str(get_sim_body_state(sim, 7)) + '\
'
        nudity_debug_info += '\
Body Additional States:\
'
        nudity_debug_info += '  Top: ' + str(get_sim_additional_body_state(sim, 6, get_sim_body_state(sim, 6))) + '\
'
        nudity_debug_info += '  Bottom: ' + str(get_sim_additional_body_state(sim, 7, get_sim_body_state(sim, 7))) + '\
'
        nudity_debug_info += '\
Body Actual States:\
'
        nudity_debug_info += '  Top: ' + str(get_sim_actual_body_state(sim, 6)) + '\
'
        nudity_debug_info += '  Bottom: ' + str(get_sim_actual_body_state(sim, 7)) + '\
'
        nudity_debug_info += '\
Outfit Body Types:\
'
        nudity_debug_info += '  Has Top: ' + str(has_sim_outfit_top(sim)) + '\
'
        nudity_debug_info += '  Has Bottom: ' + str(has_sim_outfit_bottom(sim)) + '\
'
        nudity_debug_info += '  Has Full Body: ' + str(is_sim_outfit_fullbody(sim)) + '\
'
        nudity_debug_info += '\
Nudity Outfit Parts:\
'
        nudity_debug_info += '  Top: ' + str(sim_ev(sim).nude_outfit_parts[6]) + '\
'
        nudity_debug_info += '  Bottom: ' + str(sim_ev(sim).nude_outfit_parts[7]) + '\
'
        nudity_debug_info += '  Feet: ' + str(sim_ev(sim).nude_outfit_parts[8]) + '\
'
        nudity_debug_info += '  Penis Texture: ' + str(sim_ev(sim).nude_outfit_parts[115]) + '\
'
        nudity_debug_info += '\
Penis Outfit Parts:\
'
        nudity_debug_info += '  Soft: ' + str(sim_ev(sim).penis_outfit_parts['soft']) + '\
'
        nudity_debug_info += '  Hard: ' + str(sim_ev(sim).penis_outfit_parts['hard']) + '\
'
        nudity_debug_info += '\
Penis Parts Authors:\
'
        nudity_debug_info += '  Soft: ' + str(sim_ev(sim).outfit_soft_penis_author) + '\
'
        nudity_debug_info += '  Hard: ' + str(sim_ev(sim).outfit_hard_penis_author) + '\
'
        nudity_debug_info += '\
Penis State:\
'
        nudity_debug_info += '  Is Hard: ' + str(sim_ev(sim).is_penis_hard) + '\
'
        nudity_debug_info += '  Penis Cooldown: ' + str(sim_ev(sim).penis_hard_cooldown) + '\
'
        nudity_debug_info += '\
Original Outfit Data:\
'
        nudity_debug_info += '  Has Modifications: ' + str(sim_ev(sim).has_original_outfit_modifications) + '\
'
        nudity_debug_info += '  Category: ' + str(sim_ev(sim).original_outfit_category) + '\
'
        nudity_debug_info += '  Index: ' + str(sim_ev(sim).original_outfit_index) + '\
'
        nudity_debug_info += '  Update Locked: ' + str(sim_ev(sim).is_outfit_update_locked) + '\
'
        nudity_debug_info += '\
Nudity Skill:\
'
        nudity_debug_info += '  Is Naturist/Is Exhibitionist: ' + str(is_sim_naturist(sim)) + '/' + str(is_sim_exhibitionist(sim)) + '\
'
        nudity_debug_info += '  Level: ' + str(get_sim_nudity_skill_level(sim) + get_sim_nudity_skill_progress(sim)) + '\
'
        nudity_debug_info += '  Influence Score: ' + str(sim_ev(sim).nudity_skill_influence_score) + '\
'
        nudity_debug_info += '  Fatigue: ' + str(get_sim_statistic_value(sim, SimCommodity.WW_NUDITY_SKILL_FATIGUE)) + '\
'
        nudity_debug_info += '\
Nudity Reaction:\
'
        nudity_debug_info += '  Full Reaction Cooldown: ' + str(sim_ev(sim).full_nudity_reaction_cooldown) + '\
'
        nudity_debug_info += '  Inner Reaction Cooldown: ' + str(sim_ev(sim).inner_nudity_reaction_cooldown) + '\
'
        nudity_debug_info += '\
Special:\
'
        nudity_debug_info += '  Is Flashing: ' + str(sim_ev(sim).is_flashing) + '\
'
        nudity_debug_info += '  Toilet Use Outfit State: ' + str(sim_ev(sim).on_toilet_outfit_state) + '\
'
        nudity_debug_info += '  Breast Feeding Outfit State: ' + str(sim_ev(sim).on_breast_feeding_outfit_state) + '\
'
        display_notification(text=nudity_debug_info, title=str(TurboSimUtil.Name.get_name(sim)[0]) + ' ' + str(TurboSimUtil.Name.get_name(sim)[1]) + ' Nudity Debug', secondary_icon=sim)

