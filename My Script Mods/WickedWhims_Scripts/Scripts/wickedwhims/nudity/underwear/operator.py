import random
from enums.traits_enum import SimTrait
from turbolib.cas_util import TurboCASUtil
from turbolib.manager_util import TurboManagerUtil
from turbolib.sim_util import TurboSimUtil
from wickedwhims.main.cas_config_handler import get_underwear_part_sets
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.nudity.nudity_settings import NuditySetting, get_nudity_setting
from wickedwhims.sxex_bridge.nudity import get_default_nude_cas_part_id
from wickedwhims.utils_cas import get_modified_outfit, get_sim_outfit_cas_part_from_bodytype
from wickedwhims.utils_traits import has_sim_trait
DEFAULT_UNDERWEAR_TOP_FEMALE = 24426
DEFAULT_UNDERWEAR_BOTTOM_FEMALE = 24434
DEFAULT_UNDERWEAR_BOTTOM_MALE = 24742
DEFAULT_UNDERWEAR_TOP_CHILD_FEMALE = 37518
DEFAULT_UNDERWEAR_BOTTOM_CHILD_FEMALE = 45130
DEFAULT_UNDERWEAR_BOTTOM_CHILD_MALE = 44677
MALE_UNDERWEAR_SETS_CACHE = ()
FEMALE_UNDERWEAR_SETS_CACHE = ()
CHILD_MALE_UNDERWEAR_SETS_CACHE = ()
CHILD_FEMALE_UNDERWEAR_SETS_CACHE = ()


def has_sim_underwear_data(sim_identifier, outfit_category_and_index):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    sim_is_child = TurboSimUtil.Age.get_age(sim_info) is TurboSimUtil.Age.CHILD
    outfit_code = _get_outfit_category_and_index_code(outfit_category_and_index)
    if outfit_code not in sim_ev(sim_info).underwear_outfits_parts:
        return True
    underwear_data = sim_ev(sim_info).underwear_outfits_parts[outfit_code]
    if sim_is_child:
        if (underwear_data[0] == -1 or underwear_data[0] == DEFAULT_UNDERWEAR_TOP_CHILD_FEMALE) and (underwear_data[1] == -1 or underwear_data[1] == DEFAULT_UNDERWEAR_BOTTOM_CHILD_MALE or underwear_data[1] == DEFAULT_UNDERWEAR_BOTTOM_CHILD_FEMALE):
            return False
    else:
        if (underwear_data[0] == -1 or underwear_data[0] == DEFAULT_UNDERWEAR_TOP_FEMALE) and (underwear_data[1] == -1 or underwear_data[1] == DEFAULT_UNDERWEAR_BOTTOM_MALE or underwear_data[1] == DEFAULT_UNDERWEAR_BOTTOM_FEMALE):
            return False
    return True


