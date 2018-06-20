'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from enums.interactions_enum import SimInteraction
from enums.motives_enum import SimMotive
from enums.statistics_enum import SimCommodity
from enums.traits_enum import SimTrait
from turbolib.interaction_util import TurboInteractionUtil
from turbolib.manager_util import TurboManagerUtil
from turbolib.sim_util import TurboSimUtil
from turbolib.world_util import TurboWorldUtil
from wickedwhims.main.basemental_handler import is_sim_on_basemental_drugs
from wickedwhims.sex.animations.animations_disabler_handler import get_autonomy_disabled_sex_animations
from wickedwhims.sex.animations.animations_operator import get_next_random_animation, get_next_stage_animation
from wickedwhims.sex.enums.sex_gender import get_sim_sex_gender
from wickedwhims.sex.enums.sex_type import SexCategoryType
from wickedwhims.sex.pregnancy.special_pregnancy_handler import try_pregnancy_from_sex_handler
from wickedwhims.sex.settings.sex_settings import SexSetting, get_sex_setting, SexInteractionDurationTypeSetting, SexProgressionLevelSetting, SexAnimationDurationOverrideType
from wickedwhims.sex.sex_handlers.active.utils.outfit import undress_sim
from wickedwhims.sex.sex_handlers.active.utils.strapon import update_stapon
from wickedwhims.sex.sex_handlers.sex_handler_utils import modify_sim_sex_snapshot_motive
from wickedwhims.sex.sex_operators.active_sex_handlers_operator import get_active_sex_handlers
from wickedwhims.sex.sex_privileges import is_sim_allowed_for_animation
from wickedwhims.sxex_bridge.penis import set_sim_penis_state
from wickedwhims.sxex_bridge.statistics import increase_sim_ww_statistic
from wickedwhims.utils_statistics import set_sim_statistic_value, change_sim_statistic_value
from wickedwhims.utils_traits import has_sim_trait

def update_active_sex_handler(sex_handler, ticks):
    if sex_handler.is_canceled is True:
        for sim_info in sex_handler.get_actors_sim_info_gen():
            TurboSimUtil.Interaction.cancel_queued_interaction(sim_info, SimInteraction.WW_SEX_ANIMATION_DEFAULT, finishing_type=TurboInteractionUtil.FinishingType.SI_FINISHED)
            TurboSimUtil.Interaction.cancel_running_interaction(sim_info, SimInteraction.WW_SEX_ANIMATION_DEFAULT, finishing_type=TurboInteractionUtil.FinishingType.SI_FINISHED)
        return
    is_new_animation_update = sex_handler.animation_counter <= 0
    if sex_handler.is_timer_paused is True:
        sex_handler.overall_counter = 1
    if sex_handler.is_animation_paused is True:
        sex_handler.animation_counter = 1
    if sex_handler.one_second_counter >= 1000:
        pass
    if sex_handler.sim_minute_counter >= 1500:
        pass
    if _has_interaction_finished(sex_handler):
        return
    if sex_handler.sim_minute_counter >= 1500 and _is_linked_sex_handler_active(sex_handler):
        return
    sims_list = sex_handler.get_sims_list()
    if not sims_list:
        return
    if is_new_animation_update is True or sex_handler.next_animation_instance is None and sex_handler.climax_reach_value > 0 and sex_handler.climax_counter == sex_handler.climax_reach_value:
        _prepare_next_animation(sex_handler, sims_list)
    if is_new_animation_update is True:
        _update_actors_outfit(sex_handler, sims_list)
        _update_actors_heavy_other_flags(sims_list)
    _force_actors_positions(sex_handler, sims_list)
    if sex_handler.sim_minute_counter >= 1500:
        _update_actors_light_other_flags(sex_handler, sims_list)
        _update_actors_motives(sims_list)
        try_pregnancy_from_sex_handler(sex_handler, sims_list)
    if sex_handler.one_second_counter >= 1000:
        _try_allow_for_climax(sex_handler, sims_list)
    try_progress_sex_interaction(sex_handler)


