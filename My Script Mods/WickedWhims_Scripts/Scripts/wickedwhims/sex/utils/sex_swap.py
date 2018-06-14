from turbolib.sim_util import TurboSimUtil
from wickedwhims.sex.enums.sex_gender import SexGenderType, get_sim_sex_gender
from wickedwhims.sex.settings.sex_settings import SexGenderTypeSetting, SexSetting, get_sex_setting


def is_compatible_actor(sim_identifier, sim_actor, target_sim_identifier, target_actor):
    if get_sex_setting(SexSetting.SEX_GENDER_TYPE, variable_type=int) == SexGenderTypeSetting.ANY_BASED:
        return True
    # sim_identifier is the sim wanting to swap (It contains their real gender)
    # target_sim_identifier is the sim position to swap to (It contains their real gender)
    # sim_actor has the current gender the sim wants to swap to (gender of the sim wanting to swap)
    # target_actor has the current gender the sim wants to swap to (gender of the slot the sim wants to swap with)
    # We also want to back check to see if the actor we want to swap with can take our place, so we essentially treat the actors in the reverse role as well
    swap_from_real_sex_gender = get_sim_sex_gender(sim_identifier) # MALE, FEMALE, CMALE, CFEMALE
    swap_from_animation_gender = sim_actor.get_gender_type() # BOTH, CBOTH
    swap_to_real_sex_gender = get_sim_sex_gender(target_sim_identifier) # MALE, FEMALE, CMALE, CFEMALE
    swap_to_animation_gender = target_actor.get_gender_type() # BOTH, CBOTH
    # if the animation genders are the same or if the actors have the same real gender
    if swap_from_animation_gender == swap_to_animation_gender or TurboSimUtil.Gender.get_gender(sim_identifier) == TurboSimUtil.Gender.get_gender(target_sim_identifier):
        return True
    # If the real genders match the animation genders
    if swap_from_real_sex_gender == swap_to_animation_gender and swap_to_real_sex_gender == swap_from_animation_gender:
        return True
    # Adult
    # If the slot being swapped to can fit the actor trying to swap
    if swap_to_animation_gender == SexGenderType.BOTH and (swap_from_real_sex_gender == SexGenderType.MALE or swap_from_real_sex_gender == SexGenderType.FEMALE):
        # If the slot being swapped from can fit the actor being swapped by the actor trying to swap
        if swap_from_animation_gender == swap_to_real_sex_gender:
            return True
        # If the slot being swapped from can fit the actor being swapped by the actor trying to swap
        if swap_from_animation_gender == SexGenderType.BOTH and (swap_to_real_sex_gender == SexGenderType.MALE or swap_to_real_sex_gender == SexGenderType.FEMALE):
            return True
        return False
    # Child
    # If the slot being swapped to can fit the actor trying to swap
    if swap_to_animation_gender == SexGenderType.CBOTH and (swap_from_real_sex_gender == SexGenderType.CMALE or swap_from_real_sex_gender == SexGenderType.CFEMALE):
        # If the slot being swapped from can fit the actor being swapped by the actor trying to swap
        if swap_from_animation_gender == swap_to_real_sex_gender:
            return True
        # If the slot being swapped from can fit the actor being swapped by the actor trying to swap
        if swap_from_animation_gender == SexGenderType.CBOTH and (swap_to_real_sex_gender == SexGenderType.CMALE or swap_to_real_sex_gender == SexGenderType.CFEMALE):
            return True
        return False
    return False

