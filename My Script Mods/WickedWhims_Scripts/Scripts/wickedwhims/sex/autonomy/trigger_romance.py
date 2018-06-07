'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''import randomfrom enums.interactions_enum import SimInteractionfrom enums.moods_enum import SimMoodfrom enums.tags_enum import GameTagfrom turbolib.events.interactions import register_interaction_outcome_event_methodfrom turbolib.interaction_util import TurboInteractionUtilfrom turbolib.manager_util import TurboManagerUtilfrom turbolib.resource_util import TurboResourceUtilfrom turbolib.sim_util import TurboSimUtilfrom turbolib.world_util import TurboWorldUtilfrom wickedwhims.main.sim_ev_handler import sim_evfrom wickedwhims.relationships.desire_handler import get_sim_desire_levelfrom wickedwhims.sex.autonomy.disabled_locations_handler import is_autonomy_sex_locations_disabledfrom wickedwhims.sex.autonomy.location import get_sex_location_style_and_chance, LocationStyleTypefrom wickedwhims.sex.autonomy.sims import get_time_between_sex_autonomy_attempts, get_sex_pair_scorefrom wickedwhims.sex.autonomy.triggers_handler import get_sex_autonomy_location, trigger_sex_autonomy_interactionfrom wickedwhims.sex.relationship_handler import get_relationship_sex_acceptance_thresholdfrom wickedwhims.sex.settings.sex_settings import get_sex_setting, SexSetting, SexAutonomyLevelSettingfrom wickedwhims.utils_autonomy import is_sim_allowed_for_autonomy
@register_interaction_outcome_event_method(unique_id='WickedWhims')
def _wickedwhims_on_sex_autonomy_romance_interactions_outcome(interaction_instance, outcome_result):
    if outcome_result is False:
        return
    if get_sex_setting(SexSetting.AUTONOMY_LEVEL, variable_type=int) == SexAutonomyLevelSetting.DISABLED:
        return
    if not get_sex_setting(SexSetting.AUTONOMY_ROMANCE_SEX_STATE, variable_type=bool):
        return
    interaction_guid = TurboResourceUtil.Resource.get_guid64(interaction_instance)
    if interaction_guid == SimInteraction.WW_SOCIAL_MIXER_ASK_FOR_SEX_DEFAULT or interaction_guid == SimInteraction.WW_SOCIAL_MIXER_AUTONOMY_ASK_FOR_SEX_DEFAULT:
        return
    sim_info = TurboManagerUtil.Sim.get_sim_info(TurboInteractionUtil.get_interaction_sim(interaction_instance))
    if not sim_ev(sim_info).is_ready():
        return
    if sim_ev(sim_info).active_sex_handler is not None or sim_ev(sim_info).active_pre_sex_handler is not None:
        return
    if is_autonomy_sex_locations_disabled(TurboResourceUtil.Resource.get_id(sim_info)):
        return
    target_sim_info = TurboManagerUtil.Sim.get_sim_info(TurboInteractionUtil.get_interaction_target(interaction_instance))
    if target_sim_info is None:
        return
    if sim_ev(target_sim_info).active_sex_handler is not None or sim_ev(target_sim_info).active_pre_sex_handler is not None:
        return
    if is_autonomy_sex_locations_disabled(TurboResourceUtil.Resource.get_id(target_sim_info)):
        return
    if not get_sex_setting(SexSetting.PLAYER_AUTONOMY_STATE, variable_type=bool) and TurboSimUtil.Sim.is_player(sim_info) and TurboSimUtil.Sim.is_player(target_sim_info):
        return
    if not get_sex_setting(SexSetting.TEENS_SEX_STATE, variable_type=bool) and (TurboSimUtil.Age.get_age(sim_info) == TurboSimUtil.Age.TEEN or TurboSimUtil.Age.get_age(target_sim_info) == TurboSimUtil.Age.TEEN):
        return
    if int(GameTag.SOCIAL_FLIRTY) not in TurboInteractionUtil.get_affordance_tags(interaction_instance):
        return
    if not is_sim_allowed_for_autonomy(TurboManagerUtil.Sim.get_sim_instance(sim_info)):
        return
    if TurboWorldUtil.Time.get_absolute_ticks() < sim_ev(sim_info).last_sex_autonomy + get_time_between_sex_autonomy_attempts():
        return
    if get_sex_pair_score(sim_info, target_sim_info) < get_relationship_sex_acceptance_threshold():
        return
    is_flirty_conversation = TurboSimUtil.Mood.get_mood(sim_info) == SimMood.FLIRTY and TurboSimUtil.Mood.get_mood(target_sim_info) == SimMood.FLIRTY
    has_target_high_desire = get_sim_desire_level(target_sim_info) >= 80
    if get_sex_setting(SexSetting.AUTONOMY_LEVEL, variable_type=int) == SexAutonomyLevelSetting.HIGH:
        random_chance = 0.25 + (0.25 if is_flirty_conversation else 0.0) + (0.25 if has_target_high_desire else 0.0)
    elif get_sex_setting(SexSetting.AUTONOMY_LEVEL, variable_type=int) == SexAutonomyLevelSetting.LOW:
        random_chance = 0.05 + (0.1 if is_flirty_conversation else 0.0) + (0.1 if has_target_high_desire else 0.0)
    else:
        random_chance = 0.1 + (0.2 if is_flirty_conversation else 0.0) + (0.2 if has_target_high_desire else 0.0)
    if random.uniform(0, 1) <= random_chance:
        sims_pair = (sim_info, target_sim_info)
        location_style_and_delay = get_sex_location_style_and_chance(sims_pair)
        if location_style_and_delay[0] != LocationStyleType.NONE and random.uniform(0, 1) <= location_style_and_delay[1]:
            sex_location = get_sex_autonomy_location(sims_pair, location_style=location_style_and_delay[0])
            if sex_location is not None:
                trigger_sex_autonomy_interaction(sims_pair, sex_location)
