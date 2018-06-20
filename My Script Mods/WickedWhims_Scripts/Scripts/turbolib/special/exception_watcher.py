from sims4.log import Logger
from turbolib.injector_util import inject
from turbolib.special.exceptions_feedback import call_exception_feedback

@inject(Logger, 'exception')
def _turbolib_on_exception_log(original, self, *args, **kwargs):
    result = original(self, *args, **kwargs)
    try:
        call_exception_feedback()
    except:
        pass
    return result

