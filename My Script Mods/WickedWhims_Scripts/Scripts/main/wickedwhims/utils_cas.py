from turbolib.cas_util import TurboCASUtil
from turbolib.club_util import TurboClubUtil
from turbolib.manager_util import TurboManagerUtil
from turbolib.sim_util import TurboSimUtil
from wickedwhims.main.sim_ev_handler import sim_ev

def get_modified_outfit(sim_identifier, override_category_and_index=None):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier, allow_base_wrapper=True)
    if is_sim_in_special_outfit(sim_info):
        if sim_ev(sim_info).original_outfit_category == -1:
            if override_category_and_index is None:
                outfit_category_and_index = (TurboCASUtil.OutfitCategory.SPECIAL, 0)
            else:
                outfit_category_and_index = (TurboCASUtil.OutfitCategory.get_outfit_category(override_category_and_index[0]), int(override_category_and_index[1]))
                outfit_category_and_index = (TurboCASUtil.OutfitCategory.get_outfit_category(sim_ev(sim_info).original_outfit_category), int(sim_ev(sim_info).original_outfit_index))
        else:
            outfit_category_and_index = (TurboCASUtil.OutfitCategory.get_outfit_category(sim_ev(sim_info).original_outfit_category), int(sim_ev(sim_info).original_outfit_index))
    else:
        outfit_category_and_index = (TurboCASUtil.OutfitCategory.get_outfit_category(sim_ev(sim_info).current_outfit_category), int(sim_ev(sim_info).current_outfit_index))
    if outfit_category_and_index is None or outfit_category_and_index[0] == TurboCASUtil.OutfitCategory.SPECIAL and outfit_category_and_index[1] == 0 or outfit_category_and_index[0] == TurboCASUtil.OutfitCategory.CURRENT_OUTFIT:
        outfit_category_and_index = (TurboCASUtil.OutfitCategory.EVERYDAY, 0)
    return outfit_category_and_index


def get_previous_modified_outfit(sim_identifier):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier, allow_base_wrapper=True)
    if sim_ev(sim_info).previous_outfit_category == -1 or sim_ev(sim_info).previous_outfit_index == -1:
        return (TurboCASUtil.OutfitCategory.EVERYDAY, 0)
    return (TurboCASUtil.OutfitCategory.get_outfit_category(sim_ev(sim_info).previous_outfit_category), int(sim_ev(sim_info).previous_outfit_index))


def copy_outfit_to_special(sim_identifier, set_special_outfit=False, outfit_category_and_index=None, override_outfit_parts=None, save_original=True):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier, allow_base_wrapper=True)
    current_outfit_category_and_index = get_modified_outfit(sim_info)
    if not TurboSimUtil.CAS.has_outfit(sim_info, (TurboCASUtil.OutfitCategory.SPECIAL, 0)):
        TurboSimUtil.CAS.generate_outfit(sim_info, (TurboCASUtil.OutfitCategory.SPECIAL, 0))
    current_outfit = outfit_category_and_index if outfit_category_and_index is not None else (TurboCASUtil.OutfitCategory.get_outfit_category(sim_ev(sim_info).current_outfit_category), int(sim_ev(sim_info).current_outfit_index))
    outfit_body_parts = sim_ev(sim_info).outfit_parts_cache if outfit_category_and_index is None else None
    (club, club_gathering) = TurboClubUtil.get_sim_club_gathering(sim_info)
    if club is not None and club_gathering is not None:
        set_special_outfit = True
        if current_outfit[0] == TurboCASUtil.OutfitCategory.BATHING:
            outfit_body_parts = None
        TurboCASUtil.Club.remove_sim_apprearance_modifiers(sim_info, club_gathering)
    try:
        outfit_editor = TurboCASUtil.OutfitEditor(sim_identifier, outfit_category_and_index=current_outfit, outfit_body_parts=outfit_body_parts)
    except RuntimeError:
        return False
    if override_outfit_parts:
        for (bodytype, cas_part) in override_outfit_parts.items():
            bodytype = int(bodytype)
            cas_part = int(cas_part)
            while not bodytype == -1:
                if cas_part == -1:
                    pass
                if cas_part == 0:
                    outfit_editor.remove_body_type(bodytype)
                else:
                    outfit_editor.add_cas_part(bodytype, cas_part)
    outfit_editor.apply(apply_to_outfit_category=TurboCASUtil.OutfitCategory.SPECIAL)
    if save_original is True:
        sim_ev(sim_info).has_original_outfit_modifications = True
        sim_ev(sim_info).original_outfit_category = int(current_outfit_category_and_index[0])
        sim_ev(sim_info).original_outfit_index = int(current_outfit_category_and_index[1])
    if set_special_outfit is True:
        sim_ev(sim_info).is_outfit_update_locked = True
        TurboSimUtil.CAS.set_current_outfit(sim_info, (TurboCASUtil.OutfitCategory.SPECIAL, 0))
        TurboSimUtil.CAS.update_previous_outfit(sim_info)
        sim_ev(sim_info).is_outfit_update_locked = False
        try:
            TurboSimUtil.CAS.refresh_outfit(sim_info)
        except:
            pass
    return True


