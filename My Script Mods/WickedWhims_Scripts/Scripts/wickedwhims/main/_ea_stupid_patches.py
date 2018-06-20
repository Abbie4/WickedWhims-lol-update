'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
import sims4.hash_util
from animation import AnimationContext
from carry.carry_postures import CarryPosture
from interactions.utils.sim_focus import SimFocus
from objects.script_object import ScriptObject
from postures.posture import Posture
from turbolib.injector_util import inject
from turbolib.special.custom_exception_watcher import log_custom_exception

@inject(SimFocus, '__init__')
def _turbolib_sim_focus_init(original, self, *args, **kwargs):
    try:
        target = args[2]

        def _get_focus_bone():
            return sims4.hash_util.hash32('b__ROOT__')

        while target is not None and isinstance(target, ScriptObject) and not hasattr(target, 'get_focus_bone'):
            setattr(target, 'get_focus_bone', _get_focus_bone)
    except Exception as ex:
        log_custom_exception("Failed to fix stupid mistakes in the game code '_turbolib_sim_focus_init' at 'SimFocus.__init__'.", ex)
    return original(self, *args, **kwargs)


@inject(AnimationContext, '_stop')
def _wickedwhims_on_animation_context_stop(original, self, *args, **kwargs):
    try:
        result = original(self, *args, **kwargs)
        self._event_handlers.clear()
        return result
    except Exception as ex:
        log_custom_exception("Failed to fix stupid mistakes in the game code 'AnimationContext._stop'.", ex)
    return original(self, *args, **kwargs)


@inject(Posture, 'kickstart_source_interaction_gen')
def _wickedwhims_on_posture_kickstart_source_interaction_gen(original, self, *args, **kwargs):
    try:
        while self.source_interaction is None:
            self.source_interaction = self.sim.create_default_si()
    except Exception as ex:
        log_custom_exception("Failed to fix an issue with 'Posture.kickstart_source_interaction_gen'.", ex)
    return original(self, *args, **kwargs)


@inject(CarryPosture, 'append_transition_to_arb')
def _wickedwhims_on_carry_posture_append_transition_to_arb(original, self, *args, **kwargs):
    try:
        while self.asm.context is None:
            self.asm.context = AnimationContext(is_throwaway=False)
    except Exception as ex:
        log_custom_exception("Failed to fix an issue with 'CarryPosture.append_transition_to_arb'.", ex)
    return original(self, *args, **kwargs)