def get_sim_underwear_data(sim_identifier, outfit_category_and_index):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    sim_is_child = TurboSimUtil.Age.get_age(sim_info) is TurboSimUtil.Age.CHILD
    if not get_nudity_setting(NuditySetting.UNDERWEAR_SWITCH_STATE, variable_type=bool) or has_sim_trait(sim_info, SimTrait.WW_NO_UNDERWEAR):
        return (-1, -1)
    outfit_category = outfit_category_and_index[0]
    outfit_index = outfit_category_and_index[1]
    if outfit_category == TurboCASUtil.OutfitCategory.CAREER or outfit_category == TurboCASUtil.OutfitCategory.SITUATION:
        outfit_category = TurboCASUtil.OutfitCategory.EVERYDAY
        outfit_index = 0
    if outfit_category == TurboCASUtil.OutfitCategory.SPECIAL and outfit_index == 0:
        modified_outfit = get_modified_outfit(sim_info)
        outfit_category = modified_outfit[0]
        outfit_index = modified_outfit[1]
    outfit_code = _get_outfit_category_and_index_code((outfit_category, outfit_index))
    if outfit_code in sim_ev(sim_info).underwear_outfits_parts:
        underwear_data = sim_ev(sim_info).underwear_outfits_parts[outfit_code]
    elif TurboSimUtil.Sim.is_npc(sim_info):
        underwear_data = list(get_random_underwear_set(sim_info))
    else:
        underwear_data = [-1, -1]
    if sim_is_child:
        if TurboSimUtil.Gender.is_male(sim_info):
            if underwear_data[1] == -1 or not TurboCASUtil.Outfit.is_cas_part_loaded(underwear_data[1]):
                underwear_data[1] = DEFAULT_UNDERWEAR_BOTTOM_CHILD_MALE
        else:
            if underwear_data[0] == -1 or not TurboCASUtil.Outfit.is_cas_part_loaded(underwear_data[0]):
                underwear_data[0] = DEFAULT_UNDERWEAR_TOP_CHILD_FEMALE
            if underwear_data[1] == -1 or not TurboCASUtil.Outfit.is_cas_part_loaded(underwear_data[1]):
                underwear_data[1] = DEFAULT_UNDERWEAR_BOTTOM_CHILD_FEMALE
    else:
        if TurboSimUtil.Gender.is_male(sim_info):
            if underwear_data[1] == -1 or not TurboCASUtil.Outfit.is_cas_part_loaded(underwear_data[1]):
                underwear_data[1] = DEFAULT_UNDERWEAR_BOTTOM_MALE
        else:
            if underwear_data[0] == -1 or not TurboCASUtil.Outfit.is_cas_part_loaded(underwear_data[0]):
                underwear_data[0] = DEFAULT_UNDERWEAR_TOP_FEMALE
            if underwear_data[1] == -1 or not TurboCASUtil.Outfit.is_cas_part_loaded(underwear_data[1]):
                underwear_data[1] = DEFAULT_UNDERWEAR_BOTTOM_FEMALE
    set_sim_underwear_data(sim_info, underwear_data, outfit_category_and_index)
    return underwear_data


def set_sim_underwear_data(sim_identifier, underwear_cas_ids, outfit_category_and_index):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    underwear_cas_ids = list(underwear_cas_ids)
    if underwear_cas_ids[0] == get_default_nude_cas_part_id(sim_info, 6):
        underwear_cas_ids[0] = -1
    if underwear_cas_ids[1] == get_default_nude_cas_part_id(sim_info, 7):
        underwear_cas_ids[1] = -1
    sim_ev(sim_info).underwear_outfits_parts[_get_outfit_category_and_index_code(outfit_category_and_index)] = underwear_cas_ids


def get_random_underwear_set(sim_identifier):
    global MALE_UNDERWEAR_SETS_CACHE, FEMALE_UNDERWEAR_SETS_CACHE, CHILD_MALE_UNDERWEAR_SETS_CACHE, CHILD_FEMALE_UNDERWEAR_SETS_CACHE
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    sim_is_child = TurboSimUtil.Age.get_age(sim_info) is TurboSimUtil.Age.CHILD
    if sim_is_child:
        if TurboSimUtil.Gender.is_male(sim_info):
            if CHILD_MALE_UNDERWEAR_SETS_CACHE:
                underwear_sets_list = CHILD_MALE_UNDERWEAR_SETS_CACHE
            else:
                underwear_sets_list = get_underwear_part_sets(TurboSimUtil.Gender.get_gender(sim_info))
                if not underwear_sets_list:
                    underwear_sets_list = [[-1, DEFAULT_UNDERWEAR_BOTTOM_CHILD_MALE]]
                    CHILD_MALE_UNDERWEAR_SETS_CACHE = underwear_sets_list
        elif CHILD_FEMALE_UNDERWEAR_SETS_CACHE:
            underwear_sets_list = CHILD_FEMALE_UNDERWEAR_SETS_CACHE
        else:
            underwear_sets_list = get_underwear_part_sets(TurboSimUtil.Gender.get_gender(sim_info))
            if not underwear_sets_list:
                underwear_sets_list = [[DEFAULT_UNDERWEAR_TOP_CHILD_FEMALE, DEFAULT_UNDERWEAR_BOTTOM_CHILD_FEMALE]]
                CHILD_FEMALE_UNDERWEAR_SETS_CACHE = underwear_sets_list
    else:
        if TurboSimUtil.Gender.is_male(sim_info):
            if MALE_UNDERWEAR_SETS_CACHE:
                underwear_sets_list = MALE_UNDERWEAR_SETS_CACHE
            else:
                underwear_sets_list = get_underwear_part_sets(TurboSimUtil.Gender.get_gender(sim_info))
                if not underwear_sets_list:
                    underwear_sets_list = [[-1, DEFAULT_UNDERWEAR_BOTTOM_MALE]]
                MALE_UNDERWEAR_SETS_CACHE = underwear_sets_list
        elif FEMALE_UNDERWEAR_SETS_CACHE:
            underwear_sets_list = FEMALE_UNDERWEAR_SETS_CACHE
        else:
            underwear_sets_list = get_underwear_part_sets(TurboSimUtil.Gender.get_gender(sim_info))
            if not underwear_sets_list:
                underwear_sets_list = [[DEFAULT_UNDERWEAR_TOP_FEMALE, DEFAULT_UNDERWEAR_BOTTOM_FEMALE]]
            FEMALE_UNDERWEAR_SETS_CACHE = underwear_sets_list
    random_int = random.Random(TurboManagerUtil.Sim.get_sim_id(sim_info))
    return random_int.choice(underwear_sets_list)


