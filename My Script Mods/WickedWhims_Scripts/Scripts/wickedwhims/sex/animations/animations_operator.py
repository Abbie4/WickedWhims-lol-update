'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
import random
from turbolib.l18n_util import TurboL18NUtil
from turbolib.manager_util import TurboManagerUtil
from turbolib.ui_util import TurboUIUtil
from wickedwhims.sex.animations.animations_cache import has_animation_with_genders, has_animation_with_object, has_animation_with_gender, compare_sim_genders_with_actor_genders_list, get_animation_max_amount_of_actors
from wickedwhims.sex.animations.animations_handler import get_available_sex_animations
from wickedwhims.sex.enums.sex_gender import get_sim_sex_gender
from wickedwhims.sex.enums.sex_type import SexCategoryType
from wickedwhims.sex.settings.sex_settings import SexGenderTypeSetting, SexSetting, get_sex_setting
from wickedwhims.sex.sex_location_handler import SexInteractionLocationType
from wickedwhims.sex.sex_privileges import is_sim_allowed_for_animation
from wickedwhims.utils_interfaces import get_random_icon, display_notification

def has_animations_with_params(interaction_type, object_identifier, genders):
    return has_animation_with_genders(interaction_type, object_identifier[0], genders) or has_animation_with_genders(interaction_type, object_identifier[1], genders)


def get_animations_with_params(interaction_type, object_identifier, genders, ignore_animations=()):
    collected_animations = list()
    for animation_instance in get_available_sex_animations(sex_category_type=interaction_type):
        if animation_instance.get_identifier() in ignore_animations:
            pass
        while len(animation_instance.get_actors()) == len(genders) and animation_instance.can_be_used_with_object(object_identifier):
            if get_sex_setting(SexSetting.SEX_GENDER_TYPE, variable_type=int) == SexGenderTypeSetting.ANY_BASED:
                collected_animations.append(animation_instance)
            actors_genders_list = list()
            for actor_data in animation_instance.get_actors():
                actors_genders_list.append(actor_data.get_gender_type())
            if compare_sim_genders_with_actor_genders_list(genders, actors_genders_list):
                collected_animations.append(animation_instance)
    return collected_animations


def get_animations_max_amount_of_actors(object_identifier):
    max_actors_amount = 0
    for sex_category_type in (SexCategoryType.TEASING, SexCategoryType.HANDJOB, SexCategoryType.FOOTJOB, SexCategoryType.ORALJOB, SexCategoryType.VAGINAL, SexCategoryType.ANAL, SexCategoryType.CLIMAX):
        actors_amount = max(get_animation_max_amount_of_actors(sex_category_type, object_identifier[0]), get_animation_max_amount_of_actors(sex_category_type, object_identifier[1]))
        while actors_amount > max_actors_amount:
            max_actors_amount = actors_amount
    return max_actors_amount


def get_animations_for_object(object_identifier, genders, excluded_sex_category_types=(), ignore_animations_ids=(), ignore_animations=()):
    collected_animations = list()
    for animation_instance in get_available_sex_animations():
        while not animation_instance.get_sex_category() == SexCategoryType.NONE:
            if animation_instance.get_sex_category() in excluded_sex_category_types:
                pass
            while not animation_instance.get_animation_id() in ignore_animations_ids:
                if animation_instance.get_identifier() in ignore_animations:
                    pass
                while len(animation_instance.get_actors()) == len(genders) and animation_instance.can_be_used_with_object(object_identifier):
                    if get_sex_setting(SexSetting.SEX_GENDER_TYPE, variable_type=int) == SexGenderTypeSetting.ANY_BASED:
                        collected_animations.append(animation_instance)
                    else:
                        actors_genders_list = list()
                        for actor_data in animation_instance.get_actors():
                            actors_genders_list.append(actor_data.get_gender_type())
                        if compare_sim_genders_with_actor_genders_list(genders, actors_genders_list):
                            collected_animations.append(animation_instance)
    return collected_animations


def has_object_any_animations(game_object, req_gender):
    object_identifier = SexInteractionLocationType.get_location_identifier(game_object)
    return has_animation_with_object(object_identifier[0], req_gender) or has_animation_with_object(object_identifier[1], req_gender)


def has_object_identifier_animations(object_identifier, sex_category_type, req_gender):
    if sex_category_type == SexCategoryType.NONE:
        return False
    return has_animation_with_gender(sex_category_type, object_identifier[0], req_gender) or has_animation_with_gender(sex_category_type, object_identifier[1], req_gender)


