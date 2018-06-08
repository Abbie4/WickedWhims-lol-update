from enums.interactions_enum import SimInteraction
from turbolib.events.privacy import PrivacyResult, register_privacy_sim_test_event_method
from turbolib.interaction_util import TurboInteractionUtil
from turbolib.math_util import TurboMathUtil
from turbolib.privacy_util import TurboPrivacyUtil
from turbolib.resource_util import TurboResourceUtil
from turbolib.sim_util import TurboSimUtil
from wickedwhims.nudity.nudity_settings import NuditySetting, get_nudity_setting
from wickedwhims.nudity.permissions.test import has_sim_permission_for_nudity
PRIVACY_NUDE_INTERACTIONS = (13073, 13076, 13084, 120340, 120341, 120342, 121575, 120339, 120337, 13087, 154400, 145422, 120336, 121573, 117263, 13950, 154397, 39965, 24332, 23839, 141926, 39860, 39845, 134251, 134250, 134165, 134534, 136684, 134609, 136718, 14427, 14428, 14434, SimInteraction.WW_MIRROR_ADMIRE_YOUR_BODY, 17681256309946806522)

@register_privacy_sim_test_event_method(unique_id='WickedWhims', priority=1)
def _wickedwhims_special_additional_los_test(privacy_instance, tested_sim):
    privacy_interaction = TurboPrivacyUtil.get_privacy_interaction(privacy_instance)
    if TurboResourceUtil.Resource.get_guid64(privacy_interaction) == SimInteraction.WW_MIRROR_ADMIRE_YOUR_BODY:
        sim = TurboInteractionUtil.get_interaction_sim(privacy_interaction)
        line_of_sight = TurboMathUtil.LineOfSight.create(TurboSimUtil.Location.get_routing_surface(sim), TurboSimUtil.Location.get_position(sim), 10.0)
        if not TurboPrivacyUtil.is_sim_allowed_by_privacy(tested_sim, privacy_instance) and TurboMathUtil.LineOfSight.test(line_of_sight, TurboSimUtil.Location.get_position(tested_sim)):
            return PrivacyResult.BLOCK
        return PrivacyResult.ALLOW
    return PrivacyResult.DEFAULT


@register_privacy_sim_test_event_method(unique_id='WickedWhims', priority=2)
def _wickedwhims_is_sim_allowed_for_nudity(privacy_instance, tested_sim):
    if get_nudity_setting(NuditySetting.NUDITY_PRIVACY, variable_type=bool) or TurboResourceUtil.Resource.get_guid64(TurboPrivacyUtil.get_privacy_interaction(privacy_instance)) in PRIVACY_NUDE_INTERACTIONS:
        return PrivacyResult.ALLOW
    if get_nudity_setting(NuditySetting.NUDITY_SWITCH_STATE, variable_type=bool):
        privacy_interaction = TurboPrivacyUtil.get_privacy_interaction(privacy_instance)
        if TurboResourceUtil.Resource.get_guid64(privacy_interaction) in PRIVACY_NUDE_INTERACTIONS:
            (sim_has_permission, _) = has_sim_permission_for_nudity(TurboInteractionUtil.get_interaction_sim(privacy_interaction), ignore_location_test=True, targets=(tested_sim,))
            if sim_has_permission is True:
                (target_has_permission, _) = has_sim_permission_for_nudity(tested_sim, ignore_location_test=True, targets=(TurboInteractionUtil.get_interaction_sim(privacy_interaction),))
                if target_has_permission is True:
                    return PrivacyResult.ALLOW
    return PrivacyResult.DEFAULT

