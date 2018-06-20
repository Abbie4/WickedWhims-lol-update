from enums.traits_enum import SimTrait
from turbolib.cas_util import TurboCASUtil
from turbolib.manager_util import TurboManagerUtil
from turbolib.sim_util import TurboSimUtil
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.utils_cas import get_sim_outfit_cas_part_from_bodytype
from wickedwhims.utils_traits import has_sim_trait

def setup_sim_nude_outfit(sim_info):
    if TurboSimUtil.CAS.get_current_outfit(sim_info)[0] != TurboCASUtil.OutfitCategory.BATHING:
        reset_sim_bathing_outfits(sim_info)
    update_nude_body_data(sim_info, force_update=True)


def update_nude_body_data(sim_identifier, force_update=False):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    if TurboSimUtil.Age.is_younger_than(sim_info, TurboSimUtil.Age.CHILD):
        return
    if has_sim_trait(sim_info, SimTrait.GENDEROPTIONS_TOILET_STANDING):
        from wickedwhims.sxex_bridge.penis import get_penis_soft_cas_id, get_penis_soft_texture_cas_id, get_penis_hard_cas_id, get_penis_hard_texture_cas_id
        sim_ev(sim_info).penis_outfit_parts['soft'] = get_penis_soft_cas_id(sim_info)
        sim_ev(sim_info).penis_outfit_parts['soft_texture'] = get_penis_soft_texture_cas_id(sim_info)
        sim_ev(sim_info).penis_outfit_parts['hard'] = get_penis_hard_cas_id(sim_info)
        sim_ev(sim_info).penis_outfit_parts['hard_texture'] = get_penis_hard_texture_cas_id(sim_info)
    from wickedwhims.nudity.nudity_settings import NuditySetting, get_nudity_setting
    if sim_ev(sim_info).nude_outfit_parts[TurboCASUtil.BodyType.UPPER_BODY] == -1 or force_update is True:
        if get_nudity_setting(NuditySetting.NUDITY_ASSURANCE_STATE, variable_type=bool):
            top_body_part_cas_id = get_default_nude_cas_part_id(sim_info, TurboCASUtil.BodyType.UPPER_BODY)
        else:
            top_body_part_cas_id = get_sim_outfit_cas_part_from_bodytype(sim_info, TurboCASUtil.BodyType.UPPER_BODY, outfit_category_and_index=(TurboCASUtil.OutfitCategory.BATHING, 0))
        sim_ev(sim_info).nude_outfit_parts[TurboCASUtil.BodyType.UPPER_BODY] = top_body_part_cas_id
    if sim_ev(sim_info).nude_outfit_parts[TurboCASUtil.BodyType.LOWER_BODY] == -1 or force_update is True:
        if has_sim_trait(sim_info, SimTrait.GENDEROPTIONS_TOILET_STANDING):
            sim_ev(sim_info).nude_outfit_parts[TurboCASUtil.BodyType.LOWER_BODY] = sim_ev(sim_info).penis_outfit_parts['hard'] if sim_ev(sim_info).is_penis_hard is True else sim_ev(sim_info).penis_outfit_parts['soft']
        else:
            if get_nudity_setting(NuditySetting.NUDITY_ASSURANCE_STATE, variable_type=bool):
                bottom_body_part_cas_id = get_default_nude_cas_part_id(sim_info, TurboCASUtil.BodyType.LOWER_BODY)
            else:
                bottom_body_part_cas_id = get_sim_outfit_cas_part_from_bodytype(sim_info, TurboCASUtil.BodyType.LOWER_BODY, outfit_category_and_index=(TurboCASUtil.OutfitCategory.BATHING, 0))
            sim_ev(sim_info).nude_outfit_parts[TurboCASUtil.BodyType.LOWER_BODY] = bottom_body_part_cas_id
    if sim_ev(sim_info).nude_outfit_parts[TurboCASUtil.BodyType.SHOES] == -1 or force_update is True:
        if get_nudity_setting(NuditySetting.NUDITY_ASSURANCE_STATE, variable_type=bool):
            feet_body_part_cas_id = get_default_nude_cas_part_id(sim_info, TurboCASUtil.BodyType.SHOES)
        else:
            feet_body_part_cas_id = get_sim_outfit_cas_part_from_bodytype(sim_info, TurboCASUtil.BodyType.SHOES, outfit_category_and_index=(TurboCASUtil.OutfitCategory.BATHING, 0))
        sim_ev(sim_info).nude_outfit_parts[TurboCASUtil.BodyType.SHOES] = feet_body_part_cas_id
    if (sim_ev(sim_info).nude_outfit_parts[115] == -1 or force_update is True) and has_sim_trait(sim_info, SimTrait.GENDEROPTIONS_TOILET_STANDING):
        sim_ev(sim_info).nude_outfit_parts[115] = sim_ev(sim_info).penis_outfit_parts['hard_texture'] if sim_ev(sim_info).is_penis_hard is True else sim_ev(sim_info).penis_outfit_parts['soft_texture']


