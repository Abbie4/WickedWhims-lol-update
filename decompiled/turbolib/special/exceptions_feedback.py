'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
EXCEPTION_CALLBACK_METHODS = set()

def register_exception_callback_method():

    def regiser_to_collection(method):
        EXCEPTION_CALLBACK_METHODS.add(method)
        return method

    return regiser_to_collection

def call_exception_feedback():
    from turbolib.events.core_tick import manual_register_zone_update_event_method
    manual_register_zone_update_event_method(_wickedwhims_call_exception_feedback_on_tick, unique_id='WickedWhims', always_run=True)

def _wickedwhims_call_exception_feedback_on_tick():
    global EXCEPTION_CALLBACK_METHODS
    for callback_method in EXCEPTION_CALLBACK_METHODS:
        try:
            callback_method()
        except:
            pass
    EXCEPTION_CALLBACK_METHODS = set()
    from turbolib.events.core_tick import unregister_zone_update_event_method
    unregister_zone_update_event_method('_wickedwhims_call_exception_feedback_on_tick', unique_id='WickedWhims')

