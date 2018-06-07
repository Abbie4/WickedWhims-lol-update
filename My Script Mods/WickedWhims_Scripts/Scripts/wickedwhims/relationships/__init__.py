'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''from turbolib.events.core import register_zone_load_event_method, has_game_loadedfrom turbolib.resources.affordances import register_affordance_class, AffordanceRegistrationfrom turbolib.tunable_util import TurboTunableUtilfrom wickedwhims.utils_rewards import register_satisfaction_reward
@register_zone_load_event_method(unique_id='WickedWhims', priority=5, late=True)
def _wickedwhims_add_relationship_satisfaction_rewards():
    if has_game_loaded():
        return
    register_satisfaction_reward(17018140015135385770, 1000, TurboTunableUtil.Whims.WhimAwardTypes.TRAIT)

@register_affordance_class()
class NuditySimsSocialMixerAffordanceRegistration(AffordanceRegistration):
    __qualname__ = 'NuditySimsSocialMixerAffordanceRegistration'

    def get_social_mixer_references(self):
        return (24510, 163713)

    def get_affordance_references(self):
        return (12721186483668816815,)

    def is_social_mixer(self):
        return True
