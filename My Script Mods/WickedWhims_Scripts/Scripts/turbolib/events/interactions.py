'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''from event_testing.results import TestResultfrom interactions.base.interaction import Interactionfrom interactions.interaction_queue import InteractionQueuefrom interactions.utils.outcome_enums import OutcomeResultfrom turbolib.events.events_handler import TurboEventsHandlerfrom turbolib.injector_util import injectfrom turbolib.native.enum import TurboEnumfrom turbolib.special.custom_exception_watcher import log_custom_exception
class InteractionsTurboEventsHandler(TurboEventsHandler):
    __qualname__ = 'InteractionsTurboEventsHandler'

    def execute_event_methods(self, *args, event_type=0):
        for _ in self.execute_event_methods_gen(event_type=event_type, *args):
            pass
        return True

    def execute_event_methods_gen(self, *args, event_type=0):
        return self._execute_event_methods_gen(event_type=event_type, *args)

    def _execute_event_methods_gen(self, *args, event_type=0):
        if not args or args[0] is None:
            return
        if event_type in self._event_handlers:
            handlers_list = self._event_handlers[event_type]
            for (_, __, event_method) in handlers_list:
                yield event_method(*args)
INTERACTION_EVENTS_HANDLER = InteractionsTurboEventsHandler()
class InteractionEventType(TurboEnum):
    __qualname__ = 'InteractionEventType'
    INTERACTION_RUN = 1
    INTERACTION_QUEUE = 2
    INTERACTION_OUTCOME = 3

def register_interaction_run_event_method(unique_id=None, priority=0):

    def _method_wrapper(event_method):
        INTERACTION_EVENTS_HANDLER.register_event_method(priority, unique_id, event_method, event_type=InteractionEventType.INTERACTION_RUN)
        return event_method

    return _method_wrapper

def manual_register_interaction_run_event_method(event_method, unique_id=None, priority=0):
    INTERACTION_EVENTS_HANDLER.register_event_method(priority, unique_id, event_method, event_type=InteractionEventType.INTERACTION_RUN)

@inject(InteractionQueue, 'run_interaction_gen')
def _turbolib_interaction_run(original, self, *args, **kwargs):
    result = original(self, *args, **kwargs)
    try:
        while result:
            interaction = args[1]
            if interaction is None or interaction.sim is None:
                return
            INTERACTION_EVENTS_HANDLER.execute_event_methods(interaction, event_type=InteractionEventType.INTERACTION_RUN)
    except Exception as ex:
        log_custom_exception("[TurboLib] Failed to run internal method '_turbolib_interaction_run' at 'InteractionQueue.run_interaction_gen'.", ex)
    return result

def register_interaction_queue_event_method(unique_id=None, priority=0):

    def _method_wrapper(event_method):
        INTERACTION_EVENTS_HANDLER.register_event_method(priority, unique_id, event_method, event_type=InteractionEventType.INTERACTION_QUEUE)
        return event_method

    return _method_wrapper

def manual_register_interaction_queue_event_method(event_method, unique_id=None, priority=0):
    INTERACTION_EVENTS_HANDLER.register_event_method(priority, unique_id, event_method, event_type=InteractionEventType.INTERACTION_QUEUE)

@inject(InteractionQueue, 'append')
def _turbolib_interaction_queue(original, self, *args, **kwargs):
    try:
        interaction = args[0]
        if interaction is None or interaction.sim is None:
            return
        for result in INTERACTION_EVENTS_HANDLER.execute_event_methods_gen(interaction, event_type=InteractionEventType.INTERACTION_QUEUE):
            while not result:
                return TestResult(False, 'TurboLib Interaction Cancel')
    except Exception as ex:
        log_custom_exception("[TurboLib] Failed to run internal method '_turbolib_interaction_queue' at 'InteractionQueue.append'.", ex)
    return original(self, *args, **kwargs)

def register_interaction_outcome_event_method(unique_id=None, priority=0):

    def _method_wrapper(event_method):
        INTERACTION_EVENTS_HANDLER.register_event_method(priority, unique_id, event_method, event_type=InteractionEventType.INTERACTION_OUTCOME)
        return event_method

    return _method_wrapper

def manual_register_interaction_outcome_event_method(event_method, unique_id=None, priority=0):
    INTERACTION_EVENTS_HANDLER.register_event_method(priority, unique_id, event_method, event_type=InteractionEventType.INTERACTION_OUTCOME)

@inject(Interaction, 'store_result_for_outcome')
def _turbolib_interaction_outcome_result(original, self, *args, **kwargs):
    try:
        if self.sim is None:
            return
        result = args[1]
        if result == OutcomeResult.SUCCESS:
            result = True
        elif result == OutcomeResult.FAILURE:
            result = False
        else:
            return
        INTERACTION_EVENTS_HANDLER.execute_event_methods(self, result, event_type=InteractionEventType.INTERACTION_OUTCOME)
    except Exception as ex:
        log_custom_exception("[TurboLib] Failed to run internal method '_turbolib_interaction_outcome_result' at 'Interaction.store_result_for_outcome'.", ex)
    return original(self, *args, **kwargs)
