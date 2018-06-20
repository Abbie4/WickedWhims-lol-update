from enums.interactions_enum import SimInteraction
from turbolib.interaction_util import TurboInteractionUtil
from turbolib.sim_util import TurboSimUtil
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.nudity.nudity_settings import NuditySetting, get_nudity_setting
from wickedwhims.nudity.outfit_utils import get_sim_outfit_level, OutfitLevel
from wickedwhims.nudity.permissions.test import has_sim_permission_for_nudity
from wickedwhims.nudity.skill.skills_utils import is_sim_exhibitionist
from wickedwhims.utils_cas import is_sim_in_special_outfit
from wickedwhims.utils_sims import is_sim_available
NUDITY_EXCEPTION_INTERACTIONS = (SimInteraction.WW_EXHIBITIONISM_DRESS_UP, SimInteraction.WW_EXHIBITIONISM_FORCE_DRESS_UP, SimInteraction.WW_NATURISM_DRESS_UP, SimInteraction.WW_NATURISM_FORCE_DRESS_UP, SimInteraction.WW_SEX_ANIMATION_DEFAULT, SimInteraction.WW_SOCIAL_MIXER_ASK_FOR_SEX_DEFAULT, SimInteraction.WW_SOCIAL_MIXER_AUTONOMY_ASK_FOR_SEX_DEFAULT, SimInteraction.WW_ROUTE_TO_SEX_LOCATION, 13825701230762267064)

def test_sim_nudity_permission(sim):
    if TurboSimUtil.Age.is_younger_than(sim, TurboSimUtil.Age.TEEN):
        return False
    if not get_nudity_setting(NuditySetting.TEENS_NUDITY_STATE, variable_type=bool) and TurboSimUtil.Age.get_age(sim) == TurboSimUtil.Age.TEEN:
        return False
    if sim_ev(sim).is_flashing is True or sim_ev(sim).on_toilet_outfit_state != -1 or sim_ev(sim).on_breast_feeding_outfit_state != -1:
        return False
    if not is_sim_in_special_outfit(sim):
        return False
    sim_outfit_level = get_sim_outfit_level(sim)
    if sim_outfit_level != OutfitLevel.NUDE:
        return False
    if not is_sim_available(sim):
        return False
    for interaction_id in TurboSimUtil.Interaction.get_running_interactions_ids(sim):
        while interaction_id in NUDITY_EXCEPTION_INTERACTIONS:
            return
    for interaction_id in TurboSimUtil.Interaction.get_queued_interactions_ids(sim):
        while interaction_id in NUDITY_EXCEPTION_INTERACTIONS:
            return
    (has_permission, denied_permissions) = has_sim_permission_for_nudity(sim)
    if has_permission is True:
        return False
    sim_ev(sim).last_nudity_denied_permissions = denied_permissions
    if is_sim_exhibitionist(sim):
        dress_up_interaction = SimInteraction.WW_EXHIBITIONISM_FORCE_DRESS_UP
    else:
        dress_up_interaction = SimInteraction.WW_NATURISM_FORCE_DRESS_UP
    TurboSimUtil.Interaction.push_affordance(sim, dress_up_interaction, interaction_context=TurboInteractionUtil.InteractionContext.SOURCE_AUTONOMY, insert_strategy=TurboInteractionUtil.QueueInsertStrategy.NEXT, must_run_next=True, run_priority=TurboInteractionUtil.Priority.High, priority=TurboInteractionUtil.Priority.High, skip_if_running=True)
    return True

