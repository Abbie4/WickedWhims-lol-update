from turbolib.sim_util import TurboSimUtil
from turbolib.manager_util import TurboManagerUtil
from wickedwhims.sex.enums.sex_gender import SexGenderType, get_sim_sex_gender
from wickedwhims.sex.settings.sex_settings import SexGenderTypeSetting, SexSetting, get_sex_setting

def is_compatible_actor(sim_identifier, sim_actor, target_sim_identifier, target_actor):
    if get_sex_setting(SexSetting.SEX_GENDER_TYPE, variable_type=int) == SexGenderTypeSetting.ANY_BASED:
        return True

    swap_from_real_sex_gender = get_sim_sex_gender(sim_identifier) # MALE, FEMALE, CMALE, CFEMALE
    swap_from_animation_gender = sim_actor.get_gender_type() # BOTH, CBOTH
    swap_to_real_sex_gender = get_sim_sex_gender(target_sim_identifier) # MALE, FEMALE, CMALE, CFEMALE
    swap_to_animation_gender = target_actor.get_gender_type() # BOTH, CBOTH

    gender_sim_identifier = TurboSimUtil.Gender.get_gender(sim_identifier)
    gender_target_sim_identifier = TurboSimUtil.Gender.get_gender(target_sim_identifier)
    swap_from_is_adult = swap_from_real_sex_gender == SexGenderType.MALE or swap_from_real_sex_gender == SexGenderType.FEMALE
    swap_to_is_adult = swap_to_real_sex_gender == SexGenderType.MALE or swap_to_real_sex_gender == SexGenderType.FEMALE

    swap_from_is_child = swap_from_real_sex_gender == SexGenderType.CMALE or swap_from_real_sex_gender == SexGenderType.CFEMALE
    swap_to_is_child = swap_to_real_sex_gender == SexGenderType.CMALE or swap_to_real_sex_gender == SexGenderType.CFEMALE

    if swap_from_animation_gender == swap_to_animation_gender or swap_from_real_sex_gender == swap_to_real_sex_gender or (gender_sim_identifier == gender_target_sim_identifier and swap_from_is_adult and swap_to_is_adult):
        return True

    swap_from_is_both = swap_from_animation_gender == SexGenderType.BOTH and swap_from_is_adult
    swap_to_is_both = swap_to_animation_gender == SexGenderType.BOTH and swap_to_is_adult

    swap_from_is_cboth = swap_from_animation_gender == SexGenderType.CBOTH and swap_from_is_child
    swap_to_is_cboth = swap_to_animation_gender == SexGenderType.CBOTH and swap_to_is_child

    # SAME GENDER
    # DIFFERENT GENDER, SAME AGE
    # DIFFERENT GENDER, DIFFERENT AGE

    # Adult, Child or Adult, Child
    if swap_from_is_child != swap_to_is_child or swap_from_is_adult != swap_to_is_adult:
        return False

    # BOTH, BOTH or CBOTH, CBOTH
    if (swap_from_is_both and swap_to_is_both) or (swap_from_is_cboth and swap_to_is_cboth):
        return True

    # FEMALE, FEMALE or MALE, MALE or CFEMALE, CFEMALE or CMALE, CMALE
    if swap_from_real_sex_gender == swap_to_real_sex_gender:
        return True

    # Implied from is adult, to is adult
    if swap_from_is_both and swap_to_is_adult:
        return True

    # Implied from is child, to is child
    if swap_from_is_cboth and swap_to_is_child:
        return True

    # Implied to is adult, from is adult
    if swap_to_is_both and swap_from_is_adult:
        return True

    # Implied to is child, from is child
    if swap_to_is_cboth and swap_from_is_child:
        return True

    return False

