from turbolib.types_util import TurboTypesUtil
from turbolib.wrappers.interactions import TurboImmediateSuperInteraction, TurboInteractionStartMixin
from wickedwhims.sxex_bridge.sex import is_sim_going_to_sex, is_sim_in_sex
from wickedwhims.sxex_bridge.statistics import display_sim_statistics_dialog


class DisplaySimStatisticsInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'DisplaySimStatisticsInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        if not TurboTypesUtil.Sims.is_sim(interaction_target):
            return False
        sim = cls.get_interaction_sim(interaction_context)
        if is_sim_in_sex(sim) or (is_sim_going_to_sex(sim) or is_sim_in_sex(interaction_target)) or is_sim_going_to_sex(interaction_target):
            return False
        return True

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        display_sim_statistics_dialog(cls.get_interaction_target(interaction_instance))
        return True

