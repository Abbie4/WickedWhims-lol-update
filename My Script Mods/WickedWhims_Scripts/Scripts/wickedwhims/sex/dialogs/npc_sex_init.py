'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from turbolib.l18n_util import TurboL18NUtil
from turbolib.manager_util import TurboManagerUtil
from turbolib.special.custom_exception_watcher import exception_watch
from turbolib.ui_util import TurboUIUtil
from wickedwhims.main.settings._ts4_menu_utils import get_menu_sim, clear_menu_sim
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.sex.animations.animations_cache import get_animation_max_amount_of_actors
from wickedwhims.sex.animations.animations_handler import get_available_sex_animations
from wickedwhims.sex.animations.animations_operator import get_random_animation, get_animations_with_params, ChoiceListRandomAnimationPickerRow
from wickedwhims.sex.dialogs.dialog_utils import get_sex_category_animations_stbl_name, get_sex_category_stbl_name
from wickedwhims.sex.enums.sex_gender import get_sim_sex_gender
from wickedwhims.sex.enums.sex_type import SexCategoryType
from wickedwhims.sex.sex_handlers.pre_sex_handler import PreSexInteractionHandler
from wickedwhims.sex.sex_operators.general_sex_handlers_operator import clear_sims_sex_extra_data
from wickedwhims.sex.sex_operators.pre_sex_handlers_operator import start_sex_interaction_from_pre_sex_handler
from wickedwhims.sex.sex_privileges import is_sim_allowed_for_animation, display_not_allowed_message
from wickedwhims.sex.utils.sex_init import get_nearby_sims_for_sex
from wickedwhims.utils_interfaces import display_picker_list_dialog, display_sim_picker_dialog, display_ok_dialog, get_arrow_icon

def open_sex_npc_sims_picker_dialog(origin_position, sex_category_type, location_identifier, game_object_id, object_height, lot_id, location_position, location_level, location_angle, location_route_position, route_level, is_manual=False):

    @exception_watch()
    def npc_sims_picker_callback(dialog):
        clear_menu_sim()
        if not TurboUIUtil.SimPickerDialog.get_response_result(dialog):
            return False
        picked_sims_ids = TurboUIUtil.SimPickerDialog.get_tag_results(dialog)
        if not picked_sims_ids:
            return False
        picked_sims = list()
        for sim_id in picked_sims_ids:
            sim_info = TurboManagerUtil.Sim.get_sim_info(int(sim_id))
            if sim_info is None:
                return False
            picked_sims.append(sim_info)
        is_sim_sex_allowed = is_sim_allowed_for_animation(picked_sims, sex_category_type)
        if not is_sim_sex_allowed:
            display_not_allowed_message(is_sim_sex_allowed)
            return False
        pre_sex_handler = PreSexInteractionHandler(sex_category_type, TurboManagerUtil.Sim.get_sim_id(next(iter(picked_sims))), location_identifier, game_object_id, object_height, lot_id, location_position.x, location_position.y, location_position.z, location_level, location_angle, location_route_position.x, location_route_position.y, location_route_position.z, route_level, is_manual=is_manual)
        for sim_info in picked_sims:
            pre_sex_handler.add_sim(sim_info)
            sim_ev(sim_info).active_pre_sex_handler = pre_sex_handler
        open_start_npc_sex_animations_picker_dialog(pre_sex_handler)
        return True

    max_amount_of_actors = get_animation_max_amount_of_actors(sex_category_type, location_identifier[0]) or get_animation_max_amount_of_actors(sex_category_type, location_identifier[1])
    if max_amount_of_actors <= 0:
        display_ok_dialog(text=2459296019, title=get_sex_category_animations_stbl_name(sex_category_type))
        return
    sims_list = tuple(get_nearby_sims_for_sex(origin_position, radius=32, only_npc=True))
    if not sims_list:
        display_ok_dialog(text=3288282583, text_tokens=(get_sex_category_stbl_name(sex_category_type),), title=get_sex_category_animations_stbl_name(sex_category_type))
        return
    display_sim_picker_dialog(text=389626746, title=get_sex_category_animations_stbl_name(sex_category_type), sims_id_list=sims_list, selectable_amount=max_amount_of_actors, sim=get_menu_sim(), callback=npc_sims_picker_callback)


