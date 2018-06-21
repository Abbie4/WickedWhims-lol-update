import random
from enums.traits_enum import SimTrait
from turbolib.cas_util import TurboCASUtil
from turbolib.l18n_util import TurboL18NUtil
from turbolib.manager_util import TurboManagerUtil
from turbolib.sim_util import TurboSimUtil
from turbolib.special.custom_exception_watcher import exception_watch
from turbolib.types_util import TurboTypesUtil
from turbolib.ui_util import TurboUIUtil
from turbolib.world_util import TurboWorldUtil
from turbolib.wrappers.interactions import TurboImmediateSuperInteraction, TurboInteractionStartMixin
from wickedwhims.main.cas_config_handler import get_penis_author_keys, get_penis_cas_part, get_soft_penis_picker_rows, get_hard_penis_picker_rows
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.nudity.nudity_settings import NuditySetting, get_nudity_setting
from wickedwhims.sxex_bridge.body import get_sim_body_state, BodyState
from wickedwhims.sxex_bridge.nudity import update_nude_body_data
from wickedwhims.sxex_bridge.outfit import dress_up_outfit
from wickedwhims.sxex_bridge.sex import is_sim_going_to_sex, is_sim_in_sex
from wickedwhims.utils_cas import set_bodytype_caspart
from wickedwhims.utils_interfaces import get_arrow_icon, get_selected_icon, get_unselected_icon, display_picker_list_dialog
from wickedwhims.utils_saves.save_basics import update_basic_save_data, get_basic_save_data
from wickedwhims.utils_traits import has_sim_trait
from cnutils.CNSimUtils import CNSimUtils
PENIS_SETTING_SOFT_PENIS_AUTHOR = 'Penis_Default'
PENIS_SETTING_HARD_PENIS_AUTHOR = 'Penis_Default'
PENIS_SETTING_RANDOM = False
PENIS_SETTING_RANDOM_INCLUDE_DEFAULT = True

def get_sim_soft_penis_author_key(sim_identifier):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    sim_is_child = TurboSimUtil.Age.get_age(sim_info) == TurboSimUtil.Age.CHILD
    penis_outfit_author = sim_ev(sim_info).outfit_soft_penis_author
    if not penis_outfit_author:
        if sim_is_child:
            penis_outfit_author = 'PENIS_lillithv2soft'
        else:
            if is_default_penis_random():
                penis_author_keys = get_penis_author_keys(include_default_author_key=is_default_penis_allowed_for_random())
                if len(penis_author_keys) > 0:
                    penis_outfit_author = random.choice(penis_author_keys)
                else:
                    penis_outfit_author = get_default_soft_penis_setting()
            else:
                penis_outfit_author = get_default_soft_penis_setting()
        sim_ev(sim_info).outfit_soft_penis_author = penis_outfit_author
    return penis_outfit_author


def get_penis_soft_cas_id(sim_identifier):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    sim_is_child = TurboSimUtil.Age.get_age(sim_info) == TurboSimUtil.Age.CHILD
    penis_outfit_author = get_sim_soft_penis_author_key(sim_info)
    if sim_is_child:
        penis_cas_part = get_penis_cas_part(penis_outfit_author, 'PENIS_SOFT_CAS_PART_ID_CHILD', sim_is_child)
    else:
        if TurboSimUtil.Gender.is_male(sim_info):
            if TurboSimUtil.Gender.is_male_frame(sim_info):
                penis_cas_part = get_penis_cas_part(penis_outfit_author, 'PENIS_SOFT_CAS_PART_ID_MMF')
            else:
                penis_cas_part = get_penis_cas_part(penis_outfit_author, 'PENIS_SOFT_CAS_PART_ID_MFF')
        elif TurboSimUtil.Gender.is_male_frame(sim_info):
            penis_cas_part = get_penis_cas_part(penis_outfit_author, 'PENIS_SOFT_CAS_PART_ID_FMF')
        else:
            penis_cas_part = get_penis_cas_part(penis_outfit_author, 'PENIS_SOFT_CAS_PART_ID_FFF')
    return penis_cas_part


