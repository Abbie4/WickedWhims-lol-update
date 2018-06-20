'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from enums.buffs_enum import SimBuff
from enums.traits_enum import SimTrait
from turbolib.events.core import register_zone_load_event_method, is_game_loading
from turbolib.events.interactions import register_interaction_run_event_method, register_interaction_outcome_event_method
from turbolib.events.sims import register_sim_info_instance_init_event_method
from turbolib.interaction_util import TurboInteractionUtil
from turbolib.manager_util import TurboManagerUtil
from turbolib.native.enum import TurboEnum
from turbolib.resource_util import TurboResourceUtil
from turbolib.sim_util import TurboSimUtil
from turbolib.special.custom_exception_watcher import exception_watch
from turbolib.types_util import TurboTypesUtil
from turbolib.world_util import TurboWorldUtil
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.sex.enums.sex_type import SexCategoryType
from wickedwhims.sxex_bridge.statistics import increase_sim_ww_statistic
from wickedwhims.utils_buffs import has_sim_buff, remove_sim_buff, add_sim_buff
from wickedwhims.utils_cas import clear_every_skin_overlay_for_every_outfit, set_first_free_skin_overlay_for_every_outfit, has_sim_cas_part_id
from wickedwhims.utils_traits import has_sim_trait
CUM_FACE_LAYER = 16972778289889638565
CUM_CHEST_LAYER = 9383219480370302712
CUM_BACK_LAYER = 16185173326459564428
CUM_VAGINA_LAYER = 14369177098647113263
CUM_BUTT_LAYER = 13092454024188181663
CUM_FEET_LAYER = 17831762011410340817
SIM_CLEAN_FACE_INTERACTIONS = {14238}
SIM_CLEAN_VAGINA_INTERACTIONS = {14427, 13443, 14434, 17681256309946806522}
SIM_CLEAN_BUTT_INTERACTIONS = {14427, 13443}
SIM_CLEAN_FULL_INTERACTIONS = (13439, 13949, 13950, 13952, 23839, 24332, 35123, 39845, 39860, 39965, 104658, 104659, 110817, 110818, 110819, 110820, 110821, 110822, 13073, 13076, 13084, 13087, 120340, 120341, 120339, 120337, 120342, 121575, 120336, 121573, 117263, 120124, 131566, 13441, 13621, 76688, 102325, 103784, 103790, 104744, 102550, 129587, 128625)
SIM_KISS_INTERACTIONS = {25865, 25872, 25873, 26131, 26546, 26555, 28612, 39848, 123314, 123315, 153891, 155109}

class CumLayerType(TurboEnum):
    __qualname__ = 'CumLayerType'
    NONE = -1
    DISABLED = 0
    FACE = 1
    CHEST = 2
    BACK = 3
    VAGINA = 4
    BUTT = 5
    FEET = 6


def get_cum_layer_from_sex_category(sex_category):
    if sex_category == SexCategoryType.ORALJOB:
        return CumLayerType.FACE
    if sex_category == SexCategoryType.FOOTJOB:
        return CumLayerType.FEET
    if sex_category == SexCategoryType.VAGINAL:
        return CumLayerType.VAGINA
    if sex_category == SexCategoryType.ANAL:
        return CumLayerType.BUTT
    return CumLayerType.NONE


def get_cum_layer_type_by_name(name):
    name = name.upper()
    if name == 'DISABLED':
        return CumLayerType.DISABLED
    if name == 'FACE':
        return CumLayerType.FACE
    if name == 'CHEST':
        return CumLayerType.CHEST
    if name == 'BACK':
        return CumLayerType.BACK
    if name == 'VAGINA':
        return CumLayerType.VAGINA
    if name == 'BUTT':
        return CumLayerType.BUTT
    if name == 'FEET':
        return CumLayerType.FEET
    return CumLayerType.NONE


def get_cum_layer_cas_id(cum_layer_type):
    if cum_layer_type == CumLayerType.FACE:
        return CUM_FACE_LAYER
    if cum_layer_type == CumLayerType.CHEST:
        return CUM_CHEST_LAYER
    if cum_layer_type == CumLayerType.BACK:
        return CUM_BACK_LAYER
    if cum_layer_type == CumLayerType.VAGINA:
        return CUM_VAGINA_LAYER
    if cum_layer_type == CumLayerType.BUTT:
        return CUM_BUTT_LAYER
    if cum_layer_type == CumLayerType.FEET:
        return CUM_FEET_LAYER
    return -1


def apply_sim_cum_layer(sim_identifier, cum_layer_types, force=False):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    has_applied = False
    for cum_layer_type in cum_layer_types:
        while not cum_layer_type == CumLayerType.DISABLED:
            if cum_layer_type == CumLayerType.NONE:
                pass
            if cum_layer_type == CumLayerType.VAGINA and has_sim_trait(sim_info, SimTrait.GENDEROPTIONS_TOILET_STANDING):
                cum_layer_type = CumLayerType.BUTT
            cum_cas_id = get_cum_layer_cas_id(cum_layer_type)
            if has_sim_cas_part_id(sim_info, cum_cas_id) and force is False:
                pass
            set_first_free_skin_overlay_for_every_outfit(sim_info, cum_cas_id)
            increase_sim_ww_statistic(sim_info, 'times_received_cum_' + str(cum_layer_type.name).lower())
            has_applied = True
    if has_applied is True:
        try:
            TurboSimUtil.CAS.refresh_outfit(sim_info)
        except:
            pass
        sim_ev(sim_info).cum_apply_time = TurboWorldUtil.Time.get_absolute_ticks() + 360000


