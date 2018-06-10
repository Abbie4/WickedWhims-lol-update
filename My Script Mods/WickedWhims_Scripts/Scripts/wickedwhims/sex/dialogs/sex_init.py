from turbolib.l18n_util import TurboL18NUtil
from turbolib.manager_util import TurboManagerUtil
from turbolib.special.custom_exception_watcher import exception_watch
from turbolib.ui_util import TurboUIUtil
from wickedwhims.relationships.relationship_settings import get_relationship_setting, RelationshipSetting
from wickedwhims.sex.animations.animations_handler import get_available_sex_animations
from wickedwhims.sex.animations.animations_operator import has_animations_with_params, get_random_animation, get_animations_with_params, ChoiceListRandomAnimationPickerRow
from wickedwhims.sex.dialogs.dialog_utils import get_sex_category_stbl_name, get_sex_category_animations_stbl_name
from wickedwhims.sex.enums.sex_gender import get_sim_sex_gender, SexGenderType
from wickedwhims.sex.enums.sex_type import SexCategoryType
from wickedwhims.sex.sex_operators.general_sex_handlers_operator import clear_sims_sex_extra_data
from wickedwhims.sex.sex_operators.pre_sex_handlers_operator import start_sex_interaction_from_pre_sex_handler
from wickedwhims.sex.sex_privileges import is_sim_allowed_for_animation, display_not_allowed_message
from wickedwhims.sex.utils.sex_init import get_age_limits_for_sex, get_nearby_sims_for_sex
from wickedwhims.utils_interfaces import display_sim_picker_dialog, display_ok_dialog, display_picker_list_dialog, get_arrow_icon


def open_start_sex_sims_picker_dialog(origin_position, pre_sex_handler):

    @exception_watch()
    def sim_picker_callback(dialog):
        if pre_sex_handler is None:
            return False
        if not TurboUIUtil.SimPickerDialog.get_response_result(dialog):
            clear_sims_sex_extra_data(tuple(pre_sex_handler.get_actors_sim_info_gen()))
            return False
        selected_sim_id = TurboUIUtil.SimPickerDialog.get_tag_result(dialog)
        if not selected_sim_id:
            clear_sims_sex_extra_data(tuple(pre_sex_handler.get_actors_sim_info_gen()))
            return False
        selected_sim_info = TurboManagerUtil.Sim.get_sim_info(int(selected_sim_id))
        if selected_sim_info is None:
            clear_sims_sex_extra_data(tuple(pre_sex_handler.get_actors_sim_info_gen()))
            return False
        is_sim_sex_allowed = is_sim_allowed_for_animation(tuple(pre_sex_handler.get_actors_sim_info_gen()) + (selected_sim_info,), pre_sex_handler.get_interaction_type())
        if not is_sim_sex_allowed:
            display_not_allowed_message(is_sim_sex_allowed)
            clear_sims_sex_extra_data(tuple(pre_sex_handler.get_actors_sim_info_gen()))
            return False
        pre_sex_handler.add_sim(selected_sim_id)
        open_start_sex_animations_picker_dialog(pre_sex_handler)
        return True

    creator_sim_info = TurboManagerUtil.Sim.get_sim_info(pre_sex_handler.get_creator_sim_id())
    test_incest_of_sims = () if get_relationship_setting(RelationshipSetting.INCEST_STATE, variable_type=bool) else (creator_sim_info,)
    (min_age_limit, max_age_limit) = get_age_limits_for_sex((creator_sim_info,))
    skip_males = not has_animations_with_params(pre_sex_handler.get_interaction_type(), pre_sex_handler.get_object_identifier(), (get_sim_sex_gender(creator_sim_info), SexGenderType.MALE))
    skip_females = not has_animations_with_params(pre_sex_handler.get_interaction_type(), pre_sex_handler.get_object_identifier(), (get_sim_sex_gender(creator_sim_info), SexGenderType.FEMALE))
    skip_cmales = not has_animations_with_params(pre_sex_handler.get_interaction_type(), pre_sex_handler.get_object_identifier(), (get_sim_sex_gender(creator_sim_info), SexGenderType.CMALE))
    skip_cfemales = not has_animations_with_params(pre_sex_handler.get_interaction_type(), pre_sex_handler.get_object_identifier(), (get_sim_sex_gender(creator_sim_info), SexGenderType.CFEMALE))
    sims_list = list(get_nearby_sims_for_sex(origin_position, radius=16, relative_sims=test_incest_of_sims, min_sims_age=min_age_limit, max_sims_age=max_age_limit, skip_males=skip_males, skip_females=skip_females, skip_cmales=skip_cmales, skip_cfemales=skip_cfemales, skip_sims_ids=(pre_sex_handler.get_creator_sim_id(),)))
    if has_animations_with_params(pre_sex_handler.get_interaction_type(), pre_sex_handler.get_object_identifier(), (get_sim_sex_gender(creator_sim_info),)):
        sims_list.insert(0, pre_sex_handler.get_creator_sim_id())
    if not sims_list:
        display_ok_dialog(text=780195446, text_tokens=(get_sex_category_stbl_name(pre_sex_handler.get_interaction_type()), creator_sim_info), title=get_sex_category_animations_stbl_name(pre_sex_handler.get_interaction_type()))
        clear_sims_sex_extra_data(tuple(pre_sex_handler.get_actors_sim_info_gen()))
        return
    display_sim_picker_dialog(text=906772330, title=get_sex_category_animations_stbl_name(pre_sex_handler.get_interaction_type()), sims_id_list=sims_list, callback=sim_picker_callback)


