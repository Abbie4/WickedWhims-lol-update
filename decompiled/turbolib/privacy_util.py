'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from _weakrefset import WeakSet
import services
from turbolib.manager_util import TurboManagerUtil

class TurboPrivacyUtil:
    __qualname__ = 'TurboPrivacyUtil'

    @staticmethod
    def get_privacy_interaction(privacy_instance):
        return privacy_instance.interaction

    @staticmethod
    def is_sim_allowed_by_privacy(sim_identifier, privacy_instance):
        sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
        return privacy_instance._is_sim_allowed(sim)

    @staticmethod
    def get_all_privacy_instances_gen():
        for privacy in services.privacy_service().privacy_instances:
            yield privacy

    @staticmethod
    def reevaluate_privacy_violator(privacy_owner, violator_sim):
        for privacy in services.privacy_service().privacy_instances:
            while privacy.interaction is not None and privacy.interaction.sim is not None and privacy.interaction.sim is privacy_owner:
                if violator_sim in privacy.allowed_sims:
                    privacy.allowed_sims.discard(violator_sim)
                if violator_sim in privacy.disallowed_sims:
                    privacy.disallowed_sims.discard(violator_sim)
                privacy.evaluate_sim(violator_sim)
                return

    @staticmethod
    def reevaluate_all_privacy_instances():
        for privacy in services.privacy_service().privacy_instances:
            privacy._allowed_sims = WeakSet()
            privacy._disallowed_sims = WeakSet()
            privacy._violators = WeakSet()
            privacy._late_violators = WeakSet()
            for sim in TurboManagerUtil.Sim.get_all_sim_instance_gen(humans=True, pets=False):
                privacy.handle_late_violator(sim)

