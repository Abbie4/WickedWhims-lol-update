from turbolib.l18n_util import TurboL18NUtil
from turbolib.special.custom_exception_watcher import exception_watch
from turbolib.ui_util import TurboUIUtil
from wickedwhims.sex.animations.animations_operator import get_animations_with_params, ChoiceListRandomAnimationPickerRow, has_animations_with_params
from wickedwhims.sex.dialogs.dialog_utils import get_sex_category_animations_stbl_name
from wickedwhims.sex.enums.sex_gender import get_sim_sex_gender
from wickedwhims.sex.enums.sex_type import SexCategoryType
from wickedwhims.utils_interfaces import display_picker_list_dialog, get_arrow_icon

def open_change_sex_animations_category_picker_dialog(active_sex_handler):

    @exception_watch()
    def animation_categories_picker_callback(dialog):
        if active_sex_handler is None:
            return False
        if not TurboUIUtil.ObjectPickerDialog.get_response_result(dialog):
            return False
        result_sex_category_type = TurboUIUtil.ObjectPickerDialog.get_tag_result(dialog)
        open_change_sex_animations_picker_dialog(active_sex_handler, result_sex_category_type)
        return True

    genders_list = list()
    for sim_info in active_sex_handler.get_actors_sim_info_gen():
        genders_list.append(get_sim_sex_gender(sim_info))
    category_picker_rows = list()
    animation_categories = ((0, SexCategoryType.TEASING, 77458156), (1, SexCategoryType.HANDJOB, 1425559843), (3, SexCategoryType.FOOTJOB, 223939754), (4, SexCategoryType.ORALJOB, 2747124438), (5, SexCategoryType.VAGINAL, 574589211), (6, SexCategoryType.ANAL, 1610085053), (7, SexCategoryType.CLIMAX, 3986970407))
    for (index, animation_sex_category_type, animation_sex_category_name) in animation_categories:
        if not active_sex_handler.is_at_climax and animation_sex_category_type == SexCategoryType.CLIMAX:
            pass
        if not has_animations_with_params(animation_sex_category_type, active_sex_handler.get_object_identifier(), genders_list):
            pass
        animations_list = get_animations_with_params(animation_sex_category_type, active_sex_handler.get_object_identifier(), genders_list)
        if not animations_list:
            pass
        picker_row = TurboUIUtil.ObjectPickerDialog.ListPickerRow(index, animation_sex_category_name, TurboL18NUtil.get_localized_string(3166569584, tokens=(str(len(animations_list)),)), skip_tooltip=True, icon=get_arrow_icon(), tag=animation_sex_category_type)
        category_picker_rows.append(picker_row)
    if len(category_picker_rows) <= 1:
        return
    display_picker_list_dialog(title=2301874612, picker_rows=category_picker_rows, callback=animation_categories_picker_callback)


def open_change_sex_animations_picker_dialog(active_sex_handler, sex_category_type):

    @exception_watch()
    def animation_picker_callback(dialog):
        if active_sex_handler is None:
            return False
        if not TurboUIUtil.ObjectPickerDialog.get_response_result(dialog):
            open_change_sex_animations_category_picker_dialog(active_sex_handler)
            return False
        animation_instance = TurboUIUtil.ObjectPickerDialog.get_tag_result(dialog)
        if animation_instance is not None and animation_instance is not active_sex_handler.get_animation_instance():
            active_sex_handler.set_animation_instance(animation_instance, is_animation_change=True, is_manual=True)
            active_sex_handler.play(is_animation_change=True)
            return True
        return False

    genders_list = list()
    for sim_info in active_sex_handler.get_actors_sim_info_gen():
        genders_list.append(get_sim_sex_gender(sim_info))
    animations_list = get_animations_with_params(sex_category_type, active_sex_handler.get_object_identifier(), genders_list)
    animations_rows = list()
    for animation in animations_list:
        animations_rows.append(animation.get_picker_row(display_selected=animation.get_animation_id() == active_sex_handler.get_animation_instance().get_animation_id()))
    if len(animations_rows) > 1:
        animations_rows.insert(0, ChoiceListRandomAnimationPickerRow(active_sex_handler, sex_category_type))
    display_picker_list_dialog(title=get_sex_category_animations_stbl_name(sex_category_type), picker_rows=animations_rows, callback=animation_picker_callback)


def open_change_sex_location_animations_picker_dialog(active_sex_handler, sex_category_type, new_object_identifier, game_object_id, object_height, location_x, location_y, location_z, location_level, location_angle, route_x, route_y, route_z, route_level):

    @exception_watch()
    def change_sex_location_animation_picker_callback(dialog):
        if active_sex_handler is None:
            return False
        if not TurboUIUtil.ObjectPickerDialog.get_response_result(dialog):
            return False
        animation_instance = TurboUIUtil.ObjectPickerDialog.get_tag_result(dialog)
        active_sex_handler.set_animation_instance(animation_instance, is_manual=True)
        active_sex_handler.set_object_identifier(new_object_identifier)
        active_sex_handler.set_game_object_id(game_object_id)
        active_sex_handler.set_object_height(object_height)
        active_sex_handler.set_location(location_x, location_y, location_z, location_level, location_angle)
        active_sex_handler.set_route_position(route_x, route_y, route_z, route_level)
        active_sex_handler.reassign_actors()
        active_sex_handler.restart()
        return True

    genders_list = list()
    for sim_info in active_sex_handler.get_actors_sim_info_gen():
        genders_list.append(get_sim_sex_gender(sim_info))
    animations_list = get_animations_with_params(sex_category_type, new_object_identifier, genders_list)
    animations_rows = list()
    for animation in animations_list:
        animations_rows.append(animation.get_picker_row())
    if len(animations_rows) > 1:
        animations_rows.insert(0, ChoiceListRandomAnimationPickerRow(active_sex_handler, sex_category_type, object_identifier=new_object_identifier))
    display_picker_list_dialog(title=get_sex_category_animations_stbl_name(sex_category_type), picker_rows=animations_rows, callback=change_sex_location_animation_picker_callback)

