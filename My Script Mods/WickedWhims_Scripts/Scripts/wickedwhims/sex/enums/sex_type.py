from turbolib.native.enum import TurboEnum

class SexCategoryType(TurboEnum):
    __qualname__ = 'SexCategoryType'
    NONE = -1
    TEASING = 0
    HANDJOB = 1
    FOOTJOB = 2
    ORALJOB = 3
    VAGINAL = 4
    ANAL = 5
    CLIMAX = 6


def get_sex_category_type_by_name(name):
    name = name.upper()
    if name == 'HANDJOB':
        return SexCategoryType.HANDJOB
    if name == 'FOOTJOB':
        return SexCategoryType.FOOTJOB
    if name == 'ORALJOB':
        return SexCategoryType.ORALJOB
    if name == 'TEASING':
        return SexCategoryType.TEASING
    if name == 'VAGINAL':
        return SexCategoryType.VAGINAL
    if name == 'ANAL':
        return SexCategoryType.ANAL
    if name == 'CLIMAX':
        return SexCategoryType.CLIMAX
    return SexCategoryType.NONE