def get_penis_soft_texture_cas_id(sim_identifier):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    sim_is_child = TurboSimUtil.Age.get_age(sim_info) == TurboSimUtil.Age.CHILD
    penis_outfit_author = get_sim_soft_penis_author_key(sim_info)
    if sim_is_child:
        penis_cas_texture = get_penis_cas_part(penis_outfit_author, 'PENIS_SOFT_CAS_TEXTURE_ID_CHILD')
    else:
        if TurboSimUtil.Gender.is_male(sim_info):
            if TurboSimUtil.Gender.is_male_frame(sim_info):
                penis_cas_texture = get_penis_cas_part(penis_outfit_author, 'PENIS_SOFT_CAS_TEXTURE_ID_MMF', exclude_default=True)
            else:
                penis_cas_texture = get_penis_cas_part(penis_outfit_author, 'PENIS_SOFT_CAS_TEXTURE_ID_MFF', exclude_default=True)
        elif TurboSimUtil.Gender.is_male_frame(sim_info):
            penis_cas_texture = get_penis_cas_part(penis_outfit_author, 'PENIS_SOFT_CAS_TEXTURE_ID_FMF', exclude_default=True)
        else:
            penis_cas_texture = get_penis_cas_part(penis_outfit_author, 'PENIS_SOFT_CAS_TEXTURE_ID_FFF', exclude_default=True)
    return penis_cas_texture


def get_sim_hard_penis_author_key(sim_identifier):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    sim_is_child = TurboSimUtil.Age.get_age(sim_info) == TurboSimUtil.Age.CHILD
    penis_outfit_author = sim_ev(sim_info).outfit_hard_penis_author
    if not penis_outfit_author:
        if sim_is_child:
            penis_outfit_author = 'PENIS_lillithv2'
        else:
            if is_default_penis_random():
                penis_author_keys = get_penis_author_keys(include_default_author_key=is_default_penis_allowed_for_random())
                if len(penis_author_keys) > 0:
                    penis_outfit_author = random.choice(penis_author_keys)
                else:
                    penis_outfit_author = get_default_hard_penis_setting()
            else:
                penis_outfit_author = get_default_hard_penis_setting()
        sim_ev(sim_info).outfit_hard_penis_author = penis_outfit_author
    return penis_outfit_author


def get_penis_hard_cas_id(sim_identifier):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    sim_is_child = TurboSimUtil.Age.get_age(sim_info) == TurboSimUtil.Age.CHILD
    penis_outfit_author = get_sim_hard_penis_author_key(sim_info)
    if sim_is_child:
        penis_cas_part = get_penis_cas_part(penis_outfit_author, 'PENIS_HARD_CAS_PART_ID_CHILD')
    else:
        if TurboSimUtil.Gender.is_male(sim_info):
            if TurboSimUtil.Gender.is_male_frame(sim_info):
                penis_cas_part = get_penis_cas_part(penis_outfit_author, 'PENIS_HARD_CAS_PART_ID_MMF')
            else:
                penis_cas_part = get_penis_cas_part(penis_outfit_author, 'PENIS_HARD_CAS_PART_ID_MFF')
        elif TurboSimUtil.Gender.is_male_frame(sim_info):
            penis_cas_part = get_penis_cas_part(penis_outfit_author, 'PENIS_HARD_CAS_PART_ID_FMF')
        else:
            penis_cas_part = get_penis_cas_part(penis_outfit_author, 'PENIS_HARD_CAS_PART_ID_FFF')
    return penis_cas_part


def get_penis_hard_texture_cas_id(sim_identifier):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    sim_is_child = TurboSimUtil.Age.get_age(sim_info) == TurboSimUtil.Age.CHILD
    penis_outfit_author = get_sim_hard_penis_author_key(sim_info)
    if sim_is_child:
        penis_cas_texture = get_penis_cas_part(penis_outfit_author, 'PENIS_HARD_CAS_TEXTURE_ID_CHILD')
    else:
        if TurboSimUtil.Gender.is_male(sim_info):
            if TurboSimUtil.Gender.is_male_frame(sim_info):
                penis_cas_texture = get_penis_cas_part(penis_outfit_author, 'PENIS_HARD_CAS_TEXTURE_ID_MMF', exclude_default=True)
            else:
                penis_cas_texture = get_penis_cas_part(penis_outfit_author, 'PENIS_HARD_CAS_TEXTURE_ID_MFF', exclude_default=True)
        elif TurboSimUtil.Gender.is_male_frame(sim_info):
            penis_cas_texture = get_penis_cas_part(penis_outfit_author, 'PENIS_HARD_CAS_TEXTURE_ID_FMF', exclude_default=True)
        else:
            penis_cas_texture = get_penis_cas_part(penis_outfit_author, 'PENIS_HARD_CAS_TEXTURE_ID_FFF', exclude_default=True)
    return penis_cas_texture