def set_bodytype_caspart(sim_identifier, outfit_category_and_index, bodytype, cas_id, remove=False):
    if cas_id == -1 and remove is False:
        return False
    try:
        outfit_editor = TurboCASUtil.OutfitEditor(sim_identifier, outfit_category_and_index=outfit_category_and_index)
    except RuntimeError:
        return False
    if remove is True:
        outfit_editor.remove_body_type(bodytype)
    else:
        outfit_editor.add_cas_part(bodytype, cas_id)
    outfit_editor.apply()


def set_first_free_skin_overlay_for_every_outfit(sim_identifier, cas_id):
    if cas_id == -1:
        return False
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    result = False
    for occult_sim_info in TurboSimUtil.Occult.get_all_sim_info_occults(sim_info):
        for outfit_category in (TurboCASUtil.OutfitCategory.EVERYDAY, TurboCASUtil.OutfitCategory.FORMAL, TurboCASUtil.OutfitCategory.ATHLETIC, TurboCASUtil.OutfitCategory.SLEEP, TurboCASUtil.OutfitCategory.PARTY, TurboCASUtil.OutfitCategory.BATHING, TurboCASUtil.OutfitCategory.CAREER, TurboCASUtil.OutfitCategory.SITUATION, TurboCASUtil.OutfitCategory.SPECIAL, TurboCASUtil.OutfitCategory.SWIMWEAR):
            for outfit_index in range(TurboCASUtil.OutfitCategory.get_maximum_outfits_for_outfit_category(outfit_category)):
                while TurboSimUtil.CAS.has_outfit(occult_sim_info, (outfit_category, outfit_index)):
                    if set_first_free_skin_overlay(occult_sim_info, (outfit_category, outfit_index), cas_id):
                        result = True
    return result


def set_first_free_skin_overlay(sim_identifier, outfit_category_and_index, cas_id):
    if cas_id == -1:
        return False
    try:
        outfit_editor = TurboCASUtil.OutfitEditor(sim_identifier, outfit_category_and_index=outfit_category_and_index)
    except RuntimeError:
        return False
    slots_list = (118, 119, 120, 121, 122, 123, 124, 125, 126, 127)
    empty_slot_id = -1
    for slot_id in slots_list:
        if outfit_editor.has_body_type(slot_id):
            pass
        empty_slot_id = slot_id
        break
    if empty_slot_id == -1:
        return False
    result = outfit_editor.add_cas_part(empty_slot_id, cas_id)
    outfit_editor.apply()
    return result


