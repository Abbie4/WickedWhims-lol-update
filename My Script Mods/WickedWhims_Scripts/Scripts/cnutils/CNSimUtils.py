from turbolib.sim_util import TurboSimUtil
from wickedwhims.sex.enums.sex_gender import SexGenderType
from wickedwhims.sex.settings.sex_settings import get_sex_setting, SexSetting


class CNSimUtils:
    __qualname__ = 'CNSimUtils'

    @classmethod
    def is_child(self, gender):
        return gender == SexGenderType.CBOTH or gender == SexGenderType.CFEMALE or gender == SexGenderType.CMALE

    @classmethod
    def is_adult(self, gender):
        return gender == SexGenderType.BOTH or gender == SexGenderType.FEMALE or gender == SexGenderType.MALE

    @classmethod
    def is_child_or_teen(self, sim_identifier_or_info):
        sim_age = TurboSimUtil.Age.get_age(sim_identifier_or_info)
        return sim_age == TurboSimUtil.Age.TEEN or sim_age == TurboSimUtil.Age.CHILD

    @classmethod
    def teen_sex_is_enabled(self):
        return get_sex_setting(SexSetting.TEENS_SEX_STATE, variable_type=bool)

    @classmethod
    def can_have_sex(self, sim_identifier_or_info, skip_setting_check=False):
        is_child_or_teen = self.is_child_or_teen(sim_identifier_or_info)
        # True When
        # They are not a child or a teen
        # or
        # They are a child or a teen and teen sex is enabled
        return not is_child_or_teen or self.teen_sex_is_enabled()

    @classmethod
    def is_toddler(self, sim_identifier_or_info):
        return TurboSimUtil.Age.is_younger_than(sim_identifier_or_info, TurboSimUtil.Age.CHILD)