def open_start_random_sex_sims_picker_dialog(origin_position, pre_sex_handler):

    @exception_watch()
    def random_sex_sim_picker_callback(dialog):
        if pre_sex_handler is None:
            return False
        if not TurboUIUtil.SimPickerDialog.get_response_result(dialog):
            clear_sims_sex_extra_data(tuple(pre_sex_handler.get_actors_sim_info_gen()))
            return False
        picked_sim_id = TurboUIUtil.SimPickerDialog.get_tag_result(dialog)
        if not picked_sim_id:
            clear_sims_sex_extra_data(tuple(pre_sex_handler.get_actors_sim_info_gen()))
            return False
        picked_sim = TurboManagerUtil.Sim.get_sim_info(int(picked_sim_id))
        if picked_sim is None:
            clear_sims_sex_extra_data(tuple(pre_sex_handler.get_actors_sim_info_gen()))
            return False
        pre_sex_handler.add_sim(picked_sim)
        random_animation = get_random_animation(pre_sex_handler.get_object_identifier(), tuple(pre_sex_handler.get_actors_sim_info_gen()))
        if random_animation is None:
            display_ok_dialog(text=2459296019, title=1890248379)
            return False
        pre_sex_handler.set_animation_instance(random_animation)
        start_sex_interaction_from_pre_sex_handler(pre_sex_handler)
        return True

    creator_sim_info = TurboManagerUtil.Sim.get_sim_info(pre_sex_handler.get_creator_sim_id())
    test_incest_of_sims = () if get_relationship_setting(RelationshipSetting.INCEST_STATE, variable_type=bool) else (creator_sim_info,)
    (min_age_limit, max_age_limit) = get_age_limits_for_sex((creator_sim_info,))
    skip_males = True
    skip_females = True
    skip_cmales = True
    skip_cfemales = True
    for sex_category_type in (SexCategoryType.TEASING, SexCategoryType.HANDJOB, SexCategoryType.FOOTJOB, SexCategoryType.ORALJOB, SexCategoryType.VAGINAL, SexCategoryType.ANAL):
        skip_males = not has_animations_with_params(sex_category_type, pre_sex_handler.get_object_identifier(), (get_sim_sex_gender(creator_sim_info), SexGenderType.MALE))
        if skip_males is False:
            break
    for sex_category_type in (SexCategoryType.TEASING, SexCategoryType.HANDJOB, SexCategoryType.FOOTJOB, SexCategoryType.ORALJOB, SexCategoryType.VAGINAL, SexCategoryType.ANAL):
        skip_females = not has_animations_with_params(sex_category_type, pre_sex_handler.get_object_identifier(), (get_sim_sex_gender(creator_sim_info), SexGenderType.FEMALE))
        if skip_females is False:
            break
    for sex_category_type in (SexCategoryType.TEASING, SexCategoryType.HANDJOB, SexCategoryType.FOOTJOB, SexCategoryType.ORALJOB, SexCategoryType.VAGINAL, SexCategoryType.ANAL):
        skip_cmales = not has_animations_with_params(sex_category_type, pre_sex_handler.get_object_identifier(), (get_sim_sex_gender(creator_sim_info), SexGenderType.CMALE))
        if skip_cmales is False:
            break
    for sex_category_type in (SexCategoryType.TEASING, SexCategoryType.HANDJOB, SexCategoryType.FOOTJOB, SexCategoryType.ORALJOB, SexCategoryType.VAGINAL, SexCategoryType.ANAL):
        skip_cfemales = not has_animations_with_params(sex_category_type, pre_sex_handler.get_object_identifier(), (get_sim_sex_gender(creator_sim_info), SexGenderType.CFEMALE))
        if skip_cfemales is False:
            break
    sims_list = list(get_nearby_sims_for_sex(origin_position, radius=16, relative_sims=test_incest_of_sims, min_sims_age=min_age_limit, max_sims_age=max_age_limit, skip_males=skip_males, skip_females=skip_females, skip_cmales=skip_cmales, skip_cfemales=skip_cfemales, skip_sims_ids=(pre_sex_handler.get_creator_sim_id(),)))
    for sex_category_type in (SexCategoryType.HANDJOB, SexCategoryType.ORALJOB, SexCategoryType.TEASING, SexCategoryType.VAGINAL, SexCategoryType.ANAL, SexCategoryType.FOOTJOB):
        if has_animations_with_params(sex_category_type, pre_sex_handler.get_object_identifier(), (get_sim_sex_gender(creator_sim_info),)):
            sims_list.insert(0, pre_sex_handler.get_creator_sim_id())
            break
    if not sims_list:
        display_ok_dialog(text=2459296019, title=1890248379)
        clear_sims_sex_extra_data(tuple(pre_sex_handler.get_actors_sim_info_gen()))
        return
    if len(get_available_sex_animations()) <= 4:
        display_ok_dialog(text=1066517691, title=3113927949)
    display_sim_picker_dialog(text=906772330, title=1890248379, sims_id_list=sims_list, callback=random_sex_sim_picker_callback)


