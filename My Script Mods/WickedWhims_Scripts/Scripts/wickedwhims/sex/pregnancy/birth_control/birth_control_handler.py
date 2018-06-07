from enums.traits_enum import SimTrait
from turbolib.manager_util import TurboManagerUtil
from turbolib.sim_util import TurboSimUtil
from turbolib.world_util import TurboWorldUtil
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.sex.pregnancy.birth_control.condoms import update_sim_condom_state, give_sim_condoms, get_condom_wrapper_object_id
from wickedwhims.sex.pregnancy.birth_control.pills import is_sim_allowed_for_free_birth_control, update_sim_birth_control_status_buff, update_sim_birth_control_power, take_birth_control_pill
from wickedwhims.sex.settings.sex_settings import get_sex_setting, SexSetting, NPCBirthControlModeSetting
from wickedwhims.utils_inventory import get_object_amount_in_sim_inventory
from wickedwhims.utils_traits import has_sim_trait

def update_sim_birth_control_state(sim_identifier):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    update_sim_condom_state(sim_info)
    update_sim_birth_control_status_buff(sim_info)
    update_sim_birth_control_power(sim_info)


def try_late_assign_birth_control(sim_identifier):
    if get_sex_setting(SexSetting.NPC_BIRTH_CONTROL_MODE, variable_type=int) == NPCBirthControlModeSetting.UNSAFE:
        return False
    if TurboSimUtil.Sim.is_player(sim_identifier):
        return False
    if is_sim_birth_control_safe(sim_identifier, allow_potentially=False):
        return True
    if not is_sim_allowed_for_free_birth_control(sim_identifier):
        return False
    if has_sim_trait(sim_identifier, SimTrait.GENDEROPTIONS_TOILET_STANDING):
        return give_sim_condoms(sim_identifier, amount=1)
    return take_birth_control_pill(sim_identifier, no_inventory=True)


def is_sim_birth_control_safe(sim_identifier, allow_potentially=True):
    if (not has_sim_trait(sim_identifier, SimTrait.GENDEROPTIONS_PREGNANCY_CANBEIMPREGNATED) or has_sim_trait(sim_identifier, SimTrait.GENDEROPTIONS_PREGNANCY_CANNOT_BEIMPREGNATED)) and (not has_sim_trait(sim_identifier, SimTrait.GENDEROPTIONS_PREGNANCY_CANIMPREGNATE) or has_sim_trait(sim_identifier, SimTrait.GENDEROPTIONS_PREGNANCY_CANNOTIMPREGNATE)):
        return True
    if has_sim_trait(sim_identifier, SimTrait.WW_INFERTILE):
        return True
    if has_sim_trait(sim_identifier, SimTrait.GENDEROPTIONS_TOILET_STANDING):
        if sim_ev(sim_identifier).has_condom_on is True:
            return True
        if get_object_amount_in_sim_inventory(sim_identifier, get_condom_wrapper_object_id()) > 0:
            return True
    elif sim_ev(sim_identifier).day_used_birth_control_pills == TurboWorldUtil.Time.get_absolute_days():
        return True
    if allow_potentially is True and is_sim_allowed_for_free_birth_control(sim_identifier):
        return True
    return False

