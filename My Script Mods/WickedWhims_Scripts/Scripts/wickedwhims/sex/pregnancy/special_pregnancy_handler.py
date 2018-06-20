import random
from enums.relationship_enum import SimRelationshipBit
from enums.traits_enum import SimTrait
from turbolib.events.interactions import register_interaction_queue_event_method
from turbolib.interaction_util import TurboInteractionUtil
from turbolib.manager_util import TurboManagerUtil
from turbolib.resource_util import TurboResourceUtil
from turbolib.sim_util import TurboSimUtil
from turbolib.types_util import TurboTypesUtil
from turbolib.world_util import TurboWorldUtil
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.sex.enums.sex_type import SexCategoryType
from wickedwhims.sex.pregnancy.birth_control.birth_control_handler import try_late_assign_birth_control
from wickedwhims.sex.pregnancy.birth_control.condoms import try_auto_apply_condoms
from wickedwhims.sex.pregnancy.native_pregnancy_handler import can_sim_get_pregnant, set_sim_pregnancy_discovery, apply_sim_pregnancy, can_sim_impregnate
from wickedwhims.sex.pregnancy.pregnancy_interface import get_sim_current_pregnancy_chance
from wickedwhims.sex.settings.sex_settings import BirthControlModeSetting, get_sex_setting, SexSetting, PregnancyModeSetting
from wickedwhims.sxex_bridge.sex import is_sim_going_to_sex, is_sim_in_sex
from wickedwhims.utils_relations import add_relationsip_bit_with_sim, has_relationship_bit_with_sim, get_sim_ids_with_relationsip_bit, remove_relationsip_bit_with_sim
from wickedwhims.utils_traits import has_sim_trait

def is_sex_handler_allowed_for_pregnancy(sex_handler):
    if sex_handler.get_actors_amount() <= 1:
        return False
    if sex_handler.get_animation_instance().get_sex_category() != SexCategoryType.VAGINAL and sex_handler.get_animation_instance().get_sex_category() != SexCategoryType.CLIMAX:
        return False
    return True


def try_pregnancy_from_sex_handler(sex_handler, sims_list):
    if get_sex_setting(SexSetting.PREGNANCY_MODE, variable_type=int) == PregnancyModeSetting.DISABLED:
        return
    if not is_sex_handler_allowed_for_pregnancy(sex_handler):
        return
    for (_, sim_info) in sims_list:
        try_late_assign_birth_control(sim_info)
    try_auto_apply_condoms(sex_handler, sims_list)
    if sex_handler.pregnancy_sex_counter < 10:
        return
    if sex_handler.is_npc_only() and get_sex_setting(SexSetting.PREGNANCY_MODE, variable_type=int) == PregnancyModeSetting.MENSTRUAL_CYCLE and not get_sex_setting(SexSetting.MENSTRUAL_CYCLE_NPC_PREGNANCY, variable_type=bool):
        return
    for (actor_id, sim_info) in sims_list:
        if not can_sim_get_pregnant(sim_info):
            pass
        if _is_sim_on_birth_control(sim_info):
            pass
        try_sim_pregnancy_from_sex_handler(sex_handler, sims_list, actor_id, sim_info)
    sex_handler.pregnancy_sex_counter = 0


def try_sim_pregnancy_from_sex_handler(sex_handler, sims_list, actor_id, sim_info):
    if not can_sim_get_pregnant(sim_info):
        return False
    if TurboSimUtil.Pregnancy.is_pregnant(sim_info):
        return False
    sim_pregnancy_chance = get_sim_current_pregnancy_chance(sim_info)
    if get_sex_setting(SexSetting.PREGNANCY_MODE, variable_type=int) == PregnancyModeSetting.SIMPLE and sim_pregnancy_chance <= 0.0:
        return False
    pregnancy_partners = _get_possible_partners(sex_handler, sims_list, actor_id, sim_info)
    absolute_days = TurboWorldUtil.Time.get_absolute_days()
    enable_pregnancy_discovery = False
    for (partner_sim_id, is_cum_inside) in pregnancy_partners:
        partner_sim_info = TurboManagerUtil.Sim.get_sim_info(partner_sim_id)
        if partner_sim_info is None:
            pass
        if has_relationship_bit_with_sim(sim_info, partner_sim_info, SimRelationshipBit.WW_POTENTIAL_PREGNANCY_PARENT):
            pass
        if get_sex_setting(SexSetting.BIRTH_CONTROL_MODE, variable_type=int) == BirthControlModeSetting.REALISTIC:
            enable_pregnancy_discovery = True
        if _is_sim_on_birth_control(partner_sim_info):
            pass
        enable_pregnancy_discovery = True
        partner_pregnancy_chance = get_sim_current_pregnancy_chance(partner_sim_info)
        if partner_pregnancy_chance <= 0.0:
            pass
        if is_cum_inside is False:
            if has_sim_trait(partner_sim_info, SimTrait.LAZY) or has_sim_trait(partner_sim_info, SimTrait.CLUMSY):
                partner_pregnancy_chance /= 2.0
            else:
                partner_pregnancy_chance /= 4.0
        chance_value = random.Random((absolute_days, TurboManagerUtil.Sim.get_sim_id(sim_info), partner_sim_id)).uniform(0, 1)
        while chance_value <= sim_pregnancy_chance and (sim_ev(sim_info).pregnancy_fertility_boost[0] > 0 or chance_value <= partner_pregnancy_chance):
            sim_ev(sim_info).pregnancy_coming_flag = True
            add_relationsip_bit_with_sim(sim_info, partner_sim_info, SimRelationshipBit.WW_POTENTIAL_PREGNANCY_PARENT)
            enable_pregnancy_discovery = True
    if enable_pregnancy_discovery is True and sex_handler.has_displayed_pregnancy_notification is False:
        set_sim_pregnancy_discovery(sim_info, True)
        sex_handler.has_displayed_pregnancy_notification = True