def _get_sim_soft_penis_type(sim_identifier):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    sim_is_child = TurboSimUtil.Age.get_age(sim_info) == TurboSimUtil.Age.CHILD
    if sim_is_child:
        return 'PENIS_SOFT_CAS_PART_ID_CHILD'
    else:
        if TurboSimUtil.Gender.is_male(sim_info):
            if TurboSimUtil.Gender.is_male_frame(sim_info):
                return 'PENIS_SOFT_CAS_PART_ID_MMF'
            return 'PENIS_SOFT_CAS_PART_ID_MFF'
        else:
            if TurboSimUtil.Gender.is_male_frame(sim_info):
                return 'PENIS_SOFT_CAS_PART_ID_FMF'
            return 'PENIS_SOFT_CAS_PART_ID_FFF'


def _get_sim_hard_penis_type(sim_identifier):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    sim_is_child = TurboSimUtil.Age.get_age(sim_info) == TurboSimUtil.Age.CHILD
    if sim_is_child:
        return 'PENIS_HARD_CAS_PART_ID_CHILD'
    else:
        if TurboSimUtil.Gender.is_male(sim_info):
            if TurboSimUtil.Gender.is_male_frame(sim_info):
                return 'PENIS_HARD_CAS_PART_ID_MMF'
            return 'PENIS_HARD_CAS_PART_ID_MFF'
        else:
            if TurboSimUtil.Gender.is_male_frame(sim_info):
                return 'PENIS_HARD_CAS_PART_ID_FMF'
            return 'PENIS_HARD_CAS_PART_ID_FFF'


def update_sim_penis_state(sim_identifier):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    if sim_ev(sim_info).is_penis_hard is True:
        cooldown_count = sim_ev(sim_info).penis_hard_cooldown
        if cooldown_count > 0:
            cooldown_count -= 1
        sim_ev(sim_info).penis_hard_cooldown = cooldown_count
        if cooldown_count <= 0:
            set_sim_penis_state(sim_info, False, 0, set_if_nude=True)


def set_sim_penis_state(sim_identifier, is_hard, length, set_if_nude=False, force=False):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    if not has_sim_trait(sim_info, SimTrait.GENDEROPTIONS_TOILET_STANDING):
        return
    has_to_update_state = sim_ev(sim_info).is_penis_hard != is_hard or force is True
    sim_ev(sim_info).is_penis_hard = is_hard
    sim_ev(sim_info).penis_hard_cooldown = length
    if has_to_update_state is True:
        update_nude_body_data(sim_info, force_update=True)
        current_outfit = TurboSimUtil.CAS.get_current_outfit(sim_info)
        if set_if_nude is True and (current_outfit[0] == TurboCASUtil.OutfitCategory.SPECIAL and current_outfit[1] == 0 or current_outfit[0] == TurboCASUtil.OutfitCategory.BATHING):
            bottom_body_state = get_sim_body_state(sim_info, TurboCASUtil.BodyType.LOWER_BODY)
            if bottom_body_state == BodyState.NUDE:
                set_bodytype_caspart(sim_info, (TurboCASUtil.OutfitCategory.SPECIAL, 0), TurboCASUtil.BodyType.LOWER_BODY, sim_ev(sim_info).nude_outfit_parts[7])
                update_sim_penis_texture(sim_info)
                try:
                    TurboSimUtil.CAS.refresh_outfit(sim_info)
                except:
                    pass


def update_sim_penis_texture(sim_identifier, outfit_category_and_index=None):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    if not has_sim_trait(sim_info, SimTrait.GENDEROPTIONS_TOILET_STANDING):
        return
    current_outfit = outfit_category_and_index if outfit_category_and_index is not None else TurboSimUtil.CAS.get_current_outfit(sim_info)
    is_nude_outfit = current_outfit[0] == TurboCASUtil.OutfitCategory.SPECIAL and current_outfit[1] == 0 or current_outfit[0] == TurboCASUtil.OutfitCategory.BATHING
    if is_nude_outfit is False:
        return
    sim_penis_texture_cas_id = sim_ev(sim_info).nude_outfit_parts[115]
    if sim_penis_texture_cas_id != -1:
        set_bodytype_caspart(sim_info, current_outfit, 115, sim_ev(sim_info).nude_outfit_parts[115])
    else:
        set_bodytype_caspart(sim_info, (TurboCASUtil.OutfitCategory.SPECIAL, 0), 115, -1, remove=True)


class PenisSettingsInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'PenisSettingsInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        if not TurboTypesUtil.Sims.is_sim(interaction_target):
            return False
        if TurboSimUtil.Age.is_younger_than(interaction_target, TurboSimUtil.Age.CHILD):
            return False
        if CNSimUtils.can_have_sex(interaction_target):
            return False
        if is_sim_in_sex(cls.get_interaction_sim(interaction_context)) or is_sim_going_to_sex(cls.get_interaction_sim(interaction_context)):
            return False
        if is_sim_in_sex(interaction_target) or is_sim_going_to_sex(interaction_target):
            return False
        if not has_sim_trait(interaction_target, SimTrait.GENDEROPTIONS_TOILET_STANDING):
            return False
        return True

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        TurboWorldUtil.Time.set_current_time_speed(TurboWorldUtil.Time.ClockSpeedMode.PAUSED)
        open_penis_settings(cls.get_interaction_target(interaction_instance))
        return True


def open_penis_settings(sim_identifier):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    sim_soft_penis = TurboUIUtil.ObjectPickerDialog.ListPickerRow(10, TurboL18NUtil.get_localized_string(2898758693), TurboL18NUtil.get_localized_string(0), icon=get_arrow_icon())
    sim_hard_penis = TurboUIUtil.ObjectPickerDialog.ListPickerRow(11, TurboL18NUtil.get_localized_string(1072923186), TurboL18NUtil.get_localized_string(0), icon=get_arrow_icon())
    all_sims_soft_penis = TurboUIUtil.ObjectPickerDialog.ListPickerRow(20, TurboL18NUtil.get_localized_string(2966523311), TurboL18NUtil.get_localized_string(0), icon=get_arrow_icon())
    all_sims_hard_penis = TurboUIUtil.ObjectPickerDialog.ListPickerRow(21, TurboL18NUtil.get_localized_string(4002037116), TurboL18NUtil.get_localized_string(0), icon=get_arrow_icon())
    randomize_all_sims_penis = TurboUIUtil.ObjectPickerDialog.ListPickerRow(30, TurboL18NUtil.get_localized_string(1952075710), TurboL18NUtil.get_localized_string(0), icon=get_selected_icon() if PENIS_SETTING_RANDOM is True and PENIS_SETTING_RANDOM_INCLUDE_DEFAULT is True else get_unselected_icon())
    randomize_all_sims_penis_non_default = TurboUIUtil.ObjectPickerDialog.ListPickerRow(31, TurboL18NUtil.get_localized_string(1952075710), TurboL18NUtil.get_localized_string(1490222904), icon=get_selected_icon() if PENIS_SETTING_RANDOM is True and PENIS_SETTING_RANDOM_INCLUDE_DEFAULT is False else get_unselected_icon())

    @exception_watch()
    def set_callback(dialog):
        if not dialog.accepted:
            return
        result = dialog.get_result_tags()[-1]
        if result == 10:
            open_sim_soft_penis_picker(sim_info)
        elif result == 11:
            open_sim_hard_penis_picker(sim_info)
        elif result == 20:
            open_all_sims_soft_penis_picker(sim_info)
        elif result == 21:
            open_all_sims_hard_penis_picker(sim_info)
        elif result == 30:
            randomized_all_sims_penis_models(sim_info, include_default_penis=True)
        elif result == 31:
            randomized_all_sims_penis_models(sim_info)

    display_picker_list_dialog(title=253781263, picker_rows=[sim_soft_penis, sim_hard_penis, all_sims_soft_penis, all_sims_hard_penis, randomize_all_sims_penis, randomize_all_sims_penis_non_default], callback=set_callback)


