from turbolib.events.interactions import register_interaction_run_event_method
from turbolib.interaction_util import TurboInteractionUtil
from turbolib.resource_util import TurboResourceUtil
from wickedwhims.nudity.nudity_settings import NuditySetting, get_nudity_setting
from wickedwhims.nudity.outfit_utils import get_sim_outfit_level, OutfitLevel
from wickedwhims.nudity.skill.skills_utils import increase_sim_nudity_skill, get_sim_nudity_skill_level
from turbolib.manager_util import TurboManagerUtil
NUDE_REWARD_INTERACTION_IDS = ((128625, False, 0.75), (99173, False, 3.0), (117339, False, 0.75), (120455, False, 0.75), (117755, False, 2.0), (119592, False, 2.0), (119373, False, 2.0), (33618, False, 0.65), (10213, False, 0.65), (13444, False, 0.65), (117359, False, 1.1), (119103, False, 1.45), (40145, False, 2.5), (110928, False, 1.35), (114854, True, 1.35), (114855, True, 1.35), (114858, True, 1.35), (114859, True, 1.35))

@register_interaction_run_event_method(unique_id='WickedWhims')
def _wickedwhims_increase_sim_nudity_skill_on_related_interactions(interaction_instance):
    if not get_nudity_setting(NuditySetting.NUDITY_SWITCH_STATE, variable_type=bool):
        return
    interaction_guid = TurboResourceUtil.Resource.get_guid64(interaction_instance)
    sim = TurboInteractionUtil.get_interaction_sim(interaction_instance)
    for (interaction_id, direct_target, skill_points) in NUDE_REWARD_INTERACTION_IDS:
        if interaction_id != interaction_guid:
            continue
        if direct_target is True:
            target_sim = TurboInteractionUtil.get_interaction_target(interaction_instance) or sim
            if target_sim is None:
                target_sim = sim
        else:
            target_sim = sim
        if target_sim is None:
            return
        sim_info = TurboManagerUtil.Sim.get_sim_info(target_sim)
        if sim_info is None:
            return
        target_outfit_level = get_sim_outfit_level(target_sim)
        target_nudity_skill_level = get_sim_nudity_skill_level(target_sim)
        if target_outfit_level == OutfitLevel.NUDE or target_outfit_level == OutfitLevel.BATHING:
            increase_sim_nudity_skill(target_sim, skill_points, extra_fatigue=2.0)
        else:
            if target_outfit_level == OutfitLevel.REVEALING or target_outfit_level == OutfitLevel.UNDERWEAR:
                increase_sim_nudity_skill(target_sim, skill_points/target_nudity_skill_level, extra_fatigue=2.0)

