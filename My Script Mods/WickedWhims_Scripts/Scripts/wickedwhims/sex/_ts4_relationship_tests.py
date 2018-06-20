'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from event_testing.test_based_score import TestBasedScore
from interactions import ParticipantType
from sims4.sim_irq_service import yield_to_irq
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.sex.relationship_handler import get_test_relationship_score

class RelationshipSexTestBasedScore(TestBasedScore):
    __qualname__ = 'RelationshipSexTestBasedScore'

    @classmethod
    def _verify_tuning_callback(cls):
        pass

    @classmethod
    def get_score(cls, resolver):
        yield_to_irq()
        sim = resolver.get_participant(ParticipantType.Actor)
        target = resolver.get_participant(ParticipantType.TargetSim) or resolver.get_participant(ParticipantType.Listeners)
        if sim is None or target is None:
            return 0
        pre_sex_handler = sim_ev(sim).active_pre_sex_handler
        if pre_sex_handler is not None and pre_sex_handler.is_failure_sex():
            return 0
        if pre_sex_handler is not None and pre_sex_handler.is_success_sex():
            return 1000
        return get_test_relationship_score((sim, target))