def reset_sim_bathing_outfits(sim_identifier, ignore_nudity_assurance_setting=False):
    from wickedwhims.nudity.nudity_settings import get_nudity_setting, NuditySetting
    if ignore_nudity_assurance_setting is False and not get_nudity_setting(NuditySetting.NUDITY_ASSURANCE_STATE, variable_type=bool):
        return
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier, allow_base_wrapper=True)
    for occult_sim_info in TurboSimUtil.Occult.get_all_sim_info_occults(sim_info):
        _generate_sim_nude_outfit(occult_sim_info, sim_info)


def _generate_sim_nude_outfit(sim_identifier, data_holder_sim_info, nude_outfit_assurance=True):
    TurboSimUtil.CAS.generate_outfit(sim_identifier, (TurboCASUtil.OutfitCategory.BATHING, 0))
    try:
        outfit_editor = TurboCASUtil.OutfitEditor(sim_identifier, outfit_category_and_index=(TurboCASUtil.OutfitCategory.BATHING, 0))
    except RuntimeError:
        return False
    if nude_outfit_assurance is True and TurboSimUtil.Age.is_older_than(sim_identifier, TurboSimUtil.Age.CHILD, or_equal=True):
        for bodytype in (TurboCASUtil.BodyType.UPPER_BODY, TurboCASUtil.BodyType.LOWER_BODY, TurboCASUtil.BodyType.SHOES):
            outfit_editor.add_cas_part(bodytype, get_default_nude_cas_part_id(sim_identifier, bodytype))
        if has_sim_trait(sim_identifier, SimTrait.GENDEROPTIONS_TOILET_STANDING) and sim_ev(data_holder_sim_info).nude_outfit_parts[TurboCASUtil.BodyType.LOWER_BODY] != -1:
            outfit_editor.add_cas_part(TurboCASUtil.BodyType.LOWER_BODY, sim_ev(data_holder_sim_info).nude_outfit_parts[TurboCASUtil.BodyType.LOWER_BODY])
        for bodytype in (TurboCASUtil.BodyType.FULL_BODY, TurboCASUtil.BodyType.HAT, TurboCASUtil.BodyType.CUMMERBUND, TurboCASUtil.BodyType.EARRINGS, TurboCASUtil.BodyType.GLASSES, TurboCASUtil.BodyType.NECKLACE, TurboCASUtil.BodyType.GLOVES, TurboCASUtil.BodyType.WRIST_LEFT, TurboCASUtil.BodyType.WRIST_RIGHT, TurboCASUtil.BodyType.SOCKS, TurboCASUtil.BodyType.TIGHTS):
            outfit_editor.remove_body_type(bodytype)
    outfit_editor.apply(skip_client_update=True)
    return True


def get_default_nude_cas_part_id(sim_identifier, bodytype):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    if sim_info is None:
        sim_info = TurboManagerUtil.Sim.get_active_sim()
    sim_is_child = TurboSimUtil.Age.get_age(sim_info) is TurboSimUtil.Age.CHILD
    if sim_is_child:
        if bodytype == TurboCASUtil.BodyType.UPPER_BODY:
            if TurboSimUtil.Gender.is_male(sim_identifier):
                return 22069
            else:
                return 62394
        if bodytype == TurboCASUtil.BodyType.LOWER_BODY:
            if TurboSimUtil.Gender.is_male(sim_identifier):
                return 11128915431855097336
            else:
                return 22074
        if bodytype == TurboCASUtil.BodyType.SHOES:
            return 22018
        return -1
    if bodytype == TurboCASUtil.BodyType.UPPER_BODY:
        return 6562
    if bodytype == TurboCASUtil.BodyType.LOWER_BODY:
        return 6574
    if TurboSimUtil.Gender.is_male(sim_identifier) and bodytype == TurboCASUtil.BodyType.SHOES:
        return 6563
    if bodytype == TurboCASUtil.BodyType.UPPER_BODY:
        return 6540
    if bodytype == TurboCASUtil.BodyType.LOWER_BODY:
        return 6544
    if TurboSimUtil.Gender.is_female(sim_identifier) and bodytype == TurboCASUtil.BodyType.SHOES:
        return 6543
    return -1

