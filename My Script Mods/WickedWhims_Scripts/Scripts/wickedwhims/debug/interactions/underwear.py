from enums.statistics_enum import SimCommodity
from turbolib.sim_util import TurboSimUtil
from turbolib.wrappers.interactions import TurboImmediateSuperInteraction, TurboInteractionStartMixin
from wickedwhims.debug.debug_controller import is_main_debug_flag_enabled
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.utils_interfaces import display_notification
from wickedwhims.utils_statistics import get_sim_statistic_value

class DebugUnderwearMatrixInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'DebugUnderwearMatrixInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return is_main_debug_flag_enabled()

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        sim = cls.get_interaction_target(interaction_instance)
        underwear_debug_info = ''
        underwear_debug_info += '\nUnderwear Flags:\n'
        underwear_debug_info += '  Top: ' + str(sim_ev(sim).underwear_flags['top']) + ' (stat: ' + str(get_sim_statistic_value(sim, SimCommodity.WW_NUDITY_IS_TOP_UNDERWEAR)) + ')\n'
        underwear_debug_info += '  Bottom: ' + str(sim_ev(sim).underwear_flags['bottom']) + ' (stat: ' + str(get_sim_statistic_value(sim, SimCommodity.WW_NUDITY_IS_BOTTOM_UNDERWEAR)) + ')\n'
        underwear_debug_info += '\nUnderwear Matrix:\n'
        for (outfit_id, underwear_data) in sim_ev(sim).underwear_outfits_parts.items():
            underwear_debug_info += str(outfit_id) + ' > ' + str(underwear_data) + '\n'
        display_notification(text=underwear_debug_info, title=str(TurboSimUtil.Name.get_name(sim)[0]) + ' ' + str(TurboSimUtil.Name.get_name(sim)[1]) + ' Underwear Debug', secondary_icon=sim)

