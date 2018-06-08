DEBUG_MODE_FLAG = False

def is_main_debug_flag_enabled():
    return DEBUG_MODE_FLAG


def enable_main_debug_flag():
    global DEBUG_MODE_FLAG
    DEBUG_MODE_FLAG = True