def open_start_sex_animations_category_picker_dialog(pre_sex_handler):

    @exception_watch()
    def animation_categories_picker_callback(dialog):
        if pre_sex_handler is None:
            return False
        if not TurboUIUtil.ObjectPickerDialog.get_response_result(dialog):
            clear_sims_sex_extra_data(tuple(pre_sex_handler.get_actors_sim_info_gen()))
            return False
        result_sex_category_type = TurboUIUtil.ObjectPickerDialog.get_tag_result(dialog)
        pre_sex_handler.set_interaction_type(result_sex_category_type)
        open_start_sex_animations_picker_dialog(pre_sex_handler)
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


def open_start_sex_animations_picker_dialog(pre_sex_handler):

    @exception_watch()
    def animations_picker_callback(dialog):
        if pre_sex_handler is None:
            return False
        if not TurboUIUtil.ObjectPickerDialog.get_response_result(dialog):
            open_start_sex_animations_category_picker_dialog(pre_sex_handler)
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
    if len(animations_rows) > 1:
        animations_rows.insert(0, ChoiceListRandomAnimationPickerRow(pre_sex_handler, pre_sex_handler.get_interaction_type()))
    if len(get_available_sex_animations()) <= 4:
        display_ok_dialog(text=1066517691, title=3113927949)
    display_picker_list_dialog(title=get_sex_category_animations_stbl_name(pre_sex_handler.get_interaction_type()), picker_rows=animations_rows, callback=animations_picker_callback)