def open_random_sex_npc_sims_picker_dialog(origin_position, location_identifier, game_object_id, object_height, lot_id, location_position, location_level, location_angle, location_route_position, route_level, is_manual=False):

    @exception_watch()
    def random_sex_npc_sims_picker_callback(dialog):
        clear_menu_sim()
        if not TurboUIUtil.SimPickerDialog.get_response_result(dialog):
            return False
        picked_sims_ids = TurboUIUtil.SimPickerDialog.get_tag_results(dialog)
        if not picked_sims_ids:
            return False
        picked_sims = list()
        for sim_id in picked_sims_ids:
            sim_info = TurboManagerUtil.Sim.get_sim_info(int(sim_id))
            if sim_info is None:
                return False
            picked_sims.append(sim_info)
        random_animation = get_random_animation(location_identifier, picked_sims)
        if random_animation is None:
            display_ok_dialog(text=2693069513, title=1890248379)
            return False
        pre_sex_handler = PreSexInteractionHandler(random_animation.get_sex_category(), TurboManagerUtil.Sim.get_sim_id(next(iter(picked_sims))), location_identifier, game_object_id, object_height, lot_id, location_position.x, location_position.y, location_position.z, location_level, location_angle, location_route_position.x, location_route_position.y, location_route_position.z, route_level, is_manual=is_manual)
        pre_sex_handler.set_animation_instance(random_animation)
        for sim_info in picked_sims:
            pre_sex_handler.add_sim(sim_info)
            sim_ev(sim_info).active_pre_sex_handler = pre_sex_handler
        start_sex_interaction_from_pre_sex_handler(pre_sex_handler)
        return True

    sims_list = tuple(get_nearby_sims_for_sex(origin_position, radius=32, only_npc=True))
    if not sims_list:
        display_ok_dialog(text=3288282583, title=1890248379)
        return
    display_sim_picker_dialog(text=389626746, title=1890248379, sims_id_list=sims_list, selectable_amount=48, sim=get_menu_sim(), callback=random_sex_npc_sims_picker_callback)


def open_start_npc_sex_animations_category_picker_dialog(pre_sex_handler):

    @exception_watch()
    def animation_categories_picker_callback(dialog):
        if pre_sex_handler is None:
            return False
        if not TurboUIUtil.ObjectPickerDialog.get_response_result(dialog):
            clear_sims_sex_extra_data(tuple(pre_sex_handler.get_actors_sim_info_gen()))
            return False
        result_sex_category_type = TurboUIUtil.ObjectPickerDialog.get_tag_result(dialog)
        pre_sex_handler.set_interaction_type(result_sex_category_type)
        open_start_npc_sex_animations_picker_dialog(pre_sex_handler)
        return True

    genders_list = list()
    for sim_info in pre_sex_handler.get_actors_sim_info_gen():
        genders_list.append(get_sim_sex_gender(sim_info))
    category_picker_rows = list()
    animation_categories = ((0, SexCategoryType.TEASING, 77458156), (1, SexCategoryType.HANDJOB, 1425559843), (3, SexCategoryType.FOOTJOB, 223939754), (4, SexCategoryType.ORALJOB, 2747124438), (5, SexCategoryType.VAGINAL, 574589211), (6, SexCategoryType.ANAL, 1610085053))
    for (index, animation_sex_category_type, animation_sex_category_name) in animation_categories:
        animations_list = get_animations_with_params(animation_sex_category_type, pre_sex_handler.get_object_identifier(), genders_list)
        if not animations_list:
            pass
        picker_row = TurboUIUtil.ObjectPickerDialog.ListPickerRow(index, animation_sex_category_name, TurboL18NUtil.get_localized_string(3166569584, tokens=(str(len(animations_list)),)), skip_tooltip=True, icon=get_arrow_icon(), tag=animation_sex_category_type)
        category_picker_rows.append(picker_row)
    display_picker_list_dialog(title=2301874612, picker_rows=category_picker_rows, callback=animation_categories_picker_callback)


def open_start_npc_sex_animations_picker_dialog(pre_sex_handler):

    @exception_watch()
    def animations_picker_callback(dialog):
        if pre_sex_handler is None:
            return False
        if not TurboUIUtil.ObjectPickerDialog.get_response_result(dialog):
            open_start_npc_sex_animations_category_picker_dialog(pre_sex_handler)
            return False
        animation_instance = TurboUIUtil.ObjectPickerDialog.get_tag_result(dialog)
        pre_sex_handler.set_animation_instance(animation_instance)
        start_sex_interaction_from_pre_sex_handler(pre_sex_handler)
        return True

    genders_list = list()
    for sim_info in pre_sex_handler.get_actors_sim_info_gen():
        genders_list.append(get_sim_sex_gender(sim_info))
    animations_list = get_animations_with_params(pre_sex_handler.get_interaction_type(), pre_sex_handler.get_object_identifier(), genders_list)
    animations_rows = list()
    for animation in animations_list:
        animations_rows.append(animation.get_picker_row())
    if len(animations_list) > 1:
        animations_rows.insert(0, ChoiceListRandomAnimationPickerRow(pre_sex_handler, pre_sex_handler.get_interaction_type()))
    if len(get_available_sex_animations()) <= 4:
        display_ok_dialog(text=1066517691, title=3113927949)
    display_picker_list_dialog(title=get_sex_category_animations_stbl_name(pre_sex_handler.get_interaction_type()), picker_rows=animations_rows, sim=next(iter(pre_sex_handler.get_actors_sim_info_gen())), callback=animations_picker_callback)

