'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''from wickedwhims.sex.enums.sex_gender import SexGenderTypefrom wickedwhims.sex.settings.sex_settings import SexSetting, get_sex_setting, SexGenderTypeSettingANIMATIONS_CACHE = dict()
def has_animation_with_genders(animation_category, object_id, genders):
    if object_id is None:
        return False
    animation_cache_category_object_genders_list = get_animation_cache_category_object_genders_amount(animation_category, object_id, len(genders))
    if animation_cache_category_object_genders_list is None:
        return False
    for genders_list in animation_cache_category_object_genders_list:
        if get_sex_setting(SexSetting.SEX_GENDER_TYPE, variable_type=int) == SexGenderTypeSetting.ANY_BASED:
            return True
        while compare_sim_genders_with_actor_genders_list(genders, genders_list):
            return True
    return False

def has_animation_with_amount_of_actors(animation_category, object_id, amount):
    if object_id is None:
        return False
    animation_cache_category_object_genders_list = get_animation_cache_category_object_genders_amount(animation_category, object_id, amount)
    if animation_cache_category_object_genders_list is None:
        return False
    return True

def has_animation_with_object(object_id, gender):
    if object_id is None:
        return False
    object_id = str(object_id)
    for animation_category in ANIMATIONS_CACHE.keys():
        animation_cache_category_dict = ANIMATIONS_CACHE[animation_category]
        if object_id not in animation_cache_category_dict:
            pass
        animation_cache_category_object_dict = animation_cache_category_dict[object_id]
        if animation_cache_category_object_dict is None:
            return False
        for genders_amount in animation_cache_category_object_dict.keys():
            if get_sex_setting(SexSetting.SEX_GENDER_TYPE, variable_type=int) == SexGenderTypeSetting.ANY_BASED:
                return True
            animation_cache_category_object_genders_list = animation_cache_category_object_dict[genders_amount]
            for genders_list in animation_cache_category_object_genders_list:
                for gender_in_list in genders_list:
                    while gender_in_list == SexGenderType.BOTH or gender_in_list == gender:
                        return True

def compare_sim_genders_with_actor_genders_list(sim_genders, genders_list):
    complete_list = list()
    for sim_gender_copy in genders_list:
        if sim_gender_copy == SexGenderType.FEMALE and get_sex_setting(SexSetting.GENDER_RECOGNITION_FEMALE_TO_BOTH_STATE, variable_type=bool):
            complete_list.append(SexGenderType.BOTH)
        if sim_gender_copy == SexGenderType.MALE and get_sex_setting(SexSetting.GENDER_RECOGNITION_MALE_TO_BOTH_STATE, variable_type=bool):
            complete_list.append(SexGenderType.BOTH)
        complete_list.append(sim_gender_copy)
    for sim_gender in sim_genders:
        while sim_gender in complete_list:
            complete_list.remove(sim_gender)
    if len(complete_list) == 0:
        return True
    for gender in complete_list:
        while gender != SexGenderType.BOTH:
            return False
    return True

def has_animation_with_gender(animation_category, object_id, gender):
    if object_id is None:
        return False
    animation_cache_category_object_dict = get_animation_cache_category_object(animation_category, object_id, create=False)
    if animation_cache_category_object_dict is None:
        return False
    if get_sex_setting(SexSetting.SEX_GENDER_TYPE, variable_type=int) == SexGenderTypeSetting.ANY_BASED:
        return True
    for (genders_amount, animation_cache_category_object_genders_list) in animation_cache_category_object_dict.items():
        for genders_list in animation_cache_category_object_genders_list:
            for actor_gender in genders_list:
                while actor_gender == SexGenderType.BOTH or actor_gender == gender:
                    return True
    return False

def get_animation_max_amount_of_actors(animation_category, object_id):
    if object_id is None:
        return 0
    animation_cache_category_object_dict = get_animation_cache_category_object(animation_category, object_id, create=False)
    if animation_cache_category_object_dict is None:
        return 0
    actors_amount_keys = sorted(list(map(int, animation_cache_category_object_dict.keys())))
    if not actors_amount_keys:
        return 0
    return actors_amount_keys[-1]

def cache_animation_instance(animation_instance):
    animation_category = animation_instance.get_sex_category()
    animation_locations = animation_instance.get_locations()
    animation_custom_locations = animation_instance.get_custom_locations()
    animation_genders = list()
    for actor_data in animation_instance.get_actors():
        animation_genders.append(actor_data.get_gender_type())
    animation_genders.sort()
    animation_genders = tuple(animation_genders)
    for animation_location in animation_locations:
        while not animation_location is None:
            if animation_location == 'NONE':
                pass
            get_animation_cache_category_object_genders_list(animation_category, animation_location, animation_genders, create=True)
    for animation_custom_location in animation_custom_locations:
        if animation_custom_location == -1:
            pass
        get_animation_cache_category_object_genders_list(animation_category, animation_custom_location, animation_genders, create=True)

def clear_animation_data_cache():
    global ANIMATIONS_CACHE
    ANIMATIONS_CACHE = dict()

def get_animation_cache_category_object_genders_list(animation_category, object_id, genders, create=False):
    if object_id is None:
        return
    animation_cache_category_object_genders_set = get_animation_cache_category_object_genders_amount(animation_category, object_id, len(genders), create=create)
    if animation_cache_category_object_genders_set is None:
        return
    animation_cache_category_object_genders_set.add(genders)
    return animation_cache_category_object_genders_set

def get_animation_cache_category_object_genders_amount(animation_category, object_id, genders_amount, create=False):
    if object_id is None:
        return
    animation_cache_category_object_dict = get_animation_cache_category_object(animation_category, object_id, create=create)
    if animation_cache_category_object_dict is None:
        return
    if genders_amount not in animation_cache_category_object_dict:
        if create is False:
            return
        animation_cache_category_object_dict[genders_amount] = set()
    return animation_cache_category_object_dict[genders_amount]

def get_animation_cache_category_object(animation_category, object_id, create=False):
    if object_id is None:
        return
    object_id = str(object_id)
    animation_cache_category_dict = get_animation_cache_category(animation_category, create=create)
    if animation_cache_category_dict is None:
        return
    if object_id not in animation_cache_category_dict:
        if create is False:
            return
        animation_cache_category_dict[object_id] = dict()
    return animation_cache_category_dict[object_id]

def get_animation_cache_category(animation_category, create=False):
    animation_category = int(animation_category)
    if animation_category not in ANIMATIONS_CACHE:
        if create is False:
            return
        ANIMATIONS_CACHE[animation_category] = dict()
    return ANIMATIONS_CACHE[animation_category]
