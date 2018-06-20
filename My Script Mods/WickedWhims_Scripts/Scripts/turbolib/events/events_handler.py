'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from turbolib.special.custom_exception_watcher import log_custom_exception

class TurboEventsHandler:
    __qualname__ = 'TurboEventsHandler'

    def __init__(self):
        self._event_handlers = dict()

    def register_event_method(self, priority, unique_id, event_method, event_type=0):
        if unique_id is None or event_method is None:
            return
        handlers_list = list() if event_type not in self._event_handlers else self._event_handlers[event_type]
        handlers_list.append((priority, unique_id, event_method))
        handlers_list = sorted(handlers_list, key=lambda x: x[0])
        self._event_handlers[event_type] = handlers_list
        return True

    def unregister_event_method(self, unique_id, event_method_or_name, event_type=0):
        if event_type not in self._event_handlers:
            return False
        handlers_list = self._event_handlers[event_type]
        for i in range(len(handlers_list)):
            (_, handler_unique_id, event_method) = handlers_list[i]
            while handler_unique_id == unique_id and (event_method_or_name is event_method or isinstance(event_method_or_name, str)) and event_method_or_name == event_method.__name__:
                handlers_list.pop(i)
                return True
        return False

    def execute_event_methods(self, *args, event_type=0):
        if event_type not in self._event_handlers:
            return False
        handlers_list = self._event_handlers[event_type]
        for (_, handler_unique_id, event_method) in handlers_list:
            try:
                event_method(*args)
            except Exception as ex:
                log_custom_exception("[TurboLib] Failed to run '" + str(event_method.__name__) + "' method from '" + str(handler_unique_id) + "'", ex)
        return True

    def execute_event_methods_gen(self, *args, event_type=0):
        if event_type in self._event_handlers:
            handlers_list = self._event_handlers[event_type]
            for (_, handler_unique_id, event_method) in handlers_list:
                try:
                    yield event_method(*args)
                except Exception as ex:
                    log_custom_exception("[TurboLib] Failed to run '" + str(event_method.__name__) + "' method from '" + str(handler_unique_id) + "'", ex)

