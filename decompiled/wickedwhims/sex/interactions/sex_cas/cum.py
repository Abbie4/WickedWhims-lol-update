'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from enums.traits_enum import SimTrait
from turbolib.manager_util import TurboManagerUtil
from turbolib.types_util import TurboTypesUtil
from turbolib.wrappers.interactions import TurboImmediateSuperInteraction, TurboInteractionStartMixin
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.sex.cas_cum_handler import get_cum_layer_cas_id, apply_sim_cum_layer, CumLayerType
from wickedwhims.sex.settings.sex_settings import SexSetting, get_sex_setting
from wickedwhims.utils_cas import has_sim_cas_part_id
from wickedwhims.utils_traits import has_sim_trait

def _can_sim_receive_cum(interaction_sim, interaction_target, cum_type):
    if interaction_target is None or not TurboTypesUtil.Sims.is_sim(interaction_target):
        return False
    if not get_sex_setting(SexSetting.MANUAL_NPC_SEX_STATE, variable_type=bool):
        if sim_ev(interaction_sim).active_sex_handler is None:
            return False
        if sim_ev(interaction_sim).active_sex_handler is not sim_ev(interaction_target).active_sex_handler:
            return False
    elif sim_ev(interaction_target).active_sex_handler is None:
        return False
    active_sex_handler = sim_ev(interaction_target).active_sex_handler
    if active_sex_handler.is_at_climax is False:
        return False
    if cum_type == CumLayerType.VAGINA and has_sim_trait(interaction_target, SimTrait.GENDEROPTIONS_TOILET_STANDING):
        return False
    has_sim_that_can_cum = False
    for actor_sim_info in active_sex_handler.get_actors_sim_info_gen():
        if TurboManagerUtil.Sim.get_sim_id(actor_sim_info) == TurboManagerUtil.Sim.get_sim_id(interaction_target):
            pass
        if not has_sim_trait(actor_sim_info, SimTrait.GENDEROPTIONS_TOILET_STANDING):
            pass
        has_sim_that_can_cum = True
        break
    if has_sim_that_can_cum is False:
        return False
    if has_sim_cas_part_id(interaction_target, get_cum_layer_cas_id(cum_type)):
        return False
    return True

class CumApplyOnFaceInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'CumApplyOnFaceInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _can_sim_receive_cum(cls.get_interaction_sim(interaction_context), interaction_target, CumLayerType.FACE)

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return apply_sim_cum_layer(cls.get_interaction_target(interaction_instance), (CumLayerType.FACE,), force=True)

class CumApplyOnChestInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'CumApplyOnChestInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _can_sim_receive_cum(cls.get_interaction_sim(interaction_context), interaction_target, CumLayerType.CHEST)

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return apply_sim_cum_layer(cls.get_interaction_target(interaction_instance), (CumLayerType.CHEST,), force=True)

class CumApplyOnBackInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'CumApplyOnBackInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _can_sim_receive_cum(cls.get_interaction_sim(interaction_context), interaction_target, CumLayerType.BACK)

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return apply_sim_cum_layer(cls.get_interaction_target(interaction_instance), (CumLayerType.BACK,), force=True)

class CumApplyOnVaginaInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'CumApplyOnVaginaInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _can_sim_receive_cum(cls.get_interaction_sim(interaction_context), interaction_target, CumLayerType.VAGINA)

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return apply_sim_cum_layer(cls.get_interaction_target(interaction_instance), (CumLayerType.VAGINA,), force=True)

class CumApplyOnButtInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'CumApplyOnButtInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _can_sim_receive_cum(cls.get_interaction_sim(interaction_context), interaction_target, CumLayerType.BUTT)

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return apply_sim_cum_layer(cls.get_interaction_target(interaction_instance), (CumLayerType.BUTT,), force=True)

class CumApplyOnFeetInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'CumApplyOnFeetInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _can_sim_receive_cum(cls.get_interaction_sim(interaction_context), interaction_target, CumLayerType.FEET)

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return apply_sim_cum_layer(cls.get_interaction_target(interaction_instance), (CumLayerType.FEET,), force=True)