def clear_every_skin_overlay_for_every_outfit(sim_identifier, cas_id):
    if cas_id == -1:
        return False
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    result = False
    for occult_sim_info in TurboSimUtil.Occult.get_all_sim_info_occults(sim_info):
        for outfit_category in (TurboCASUtil.OutfitCategory.EVERYDAY, TurboCASUtil.OutfitCategory.FORMAL, TurboCASUtil.OutfitCategory.ATHLETIC, TurboCASUtil.OutfitCategory.SLEEP, TurboCASUtil.OutfitCategory.PARTY, TurboCASUtil.OutfitCategory.BATHING, TurboCASUtil.OutfitCategory.CAREER, TurboCASUtil.OutfitCategory.SITUATION, TurboCASUtil.OutfitCategory.SPECIAL, TurboCASUtil.OutfitCategory.SWIMWEAR):
            for outfit_index in range(TurboCASUtil.OutfitCategory.get_maximum_outfits_for_outfit_category(outfit_category)):
                while TurboSimUtil.CAS.has_outfit(occult_sim_info, (outfit_category, outfit_index)):
                    if clear_every_skin_overlay(occult_sim_info, (outfit_category, outfit_index), cas_id):
                        result = True
    return result


def clear_every_skin_overlay(sim_identifier, outfit_category_and_index, cas_id):
    if cas_id == -1:
        return False
    try:
        outfit_editor = TurboCASUtil.OutfitEditor(sim_identifier, outfit_category_and_index=outfit_category_and_index)
    except RuntimeError:
        return False
    result = outfit_editor.remove_cas_part(cas_id)
    outfit_editor.apply()
    return result


def get_sim_outfit_parts(sim_identifier, outfit_category_and_index=None):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    current_outfit_category_and_index = TurboSimUtil.CAS.get_current_outfit(sim_info)
    if outfit_category_and_index is not None and (current_outfit_category_and_index[0] != outfit_category_and_index[0] or current_outfit_category_and_index[1] != outfit_category_and_index[1]):
        return TurboSimUtil.CAS.get_outfit_parts(sim_info, outfit_category_and_index)
    outfit_parts_cache = sim_ev(sim_info).outfit_parts_cache
    if outfit_parts_cache:
        return outfit_parts_cache
    outfit_parts = TurboSimUtil.CAS.get_outfit_parts(sim_info, current_outfit_category_and_index)
    sim_ev(sim_info).outfit_parts_cache = outfit_parts
    return outfit_parts


def get_sim_outfit_cas_part_from_bodytype(sim_identifier, bodytype, outfit_category_and_index=None):
    body_parts = get_sim_outfit_parts(sim_identifier, outfit_category_and_index=outfit_category_and_index)
    if not body_parts:
        return -1
    bodytype = int(bodytype)
    if bodytype not in body_parts:
        return -1
    return body_parts[bodytype]


def has_sim_body_part(sim_or_sim_info, bodypart_id, outfit_category_and_index=None):
    body_parts = get_sim_outfit_parts(sim_or_sim_info, outfit_category_and_index=outfit_category_and_index)
    if not body_parts:
        return False
    return int(bodypart_id) in body_parts


def has_sim_cas_part_id(sim_or_sim_info, cas_part_id_or_tuple, outfit_category_and_index=None):
    body_parts = get_sim_outfit_parts(sim_or_sim_info, outfit_category_and_index=outfit_category_and_index)
    if not body_parts:
        return False
    outfit_part_ids = body_parts.values()
    if isinstance(cas_part_id_or_tuple, int):
        return cas_part_id_or_tuple in outfit_part_ids
    if isinstance(cas_part_id_or_tuple, tuple):
        for cas_id in cas_part_id_or_tuple:
            while cas_id in outfit_part_ids:
                return True
    return False


def is_sim_in_special_outfit(sim_info):
    current_outfit = TurboSimUtil.CAS.get_current_outfit(sim_info)
    return current_outfit[0] == TurboCASUtil.OutfitCategory.SPECIAL and current_outfit[1] == 0

