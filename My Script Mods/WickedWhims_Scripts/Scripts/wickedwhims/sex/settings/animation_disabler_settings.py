'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''from collections import OrderedDictfrom turbolib.l18n_util import TurboL18NUtilfrom turbolib.special.custom_exception_watcher import exception_watchfrom turbolib.ui_util import TurboUIUtilfrom wickedwhims.main.settings._ts4_menu_utils import get_menu_simfrom wickedwhims.sex.animations.animations_disabler_handler import update_disabled_sex_animation_data, is_sex_animation_disabled, switch_disabled_sex_animationfrom wickedwhims.sex.animations.animations_handler import recollect_sex_animation_packages, get_all_sex_animationsfrom wickedwhims.sex.enums.sex_type import SexCategoryTypefrom wickedwhims.sex.sex_location_handler import SexLocationTypefrom wickedwhims.utils_interfaces import get_arrow_icon, display_picker_list_dialog, get_selected_icon, get_unselected_icon, display_ok_dialog, get_action_icon_CURRENT_AUTHOR_NAME = None
def open_player_animations_disabler():

    def ok_dialog_callback(_):
        _open_animation_authors_picker()

    display_ok_dialog(text=2011685353, title=1853900111, callback=ok_dialog_callback)

def open_autonomy_animations_disabler():

    def ok_dialog_callback(_):
        _open_animation_authors_picker(autonomy=True)

    display_ok_dialog(text=2011685353, title=2284702213, callback=ok_dialog_callback)

def _open_animation_authors_picker(autonomy=False):
    global _CURRENT_AUTHOR_NAME
    _CURRENT_AUTHOR_NAME = None

    @exception_watch()
    def animation_authors_callback(dialog):
        if not TurboUIUtil.ObjectPickerDialog.get_response_result(dialog):
            update_disabled_sex_animation_data()
            recollect_sex_animation_packages()
            from wickedwhims.sex.settings.sex_settings import _open_sex_settings, _open_sex_autonomy_settings
            if autonomy is False:
                _open_sex_settings()
            else:
                _open_sex_autonomy_settings()
            return False
        result_author_name = str(TurboUIUtil.ObjectPickerDialog.get_tag_result(dialog))
        _open_animation_category_picker(result_author_name, autonomy=autonomy)
        return True

    animation_author_picker_rows = list()
    animation_authors = OrderedDict()
    for animation_instance in get_all_sex_animations():
        is_enabled = not is_sex_animation_disabled(animation_instance.get_identifier(), autonomy=autonomy)
        if animation_instance.get_author() not in animation_authors:
            animation_authors[animation_instance.get_author()] = (1, 1 if is_enabled else 0)
        else:
            (overall_animations, enabled_animations) = animation_authors[animation_instance.get_author()]
            animation_authors[animation_instance.get_author()] = (overall_animations + 1, enabled_animations + (1 if is_enabled else 0))
    index = 0
    for (animation_author_name, (overall_animations_count, enabled_animations_count)) in animation_authors.items():
        picker_row = TurboUIUtil.ObjectPickerDialog.ListPickerRow(index, animation_author_name, TurboL18NUtil.get_localized_string(2223654951, (str(enabled_animations_count) + '/' + str(overall_animations_count),)), skip_tooltip=True, icon=get_arrow_icon(), tag=animation_author_name)
        animation_author_picker_rows.append(picker_row)
        index += 1
    display_picker_list_dialog(text=4285227430, title=1853900111 if autonomy is False else 2284702213, picker_rows=animation_author_picker_rows, sim=get_menu_sim(), callback=animation_authors_callback)