def open_sim_soft_penis_picker(sim_identifier):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)

    @exception_watch()
    def set_callback(dialog):
        global PENIS_SETTING_RANDOM, PENIS_SETTING_RANDOM_INCLUDE_DEFAULT
        if not dialog.accepted:
            open_penis_settings(sim_info)
            return
        penis_author = dialog.get_result_tags()[-1]
        PENIS_SETTING_RANDOM = False
        PENIS_SETTING_RANDOM_INCLUDE_DEFAULT = True
        update_basic_save_data(get_basic_penis_save_data())
        sim_ev(sim_info).outfit_soft_penis_author = penis_author
        dress_up_outfit(sim_info)
        set_sim_penis_state(sim_info, False, 0)
        update_nude_body_data(sim_info, force_update=True)
        open_sim_soft_penis_picker(sim_info)

    soft_penis_picker_rows = get_soft_penis_picker_rows(selected_part=get_sim_soft_penis_author_key(sim_info), specific_part_type=_get_sim_soft_penis_type(sim_info))
    display_picker_list_dialog(title=277158998, picker_rows=soft_penis_picker_rows, callback=set_callback)


def open_sim_hard_penis_picker(sim_identifier):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)

    @exception_watch()
    def set_callback(dialog):
        global PENIS_SETTING_RANDOM, PENIS_SETTING_RANDOM_INCLUDE_DEFAULT
        if not dialog.accepted:
            open_penis_settings(sim_info)
            return
        penis_author = dialog.get_result_tags()[-1]
        PENIS_SETTING_RANDOM = False
        PENIS_SETTING_RANDOM_INCLUDE_DEFAULT = True
        update_basic_save_data(get_basic_penis_save_data())
        sim_ev(sim_info).outfit_hard_penis_author = penis_author
        dress_up_outfit(sim_info)
        set_sim_penis_state(sim_info, False, 0)
        update_nude_body_data(sim_info, force_update=True)
        open_sim_hard_penis_picker(sim_info)

    hard_penis_picker_rows = get_hard_penis_picker_rows(selected_part=get_sim_hard_penis_author_key(sim_info), specific_part_type=_get_sim_hard_penis_type(sim_info))
    display_picker_list_dialog(title=1516569631, picker_rows=hard_penis_picker_rows, callback=set_callback)


def open_all_sims_soft_penis_picker(sim_identifier):
    creator_sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)

    @exception_watch()
    def set_callback(dialog):
        global PENIS_SETTING_SOFT_PENIS_AUTHOR, PENIS_SETTING_RANDOM, PENIS_SETTING_RANDOM_INCLUDE_DEFAULT
        if not dialog.accepted:
            open_penis_settings(creator_sim_info)
            return
        penis_author = dialog.get_result_tags()[-1]
        PENIS_SETTING_SOFT_PENIS_AUTHOR = penis_author
        PENIS_SETTING_RANDOM = False
        PENIS_SETTING_RANDOM_INCLUDE_DEFAULT = True
        update_basic_save_data(get_basic_penis_save_data())
        for sim_info in TurboManagerUtil.Sim.get_all_sim_info_gen(humans=True, pets=False):
            if sim_info is None:
                continue
            sim_ev(sim_info).outfit_soft_penis_author = penis_author
            dress_up_outfit(sim_info)
            set_sim_penis_state(sim_info, False, 0)
            update_nude_body_data(sim_info, force_update=True)
        open_all_sims_soft_penis_picker(creator_sim_info)

    soft_penis_picker_rows = get_soft_penis_picker_rows(selected_part=PENIS_SETTING_SOFT_PENIS_AUTHOR)
    display_picker_list_dialog(title=277158998, picker_rows=soft_penis_picker_rows, callback=set_callback)


def open_all_sims_hard_penis_picker(sim_identifier):
    creator_sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)

    @exception_watch()
    def set_callback(dialog):
        global PENIS_SETTING_HARD_PENIS_AUTHOR, PENIS_SETTING_RANDOM, PENIS_SETTING_RANDOM_INCLUDE_DEFAULT
        if not dialog.accepted:
            open_penis_settings(creator_sim_info)
            return
        penis_author = dialog.get_result_tags()[-1]
        PENIS_SETTING_HARD_PENIS_AUTHOR = penis_author
        PENIS_SETTING_RANDOM = False
        PENIS_SETTING_RANDOM_INCLUDE_DEFAULT = True
        update_basic_save_data(get_basic_penis_save_data())
        for sim_info in TurboManagerUtil.Sim.get_all_sim_info_gen(humans=True, pets=False):
            if sim_info is None:
                continue
            sim_ev(sim_info).outfit_hard_penis_author = penis_author
            dress_up_outfit(sim_info)
            set_sim_penis_state(sim_info, False, 0)
            update_nude_body_data(sim_info, force_update=True)
        open_all_sims_hard_penis_picker(creator_sim_info)

    hard_penis_picker_rows = get_hard_penis_picker_rows(selected_part=PENIS_SETTING_HARD_PENIS_AUTHOR)
    display_picker_list_dialog(title=1516569631, picker_rows=hard_penis_picker_rows, callback=set_callback)


