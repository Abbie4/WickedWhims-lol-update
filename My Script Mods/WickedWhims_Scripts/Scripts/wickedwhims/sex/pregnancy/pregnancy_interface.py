from enums.traits_enum import SimTrait
from turbolib.sim_util import TurboSimUtil
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.sex.pregnancy.menstrual_cycle_handler import get_sim_current_menstrual_pregnancy_chance
from wickedwhims.sex.settings.sex_settings import PregnancyModeSetting, get_sex_setting, SexSetting
from wickedwhims.utils_traits import has_sim_trait

def get_sim_current_pregnancy_chance(sim_identifier):
    if get_sex_setting(SexSetting.PREGNANCY_MODE, variable_type=int) == PregnancyModeSetting.DISABLED:
        return 0.0
    chance_modifier = 1.0
    chance_modifier -= sim_ev(sim_identifier).birth_control_pill_power
    if get_sex_setting(SexSetting.PREGNANCY_MODE, variable_type=int) == PregnancyModeSetting.SIMPLE:
        if has_sim_trait(sim_identifier, SimTrait.WW_INFERTILE):
            return 0.0
        if TurboSimUtil.Sim.is_npc(sim_identifier):
            return get_sex_setting(SexSetting.SIMPLE_NPC_PREGNANCY_CHANCE, variable_type=int)/100.0*chance_modifier
        return get_sex_setting(SexSetting.SIMPLE_PREGNANCY_CHANCE, variable_type=int)/100.0*chance_modifier
    elif get_sex_setting(SexSetting.PREGNANCY_MODE, variable_type=int) == PregnancyModeSetting.MENSTRUAL_CYCLE:
        return get_sim_current_menstrual_pregnancy_chance(sim_identifier)*chance_modifier
    return 0.0

