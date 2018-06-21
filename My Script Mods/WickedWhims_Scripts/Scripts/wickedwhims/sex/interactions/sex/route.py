from enums.interactions_enum import SimInteraction
from turbolib.interaction_util import TurboInteractionUtil
from turbolib.manager_util import TurboManagerUtil
from turbolib.math_util import TurboMathUtil
from turbolib.sim_util import TurboSimUtil
from turbolib.wrappers.interactions import TurboInteractionStartMixin, TurboInteractionCancelMixin, TurboInteractionConstraintMixin, TurboSuperInteraction, TurboBaseSuperInteraction, TurboInteractionInitMixin
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.sex.sex_operators.general_sex_handlers_operator import clear_sim_sex_extra_data
from wickedwhims.sex.sex_operators.pre_sex_handlers_operator import unprepare_npc_sim_from_sex

class WaitForSexPartnerInteraction(TurboBaseSuperInteraction, TurboInteractionInitMixin, TurboInteractionStartMixin, TurboInteractionCancelMixin):
    __qualname__ = 'WaitForSexPartnerInteraction'

    @classmethod
    def on_interaction_init(cls, interaction_instance):
        interaction_instance.has_proceeded = False

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return True

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        sim = cls.get_interaction_sim(interaction_instance)
        pre_sex_handler = sim_ev(sim).active_pre_sex_handler
        sim_ev(sim).is_ready_to_sex = True
        if pre_sex_handler is None:
            unprepare_npc_sim_from_sex(sim)
            return False
        if _attempt_sex_init(pre_sex_handler):
            interaction_instance.has_proceeded = True
        return True

    @classmethod
    def on_interaction_cancel(cls, interaction_instance, finishing_type):
        if interaction_instance.has_proceeded is True:
            return
        if finishing_type == TurboInteractionUtil.FinishingType.USER_CANCEL:
            sim = cls.get_interaction_sim(interaction_instance)
            pre_sex_handler = sim_ev(sim).active_pre_sex_handler
            clear_sim_sex_extra_data(sim, only_pre_active_data=True)
            unprepare_npc_sim_from_sex(sim)
            if pre_sex_handler is None:
                return
            for actor_sim_info in pre_sex_handler.get_actors_sim_info_gen():
                if sim_ev(actor_sim_info).in_sex_process_interaction is not None:
                    cls.kill_interaction(sim_ev(actor_sim_info).in_sex_process_interaction)
                clear_sim_sex_extra_data(actor_sim_info, only_pre_active_data=True)
                while sim_ev(actor_sim_info).active_sex_handler is None:
                    unprepare_npc_sim_from_sex(actor_sim_info)


class RouteToSexDestinationInteraction(TurboSuperInteraction, TurboInteractionInitMixin, TurboInteractionConstraintMixin, TurboInteractionStartMixin, TurboInteractionCancelMixin):
    __qualname__ = 'RouteToSexDestinationInteraction'

    @classmethod
    def on_interaction_init(cls, interaction_instance):
        interaction_instance.has_proceeded = False

    @classmethod
    def on_constraint(cls, interaction_instance, interaction_sim, interaction_target):
        pre_sex_handler = sim_ev(interaction_sim).active_pre_sex_handler
        if pre_sex_handler is None:
            return cls.get_stand_or_move_stand_posture_constraint()
        routing_surface = TurboMathUtil.Location.create_routing_identifier(pre_sex_handler.get_route_level())
        circle_constraint = cls.get_circle_constraint(pre_sex_handler.get_route_position(), 1.5, routing_surface, ideal_radius=0.5, ideal_radius_width=0.5)
        posture_constraint = cls.get_stand_or_move_stand_posture_constraint()
        return cls.combine_constraints((circle_constraint, posture_constraint))

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return True

    @classmethod
    def on_interaction_run(cls, interaction_instance):
        return True

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        sim = cls.get_interaction_sim(interaction_instance)
        pre_sex_handler = sim_ev(sim).active_pre_sex_handler
        sim_ev(sim).is_ready_to_sex = True
        if pre_sex_handler is None:
            clear_sim_sex_extra_data(sim, only_pre_active_data=True)
            unprepare_npc_sim_from_sex(sim)
            return False
        if not _attempt_sex_init(pre_sex_handler):
            result = TurboSimUtil.Interaction.push_affordance(sim, SimInteraction.WW_WAIT_FOR_SEX_PARTNER, insert_strategy=TurboInteractionUtil.QueueInsertStrategy.FIRST, run_priority=TurboInteractionUtil.Priority.Critical, priority=TurboInteractionUtil.Priority.Critical, skip_if_running=True)
            if result:
                sim_ev(sim).in_sex_process_interaction = TurboInteractionUtil.get_interaction_from_enqueue_result(result)
            cls.cancel_interaction(interaction_instance, finishing_type=TurboInteractionUtil.FinishingType.NATURAL)
        else:
            interaction_instance.has_proceeded = True

    @classmethod
    def on_interaction_cancel(cls, interaction_instance, finishing_type):
        if interaction_instance.has_proceeded is True:
            return
        if finishing_type == TurboInteractionUtil.FinishingType.USER_CANCEL or finishing_type == TurboInteractionUtil.FinishingType.TRANSITION_FAILURE:
            sim = cls.get_interaction_sim(interaction_instance)
            pre_sex_handler = sim_ev(sim).active_pre_sex_handler
            clear_sim_sex_extra_data(sim, only_pre_active_data=True)
            unprepare_npc_sim_from_sex(sim)
            if pre_sex_handler is None:
                return
            for actor_sim_info in pre_sex_handler.get_actors_sim_info_gen():
                if sim_ev(actor_sim_info).in_sex_process_interaction is not None:
                    cls.kill_interaction(sim_ev(actor_sim_info).in_sex_process_interaction)
                clear_sim_sex_extra_data(actor_sim_info, only_pre_active_data=True)
                while sim_ev(actor_sim_info).active_sex_handler is None:
                    unprepare_npc_sim_from_sex(actor_sim_info)


def _attempt_sex_init(pre_sex_handler):
    if pre_sex_handler.get_sims_amount() == 1:
        pre_sex_handler.start_sex_interaction()
        return True
    if pre_sex_handler.are_all_sims_ready():
        if pre_sex_handler.is_joining_sex():
            creator_sim = TurboManagerUtil.Sim.get_sim_info(pre_sex_handler.get_creator_sim_id())
            active_sex_handler = sim_ev(creator_sim).active_sex_handler
            if active_sex_handler is not None:
                active_sex_handler.stop(hard_stop=True, no_teleport=True, is_joining_stop=True, stop_reason='Joining To Sex!')
                pre_sex_handler.start_sex_interaction()
                return True
            for sim_info in pre_sex_handler.get_actors_sim_info_gen():
                clear_sim_sex_extra_data(sim_info, only_pre_active_data=True)
                while sim_ev(sim_info).is_playing_sex is True:
                    unprepare_npc_sim_from_sex(sim_info)
        pre_sex_handler.start_sex_interaction()
        return True
    return False

