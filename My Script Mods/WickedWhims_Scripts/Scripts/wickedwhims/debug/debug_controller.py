'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
DEBUG_MODE_FLAG = False

def is_main_debug_flag_enabled():
    return DEBUG_MODE_FLAG


def enable_main_debug_flag():
    global DEBUG_MODE_FLAG
    DEBUG_MODE_FLAG = True

