'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from turbolib.manager_util import TurboManagerUtil
from turbolib.special.custom_exception_watcher import exception_watch
from turbolib.ui_util import TurboUIUtil
from wickedwhims.relationships.relationship_settings import get_relationship_setting, RelationshipSetting
from wickedwhims.sex.animations.animations_cache import get_animation_max_amount_of_actors
from wickedwhims.sex.animations.animations_operator import get_random_animation, has_animations_with_params, get_animations_with_params, ChoiceListRandomAnimationPickerRow
from wickedwhims.sex.dialogs.dialog_utils import get_sex_category_stbl_name, get_sex_category_animations_stbl_name
from wickedwhims.sex.enums.sex_gender import get_sim_sex_gender
from wickedwhims.sex.sex_operators.pre_sex_handlers_operator import join_sex_interaction_from_pre_sex_handler
from wickedwhims.sex.sex_privileges import is_sim_allowed_for_animation, display_not_allowed_message
from wickedwhims.sex.utils.sex_init import get_age_limits_for_sex, get_nearby_sims_for_sex
from wickedwhims.utils_interfaces import display_ok_dialog, display_sim_picker_dialog, display_picker_list_dialog

def open_join_sims_picker_dialog(pre_sex_handler, sex_category_type, selected_sims_ids=()):

    @exception_watch()
    def join_sims_picker_callback(dialog):
        if pre_sex_handler is None:
            return False
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
        for sim_info in picked_sims:
            pre_sex_handler.add_sim(sim_info)
        genders_list = list()
        for sim_info in pre_sex_handler.get_actors_sim_info_gen():
            genders_list.append(get_sim_sex_gender(sim_info))
        if sex_category_type is not None:
            sex_allowed = is_sim_allowed_for_animation(tuple(picked_sims), sex_category_type, is_joining=True)
            if not sex_allowed:
                display_not_allowed_message(sex_allowed)
                return False
            has_animations = False
            if has_animations_with_params(sex_category_type, pre_sex_handler.get_object_identifier(), genders_list):
                has_animations = True
            if has_animations is False:
                display_ok_dialog(text=2693069513, title=get_sex_category_animations_stbl_name(sex_category_type))
                return False
            open_join_sex_animations_picker_dialog(pre_sex_handler, picked_sims, sex_category_type)
        else:
            random_animation = get_random_animation(pre_sex_handler.get_object_identifier(), tuple(pre_sex_handler.get_actors_sim_info_gen()))
            if random_animation is None:
                display_ok_dialog(text=2693069513, title=1890248379)
                return False
            pre_sex_handler.set_animation_instance(random_animation)
            join_sex_interaction_from_pre_sex_handler(pre_sex_handler, picked_sims)
        return True

    if sex_category_type is not None:
        max_amount_of_actors = max(get_animation_max_amount_of_actors(sex_category_type, pre_sex_handler.get_object_identifier()[0]), get_animation_max_amount_of_actors(sex_category_type, pre_sex_handler.get_object_identifier()[1]))
    else:
        max_amount_of_actors = 48
    if max_amount_of_actors <= 0:
        if sex_category_type is not None:
            display_ok_dialog(text=443330929, text_tokens=(get_sex_category_animations_stbl_name(sex_category_type),), title=get_sex_category_animations_stbl_name(sex_category_type))
        else:
            display_ok_dialog(text=3121278879, title=1890248379)
        return
    creator_sim = TurboManagerUtil.Sim.get_sim_info(pre_sex_handler.get_creator_sim_id())
    test_incest_of_sims = () if get_relationship_setting(RelationshipSetting.INCEST_STATE, variable_type=bool) else tuple(pre_sex_handler.get_actors_sim_info_gen())
    (min_age_limit, max_age_limit) = get_age_limits_for_sex(tuple(pre_sex_handler.get_actors_sim_info_gen()))
    skip_sims_ids = [TurboManagerUtil.Sim.get_sim_id(actor_sim_info) for actor_sim_info in pre_sex_handler.get_actors_sim_info_gen()]
    sims_list = tuple(get_nearby_sims_for_sex(pre_sex_handler.get_los_position(), radius=16, relative_sims=test_incest_of_sims, min_sims_age=min_age_limit, max_sims_age=max_age_limit, skip_sims_ids=skip_sims_ids))
    if not sims_list:
        display_ok_dialog(text=2721401338, text_tokens=(get_sex_category_stbl_name(sex_category_type), creator_sim), title=get_sex_category_animations_stbl_name(sex_category_type))
        return
    display_sim_picker_dialog(text=747723284, title=get_sex_category_animations_stbl_name(sex_category_type), sims_id_list=sims_list, selected_sims_id_list=selected_sims_ids, selectable_amount=max_amount_of_actors - pre_sex_handler.get_sims_amount(), sim=creator_sim, callback=join_sims_picker_callback)

def open_join_sex_animations_picker_dialog(pre_sex_handler, joining_sims_list, sex_category_type, flip_relationship_check=False):

    @exception_watch()
    def join_sex_animation_picker_callback(dialog):
        if pre_sex_handler is None:
            return False
        if not TurboUIUtil.ObjectPickerDialog.get_response_result(dialog):
            return False
        animation_instance = TurboUIUtil.ObjectPickerDialog.get_tag_result(dialog)
        pre_sex_handler.set_animation_instance(animation_instance)
        join_sex_interaction_from_pre_sex_handler(pre_sex_handler, joining_sims_list, flip_relationship_check=flip_relationship_check)
        return True

    genders_list = list()
    for sim_info in pre_sex_handler.get_actors_sim_info_gen():
        genders_list.append(get_sim_sex_gender(sim_info))
    animations_list = get_animations_with_params(sex_category_type, pre_sex_handler.get_object_identifier(), genders_list)
    animations_rows = list()
    for animation in animations_list:
        animations_rows.append(animation.get_picker_row())
    if len(animations_list) > 1:
        animations_rows.insert(0, ChoiceListRandomAnimationPickerRow(pre_sex_handler, sex_category_type))
    display_picker_list_dialog(title=get_sex_category_animations_stbl_name(sex_category_type), picker_rows=animations_rows, sim=pre_sex_handler.get_creator_sim_id(), callback=join_sex_animation_picker_callback)

