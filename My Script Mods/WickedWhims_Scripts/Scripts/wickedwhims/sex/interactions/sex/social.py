'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from enums.interactions_enum import SimInteraction
from turbolib.interaction_util import TurboInteractionUtil
from turbolib.sim_util import TurboSimUtil
from turbolib.wrappers.interactions import TurboImmediateSuperInteraction, TurboInteractionStartMixin, TurboSocialMixerInteraction, TurboInteractionCancelMixin, TurboInteractionInitMixin
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.sex.relationship_handler import apply_asking_for_woohoo_relations
from wickedwhims.sex.sex_operators.general_sex_handlers_operator import clear_sim_sex_extra_data
from wickedwhims.sex.sex_operators.pre_sex_handlers_operator import prepare_npc_sim_to_sex

class AskForSexSocialMixerInteraction(TurboSocialMixerInteraction, TurboInteractionInitMixin, TurboInteractionStartMixin, TurboInteractionCancelMixin):
    __qualname__ = 'AskForSexSocialMixerInteraction'

    @classmethod
    def on_interaction_init(cls, interaction_instance):
        interaction_instance.has_attempted_asking_for_sex = False

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return True

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        interaction_instance.has_attempted_asking_for_sex = True

    @classmethod
    def on_interaction_cancel(cls, interaction_instance, interaction_finishing_type):
        if interaction_finishing_type == TurboInteractionUtil.FinishingType.USER_CANCEL or interaction_instance.has_attempted_asking_for_sex is False:
            pre_sex_handler = sim_ev(cls.get_interaction_sim(interaction_instance)).active_pre_sex_handler
            if pre_sex_handler is not None:
                while True:
                    for sim_info in pre_sex_handler.get_actors_sim_info_gen():
                        clear_sim_sex_extra_data(sim_info)


class AskForSexSocialSuccessInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'AskForSexSocialSuccessInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return True

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        sim = cls.get_interaction_sim(interaction_instance)
        target = cls.get_interaction_target(interaction_instance)
        pre_sex_handler = sim_ev(sim).active_pre_sex_handler
        if pre_sex_handler is None or target is None:
            clear_sim_sex_extra_data(sim)
            if target is not None:
                clear_sim_sex_extra_data(target)
            return False
        apply_asking_for_woohoo_relations(sim, target, True)
        for actor_sim in pre_sex_handler.get_actors_sim_instance_gen():
            sim_ev(actor_sim).is_in_process_to_sex = True
            sim_ev(actor_sim).active_pre_sex_handler = pre_sex_handler
            prepare_npc_sim_to_sex(actor_sim)
            TurboSimUtil.Routing.refresh_portals(actor_sim)
            TurboSimUtil.Interaction.unlock_queue(actor_sim)
            result = TurboSimUtil.Interaction.push_affordance(actor_sim, SimInteraction.WW_ROUTE_TO_SEX_LOCATION, insert_strategy=TurboInteractionUtil.QueueInsertStrategy.FIRST, priority=TurboInteractionUtil.Priority.Critical, run_priority=TurboInteractionUtil.Priority.Critical)
            while result:
                sim_ev(actor_sim).in_sex_process_interaction = TurboInteractionUtil.get_interaction_from_enqueue_result(result)
        return True


class AskForSexSocialFailureInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'AskForSexSocialFailureInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return True

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        sim = cls.get_interaction_sim(interaction_instance)
        target = cls.get_interaction_target(interaction_instance)
        clear_sim_sex_extra_data(sim)
        if target is not None:
            clear_sim_sex_extra_data(target)
        apply_asking_for_woohoo_relations(sim, target, False)
        return True

