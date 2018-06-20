'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from enums.interactions_enum import SimInteraction
from turbolib.events.interactions import register_interaction_run_event_method
from turbolib.interaction_util import TurboInteractionUtil
from turbolib.resource_util import TurboResourceUtil
from turbolib.sim_util import TurboSimUtil
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.nudity.outfit_utils import get_sim_outfit_level, OutfitLevel
from wickedwhims.nudity.skill.skills_utils import NuditySkillIncreaseReason, get_nudity_skill_points_modifier, increase_sim_nudity_skill, get_sim_nudity_skill_level

def update_sim_nudity_skill_on_mirror_use(sim_identifier):
    if sim_ev(sim_identifier).is_running_mirror_nudity_skill_interaction is False:
        return
    if not TurboSimUtil.Interaction.is_running_interaction(sim_identifier, SimInteraction.WW_MIRROR_ADMIRE_YOUR_BODY):
        sim_ev(sim_identifier).is_running_mirror_nudity_skill_interaction = False
        return
    sim_outfit_level = get_sim_outfit_level(sim_identifier)
    sim_nudity_skill_level = get_sim_nudity_skill_level(sim_identifier)
    if sim_outfit_level == OutfitLevel.NUDE or sim_outfit_level == OutfitLevel.BATHING:
        increase_sim_nudity_skill(sim_identifier, get_nudity_skill_points_modifier(NuditySkillIncreaseReason.MIRROR_NAKED_OUTFIT)/sim_nudity_skill_level, extra_fatigue=0.2, reason=NuditySkillIncreaseReason.MIRROR_NAKED_OUTFIT)
    else:
        increase_sim_nudity_skill(sim_identifier, get_nudity_skill_points_modifier(NuditySkillIncreaseReason.MIRROR_REVEALING_OUTFIT)/sim_nudity_skill_level, extra_fatigue=0.05, reason=NuditySkillIncreaseReason.MIRROR_REVEALING_OUTFIT)


@register_interaction_run_event_method(unique_id='WickedWhims')
def _wickedwhims_flag_on_nudity_skill_mirror_use(interaction_instance):
    interaction_guid = TurboResourceUtil.Resource.get_guid64(interaction_instance)
    if interaction_guid == SimInteraction.WW_MIRROR_ADMIRE_YOUR_BODY:
        sim = TurboInteractionUtil.get_interaction_sim(interaction_instance)
        sim_ev(sim).is_running_mirror_nudity_skill_interaction = True