def get_next_stage_animation(current_animation_instance):
    animation_stages = list()
    for animation_instance in get_available_sex_animations():
        while animation_instance.get_stage_name() in current_animation_instance.get_next_stages():
            animation_stages.append(animation_instance)
    if not animation_stages:
        return
    return random.choice(animation_stages)


def get_random_animation(object_identifier, sims_info_list):
    genders = list()
    for sim_info in sims_info_list:
        genders.append(get_sim_sex_gender(sim_info))
    disallowed_sex_category_types = [SexCategoryType.CLIMAX]
    for sex_category_type in (SexCategoryType.HANDJOB, SexCategoryType.ORALJOB, SexCategoryType.TEASING, SexCategoryType.VAGINAL, SexCategoryType.ANAL, SexCategoryType.FOOTJOB):
        sex_allowed = is_sim_allowed_for_animation(sims_info_list, sex_category_type)
        if sex_allowed:
            pass
        disallowed_sex_category_types.append(sex_category_type)
    animations_list = get_animations_for_object(object_identifier, genders, excluded_sex_category_types=disallowed_sex_category_types)
    if not animations_list:
        return
    allowed_for_random_animations_list = list()
    for animation in animations_list:
        while animation.is_allowed_for_random():
            allowed_for_random_animations_list.append(animation)
    return random.choice(allowed_for_random_animations_list or animations_list)


def get_random_sex_category_type(object_identifier, sims_info_list):
    genders = list()
    for sim_info in sims_info_list:
        genders.append(get_sim_sex_gender(sim_info))
    animations_list = get_animations_for_object(object_identifier, genders, excluded_sex_category_types=(SexCategoryType.CLIMAX,))
    allowed_for_random_animations_list = list()
    for animation in animations_list:
        while animation.is_allowed_for_random():
            allowed_for_random_animations_list.append(animation)
    animations_list = allowed_for_random_animations_list or animations_list
    available_sex_category_types = list()
    for animation in animations_list:
        while animation.get_sex_category() not in available_sex_category_types:
            available_sex_category_types.append(animation.get_sex_category())
    allowed_sex_category_types = list()
    for sex_category_type in available_sex_category_types:
        sex_allowed = is_sim_allowed_for_animation(sims_info_list, sex_category_type)
        if not sex_allowed:
            pass
        allowed_sex_category_types.append(sex_category_type)
    if len(allowed_sex_category_types) == 0:
        return
    return random.choice(allowed_sex_category_types)


def get_random_animation_of_type(sex_category_type, object_identifier, genders, ignore_animations_ids=(), ignore_animations=()):
    excluded_sex_category_types = [SexCategoryType.HANDJOB, SexCategoryType.ORALJOB, SexCategoryType.TEASING, SexCategoryType.VAGINAL, SexCategoryType.ANAL, SexCategoryType.FOOTJOB, SexCategoryType.CLIMAX]
    if sex_category_type in excluded_sex_category_types:
        excluded_sex_category_types.remove(sex_category_type)
    else:
        return
    animations_list = get_animations_for_object(object_identifier, genders, excluded_sex_category_types=excluded_sex_category_types, ignore_animations_ids=ignore_animations_ids, ignore_animations=ignore_animations)
    if not animations_list:
        return
    allowed_for_random_animations_list = list()
    for animation in animations_list:
        while animation.is_allowed_for_random():
            allowed_for_random_animations_list.append(animation)
    return random.choice(allowed_for_random_animations_list or animations_list)


