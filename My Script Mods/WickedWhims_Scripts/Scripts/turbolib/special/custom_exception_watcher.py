import os
import datetime
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


def log_message(message):
    _log_message_text("TurboLib: " + message + "\n")


def _log_message_text(message):
    msg = '{} {}\n'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'), message)
    try:
        file_path = _get_ww_message_file_path()
        if file_path is not None:
            log_file = open(file_path, 'a', buffering=1, encoding='utf-8')
            log_file.write(msg)
            log_file.flush()
    except:
        pass


def _get_ww_message_file_path():
    root_path = ''
    root_file = os.path.normpath(os.path.dirname(os.path.realpath(__file__))).replace(os.sep, '/')
    root_file_split = root_file.split('/')
    exit_index = len(root_file_split) - root_file_split.index('Mods')
    for index in range(0, len(root_file_split) - exit_index):
        root_path += str(root_file_split[index]) + '/'
    from wickedwhims.version_registry import get_mod_version_str
    mod_version = get_mod_version_str()
    file_path = root_path + 'WickedWhims_' + str(mod_version) + '_Message.txt'
    if os.path.exists(file_path) and os.path.getsize(file_path) >> 20 >= 5:
        current_date = str(datetime.datetime.today().day) + '_' + str(datetime.datetime.today().strftime('%B')) + '_' + str(datetime.datetime.today().year)
        os.rename(file_path, root_path + 'Old_WickedWhims_' + str(mod_version) + '_Message_' + current_date + '.txt')
    return file_path


def log_custom_exception(exception_message, exception=None):
    stack_trace = ''.join(traceback.format_stack())
    stack_trace += 'TurboLib: ' + exception_message + ' -> ' + str(exception) + '\n'
    _log_trackback(stack_trace)


def _log_trackback(trackback):
    call_exception_feedback()
    exception_trackback_text = '{} {}\n'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'), trackback)
    for exception_watch_callback in EXCEPTION_WATCH_CALLBACKS:
        try:
            file_path = exception_watch_callback()
            if file_path is not None:
                log_file = open(file_path, 'a', buffering=1, encoding='utf-8')
                log_file.write(exception_trackback_text)
                log_file.flush()
        except:
            pass

