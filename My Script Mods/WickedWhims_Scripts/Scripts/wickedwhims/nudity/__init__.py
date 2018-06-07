from enums.interactions_enum import SimInteraction
from enums.tags_enum import GameTag
from enums.whims_enum import WhimSet
from turbolib.events.core import register_zone_load_event_method, has_game_loaded
from turbolib.object_util import TurboObjectUtil
from turbolib.resources.affordances import AffordanceRegistration, register_affordance_class
from turbolib.resources.whims import WhimRegistration, register_whim_class
from turbolib.sim_util import TurboSimUtil
from turbolib.tunable_util import TurboTunableUtil
from turbolib.types_util import TurboTypesUtil
from wickedwhims.utils_rewards import register_satisfaction_reward

@register_zone_load_event_method(unique_id='WickedWhims', priority=5, late=True)
def _wickedwhims_add_nudity_satisfaction_rewards():
    if has_game_loaded():
        return
    register_satisfaction_reward(15267048880004589952, 250, TurboTunableUtil.Whims.WhimAwardTypes.TRAIT)
    register_satisfaction_reward(12422920560197330477, 500, TurboTunableUtil.Whims.WhimAwardTypes.TRAIT)


@register_affordance_class()
class NuditySimsAffordanceRegistration(AffordanceRegistration):
    __qualname__ = 'NuditySimsAffordanceRegistration'

    def get_affordance_references(self):
        return (SimInteraction.WW_PENIS_SETTINGS, 14369679725457799948, SimInteraction.WW_EXHIBITIONISM_UNDRESS_OUTFIT_TOP, SimInteraction.WW_EXHIBITIONISM_UNDRESS_OUTFIT_BOTTOM, SimInteraction.WW_EXHIBITIONISM_UNDRESS_OUTFIT_SHOES, SimInteraction.WW_EXHIBITIONISM_UNDRESS_OUTFIT, SimInteraction.WW_EXHIBITIONISM_UNDRESS_TO_NUDE, SimInteraction.WW_EXHIBITIONISM_DRESS_UP, SimInteraction.WW_EXHIBITIONISM_UNDRESS_UNDERWEAR_TOP, SimInteraction.WW_EXHIBITIONISM_UNDRESS_UNDERWEAR_BOTTOM, SimInteraction.WW_EXHIBITIONISM_UNDRESS_UNDERWEAR, SimInteraction.WW_EXHIBITIONISM_PUT_ON_UNDERWAER, SimInteraction.WW_SOCIAL_FLASH, SimInteraction.WW_START_STREAKING, SimInteraction.WW_NATURISM_UNDRESS_OUTFIT_TOP, SimInteraction.WW_NATURISM_UNDRESS_OUTFIT_BOTTOM, SimInteraction.WW_NATURISM_UNDRESS_OUTFIT_SHOES, SimInteraction.WW_NATURISM_UNDRESS_OUTFIT, SimInteraction.WW_NATURISM_UNDRESS_TO_NUDE, SimInteraction.WW_NATURISM_DRESS_UP, SimInteraction.WW_NATURISM_UNDRESS_UNDERWEAR_TOP, SimInteraction.WW_NATURISM_UNDRESS_UNDERWEAR_BOTTOM, SimInteraction.WW_NATURISM_UNDRESS_UNDERWEAR, SimInteraction.WW_NATURISM_PUT_ON_UNDERWAER)

    def is_script_object(self, script_object):
        return TurboTypesUtil.Sims.is_sim(script_object) and TurboSimUtil.Species.is_human(script_object)

    def is_relationship_panel(self):
        return False


@register_affordance_class()
class NuditySimsSocialMixerAffordanceRegistration(AffordanceRegistration):
    __qualname__ = 'NuditySimsSocialMixerAffordanceRegistration'

    def get_affordance_references(self):
        return (11151772469417588922, 12292735396648046883, 13451548886674510474, 10862624661993502652, 9861557282880692657, 11948461369467711666, 18209219286625006841, 11284927627327383595, 16915352448994554586, 10098465505578832733)

    def is_social_mixer(self):
        return True


@register_affordance_class()
class NuditySteamRoomObjectAffordanceRegistration(AffordanceRegistration):
    __qualname__ = 'NuditySteamRoomObjectAffordanceRegistration'

    def get_affordance_references(self):
        return (120455,)

    def is_script_object(self, script_object):
        if not TurboTypesUtil.Objects.is_game_object(script_object):
            return False
        object_tags = TurboObjectUtil.GameObject.get_game_tags(script_object)
        for object_tag in object_tags:
            while object_tag == GameTag.FUNC_STEAMROOM:
                return True
        return False


@register_affordance_class()
class NudityMirrorObjectAffordanceRegistration(AffordanceRegistration):
    __qualname__ = 'NudityMirrorObjectAffordanceRegistration'

    def get_affordance_references(self):
        return (SimInteraction.WW_MIRROR_ADMIRE_YOUR_BODY,)

    def is_script_object(self, script_object):
        if not TurboTypesUtil.Objects.is_game_object(script_object):
            return False
        object_tags = TurboObjectUtil.GameObject.get_game_tags(script_object)
        for object_tag in object_tags:
            while object_tag == GameTag.BUYCATLD_MIRROR:
                return True
        return False


@register_affordance_class()
class NudityDresserObjectAffordanceRegistration(AffordanceRegistration):
    __qualname__ = 'NudityDresserObjectAffordanceRegistration'

    def get_affordance_references(self):
        return (118457,)

    def test_for_duplicates(self):
        return True

    def is_script_object(self, script_object):
        if not TurboTypesUtil.Objects.is_game_object(script_object):
            return False
        object_tags = TurboObjectUtil.GameObject.get_game_tags(script_object)
        for object_tag in object_tags:
            while object_tag == GameTag.BUYCATSS_DRESSER:
                return True
        return False


@register_whim_class()
class NudityWhimsRegistration(WhimRegistration):
    __qualname__ = 'NudityWhimsRegistration'

    def get_whim_references(self):
        return ((15707416803050830021, 0.65), (16513863394650933038, 0.65), (12247263970138015276, 0.65), (16671232001435073015, 0.65))

    def get_whim_set_references(self):
        return (WhimSet.EMOTIONFLIRTY, WhimSet.EMOTIONCONFIDENT, WhimSet.EMOTIONPLAYFUL)


@register_whim_class()
class NudityBasementalWhimsRegistration(WhimRegistration):
    __qualname__ = 'NudityBasementalWhimsRegistration'

    def get_whim_references(self):
        return ((15707416803050830021, 0.65), (12247263970138015276, 0.65), (16671232001435073015, 0.65))

    def get_whim_set_references(self):
        return (WhimSet.BASEMENTAL_MDMA,)

