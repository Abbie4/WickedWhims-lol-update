import sys
import traceback
from datetime import datetime
from functools import wraps
from traceback import format_exc
from turbolib.special.exceptions_feedback import call_exception_feedback
EXCEPTION_WATCH_CALLBACKS = list()

def exception_watch():

    def catch_exception(exception_function):

        @wraps(exception_function)
        def wrapper(*args, **kwargs):
            try:
                return exception_function(*args, **kwargs)
            except:
                _log_trackback(format_exc())

        return wrapper

    return catch_exception


def register_exception_watch_callback():

    def _wrapper(method):
        EXCEPTION_WATCH_CALLBACKS.append(method)
        return method

    return _wrapper


def log_custom_exception(exception_message, exception=None):
    exc_info = sys.exc_info()
    if exc_info[1] is not None:
        stack_trace = ''.join(traceback.format_exception(*exc_info))
    else:
        stack_trace = ''.join(traceback.format_stack())
    stack_trace += 'TurboLib: ' + exception_message + ' -> ' + str(type(exception).__name__) + ': ' + str(exception) + '\n'
    _log_trackback(stack_trace)


def _log_trackback(trackback):
    call_exception_feedback()
    exception_trackback_text = '{} {}\n'.format(datetime.now().strftime('%x %X'), trackback)
    for exception_watch_callback in EXCEPTION_WATCH_CALLBACKS:
        try:
            file_path = exception_watch_callback()
            while file_path is not None:
                log_file = open(file_path, 'a', buffering=1, encoding='utf-8')
                log_file.write(exception_trackback_text)
                log_file.flush()
        except:
            pass