def _is_linked_sex_handler_active(sex_handler):
    if sex_handler.linked_sex_handler_identifier is None:
        return False
    for _sex_handler in get_active_sex_handlers():
        while _sex_handler.get_identifier() == sex_handler.linked_sex_handler_identifier:
            return False
    sex_handler.stop(is_end=True, stop_reason="Linked Sex Handler Doesn't Exist Anymore!")
    return True


def _has_interaction_finished(sex_handler):
    if sex_handler.is_npc_only():
        if sex_handler.get_animation_instance().get_sex_category() == SexCategoryType.CLIMAX:
            if sex_handler.animation_counter >= int(sex_handler.get_animation_instance().get_duration_milliseconds()) - 4:
                sex_handler.stop(is_end=True, stop_reason='NPC Sims Reached Climax!')
                return True
                if sex_handler.overall_counter > get_sex_setting(SexSetting.NPC_SEX_DURATION_VALUE, variable_type=int)*60000:
                    sex_handler.stop(is_end=True, stop_reason='Climax Reached!')
                    return True
        elif sex_handler.overall_counter > get_sex_setting(SexSetting.NPC_SEX_DURATION_VALUE, variable_type=int)*60000:
            sex_handler.stop(is_end=True, stop_reason='Climax Reached!')
            return True
    elif get_sex_setting(SexSetting.SEX_DURATION_TYPE, variable_type=int) == SexInteractionDurationTypeSetting.CLIMAX:
        if sex_handler.get_animation_instance().get_sex_category() == SexCategoryType.CLIMAX:
            if sex_handler.animation_counter >= int(sex_handler.get_animation_instance().get_duration_milliseconds()) - 4:
                sex_handler.stop(is_end=True, stop_reason='Climax reached and finished!')
                return True
    elif sex_handler.overall_counter > get_sex_setting(SexSetting.SEX_DURATION_VALUE, variable_type=int)*60000:
        sex_handler.stop(is_end=True, stop_reason='Interaction Duration reached end!')
        return True
    return False


def _force_actors_positions(sex_handler, sims_list):
    if sex_handler.force_positioning_count > 2:
        return
    for (actor_id, sim_info) in sims_list:
        sim = TurboManagerUtil.Sim.get_sim_instance(sim_info)
        while sim is not None:
            actor_data = sex_handler.get_animation_instance().get_actor(actor_id)
            TurboWorldUtil.Location.move_object_to(sim, sex_handler.get_location(), y_offset=actor_data.y_offset, orientation_offset=actor_data.facing_offset)


def _update_actors_light_other_flags(sex_handler, sims_list):
    for (_, sim_info) in sims_list:
        set_sim_statistic_value(sim_info, 1, SimCommodity.WW_IS_SIM_IN_SEX)
        increase_sim_ww_statistic(sim_info, 'time_spent_on_sex_' + str(sex_handler.get_animation_instance().get_sex_category().name.lower()))
        set_sim_penis_state(sim_info, True, 9999, set_if_nude=True)


def _update_actors_heavy_other_flags(sims_list):
    for (_, sim_info) in sims_list:
        set_sim_penis_state(sim_info, True, 9999, set_if_nude=True, force=True)


def _update_actors_outfit(sex_handler, sims_list):
    for (actor_id, sim_info) in sims_list:
        actor_data = sex_handler.get_animation_instance().get_actor(actor_id)
        undress_sim(sim_info, actor_data, is_npc_only=sex_handler.is_npc_only())
        update_stapon(sim_info, actor_data=actor_data, is_npc_only=sex_handler.is_npc_only())


