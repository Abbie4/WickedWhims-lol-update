'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from event_testing.test_based_score import TestBasedScore
from interactions import ParticipantType
from sims4.sim_irq_service import yield_to_irq
from wickedwhims.nudity.permissions.test import has_sim_permission_for_nudity

class NudityPermissionActorTestBasedScore(TestBasedScore):
    __qualname__ = 'NudityPermissionActorTestBasedScore'

    @classmethod
    def _verify_tuning_callback(cls):
        pass

    @classmethod
    def get_score(cls, resolver):
        yield_to_irq()
        sim = resolver.get_participant(ParticipantType.Actor)
        if has_sim_permission_for_nudity(sim)[0]:
            return 100
        return 0


class NudityPermissionTargetTestBasedScore(TestBasedScore):
    __qualname__ = 'NudityPermissionTargetTestBasedScore'

    @classmethod
    def _verify_tuning_callback(cls):
        pass

    @classmethod
    def get_score(cls, resolver):
        yield_to_irq()
        target = resolver.get_participant(ParticipantType.TargetSim) or resolver.get_participant(ParticipantType.Listeners)
        if has_sim_permission_for_nudity(target)[0]:
            return 100
        return 0