def clean_sim_cum_layers(sim_identifier, layers_to_clean=(CumLayerType.FACE, CumLayerType.CHEST, CumLayerType.BACK, CumLayerType.VAGINA, CumLayerType.BUTT, CumLayerType.FEET)):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    sim_ev(sim_info).cum_apply_time = -1
    has_cleaned = False
    for cum_layer_type in layers_to_clean:
        cum_cas_id = get_cum_layer_cas_id(cum_layer_type)
        while cum_cas_id != -1 and has_sim_cas_part_id(sim_info, cum_cas_id):
            if clear_every_skin_overlay_for_every_outfit(sim_info, cum_cas_id):
                has_cleaned = True
    if has_cleaned is True:
        try:
            TurboSimUtil.CAS.refresh_outfit(sim_info)
        except:
            pass


@register_sim_info_instance_init_event_method(unique_id='WickedWhims', priority=1, late=True)
def _wickedwhims_register_cum_outfit_change_callback_on_new_sim(sim_info):
    if is_game_loading():
        return
    if TurboSimUtil.Species.is_human(sim_info):
        TurboSimUtil.CAS.register_for_outfit_changed_callback(sim_info, _on_sim_outfit_change)


@register_zone_load_event_method(unique_id='WickedWhims', priority=40, late=True)
def _wickedwhims_register_cum_outfit_change_callback():
    for sim_info in TurboManagerUtil.Sim.get_all_sim_info_gen(humans=True, pets=False):
        TurboSimUtil.CAS.register_for_outfit_changed_callback(sim_info, _on_sim_outfit_change)


@exception_watch()
def _on_sim_outfit_change(sim_info, category_and_index):
    update_cum_buffs(sim_info, outfit_category_and_index=category_and_index)


def update_cum_buffs(sim_info, outfit_category_and_index=None):
    if TurboSimUtil.Age.is_younger_than(sim_info, TurboSimUtil.Age.TEEN):
        return
    has_positive_buff = has_sim_buff(sim_info, SimBuff.WW_CUM_ON_BODY_POSITIVE)
    has_negative_buff = has_sim_buff(sim_info, SimBuff.WW_CUM_ON_BODY_NEGATIVE)
    if has_sim_cas_part_id(sim_info, (CUM_FACE_LAYER, CUM_CHEST_LAYER, CUM_BACK_LAYER, CUM_VAGINA_LAYER, CUM_BUTT_LAYER, CUM_FEET_LAYER), outfit_category_and_index=outfit_category_and_index):
        if has_positive_buff is False and has_negative_buff is False:
            if has_sim_trait(sim_info, SimTrait.WW_CUMSLUT) or has_sim_trait(sim_info, SimTrait.ROMANTIC):
                add_sim_buff(sim_info, SimBuff.WW_CUM_ON_BODY_POSITIVE)
            elif has_sim_trait(sim_info, SimTrait.HATESCHILDREN):
                pass
            else:
                add_sim_buff(sim_info, SimBuff.WW_CUM_ON_BODY_NEGATIVE)
        return
    if has_positive_buff is True:
        remove_sim_buff(sim_info, SimBuff.WW_CUM_ON_BODY_POSITIVE)
    if has_negative_buff is True:
        remove_sim_buff(sim_info, SimBuff.WW_CUM_ON_BODY_NEGATIVE)


@register_interaction_run_event_method(unique_id='WickedWhims')
def _wickedwhims_clean_cum_on_hygiene_interactions(interaction_instance):
    interaction_guid = TurboResourceUtil.Resource.get_guid64(interaction_instance)
    sim = TurboInteractionUtil.get_interaction_sim(interaction_instance)
    if interaction_guid in SIM_CLEAN_FULL_INTERACTIONS:
        clean_sim_cum_layers(sim)
        return
    if interaction_guid in SIM_CLEAN_VAGINA_INTERACTIONS:
        clean_sim_cum_layers(sim, layers_to_clean=(CumLayerType.VAGINA,))
        return
    if interaction_guid in SIM_CLEAN_BUTT_INTERACTIONS:
        clean_sim_cum_layers(sim, layers_to_clean=(CumLayerType.VAGINA, CumLayerType.BUTT))
        return
    if interaction_guid in SIM_CLEAN_FACE_INTERACTIONS:
        clean_sim_cum_layers(sim, layers_to_clean=(CumLayerType.FACE,))
        return
    if TurboTypesUtil.Interactions.is_npc_leave_lot_interaction(interaction_instance):
        clean_sim_cum_layers(sim)
        return


def try_clean_sim_cum(sim_identifier):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    if TurboSimUtil.Sim.is_player(sim_info):
        return
    if sim_ev(sim_info).cum_apply_time == -1:
        return
    if TurboWorldUtil.Time.get_absolute_ticks() < sim_ev(sim_info).cum_apply_time:
        return
    clean_sim_cum_layers(sim_info)


@register_interaction_outcome_event_method(unique_id='WickedWhims')
def _wickedwhims_on_kiss_interactions_outcome(interaction_instance, outcome_result):
    if outcome_result:
        interaction_guid = TurboResourceUtil.Resource.get_guid64(interaction_instance)
        if interaction_guid in SIM_KISS_INTERACTIONS:
            sim_info = TurboManagerUtil.Sim.get_sim_info(TurboInteractionUtil.get_interaction_sim(interaction_instance))
            target_sim_info = TurboManagerUtil.Sim.get_sim_info(TurboInteractionUtil.get_interaction_target(interaction_instance))
            if target_sim_info is not None and (has_sim_trait(target_sim_info, SimTrait.WW_CUMSLUT) or has_sim_trait(target_sim_info, SimTrait.SLOB)):
                if has_sim_cas_part_id(sim_info, CUM_FACE_LAYER):
                    apply_sim_cum_layer(target_sim_info, (CumLayerType.FACE,))