def _update_actors_motives(sims_list):
    for (_, sim_info) in sims_list:
        if has_sim_trait(sim_info, SimTrait.INSIDER):
            change_sim_statistic_value(sim_info, 10, SimCommodity.BUFF_INSIDERTRAIT_MISSHANGINGOUT)
        change_sim_statistic_value(sim_info, 0.25, SimCommodity.TRAIT_ROMANTIC_AFFECTION)
        if get_sex_setting(SexSetting.NEEDS_DECAY_STATE, variable_type=bool):
            change_sim_statistic_value(sim_info, -5, SimCommodity.MOTIVE_HYGIENEHANDS)
        is_sim_vampire = has_sim_trait(sim_info, SimTrait.OCCULTVAMPIRE)
        is_sim_plant = has_sim_trait(sim_info, SimTrait.PLANTSIM)
        is_sim_human = not is_sim_vampire and not is_sim_plant
        modify_sim_sex_snapshot_motive(sim_info, SimMotive.FUN, 'motive_fun', 4.8188, max_value=100)
        modify_sim_sex_snapshot_motive(sim_info, SimMotive.SOCIAL, 'motive_social', 3.0868, max_value=100)
        modify_sim_sex_snapshot_motive(sim_info, SimMotive.HYGIENE, 'motive_hygiene', -0.9306, min_value=-41)
        if is_sim_human:
            modify_sim_sex_snapshot_motive(sim_info, SimMotive.BLADDER, 'motive_bladder', 0, min_value=-10)
        if is_sim_human or is_sim_plant:
            modify_sim_sex_snapshot_motive(sim_info, SimMotive.HUNGER, 'motive_hunger', 0, min_value=-41)
            modify_sim_sex_snapshot_motive(sim_info, SimMotive.ENERGY, 'motive_energy', 0, min_value=-41)
        if is_sim_vampire:
            modify_sim_sex_snapshot_motive(sim_info, SimMotive.VAMPIRE_POWER, 'motive_vampire_power', 0, min_value=-41)
            modify_sim_sex_snapshot_motive(sim_info, SimMotive.VAMPIRE_THIRST, 'motive_vampire_thirst', 0, min_value=-41)
        while is_sim_plant:
            modify_sim_sex_snapshot_motive(sim_info, SimMotive.PLANTSIM_WATER, 'motive_plantsim_water', 0, min_value=-41)


def _try_allow_for_climax(sex_handler, sims_list):
    if sex_handler.is_at_climax is True:
        return
    if sex_handler.climax_reach_value == 0:
        base_climax_reach_value = 25
        for (_, sim_info) in sims_list:
            while is_sim_on_basemental_drugs(sim_info, skip_weed=True):
                base_climax_reach_value += 20
                break
        sex_handler.climax_reach_value = base_climax_reach_value
        if sex_handler.is_npc_only():
            sex_handler.climax_reach_value = max(base_climax_reach_value, get_sex_setting(SexSetting.NPC_SEX_DURATION_VALUE, variable_type=int)*60 - 60)
        sex_handler.climax_reach_value = int(sex_handler.climax_reach_value)
    if sex_handler.climax_counter >= sex_handler.climax_reach_value:
        sex_handler.is_at_climax = True
        for (_, sim_info) in sims_list:
            set_sim_statistic_value(sim_info, 1, SimCommodity.WW_READY_TO_CLIMAX)


def _prepare_next_animation(sex_handler, sims_list):
    if sex_handler.next_animation_instance is not None:
        return
    ignored_animations = get_autonomy_disabled_sex_animations() if sex_handler.is_autonomy_sex() or sex_handler.is_npc_only() else ()
    sex_handler.next_animation_instance = _get_next_sex_interaction_animation(sex_handler, sims_list, ignored_animations=ignored_animations)


