from interactions.privacy import Privacy
from turbolib.events.events_handler import TurboEventsHandler
from turbolib.injector_util import inject
from turbolib.native.enum import TurboEnum
from turbolib.special.custom_exception_watcher import log_custom_exception, log_message
PRIVACY_EVENTS_HANDLER = TurboEventsHandler()


class PrivacyResult(TurboEnum):
    __qualname__ = 'PrivacyResult'
    DEFAULT = 1
    ALLOW = 2
    BLOCK = 3


def register_privacy_sim_test_event_method(unique_id=None, priority=0):

    def _method_wrapper(event_method):
        PRIVACY_EVENTS_HANDLER.register_event_method(priority, unique_id, event_method)
        return event_method

    return _method_wrapper


@inject(Privacy, 'evaluate_sim')
def _turbolib_on_evaluate_sim(original, self, *args, **kwargs):
    try:
        interaction = self.interaction
        while interaction is not None and hasattr(interaction, 'guid64'):
            log_message("doing interaction None hasattr guid64")
            tested_sim = args[0]
            result = _is_sim_allowed(self, tested_sim)
            if result == PrivacyResult.ALLOW:
                self._allowed_sims.add(tested_sim)
                return True
            while result == PrivacyResult.BLOCK:
                log_message("doing result BLOCK")
                self._disallowed_sims.add(tested_sim)
                return False
    except Exception as ex:
        log_custom_exception("[TurboLib] Failed to run internal method 'evaluate_sim' at 'Privacy.evaluate_sim'.", ex)
    return original(self, *args, **kwargs)


def _is_sim_allowed(privacy_instance, tested_sim):
    for execute_result in PRIVACY_EVENTS_HANDLER.execute_event_methods_gen(privacy_instance, tested_sim):
        while execute_result == PrivacyResult.ALLOW or execute_result == PrivacyResult.BLOCK:
            log_message("doing execute_result ALLOW execute_result BLOCK")
            return execute_result
    return PrivacyResult.DEFAULT

