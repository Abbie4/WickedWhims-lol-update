'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''from enums.interactions_enum import SimInteractionfrom turbolib.cas_util import TurboCASUtilfrom turbolib.events.interactions import register_interaction_run_event_methodfrom turbolib.interaction_util import TurboInteractionUtilfrom turbolib.resource_util import TurboResourceUtilfrom turbolib.sim_util import TurboSimUtilfrom turbolib.world_util import TurboWorldUtilfrom wickedwhims.nudity.skill.skills_utils import get_sim_nudity_skill_levelfrom wickedwhims.sxex_bridge.body import set_sim_top_naked_state, set_sim_bottom_naked_statefrom wickedwhims.sxex_bridge.outfit import strip_outfit, StripTypefrom wickedwhims.sxex_bridge.underwear import set_sim_top_underwear_state, set_sim_bottom_underwear_stateADMIRE_YOUR_BODY_AFFORDANCES = (SimInteraction.WW_MIRROR_ADMIRE_NUDITY_1, SimInteraction.WW_MIRROR_ADMIRE_NUDITY_2, SimInteraction.WW_MIRROR_ADMIRE_NUDITY_3, SimInteraction.WW_MIRROR_ADMIRE_NUDITY_4, SimInteraction.WW_MIRROR_ADMIRE_NUDITY_5)
@register_interaction_run_event_method(unique_id='WickedWhims')
def _wickedwhims_strip_clothing_while_admiring_your_body(interaction_instance):
    interaction_guid = TurboResourceUtil.Resource.get_guid64(interaction_instance)
    if interaction_guid in ADMIRE_YOUR_BODY_AFFORDANCES:
        sim = TurboInteractionUtil.get_interaction_sim(interaction_instance)
        skill_level = get_sim_nudity_skill_level(sim)
        strip_nude = skill_level >= 3 or skill_level == 2 and TurboWorldUtil.Lot.is_sim_on_home_lot(sim)
        if strip_nude is True:
            strip_result = strip_outfit(sim, strip_type_top=StripType.NUDE, strip_type_bottom=StripType.NUDE, save_original=False)
            set_sim_top_naked_state(sim, True)
            set_sim_bottom_naked_state(sim, True)
            set_sim_top_underwear_state(sim, False)
            set_sim_bottom_underwear_state(sim, False)
        else:
            if not TurboSimUtil.CAS.has_outfit(sim, (TurboCASUtil.OutfitCategory.SWIMWEAR, 0)):
                TurboSimUtil.CAS.generate_outfit(sim, (TurboCASUtil.OutfitCategory.SWIMWEAR, 0))
            TurboSimUtil.CAS.set_current_outfit(sim, (TurboCASUtil.OutfitCategory.SWIMWEAR, 0))
