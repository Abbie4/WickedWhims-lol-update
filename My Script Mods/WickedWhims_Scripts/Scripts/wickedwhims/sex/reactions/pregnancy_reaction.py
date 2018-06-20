'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from enums.buffs_enum import SimBuff
from enums.interactions_enum import SimInteraction
from enums.relationship_enum import SimRelationshipBit
from enums.situations_enum import SimSituation
from turbolib.events.core import register_zone_load_event_method, is_game_loading
from turbolib.events.sims import register_sim_info_instance_init_event_method
from turbolib.interaction_util import TurboInteractionUtil
from turbolib.manager_util import TurboManagerUtil
from turbolib.math_util import TurboMathUtil
from turbolib.resource_util import TurboResourceUtil
from turbolib.sim_util import TurboSimUtil
from wickedwhims.sex.settings.sex_settings import SexSetting, get_sex_setting
from wickedwhims.sxex_bridge.reactions import register_sim_reaction_function
from wickedwhims.utils_buffs import add_sim_buff, has_sim_buffs
from wickedwhims.utils_relations import has_relationship_bit_with_sim, get_sim_ids_with_relationsip_bit, add_relationsip_bit_with_sim, remove_relationsip_bit_with_sim
from wickedwhims.utils_sims import is_sim_available
from wickedwhims.utils_situations import has_sim_situations
TEEN_PREGNANCY_REACTION_BUFFS = (SimBuff.PREGNANCY_TRIMESTER2, SimBuff.PREGNANCY_TRIMESTER3, SimBuff.PREGNANCY_TRIMESTER2_HATESCHILDREN, SimBuff.PREGNANCY_TRIMESTER3_HATESCHILDREN, SimBuff.PREGNANCY_TRIMESTER2_MALE, SimBuff.PREGNANCY_TRIMESTER3_MALE)

@register_sim_info_instance_init_event_method(unique_id='WickedWhims', priority=1, late=True)
def _wickedwhims_register_pregnancy_labor_buff_callback_on_new_sim(sim_info):
    if is_game_loading():
        return
    if TurboSimUtil.Species.is_human(sim_info):
        TurboSimUtil.Buff.register_for_buff_added_callback(sim_info, _clear_teen_sims_pregnancy_reaction_data)
        TurboSimUtil.Buff.register_for_buff_removed_callback(sim_info, _clear_teen_sims_pregnancy_reaction_data)


@register_zone_load_event_method(unique_id='WickedWhims', priority=40, late=True)
def _wickedwhims_register_pregnancy_labor_buff_callback():
    for sim_info in TurboManagerUtil.Sim.get_all_sim_info_gen(humans=True, pets=False):
        TurboSimUtil.Buff.register_for_buff_added_callback(sim_info, _clear_teen_sims_pregnancy_reaction_data)
        TurboSimUtil.Buff.register_for_buff_removed_callback(sim_info, _clear_teen_sims_pregnancy_reaction_data)


@register_sim_reaction_function(priority=2)
def _reaction_to_teen_sims_pregnancy(sim):
    if not get_sex_setting(SexSetting.REACTION_TO_TEEN_PREGNANCY_STATE, variable_type=bool):
        return False
    if TurboSimUtil.Age.get_age(sim) != TurboSimUtil.Age.TEEN:
        return False
    if not TurboSimUtil.Pregnancy.is_pregnant(sim):
        return False
    if not has_sim_buffs(sim, TEEN_PREGNANCY_REACTION_BUFFS):
        return False
    if not TurboSimUtil.Location.is_visible(sim):
        return False
    if TurboSimUtil.Spawner.is_leaving(sim):
        return False
    sim_parents_ids = get_sim_ids_with_relationsip_bit(sim, SimRelationshipBit.FAMILY_PARENT)
    if not sim_parents_ids:
        return False
    sim_pregnancy_partner = TurboSimUtil.Pregnancy.get_partner(sim)
    parent_sims = list()
    for parent_sim_id in sim_parents_ids:
        parent_sim = TurboManagerUtil.Sim.get_sim_info(parent_sim_id)
        if parent_sim is None:
            pass
        if has_relationship_bit_with_sim(parent_sim, sim, SimRelationshipBit.WW_KNOWS_ABOUT_TEEN_PREGNANCY):
            pass
        if sim_pregnancy_partner is not None and TurboManagerUtil.Sim.get_sim_id(sim_pregnancy_partner) == parent_sim_id:
            pass
        parent_sims.append(parent_sim)
    if not parent_sims:
        return False
    line_of_sight = TurboMathUtil.LineOfSight.create(TurboSimUtil.Location.get_routing_surface(sim), TurboSimUtil.Location.get_position(sim), 8.0)
    for parent_sim_info in parent_sims:
        target = TurboManagerUtil.Sim.get_sim_instance(parent_sim_info)
        if target is None:
            pass
        if has_sim_situations(target, (SimSituation.GRIMREAPER, SimSituation.FIRE, SimSituation.BABYBIRTH_HOSPITAL)):
            pass
        if not is_sim_available(target):
            pass
        if not TurboMathUtil.LineOfSight.test(line_of_sight, TurboSimUtil.Location.get_position(target)):
            pass
        while _reaction_to_pregnancy(target, sim):
            return True
    return False


def _reaction_to_pregnancy(sim, target):
    si_result = TurboSimUtil.Interaction.push_affordance(sim, SimInteraction.WW_TEEN_PREGNANCY_REACTION, target=target, interaction_context=TurboInteractionUtil.InteractionContext.SOURCE_SCRIPT, insert_strategy=TurboInteractionUtil.QueueInsertStrategy.NEXT, priority=TurboInteractionUtil.Priority.Critical, run_priority=TurboInteractionUtil.Priority.Critical)
    if si_result:
        add_relationsip_bit_with_sim(sim, target, SimRelationshipBit.WW_KNOWS_ABOUT_TEEN_PREGNANCY)
        add_sim_buff(sim, SimBuff.WW_ANGRY_AT_TEEN_PREGNANCY)
        return True
    return False


def _clear_teen_sims_pregnancy_reaction_data(buff_type, sim_id):
    if buff_type is None:
        return
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_id)
    if sim_info is None:
        return
    buff_id = TurboResourceUtil.Resource.get_guid64(buff_type)
    if buff_id == SimBuff.PREGNANCY_INLABOR or buff_id == SimBuff.PREGNANCY_INLABOR_MALE:
        targets_ids_list = get_sim_ids_with_relationsip_bit(sim_info, SimRelationshipBit.WW_KNOWS_ABOUT_TEEN_PREGNANCY)
        for target_sim_id in targets_ids_list:
            target_sim_info = TurboManagerUtil.Sim.get_sim_info(target_sim_id)
            while target_sim_info is not None:
                remove_relationsip_bit_with_sim(sim_info, target_sim_info, SimRelationshipBit.WW_KNOWS_ABOUT_TEEN_PREGNANCY)

