from enums.statistics_enum import SimCommodity
from turbolib.sim_util import TurboSimUtil
from turbolib.wrappers.interactions import TurboImmediateSuperInteraction, TurboInteractionStartMixin
from wickedwhims.debug.debug_controller import is_main_debug_flag_enabled
from wickedwhims.sex.autonomy.sims import get_sex_pair_score
from wickedwhims.sex.relationship_handler import get_relationship_score
from wickedwhims.utils_interfaces import display_notification
from wickedwhims.utils_statistics import get_sim_statistic_value


class DebugRelationshipInfoInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'DebugRelationshipInfoInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return is_main_debug_flag_enabled()

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        sim = cls.get_interaction_sim(interaction_instance)
        target = cls.get_interaction_target(interaction_instance)
        relationship_debug_info = ''
        relationship_debug_info += 'Desire Data:\n'
        relationship_debug_info += '  Master Desire Level: ' + str(get_sim_statistic_value(target, SimCommodity.WW_SEX_MASTER_DESIRE)) + '\n'
        if sim is not target:
            relationship_debug_info += '\n' + str(TurboSimUtil.Name.get_name(sim)[0]) + ' ' + str(TurboSimUtil.Name.get_name(sim)[1]) + ' and ' + str(TurboSimUtil.Name.get_name(target)[0]) + ' ' + str(TurboSimUtil.Name.get_name(target)[1]) + ':'
            rel_score_a = get_relationship_score(sim, target)
            rel_score_b = get_relationship_score(target, sim)
            relationship_debug_info += '\n  Relationship Score: ' + str(rel_score_a) + ' / ' + str(rel_score_b) + ' / ' + str(get_sex_pair_score(sim, target))
        display_notification(text=relationship_debug_info, title=str(TurboSimUtil.Name.get_name(target)[0]) + ' ' + str(TurboSimUtil.Name.get_name(target)[1]) + ' Relationship Debug', secondary_icon=target)

