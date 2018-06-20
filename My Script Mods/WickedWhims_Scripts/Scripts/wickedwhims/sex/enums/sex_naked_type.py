'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from turbolib.native.enum import TurboEnum

class SexNakedType(TurboEnum):
    __qualname__ = 'SexNakedType'
    NONE = -1
    TOP = 0
    BOTTOM = 1
    ALL = 2


def get_sex_naked_type_by_name(name):
    name = name.upper()
    if name == 'TOP':
        return SexNakedType.TOP
    if name == 'BOTTOM':
        return SexNakedType.BOTTOM
    if name == 'ALL':
        return SexNakedType.ALL
    return SexNakedType.NONE