def _get_possible_partners(sex_handler, sims_list, actor_id, sim_info):
    checked_sim_ids = set()
    pregnancy_pairs = set()
    actions = sex_handler.get_animation_instance().get_actor_received_actions(actor_id)
    for (action_actor_id, action_type, is_cum_inside) in actions:
        if action_type != SexCategoryType.VAGINAL:
            pass
        if actor_id == action_actor_id:
            pass
        actor_sim_id = sex_handler.get_sim_id_by_actor_id(action_actor_id)
        if actor_sim_id in checked_sim_ids:
            pass
        actor_sim_info = TurboManagerUtil.Sim.get_sim_info(actor_sim_id)
        while not actor_sim_info is None:
            if actor_sim_info is sim_info:
                pass
            if has_relationship_bit_with_sim(sim_info, actor_sim_info, SimRelationshipBit.WW_POTENTIAL_PREGNANCY_PARENT):
                checked_sim_ids.add(actor_sim_id)
            if not can_sim_impregnate(actor_sim_info):
                pass
            pregnancy_pairs.add((actor_sim_id, is_cum_inside))
            checked_sim_ids.add(actor_sim_id)
    if len(sims_list) == 2 and sex_handler.get_animation_instance().get_sex_category() == SexCategoryType.VAGINAL:
        for (action_actor_id, actor_sim_info) in sims_list:
            if actor_id == action_actor_id:
                pass
            if action_actor_id in checked_sim_ids:
                pass
            if actor_sim_info is sim_info:
                pass
            actor_sim_id = TurboManagerUtil.Sim.get_sim_id(actor_sim_info)
            if has_relationship_bit_with_sim(sim_info, actor_sim_info, SimRelationshipBit.WW_POTENTIAL_PREGNANCY_PARENT):
                checked_sim_ids.add(actor_sim_id)
            if not can_sim_impregnate(actor_sim_info):
                pass
            pregnancy_pairs.add((actor_sim_id, True))
            checked_sim_ids.add(actor_sim_id)
    return pregnancy_pairs


def _is_sim_on_birth_control(sim_identifier):
    if get_sex_setting(SexSetting.BIRTH_CONTROL_MODE, variable_type=int) == BirthControlModeSetting.PERFECT:
        if has_sim_trait(sim_identifier, SimTrait.GENDEROPTIONS_PREGNANCY_CANIMPREGNATE) and sim_ev(sim_identifier).has_condom_on is True:
            return True
        if has_sim_trait(sim_identifier, SimTrait.GENDEROPTIONS_PREGNANCY_CANBEIMPREGNATED) and sim_ev(sim_identifier).day_used_birth_control_pills == TurboWorldUtil.Time.get_absolute_days():
            return True
        return False
    if get_sex_setting(SexSetting.BIRTH_CONTROL_MODE, variable_type=int) == BirthControlModeSetting.REALISTIC:
        random_inst = random.Random((TurboWorldUtil.Time.get_absolute_days() + TurboWorldUtil.Time.get_absolute_hours())*768)
        if has_sim_trait(sim_identifier, SimTrait.GENDEROPTIONS_PREGNANCY_CANIMPREGNATE) and sim_ev(sim_identifier).has_condom_on is True:
            return random_inst.uniform(0, 1) < 0.95
        if has_sim_trait(sim_identifier, SimTrait.GENDEROPTIONS_PREGNANCY_CANBEIMPREGNATED) and sim_ev(sim_identifier).day_used_birth_control_pills == TurboWorldUtil.Time.get_absolute_days():
            return random_inst.uniform(0, 1) < 0.91
        return False
    return False


def update_sim_coming_pregnancy(sim_identifier, force=False):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    if sim_ev(sim_info).pregnancy_coming_flag is False:
        return
    if is_sim_in_sex(sim_info) or is_sim_going_to_sex(sim_info):
        return
    if sim_ev(sim_info).pregnancy_counter <= 120 and force is False:
        return
    sim_ev(sim_info).pregnancy_coming_flag = False
    sim_ev(sim_info).pregnancy_counter = 0
    partners_ids_list = get_sim_ids_with_relationsip_bit(sim_info, SimRelationshipBit.WW_POTENTIAL_PREGNANCY_PARENT)
    if not partners_ids_list:
        return
    sims_list = list()
    for partner_sim_id in partners_ids_list:
        partner_sim_info = TurboManagerUtil.Sim.get_sim_info(partner_sim_id)
        while partner_sim_info is not None:
            sims_list.append(partner_sim_info)
            remove_relationsip_bit_with_sim(sim_info, partner_sim_info, SimRelationshipBit.WW_POTENTIAL_PREGNANCY_PARENT)
    if not sims_list:
        return
    random_sim_partner = random.choice(sims_list)
    apply_sim_pregnancy(sim_info, random_sim_partner)


@register_interaction_queue_event_method(unique_id='WickedWhims')
def _wickedwhims_on_pregnancy_trigger_interaction_queue(interaction_instance):
    sim = TurboInteractionUtil.get_interaction_sim(interaction_instance)
    if sim_ev(sim).is_ready() and sim_ev(sim).pregnancy_coming_flag is True:
        interaction_guid = TurboResourceUtil.Resource.get_guid64(interaction_instance)
        if interaction_guid == 14434 or TurboTypesUtil.Interactions.is_npc_leave_lot_interaction(interaction_instance):
            update_sim_coming_pregnancy(sim, force=True)
    return True