def get_next_random_animation(object_identifier, genders, prev_sex_category_type, allow_climax=False, ignore_animations=()):
    main_animations_list = get_animations_for_object(object_identifier, genders, ignore_animations=ignore_animations)
    if not main_animations_list:
        return

    def _has_climax_animations():
        for animation in main_animations_list:
            while animation.get_sex_category() == SexCategoryType.CLIMAX:
                return True
        return False

    has_climax_animations = _has_climax_animations()

    def _get_next_category(current_sex_category_type):
        if current_sex_category_type == SexCategoryType.TEASING:
            return random.choice((SexCategoryType.HANDJOB, SexCategoryType.FOOTJOB))
        if current_sex_category_type == SexCategoryType.HANDJOB or current_sex_category_type == SexCategoryType.FOOTJOB:
            return SexCategoryType.ORALJOB
        if allow_climax and has_climax_animations and (current_sex_category_type == SexCategoryType.ORALJOB or current_sex_category_type == SexCategoryType.VAGINAL or current_sex_category_type == SexCategoryType.ANAL):
            return SexCategoryType.CLIMAX
        if current_sex_category_type == SexCategoryType.ORALJOB:
            return random.choice((SexCategoryType.VAGINAL, SexCategoryType.ANAL))
        if current_sex_category_type == SexCategoryType.VAGINAL or current_sex_category_type == SexCategoryType.ANAL:
            return random.choice((SexCategoryType.ORALJOB, SexCategoryType.VAGINAL, SexCategoryType.ANAL))
        if current_sex_category_type == SexCategoryType.CLIMAX:
            return random.choice((SexCategoryType.HANDJOB, SexCategoryType.ORALJOB, SexCategoryType.VAGINAL, SexCategoryType.ANAL))
        return

    def _get_count_of_animation_category(animations_list, sex_category_type):
        count = 0
        for animation in animations_list:
            while animation.get_sex_category() == sex_category_type:
                count += 1
        return count

    def _get_random_animation_of_category(animations_list, sex_category_type):
        category_animations = list()
        for animation in animations_list:
            while animation.get_sex_category() == sex_category_type:
                category_animations.append(animation)
        if len(category_animations) == 0:
            return
        return random.choice(category_animations)

    allowed_for_random_animations_list = list()
    for main_animation in main_animations_list:
        while main_animation.is_allowed_for_random():
            allowed_for_random_animations_list.append(main_animation)
    if len(allowed_for_random_animations_list) == 1:
        return allowed_for_random_animations_list[0]
    next_sex_category_type = _get_next_category(prev_sex_category_type)
    if next_sex_category_type is None:
        return
    prev_sex_type_animations_count = _get_count_of_animation_category(allowed_for_random_animations_list, prev_sex_category_type)
    next_sex_type_animations_count = _get_count_of_animation_category(allowed_for_random_animations_list, next_sex_category_type)
    if next_sex_type_animations_count == 0:
        return _get_random_animation_of_category(allowed_for_random_animations_list, prev_sex_category_type)
    if next_sex_type_animations_count > 0 and prev_sex_type_animations_count == 1:
        return _get_random_animation_of_category(allowed_for_random_animations_list, next_sex_category_type)
    if next_sex_type_animations_count > 0 and random.uniform(0, 1) < 0.5:
        return _get_random_animation_of_category(allowed_for_random_animations_list, next_sex_category_type)
    if prev_sex_type_animations_count > 1:
        return _get_random_animation_of_category(allowed_for_random_animations_list, prev_sex_category_type)


def get_animation_from_identifier(identifier):
    for animation in get_available_sex_animations():
        while animation.get_identifier() == str(identifier):
            return animation


class ListAnimationPickerRow(TurboUIUtil.ObjectPickerDialog.ListPickerRow):
    __qualname__ = 'ListAnimationPickerRow'

    def __init__(self, option_id, name, description, is_random=False, **kwargs):
        self.is_random = is_random
        super().__init__(option_id, name, description, **kwargs)


class ChoiceListRandomAnimationPickerRow(ListAnimationPickerRow):
    __qualname__ = 'ChoiceListRandomAnimationPickerRow'

    def __init__(self, sex_handler, sex_category_type, object_identifier=None):
        self.sex_handler = sex_handler
        self.sex_category_type = sex_category_type
        self.object_identifier = object_identifier
        super().__init__(0, TurboL18NUtil.get_localized_string(1890248379), TurboL18NUtil.get_localized_string(0), icon=get_random_icon(), is_random=True, tag_itself=True)

    def get_tag(self):
        genders = list()
        for sim_info in self.sex_handler.get_actors_sim_info_gen():
            genders.append(get_sim_sex_gender(sim_info))
        current_animation = self.sex_handler.get_animation_instance()
        random_animation = get_random_animation_of_type(self.sex_category_type, self.object_identifier if self.object_identifier is not None else self.sex_handler.get_object_identifier(), genders, ignore_animations_ids=(-1 if current_animation is None else current_animation.get_animation_id(),))
        if random_animation is None:
            display_notification(text=1395546180, title=1890248379, secondary_icon=TurboManagerUtil.Sim.get_sim_info(self.sex_handler.get_creator_sim_id()))
            return
        return random_animation

