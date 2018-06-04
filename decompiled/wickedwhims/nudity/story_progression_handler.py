'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from turbolib.components_util import TurboComponentUtil
from turbolib.manager_util import TurboManagerUtil
from turbolib.sim_util import TurboSimUtil
from turbolib.world_util import TurboWorldUtil
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.main.tick_handler import register_on_game_update_method
from wickedwhims.nudity.notifications_handler import nudity_notification
from wickedwhims.nudity.nudity_settings import get_nudity_setting, NuditySetting
from wickedwhims.nudity.skill.skills_utils import get_sim_nudity_skill_level, has_sim_reached_max_nudity_skill_level, get_sim_nudity_skill_progress, increase_sim_nudity_skill
LAST_DAY_VALUE = -1

@register_on_game_update_method(interval=10000)
def _update_nudity_story_progression_on_game_update():
    global LAST_DAY_VALUE
    if not get_nudity_setting(NuditySetting.NUDITY_SWITCH_STATE, variable_type=bool) or not get_nudity_setting(NuditySetting.STORY_PROGRESSION_STATE, variable_type=bool):
        return
    current_day = TurboWorldUtil.Time.get_day_of_week()
    if LAST_DAY_VALUE == -1:
        LAST_DAY_VALUE = current_day
        return
    if current_day <= LAST_DAY_VALUE:
        return
    LAST_DAY_VALUE = current_day
    trigger_story_progression()

def trigger_story_progression():
    story_progression_debug_sims_count = 0
    story_progression_debug_data = list()
    for sim_info in TurboManagerUtil.Sim.get_all_sim_info_gen(humans=True, pets=False):
        if TurboSimUtil.Age.is_younger_than(sim_info, TurboSimUtil.Age.CHILD):
            pass
        if not TurboSimUtil.Component.has_component(sim_info, TurboComponentUtil.ComponentType.STATISTIC):
            pass
        if has_sim_reached_max_nudity_skill_level(sim_info):
            pass
        nudity_skill_value = get_sim_nudity_skill_level(sim_info) + get_sim_nudity_skill_progress(sim_info)
        influence_amount = _update_and_get_influence_score(sim_info)
        if influence_amount > 0:
            increase_sim_nudity_skill(sim_info, influence_amount)
            story_progression_debug_data.append((TurboSimUtil.Name.get_name(sim_info), nudity_skill_value, influence_amount))
        story_progression_debug_sims_count += 1
    from wickedwhims.debug.debug_controller import is_main_debug_flag_enabled
    if is_main_debug_flag_enabled():
        debug_text = ''
        for ((sim_first_name, sim_last_name), current_skill_value, influence_amount) in story_progression_debug_data:
            debug_text += '\
' + str(sim_first_name) + ' ' + str(sim_last_name) + ': ' + str('%.2f' % current_skill_value) + ' -> ' + str('%.2f' % (current_skill_value + influence_amount/100))
        nudity_notification(text='Checked Sims: ' + str(story_progression_debug_sims_count) + '\
Leveled Sims:' + debug_text, title='Nudity Story Progression')

def _update_and_get_influence_score(sim_info):
    influence_score = 7 if sim_ev(sim_info).nudity_skill_influence_score >= 7 else sim_ev(sim_info).nudity_skill_influence_score
    sim_ev(sim_info).nudity_skill_influence_score = max(0, sim_ev(sim_info).nudity_skill_influence_score - influence_score)
    return influence_score