def _open_animation_category_picker(author_name, autonomy=False):
    global _CURRENT_AUTHOR_NAME
    _CURRENT_AUTHOR_NAME = author_name

    @exception_watch()
    def animation_categories_callback(dialog):
        if not TurboUIUtil.ObjectPickerDialog.get_response_result(dialog):
            _open_animation_authors_picker(autonomy=autonomy)
            return False
        (result_author_name, result_category_type) = TurboUIUtil.ObjectPickerDialog.get_tag_result(dialog)
        _open_animations_picker(result_author_name, result_category_type, autonomy=autonomy)
        return True

    category_picker_rows = list()
    animation_categories = ((0, SexCategoryType.TEASING, 1782200665), (1, SexCategoryType.HANDJOB, 2036049244), (3, SexCategoryType.FOOTJOB, 122220731), (4, SexCategoryType.ORALJOB, 1133298919), (5, SexCategoryType.VAGINAL, 2874903428), (6, SexCategoryType.ANAL, 3553429146), (7, SexCategoryType.CLIMAX, 1579105152))
    for (index, animation_category_type, animation_category_name) in animation_categories:
        overall_animations_count = 0
        enabled_animations_count = 0
        for animation_instance in get_all_sex_animations():
            while animation_instance.get_sex_category() == animation_category_type and animation_instance.get_author() == author_name:
                overall_animations_count += 1
                if not is_sex_animation_disabled(animation_instance.get_identifier(), autonomy=autonomy):
                    enabled_animations_count += 1
        if overall_animations_count <= 0:
            pass
        picker_row = TurboUIUtil.ObjectPickerDialog.ListPickerRow(index, animation_category_name, TurboL18NUtil.get_localized_string(583685786, (str(enabled_animations_count) + '/' + str(overall_animations_count), author_name)), skip_tooltip=True, icon=get_arrow_icon(), tag=(author_name, animation_category_type))
        category_picker_rows.append(picker_row)
    if autonomy is False:
        title = TurboL18NUtil.get_localized_string(2380367292, (author_name,))
    else:
        title = TurboL18NUtil.get_localized_string(3773354670, (author_name,))
    display_picker_list_dialog(title=title, picker_rows=category_picker_rows, sim=get_menu_sim(), callback=animation_categories_callback)

def _open_animations_picker(author_name, animation_category, autonomy=False):

    @exception_watch()
    def _get_animations_list():
        animations_list = list()
        for animation_instance_x in get_all_sex_animations():
            while animation_instance_x.get_sex_category() == animation_category and animation_instance_x.get_author() == author_name:
                is_disabled_x = is_sex_animation_disabled(animation_instance_x.get_identifier(), autonomy=autonomy)
                animations_list.append((animation_instance_x, is_disabled_x))
        return animations_list

    @exception_watch()
    def animations_callback(dialog):
        if not TurboUIUtil.ObjectPickerDialog.get_response_result(dialog):
            if _CURRENT_AUTHOR_NAME is None:
                _open_animation_authors_picker(autonomy=autonomy)
            else:
                _open_animation_category_picker(_CURRENT_AUTHOR_NAME, autonomy=autonomy)
            return False
        (result_author_name, result_animation_category, result_animation_identifier) = TurboUIUtil.ObjectPickerDialog.get_tag_result(dialog)
        if result_animation_identifier is None:
            animations_to_toggle = _get_animations_list()
            has_disabled_animations = False
            for (_, is_disabled_y) in animations_to_toggle:
                while is_disabled_y is True:
                    has_disabled_animations = True
                    break
            for (animation_instance_y, is_disabled_y) in animations_to_toggle:
                if has_disabled_animations is True and is_disabled_y is True:
                    switch_disabled_sex_animation(animation_instance_y.get_identifier(), autonomy=autonomy)
                else:
                    while has_disabled_animations is False and is_disabled_y is False:
                        switch_disabled_sex_animation(animation_instance_y.get_identifier(), autonomy=autonomy)
        else:
            switch_disabled_sex_animation(result_animation_identifier, autonomy=autonomy)
        _open_animations_picker(result_author_name, result_animation_category, autonomy=autonomy)
        return True

    animation_picker_rows = list()
    toggle_select = TurboUIUtil.ObjectPickerDialog.ListPickerRow(0, 4201638866, 1537618859, icon=get_action_icon(), tag=(author_name, animation_category, None))
    animation_picker_rows.append(toggle_select)
    index = 1
    for (animation_instance, is_disabled) in _get_animations_list():
        animation_locations = list()
        for animation_location in animation_instance.get_locations():
            animation_locations.append(SexLocationType.get_user_name(animation_location))
        if animation_instance.get_custom_locations():
            animation_locations.append('Custom Locations')
        picker_row = TurboUIUtil.ObjectPickerDialog.ListPickerRow(index, animation_instance.get_display_name(), TurboL18NUtil.get_localized_string(708866741, (', '.join(animation_locations),)), skip_tooltip=True, icon=get_unselected_icon() if is_disabled is True else get_selected_icon(), tag=(author_name, animation_category, animation_instance.get_identifier()))
        animation_picker_rows.append(picker_row)
        index += 1
    if autonomy is False:
        title = TurboL18NUtil.get_localized_string(2380367292, (author_name,))
    else:
        title = TurboL18NUtil.get_localized_string(3773354670, (author_name,))
    display_picker_list_dialog(title=title, picker_rows=animation_picker_rows, sim=get_menu_sim(), callback=animations_callback)
