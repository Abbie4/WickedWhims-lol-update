'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from turbolib.sim_util import TurboSimUtil
from turbolib.wrappers.interactions import TurboImmediateSuperInteraction, TurboInteractionStartMixin
from wickedwhims.debug.debug_controller import is_main_debug_flag_enabled
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.utils_interfaces import display_notification

class DebugSexInfoInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'DebugSexInfoInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return is_main_debug_flag_enabled()

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        sim = cls.get_interaction_target(interaction_instance)
        sex_debug_info = ''
        sex_debug_info += '\
Sex Data:\
'
        sex_debug_info += '  Is Playing Sex: ' + str(sim_ev(sim).is_playing_sex) + '\
'
        sex_debug_info += '  Active Sex Handler Id: ' + str(sim_ev(sim).active_sex_handler_identifier) + '\
'
        sex_debug_info += '\
  Has Setup Sex: ' + str(sim_ev(sim).has_setup_sex) + '\
'
        sex_debug_info += '  Is Ready To Sex: ' + str(sim_ev(sim).is_ready_to_sex) + '\
'
        sex_debug_info += '  Is In Process To Sex: ' + str(sim_ev(sim).is_in_process_to_sex) + '\
'
        sex_debug_info += '  Has Sex Process Insteraction: ' + str(sim_ev(sim).in_sex_process_interaction is not None) + '\
'
        sex_debug_info += '\
  Cum Apply Time: ' + str(sim_ev(sim).cum_apply_time) + '\
'
        sex_debug_info += '\
  Is Stapon Allowed: ' + str(sim_ev(sim).is_strapon_allowed) + '\
'
        sex_debug_info += '  Strapon Part Id: ' + str(sim_ev(sim).strapon_part_id) + '\
'
        sex_debug_info += '  Sex Reaction Cooldown: ' + str(sim_ev(sim).sex_reaction_cooldown) + '\
'
        sex_debug_info += '  Sex Reaction Skip Handlers: ' + str(sim_ev(sim).sex_reaction_handlers_list) + '\
'
        sex_debug_info += '  Sim State Snapshot: ' + str([str(key) + ': ' + str(value) for (key, value) in sim_ev(sim).sim_sex_state_snapshot.items()]) + '\
'
        sex_debug_info += '  Immutable Sim State Snapshot: ' + str([str(key) + ': ' + str(value) for (key, value) in sim_ev(sim).sim_immutable_sex_state_snapshot.items()]) + '\
'
        sex_debug_info += '\
  Pre Sex Handler: ' + (str(sim_ev(sim).active_pre_sex_handler.get_string_data()) if sim_ev(sim).active_pre_sex_handler is not None else str(None)) + '\
'
        sex_debug_info += '  Active Sex Handler: ' + (str(sim_ev(sim).active_sex_handler.get_string_data()) if sim_ev(sim).active_sex_handler is not None else str(None)) + '\
'
        display_notification(text=sex_debug_info, title=str(TurboSimUtil.Name.get_name(sim)[0]) + ' ' + str(TurboSimUtil.Name.get_name(sim)[1]) + ' Sex Debug', secondary_icon=sim)

