from enums.interactions_enum import SimInteraction
from turbolib.interaction_util import TurboInteractionUtil
from turbolib.manager_util import TurboManagerUtil
from turbolib.math_util import TurboMathUtil
from turbolib.sim_util import TurboSimUtil
from turbolib.types_util import TurboTypesUtil
from turbolib.wrappers.interactions import TurboImmediateSuperInteraction, TurboInteractionStartMixin
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.sex._ts4_sex_utils import route_sim_away_from_interaction

class GoAwayInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'GoAwayInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return True

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return route_sim_away_from_interaction(interaction_instance, cls.get_interaction_sim(interaction_instance))


class AskToGoAwayInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'AskToGoAwayInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        if interaction_target is None or not TurboTypesUtil.Sims.is_sim(interaction_target):
            return False
        sex_handler = sim_ev(cls.get_interaction_sim(interaction_context)).active_sex_handler
        if sex_handler is None:
            return False
        if sim_ev(interaction_target).active_sex_handler is not None:
            return False
        if TurboManagerUtil.Sim.get_sim_id(interaction_target) in sex_handler.go_away_sims_list:
            return False
        line_of_sight = TurboMathUtil.LineOfSight.create(TurboMathUtil.Location.get_location_routing_surface(sex_handler.get_location()), TurboMathUtil.Location.get_location_translation(sex_handler.get_location()), 8.0)
        if not TurboMathUtil.LineOfSight.test(line_of_sight, TurboSimUtil.Location.get_position(interaction_target)):
            return False
        return True

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        sim_ev(cls.get_interaction_sim(interaction_instance)).active_sex_handler.go_away_sims_list.add(TurboManagerUtil.Sim.get_sim_id(cls.get_interaction_target(interaction_instance)))
        result = TurboSimUtil.Interaction.push_affordance(cls.get_interaction_target(interaction_instance), SimInteraction.WW_GO_AWAY_FROM_SEX, target=cls.get_interaction_sim(interaction_instance), interaction_context=TurboInteractionUtil.InteractionContext.SOURCE_SCRIPT, insert_strategy=TurboInteractionUtil.QueueInsertStrategy.NEXT, must_run_next=True, priority=TurboInteractionUtil.Priority.High, run_priority=TurboInteractionUtil.Priority.High)
        return bool(result)

