'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''from wickedwhims.sex.enums.sex_type import SexCategoryType
def get_sex_category_stbl_name(sex_category_type):
    if sex_category_type == SexCategoryType.TEASING:
        return 1782200665
    if sex_category_type == SexCategoryType.HANDJOB:
        return 2036049244
    if sex_category_type == SexCategoryType.FOOTJOB:
        return 122220731
    if sex_category_type == SexCategoryType.ORALJOB:
        return 1133298919
    if sex_category_type == SexCategoryType.VAGINAL:
        return 2874903428
    if sex_category_type == SexCategoryType.ANAL:
        return 3553429146
    if sex_category_type == SexCategoryType.CLIMAX:
        return 1579105152
    return 1890248379

def get_sex_category_animations_stbl_name(sex_category_type):
    if sex_category_type == SexCategoryType.TEASING:
        return 77458156
    if sex_category_type == SexCategoryType.HANDJOB:
        return 1425559843
    if sex_category_type == SexCategoryType.FOOTJOB:
        return 223939754
    if sex_category_type == SexCategoryType.ORALJOB:
        return 2747124438
    if sex_category_type == SexCategoryType.VAGINAL:
        return 574589211
    if sex_category_type == SexCategoryType.ANAL:
        return 1610085053
    if sex_category_type == SexCategoryType.CLIMAX:
        return 3986970407
    return 3494584829