def randomized_all_sims_penis_models(sim_identifier, include_default_penis=False):
    global PENIS_SETTING_RANDOM, PENIS_SETTING_RANDOM_INCLUDE_DEFAULT
    creator_sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    PENIS_SETTING_RANDOM = True
    PENIS_SETTING_RANDOM_INCLUDE_DEFAULT = include_default_penis
    update_basic_save_data(get_basic_penis_save_data())
    penis_author_keys = get_penis_author_keys(include_default_author_key=include_default_penis)
    if len(penis_author_keys) == 0:
        open_penis_settings(creator_sim_info)
        return
    for sim_info in TurboManagerUtil.Sim.get_all_sim_info_gen(humans=True, pets=False):
        if sim_info is None:
            continue
        random_penis_author = random.choice(penis_author_keys)
        sim_ev(sim_info).outfit_soft_penis_author = random_penis_author
        sim_ev(sim_info).outfit_hard_penis_author = random_penis_author
        dress_up_outfit(sim_info)
        set_sim_penis_state(sim_info, False, 0)
        update_nude_body_data(sim_info, force_update=True)
    open_penis_settings(creator_sim_info)


def get_basic_penis_save_data():
    general_dict = dict()
    penis_dict = dict()
    penis_dict['default_soft_penis_author'] = str(PENIS_SETTING_SOFT_PENIS_AUTHOR)
    penis_dict['default_hard_penis_author'] = str(PENIS_SETTING_HARD_PENIS_AUTHOR)
    penis_dict['random_penis_flag'] = int(PENIS_SETTING_RANDOM)
    penis_dict['random_penis_include_default_flag'] = int(PENIS_SETTING_RANDOM_INCLUDE_DEFAULT)
    general_dict['penis_data'] = penis_dict
    return general_dict


def apply_basic_penis_save_data():
    global PENIS_SETTING_SOFT_PENIS_AUTHOR, PENIS_SETTING_HARD_PENIS_AUTHOR, PENIS_SETTING_RANDOM, PENIS_SETTING_RANDOM_INCLUDE_DEFAULT
    basic_save_data = get_basic_save_data()
    if 'penis_data' in basic_save_data:
        penis_dict = basic_save_data['penis_data']
        PENIS_SETTING_SOFT_PENIS_AUTHOR = str(penis_dict.get('default_soft_penis_author', PENIS_SETTING_SOFT_PENIS_AUTHOR))
        PENIS_SETTING_HARD_PENIS_AUTHOR = str(penis_dict.get('default_hard_penis_author', PENIS_SETTING_HARD_PENIS_AUTHOR))
        PENIS_SETTING_RANDOM = bool(penis_dict.get('random_penis_flag', PENIS_SETTING_RANDOM))
        PENIS_SETTING_RANDOM_INCLUDE_DEFAULT = bool(penis_dict.get('random_penis_include_default_flag', PENIS_SETTING_RANDOM_INCLUDE_DEFAULT))
    update_basic_save_data(get_basic_penis_save_data())


def get_default_soft_penis_setting():
    return PENIS_SETTING_SOFT_PENIS_AUTHOR


def get_default_hard_penis_setting():
    return PENIS_SETTING_HARD_PENIS_AUTHOR


def is_default_penis_random():
    return PENIS_SETTING_RANDOM


def is_default_penis_allowed_for_random():
    return PENIS_SETTING_RANDOM_INCLUDE_DEFAULT


def reset_penis_data():
    global PENIS_SETTING_SOFT_PENIS_AUTHOR, PENIS_SETTING_HARD_PENIS_AUTHOR, PENIS_SETTING_RANDOM, PENIS_SETTING_RANDOM_INCLUDE_DEFAULT
    PENIS_SETTING_SOFT_PENIS_AUTHOR = 'Penis_Default'
    PENIS_SETTING_HARD_PENIS_AUTHOR = 'Penis_Default'
    PENIS_SETTING_RANDOM = False
    PENIS_SETTING_RANDOM_INCLUDE_DEFAULT = True
    update_basic_save_data(get_basic_penis_save_data())

