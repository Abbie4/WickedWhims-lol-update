import enum
from enums.traits_enum import SimTrait
from turbolib.manager_util import TurboManagerUtil
from turbolib.sim_util import TurboSimUtil
from turbolib.world_util import TurboWorldUtil
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.sex.enums.sex_type import SexCategoryType
from wickedwhims.sex.pregnancy.birth_control.birth_control_handler import try_late_assign_birth_control
from wickedwhims.sex.pregnancy.birth_control.condoms import get_condom_wrapper_object_id
from wickedwhims.sex.pregnancy.native_pregnancy_handler import can_sim_get_pregnant
from wickedwhims.sex.settings.sex_settings import SexSetting, get_sex_setting, PregnancyModeSetting
from wickedwhims.utils_interfaces import display_notification
from wickedwhims.utils_inventory import get_object_amount_in_sim_inventory
from wickedwhims.utils_traits import has_sim_trait


class SexDenialReasonType(enum.Int, export=False):
    __qualname__ = 'SexDenialReasonType'
    NONE = 0
    NO_PROTECTION_HATES_CHILDREN = 1


class SexDenialReason:
    __qualname__ = 'SexDenialReason'

    def __init__(self, flag, reason, sim_info):
        self.flag = flag
        self.reason = reason
        self.sim_info = sim_info

    def __bool__(self):
        return self.flag

    def get_reason(self):
        return self.reason

    def get_sim_info(self):
        return self.sim_info

POSITIVE_RESULT = SexDenialReason(True, SexDenialReasonType.NONE, None)

def is_sim_allowed_for_animation(sims_list, animation_category, **kwargs):
    allowing_tests = (_test_for_children_hater,)
    sim_info_list = list()
    for sim in sims_list:
        sim_info_list.append(TurboManagerUtil.Sim.get_sim_info(sim))
    for sim_info in sim_info_list:
        for test in allowing_tests:
            result = test(sim_info, sim_info_list, animation_category, **kwargs)
            if not result:
                return result
    return POSITIVE_RESULT


def display_not_allowed_message(sex_denial_reason):
    if sex_denial_reason:
        return
    if sex_denial_reason.get_reason() == SexDenialReasonType.NO_PROTECTION_HATES_CHILDREN:
        display_notification(text=866800069, text_tokens=(sex_denial_reason.get_sim_info(),), title=2175203501, secondary_icon=sex_denial_reason.get_sim_info())


def _test_for_children_hater(sim_info, sim_info_list, animation_category, **args):
    if get_sex_setting(SexSetting.ALWAYS_ACCEPT_STATE, variable_type=bool):
        return True
    if get_sex_setting(SexSetting.PREGNANCY_MODE, variable_type=int) == PregnancyModeSetting.DISABLED:
        return True
    if animation_category != SexCategoryType.VAGINAL and animation_category != SexCategoryType.CLIMAX:
        return True
    if not has_sim_trait(sim_info, SimTrait.HATESCHILDREN):
        return True
    if not can_sim_get_pregnant(sim_info):
        return True
    is_npc_only = False not in [TurboSimUtil.Sim.is_npc(target_sim_info) for target_sim_info in sim_info_list]
    if get_sex_setting(SexSetting.PREGNANCY_MODE, variable_type=int) == PregnancyModeSetting.SIMPLE:
        if is_npc_only:
            if get_sex_setting(SexSetting.SIMPLE_NPC_PREGNANCY_CHANCE, variable_type=int) <= 0:
                return True
            elif get_sex_setting(SexSetting.SIMPLE_PREGNANCY_CHANCE, variable_type=int) <= 0:
                return True
        elif get_sex_setting(SexSetting.SIMPLE_PREGNANCY_CHANCE, variable_type=int) <= 0:
            return True
    try_late_assign_birth_control(sim_info)
    if sim_ev(sim_info).has_condom_on is True or sim_ev(sim_info).day_used_birth_control_pills == TurboWorldUtil.Time.get_absolute_days():
        return True
    condoms_needed = 0
    if 'is_joining' in args:
        for actor_sim_info in sim_info_list:
            if sim_ev(actor_sim_info).has_condom_on is False and has_sim_trait(actor_sim_info, SimTrait.GENDEROPTIONS_PREGNANCY_CANIMPREGNATE):
                condoms_needed += 1
    elif sim_ev(sim_info).active_sex_handler is not None:
        for actor_sim_info in sim_ev(sim_info).active_sex_handler.get_actors_sim_info_gen():
            if sim_ev(actor_sim_info).has_condom_on is False and has_sim_trait(actor_sim_info, SimTrait.GENDEROPTIONS_PREGNANCY_CANIMPREGNATE):
                condoms_needed += 1
    else:
        condoms_needed = 1
    if condoms_needed == 0:
        return True
    has_needed_condoms = False
    for actor_sim_info in sim_info_list:
        condoms_count = get_object_amount_in_sim_inventory(actor_sim_info, get_condom_wrapper_object_id())
        if condoms_count >= condoms_needed:
            has_needed_condoms = True
            break
    if has_needed_condoms is False:
        return SexDenialReason(False, SexDenialReasonType.NO_PROTECTION_HATES_CHILDREN, sim_info)
    return True