def validate_outfit_underwear(sim_identifier, outfit_category_and_index):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    sim_is_child = TurboSimUtil.Age.get_age(sim_info) is TurboSimUtil.Age.CHILD
    underwear_data = get_sim_underwear_data(sim_info, outfit_category_and_index)
    if sim_is_child:
        if TurboSimUtil.Gender.is_male(sim_info):
            outfit_bottom_part = get_sim_outfit_cas_part_from_bodytype(sim_info, 7, outfit_category_and_index=outfit_category_and_index)
            if underwear_data[1] == outfit_bottom_part:
                set_sim_underwear_data(sim_info, [-1, DEFAULT_UNDERWEAR_BOTTOM_CHILD_MALE], outfit_category_and_index)
        else:
            outfit_top_part = get_sim_outfit_cas_part_from_bodytype(sim_info, 6, outfit_category_and_index=outfit_category_and_index)
            outfit_bottom_part = get_sim_outfit_cas_part_from_bodytype(sim_info, 7, outfit_category_and_index=outfit_category_and_index)
            if underwear_data[0] == outfit_top_part or underwear_data[1] == outfit_bottom_part:
                set_sim_underwear_data(sim_info, [DEFAULT_UNDERWEAR_TOP_CHILD_FEMALE, DEFAULT_UNDERWEAR_BOTTOM_CHILD_FEMALE], outfit_category_and_index)
    else:
        if TurboSimUtil.Gender.is_male(sim_info):
            outfit_bottom_part = get_sim_outfit_cas_part_from_bodytype(sim_info, 7, outfit_category_and_index=outfit_category_and_index)
            if underwear_data[1] == outfit_bottom_part:
                set_sim_underwear_data(sim_info, [-1, DEFAULT_UNDERWEAR_BOTTOM_MALE], outfit_category_and_index)
        else:
            outfit_top_part = get_sim_outfit_cas_part_from_bodytype(sim_info, 6, outfit_category_and_index=outfit_category_and_index)
            outfit_bottom_part = get_sim_outfit_cas_part_from_bodytype(sim_info, 7, outfit_category_and_index=outfit_category_and_index)
            if underwear_data[0] == outfit_top_part or underwear_data[1] == outfit_bottom_part:
                set_sim_underwear_data(sim_info, [DEFAULT_UNDERWEAR_TOP_FEMALE, DEFAULT_UNDERWEAR_BOTTOM_FEMALE], outfit_category_and_index)


def _get_outfit_category_and_index_code(outfit_category_and_index):
    return str(int(outfit_category_and_index[0])) + str(int(outfit_category_and_index[1]))

