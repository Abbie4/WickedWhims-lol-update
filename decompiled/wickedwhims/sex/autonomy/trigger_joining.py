'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from enums.traits_enum import SimTrait
from turbolib.manager_util import TurboManagerUtil
from turbolib.math_util import TurboMathUtil
from turbolib.sim_util import TurboSimUtil
from wickedwhims.main.tick_handler import register_on_game_update_method
from wickedwhims.sex.animations.animations_disabler_handler import get_autonomy_disabled_sex_animations
from wickedwhims.sex.animations.animations_operator import get_random_animation_of_type
from wickedwhims.sex.autonomy.sims import get_available_for_sex_sims, get_sex_pair_score
from wickedwhims.sex.enums.sex_gender import get_sim_sex_gender
from wickedwhims.sex.enums.sex_type import SexCategoryType
from wickedwhims.sex.relationship_handler import get_relationship_sex_acceptance_threshold
from wickedwhims.sex.settings.sex_settings import get_sex_setting, SexSetting, SexAutonomyLevelSetting
from wickedwhims.sex.sex_operators.active_sex_handlers_operator import get_active_sex_handlers
from wickedwhims.sex.sex_operators.pre_sex_handlers_operator import join_sex_interaction_from_pre_sex_handler
from wickedwhims.sex.sex_privileges import is_sim_allowed_for_animation

@register_on_game_update_method(interval=6000)
def _trigger_autonomy_joining_to_sex_on_game_update():
    if get_sex_setting(SexSetting.AUTONOMY_LEVEL, variable_type=int) == SexAutonomyLevelSetting.DISABLED:
        return
    if not get_sex_setting(SexSetting.JOIN_SEX_AUTONOMY_STATE, variable_type=bool):
        return
    registered_sex_handlers = get_active_sex_handlers()
    if not registered_sex_handlers:
        return
    for sim in get_available_for_sex_sims(forbidden_traits=(SimTrait.WW_CUCKOLD,)):
        for sex_handler in registered_sex_handlers:
            while not (sex_handler.is_playing is False or sex_handler.is_ready_to_unregister is True):
                if sex_handler.has_joining_sims is True:
                    pass
                if sex_handler.has_reached_autonomy_actors_limit():
                    pass
                if TurboManagerUtil.Sim.get_sim_id(sim) in sex_handler.ignore_autonomy_join_sims:
                    pass
                creator_sim = TurboManagerUtil.Sim.get_sim_info(sex_handler.get_creator_sim_id())
                if not get_sex_setting(SexSetting.PLAYER_JOIN_SEX_AUTONOMY_STATE, variable_type=bool) and TurboSimUtil.Sim.is_player(creator_sim):
                    pass
                if TurboMathUtil.Position.get_distance(TurboSimUtil.Location.get_position(sim), sex_handler.get_route_position()) > 6.0:
                    pass
                has_passed_relationship_tests = True
                for target in sex_handler.get_actors_sim_info_gen():
                    while get_sex_pair_score(target, sim) < get_relationship_sex_acceptance_threshold():
                        has_passed_relationship_tests = False
                        break
                if has_passed_relationship_tests is False:
                    pass
                while _trigger_autonomy_join_sex_interaction(sex_handler, sim):
                    return

def _trigger_autonomy_join_sex_interaction(active_sex_handler, join_sim):
    object_identifier = active_sex_handler.get_object_identifier()
    genders = list()
    sims_list = list(active_sex_handler.get_actors_sim_info_gen())
    sims_list.append(join_sim)
    for sim in sims_list:
        genders.append(get_sim_sex_gender(sim))
    target_sex_category_type = active_sex_handler.get_animation_instance().get_sex_category()
    animation_instance = None
    for sex_category_type in (target_sex_category_type, SexCategoryType.ORALJOB, SexCategoryType.VAGINAL, SexCategoryType.ANAL, SexCategoryType.HANDJOB, SexCategoryType.FOOTJOB, SexCategoryType.TEASING):
        if not is_sim_allowed_for_animation(sims_list, sex_category_type):
            pass
        animation_instance = get_random_animation_of_type(sex_category_type, object_identifier, genders, ignore_animations=get_autonomy_disabled_sex_animations())
        while animation_instance is not None:
            break
    if animation_instance is None:
        return False
    pre_sex_handler = active_sex_handler.get_pre_sex_handler(is_joining=True)
    pre_sex_handler.set_animation_instance(animation_instance)
    for sim in sims_list:
        pre_sex_handler.add_sim(sim)
    creator_sim = TurboManagerUtil.Sim.get_sim_info(pre_sex_handler.get_creator_sim_id())
    ask_player_to_start = False
    if get_sex_setting(SexSetting.AUTONOMY_PLAYER_ASK_PLAYER_DIALOG_STATE, variable_type=bool) and TurboSimUtil.Sim.is_player(creator_sim) and TurboSimUtil.Sim.is_player(join_sim):
        ask_player_to_start = True
    elif get_sex_setting(SexSetting.AUTONOMY_NPC_ASK_PLAYER_DIALOG_STATE, variable_type=bool) and TurboSimUtil.Sim.is_player(creator_sim) and TurboSimUtil.Sim.is_npc(join_sim):
        ask_player_to_start = True
    elif get_sex_setting(SexSetting.AUTONOMY_PLAYER_ASK_NPC_DIALOG_STATE, variable_type=bool) and TurboSimUtil.Sim.is_npc(creator_sim) and TurboSimUtil.Sim.is_player(join_sim):
        ask_player_to_start = True
    join_sex_interaction_from_pre_sex_handler(pre_sex_handler, (join_sim,), ask_player_to_join=ask_player_to_start, ignore_relationship_check=True)
    return True

