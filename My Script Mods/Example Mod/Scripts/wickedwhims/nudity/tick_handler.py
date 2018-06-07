'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''from turbolib.manager_util import TurboManagerUtilfrom wickedwhims.main.tick_handler import register_on_game_update_methodfrom wickedwhims.nudity.nudity_settings import NuditySetting, get_nudity_settingfrom wickedwhims.nudity.permissions.active_test import test_sim_nudity_permissionfrom wickedwhims.nudity.skill.active_nudity import update_sim_nudity_skill_on_active_nudityfrom wickedwhims.nudity.skill.mirror_nudity import update_sim_nudity_skill_on_mirror_usefrom wickedwhims.nudity.skill.skills_utils import update_sim_nudity_skill_fatiguefrom wickedwhims.nudity.statistics.nudity import increase_sim_nudity_time_statisticfrom wickedwhims.sxex_bridge.penis import update_sim_penis_state
@register_on_game_update_method(interval=1500)
def _update_nudity_on_game_update():
    for sim in TurboManagerUtil.Sim.get_all_sim_instance_gen(humans=True, pets=False):
        update_sim_penis_state(sim)
        increase_sim_nudity_time_statistic(sim)
        while get_nudity_setting(NuditySetting.NUDITY_SWITCH_STATE, variable_type=bool):
            test_sim_nudity_permission(sim)
            update_sim_nudity_skill_on_mirror_use(sim)
            update_sim_nudity_skill_on_active_nudity(sim)
            update_sim_nudity_skill_fatigue(sim)