def _get_next_sex_interaction_animation(sex_handler, sims_list, ignored_animations=()):
    genders = list()
    for (_, sim_info) in sims_list:
        genders.append(get_sim_sex_gender(sim_info))
    sex_progression_type = get_sex_setting(SexSetting.SEX_PROGRESSION_TYPE, variable_type=int) if not sex_handler.is_npc_only() else SexProgressionLevelSetting.FULL
    if sex_progression_type == SexProgressionLevelSetting.RANDOM:
        return get_next_random_animation(sex_handler.get_object_identifier(), genders, sex_handler.get_animation_instance().get_sex_category(), allow_climax=sex_handler.is_at_climax, ignore_animations=ignored_animations)
    if sex_progression_type == SexProgressionLevelSetting.STAGE_ONLY:
        next_stage_animation = get_next_stage_animation(sex_handler.get_animation_instance())
        if next_stage_animation is not None and next_stage_animation.get_sex_category() == SexCategoryType.CLIMAX and not sex_handler.is_at_climax:
            return
        return next_stage_animation
    if sex_progression_type == SexProgressionLevelSetting.FULL:
        next_animation = get_next_stage_animation(sex_handler.get_animation_instance())
        if not (next_animation is None or next_animation is not None and (next_animation.get_sex_category() == SexCategoryType.CLIMAX and not sex_handler.is_at_climax)):
            return next_animation
    return get_next_random_animation(sex_handler.get_object_identifier(), genders, sex_handler.get_animation_instance().get_sex_category(), allow_climax=sex_handler.is_at_climax, ignore_animations=ignored_animations)


def try_progress_sex_interaction(sex_handler, is_manual=False):
    if sex_handler.is_npc_only():
        if sex_handler.get_animation_instance().get_sex_category() == SexCategoryType.CLIMAX:
            return
        animation_duration = _get_sex_handler_animation_duration(sex_handler.get_animation_instance(), is_npc_only=True)
    else:
        if get_sex_setting(SexSetting.SEX_PROGRESSION_TYPE, variable_type=int) == SexProgressionLevelSetting.DISABLED and is_manual is False:
            return
        if sex_handler.get_animation_instance().get_sex_category() == SexCategoryType.CLIMAX and not get_sex_setting(SexSetting.CLIMAX_SEX_PROGRESSION_STATE, variable_type=bool):
            return
        animation_duration = _get_sex_handler_animation_duration(sex_handler.get_animation_instance())
    if is_manual is True or sex_handler.animation_counter >= animation_duration:
        sex_handler.animation_counter = 0
        if sex_handler.next_animation_instance is not None and sex_handler.next_animation_instance != sex_handler.get_animation_instance():
            if is_sim_allowed_for_animation(sex_handler.get_actors_sim_info_gen(), sex_handler.next_animation_instance.get_sex_category()):
                sex_handler.set_animation_instance(sex_handler.next_animation_instance, is_animation_change=True)
                sex_handler.next_animation_instance = None
                sex_handler.play(is_animation_change=True)


def _get_sex_handler_animation_duration(animation_instance, is_npc_only=False):
    if is_npc_only is True:
        animation_single_loop_duration = animation_instance.get_single_loop_duration()
        progression_duration = get_sex_setting(SexSetting.NPC_SEX_DURATION_VALUE, variable_type=int)*60/12
        if progression_duration >= int(animation_instance.get_duration()):
            animation_duration = int(animation_instance.get_duration_milliseconds()) - 4
        else:
            animation_duration = int(max(int(progression_duration/animation_single_loop_duration), 1)*animation_single_loop_duration*1000) - 4
    elif get_sex_setting(SexSetting.SEX_ANIMATION_DURATION_OVERRIDE_TYPE, variable_type=int) == SexAnimationDurationOverrideType.OVERRIDE:
        animation_single_loop_duration = animation_instance.get_single_loop_duration()
        animation_duration = int(max(1, int(get_sex_setting(SexSetting.SEX_ANIMATION_DURATION_OVERRIDE_VALUE, variable_type=int)/animation_single_loop_duration))*animation_single_loop_duration*1000)
    else:
        animation_duration = int(animation_instance.get_duration_milliseconds())
    return animation_duration

