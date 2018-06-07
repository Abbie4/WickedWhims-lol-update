'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''from turbolib.wrappers.interactions import TurboImmediateSuperInteraction, TurboInteractionStartMixinfrom wickedwhims.debug.debug_controller import is_main_debug_flag_enabled
class DebugInfoTempInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'DebugInfoTempInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return is_main_debug_flag_enabled()

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        pass
