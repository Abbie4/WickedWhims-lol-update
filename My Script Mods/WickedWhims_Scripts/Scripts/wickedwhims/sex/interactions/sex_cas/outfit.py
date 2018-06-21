from turbolib.cas_util import TurboCASUtil
from turbolib.manager_util import TurboManagerUtil
from turbolib.sim_util import TurboSimUtil
from turbolib.types_util import TurboTypesUtil
from turbolib.ui_util import TurboUIUtil
from turbolib.wrappers.interactions import TurboImmediateSuperInteraction, TurboInteractionStartMixin
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.nudity.nudity_settings import CompleteUndressingTypeSetting, NuditySetting, get_nudity_setting
from wickedwhims.sex.settings.sex_settings import SexSetting, get_sex_setting
from wickedwhims.sex.sex_handlers.active.utils.outfit import undress_sim
from wickedwhims.sxex_bridge.body import BodyState, get_sim_actual_body_state, set_sim_bottom_naked_state, set_sim_top_naked_state, get_sim_body_state
from wickedwhims.sxex_bridge.nudity import reset_sim_bathing_outfits
from wickedwhims.sxex_bridge.outfit import strip_outfit, dress_up_outfit, StripType
from wickedwhims.sxex_bridge.underwear import set_sim_top_underwear_state, set_sim_bottom_underwear_state, is_underwear_outfit
from wickedwhims.utils_cas import get_sim_outfit_cas_part_from_bodytype, has_sim_body_part, copy_outfit_to_special, get_modified_outfit
from wickedwhims.utils_interfaces import display_outfit_picker_dialog

class ChangeActorOutfitInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'ChangeActorOutfitInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        if interaction_target is None or not TurboTypesUtil.Sims.is_sim(interaction_target):
            return False
        if get_sex_setting(SexSetting.INSTANT_UNDRESSING_STATE, variable_type=bool):
            return True
        interaction_sim = cls.get_interaction_sim(interaction_context)
        if not get_sex_setting(SexSetting.MANUAL_NPC_SEX_STATE, variable_type=bool):
            if sim_ev(interaction_sim).active_sex_handler is None:
                return False
            if sim_ev(interaction_sim).active_sex_handler is not sim_ev(interaction_target).active_sex_handler:
                return False
        elif sim_ev(interaction_target).active_sex_handler is None:
            return False
        return True

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        target = cls.get_interaction_target(interaction_instance)
        outfits = list()

        def _outfit_picker_callback(dialog):
            if not TurboUIUtil.ObjectPickerDialog.get_response_result(dialog):
                return
            picked_outfit = TurboUIUtil.ObjectPickerDialog.get_tag_result(dialog)
            dress_up_outfit(target, override_outfit_category_and_index=picked_outfit)
            active_sex_handler = sim_ev(target).active_sex_handler
            if active_sex_handler is not None:
                actor_data = active_sex_handler.get_animation_instance().get_actor(active_sex_handler.get_actor_id_by_sim_id(TurboManagerUtil.Sim.get_sim_id(target)))
                undress_sim(target, actor_data=actor_data)

        for outfit_category in (TurboCASUtil.OutfitCategory.EVERYDAY, TurboCASUtil.OutfitCategory.FORMAL, TurboCASUtil.OutfitCategory.ATHLETIC, TurboCASUtil.OutfitCategory.SLEEP, TurboCASUtil.OutfitCategory.PARTY, TurboCASUtil.OutfitCategory.SWIMWEAR, TurboCASUtil.OutfitCategory.HOTWEATHER, TurboCASUtil.OutfitCategory.COLDWEATHER):
            for outfit_index in range(TurboCASUtil.OutfitCategory.get_maximum_outfits_for_outfit_category(outfit_category)):
                while TurboSimUtil.CAS.has_outfit(target, (outfit_category, outfit_index)):
                    outfits.append((outfit_category, outfit_index))
        display_outfit_picker_dialog(title=4119196202, title_tokens=(target,), outfits=outfits, sim=target, callback=_outfit_picker_callback)


def _has_outfit_parts_to_undress(interaction_sim, interaction_target, body_types):
    if interaction_target is None or not TurboTypesUtil.Sims.is_sim(interaction_target):
        return False
    if not get_sex_setting(SexSetting.INSTANT_UNDRESSING_STATE, variable_type=bool):
        if not get_sex_setting(SexSetting.MANUAL_NPC_SEX_STATE, variable_type=bool):
            if sim_ev(interaction_sim).active_sex_handler is None:
                return False
            if sim_ev(interaction_sim).active_sex_handler is not sim_ev(interaction_target).active_sex_handler:
                return False
                if sim_ev(interaction_target).active_sex_handler is None:
                    return False
        elif sim_ev(interaction_target).active_sex_handler is None:
            return False
    for body_type in body_types:
        body_state = get_sim_actual_body_state(interaction_target, body_type)
        if body_state == BodyState.NUDE:
            pass
        part_id = get_sim_outfit_cas_part_from_bodytype(interaction_target, body_type)
        if part_id == -1:
            pass
    return False


class UndressActorTopInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'UndressActorTopInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _has_outfit_parts_to_undress(cls.get_interaction_sim(interaction_context), interaction_target, (TurboCASUtil.BodyType.UPPER_BODY,))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        target = cls.get_interaction_target(interaction_instance)
        strip_type_top = StripType.NUDE if get_sim_body_state(target, TurboCASUtil.BodyType.UPPER_BODY) == BodyState.UNDERWEAR else StripType.UNDERWEAR if TurboSimUtil.Gender.is_female(target) and is_underwear_outfit(get_modified_outfit(target)[0]) else StripType.NUDE
        strip_outfit(target, strip_type_top=strip_type_top)
        set_sim_top_naked_state(target, strip_type_top == StripType.NUDE)
        set_sim_top_underwear_state(target, strip_type_top != StripType.NUDE)
        return True


class UndressActorBottomInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'UndressActorBottomInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _has_outfit_parts_to_undress(cls.get_interaction_sim(interaction_context), interaction_target, (TurboCASUtil.BodyType.LOWER_BODY,))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        target = cls.get_interaction_target(interaction_instance)
        strip_type_bottom = StripType.NUDE if get_sim_body_state(target, TurboCASUtil.BodyType.LOWER_BODY) == BodyState.UNDERWEAR else StripType.UNDERWEAR if is_underwear_outfit(get_modified_outfit(target)[0]) else StripType.NUDE
        strip_outfit(target, strip_type_bottom=strip_type_bottom)
        set_sim_bottom_naked_state(target, strip_type_bottom == StripType.NUDE)
        set_sim_bottom_underwear_state(target, strip_type_bottom != StripType.NUDE)
        return True


class UndressActorOutfitInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'UndressActorOutfitInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _has_outfit_parts_to_undress(cls.get_interaction_sim(interaction_context), interaction_target, (TurboCASUtil.BodyType.FULL_BODY, TurboCASUtil.BodyType.UPPER_BODY, TurboCASUtil.BodyType.LOWER_BODY))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        target = cls.get_interaction_target(interaction_instance)
        strip_type_top = StripType.NUDE if get_sim_body_state(target, TurboCASUtil.BodyType.UPPER_BODY) == BodyState.UNDERWEAR else StripType.UNDERWEAR if TurboSimUtil.Gender.is_female(target) and is_underwear_outfit(get_modified_outfit(target)[0]) else StripType.NUDE
        strip_type_bottom = StripType.NUDE if get_sim_body_state(target, TurboCASUtil.BodyType.LOWER_BODY) == BodyState.UNDERWEAR else StripType.UNDERWEAR if is_underwear_outfit(get_modified_outfit(target)[0]) else StripType.NUDE
        strip_outfit(target, strip_type_top=strip_type_top, strip_type_bottom=strip_type_bottom)
        set_sim_top_naked_state(target, strip_type_top == StripType.NUDE)
        set_sim_top_underwear_state(target, strip_type_top != StripType.NUDE)
        set_sim_bottom_naked_state(target, strip_type_bottom == StripType.NUDE)
        set_sim_bottom_underwear_state(target, strip_type_bottom != StripType.NUDE)
        return True


class UndressActorCompletelyInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'UndressActorCompletelyInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _has_outfit_parts_to_undress(cls.get_interaction_sim(interaction_context), interaction_target, (TurboCASUtil.BodyType.UPPER_BODY, TurboCASUtil.BodyType.LOWER_BODY, TurboCASUtil.BodyType.SHOES, TurboCASUtil.BodyType.FULL_BODY, TurboCASUtil.BodyType.HAT, TurboCASUtil.BodyType.CUMMERBUND, TurboCASUtil.BodyType.EARRINGS, TurboCASUtil.BodyType.GLASSES, TurboCASUtil.BodyType.NECKLACE, TurboCASUtil.BodyType.GLOVES, TurboCASUtil.BodyType.WRIST_LEFT, TurboCASUtil.BodyType.WRIST_RIGHT, TurboCASUtil.BodyType.SOCKS, TurboCASUtil.BodyType.TIGHTS))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        target = cls.get_interaction_target(interaction_instance)
        if get_nudity_setting(NuditySetting.COMPLETE_UNDRESSING_TYPE, variable_type=int) == CompleteUndressingTypeSetting.DEFAULT:
            reset_sim_bathing_outfits(target)
            copy_outfit_to_special(target, set_special_outfit=True, outfit_category_and_index=(TurboCASUtil.OutfitCategory.BATHING, 0), override_outfit_parts={115: sim_ev(target).nude_outfit_parts[115]})
        else:
            copy_outfit_to_special(target, set_special_outfit=True, outfit_category_and_index=get_modified_outfit(target), override_outfit_parts={TurboCASUtil.BodyType.UPPER_BODY: sim_ev(target).nude_outfit_parts[TurboCASUtil.BodyType.UPPER_BODY], TurboCASUtil.BodyType.LOWER_BODY: sim_ev(target).nude_outfit_parts[TurboCASUtil.BodyType.LOWER_BODY], TurboCASUtil.BodyType.SHOES: sim_ev(target).nude_outfit_parts[TurboCASUtil.BodyType.SHOES], TurboCASUtil.BodyType.FULL_BODY: 0, TurboCASUtil.BodyType.HAT: 0, TurboCASUtil.BodyType.CUMMERBUND: 0, TurboCASUtil.BodyType.EARRINGS: 0, TurboCASUtil.BodyType.GLASSES: 0, TurboCASUtil.BodyType.NECKLACE: 0, TurboCASUtil.BodyType.GLOVES: 0, TurboCASUtil.BodyType.WRIST_LEFT: 0, TurboCASUtil.BodyType.WRIST_RIGHT: 0, TurboCASUtil.BodyType.SOCKS: 0, TurboCASUtil.BodyType.TIGHTS: 0, 115: sim_ev(target).nude_outfit_parts[115]})
        set_sim_top_naked_state(target, True)
        set_sim_bottom_naked_state(target, True)
        set_sim_top_underwear_state(target, False)
        set_sim_bottom_underwear_state(target, False)
        return True


class UndressActorShoesInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'UndressActorShoesInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _has_outfit_parts_to_undress(cls.get_interaction_sim(interaction_context), interaction_target, (TurboCASUtil.BodyType.SHOES,))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return strip_outfit(cls.get_interaction_target(interaction_instance), strip_bodytype=TurboCASUtil.BodyType.SHOES)


class UndressActorHatInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'UndressActorHatInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _has_outfit_parts_to_undress(cls.get_interaction_sim(interaction_context), interaction_target, (TurboCASUtil.BodyType.HAT,))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return strip_outfit(cls.get_interaction_target(interaction_instance), strip_bodytype=TurboCASUtil.BodyType.HAT)


class UndressActorLeggingsInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'UndressActorLeggingsInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _has_outfit_parts_to_undress(cls.get_interaction_sim(interaction_context), interaction_target, (TurboCASUtil.BodyType.TIGHTS,))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return strip_outfit(cls.get_interaction_target(interaction_instance), strip_bodytype=TurboCASUtil.BodyType.TIGHTS)


class UndressActorSocksInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'UndressActorSocksInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _has_outfit_parts_to_undress(cls.get_interaction_sim(interaction_context), interaction_target, (TurboCASUtil.BodyType.SOCKS,))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return strip_outfit(cls.get_interaction_target(interaction_instance), strip_bodytype=TurboCASUtil.BodyType.SOCKS)


class UndressActorGlovesInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'UndressActorGlovesInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _has_outfit_parts_to_undress(cls.get_interaction_sim(interaction_context), interaction_target, (TurboCASUtil.BodyType.GLOVES,))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return strip_outfit(cls.get_interaction_target(interaction_instance), strip_bodytype=TurboCASUtil.BodyType.GLOVES)


class UndressActorGlassesInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'UndressActorGlassesInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _has_outfit_parts_to_undress(cls.get_interaction_sim(interaction_context), interaction_target, (TurboCASUtil.BodyType.GLASSES,))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return strip_outfit(cls.get_interaction_target(interaction_instance), strip_bodytype=TurboCASUtil.BodyType.GLASSES)


class UndressActorHeadInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'UndressActorHeadInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _has_outfit_parts_to_undress(cls.get_interaction_sim(interaction_context), interaction_target, (TurboCASUtil.BodyType.EARRINGS, TurboCASUtil.BodyType.NECKLACE, TurboCASUtil.BodyType.LIP_RING_LEFT, TurboCASUtil.BodyType.LIP_RING_RIGHT, TurboCASUtil.BodyType.NOSE_RING_LEFT, TurboCASUtil.BodyType.NOSE_RING_RIGHT, TurboCASUtil.BodyType.BROW_RING_LEFT, TurboCASUtil.BodyType.BROW_RING_RIGHT))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        if has_sim_body_part(cls.get_interaction_target(interaction_instance), TurboCASUtil.BodyType.EARRINGS):
            strip_outfit(cls.get_interaction_target(interaction_instance), strip_bodytype=TurboCASUtil.BodyType.EARRINGS)
        if has_sim_body_part(cls.get_interaction_target(interaction_instance), TurboCASUtil.BodyType.NECKLACE):
            strip_outfit(cls.get_interaction_target(interaction_instance), strip_bodytype=TurboCASUtil.BodyType.NECKLACE)
        if has_sim_body_part(cls.get_interaction_target(interaction_instance), TurboCASUtil.BodyType.LIP_RING_LEFT):
            strip_outfit(cls.get_interaction_target(interaction_instance), strip_bodytype=TurboCASUtil.BodyType.LIP_RING_LEFT)
        if has_sim_body_part(cls.get_interaction_target(interaction_instance), TurboCASUtil.BodyType.LIP_RING_RIGHT):
            strip_outfit(cls.get_interaction_target(interaction_instance), strip_bodytype=TurboCASUtil.BodyType.LIP_RING_RIGHT)
        if has_sim_body_part(cls.get_interaction_target(interaction_instance), TurboCASUtil.BodyType.NOSE_RING_LEFT):
            strip_outfit(cls.get_interaction_target(interaction_instance), strip_bodytype=TurboCASUtil.BodyType.NOSE_RING_LEFT)
        if has_sim_body_part(cls.get_interaction_target(interaction_instance), TurboCASUtil.BodyType.NOSE_RING_RIGHT):
            strip_outfit(cls.get_interaction_target(interaction_instance), strip_bodytype=TurboCASUtil.BodyType.NOSE_RING_RIGHT)
        if has_sim_body_part(cls.get_interaction_target(interaction_instance), TurboCASUtil.BodyType.BROW_RING_LEFT):
            strip_outfit(cls.get_interaction_target(interaction_instance), strip_bodytype=TurboCASUtil.BodyType.BROW_RING_LEFT)
        if has_sim_body_part(cls.get_interaction_target(interaction_instance), TurboCASUtil.BodyType.BROW_RING_RIGHT):
            strip_outfit(cls.get_interaction_target(interaction_instance), strip_bodytype=TurboCASUtil.BodyType.BROW_RING_RIGHT)
        return True


class UndressActorLeftHandInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'UndressActorLeftHandInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _has_outfit_parts_to_undress(cls.get_interaction_sim(interaction_context), interaction_target, (TurboCASUtil.BodyType.WRIST_LEFT, TurboCASUtil.BodyType.INDEX_FINGER_LEFT, TurboCASUtil.BodyType.RING_FINGER_LEFT, TurboCASUtil.BodyType.MIDDLE_FINGER_LEFT))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        if has_sim_body_part(cls.get_interaction_target(interaction_instance), TurboCASUtil.BodyType.WRIST_LEFT):
            strip_outfit(cls.get_interaction_target(interaction_instance), strip_bodytype=TurboCASUtil.BodyType.WRIST_LEFT)
        if has_sim_body_part(cls.get_interaction_target(interaction_instance), TurboCASUtil.BodyType.INDEX_FINGER_LEFT):
            strip_outfit(cls.get_interaction_target(interaction_instance), strip_bodytype=TurboCASUtil.BodyType.INDEX_FINGER_LEFT)
        if has_sim_body_part(cls.get_interaction_target(interaction_instance), TurboCASUtil.BodyType.RING_FINGER_LEFT):
            strip_outfit(cls.get_interaction_target(interaction_instance), strip_bodytype=TurboCASUtil.BodyType.RING_FINGER_LEFT)
        if has_sim_body_part(cls.get_interaction_target(interaction_instance), TurboCASUtil.BodyType.MIDDLE_FINGER_LEFT):
            strip_outfit(cls.get_interaction_target(interaction_instance), strip_bodytype=TurboCASUtil.BodyType.MIDDLE_FINGER_LEFT)
        return True


class UndressActorRightHandInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'UndressActorRightHandInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _has_outfit_parts_to_undress(cls.get_interaction_sim(interaction_context), interaction_target, (TurboCASUtil.BodyType.WRIST_RIGHT, TurboCASUtil.BodyType.INDEX_FINGER_RIGHT, TurboCASUtil.BodyType.RING_FINGER_RIGHT, TurboCASUtil.BodyType.MIDDLE_FINGER_RIGHT))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        if has_sim_body_part(cls.get_interaction_target(interaction_instance), TurboCASUtil.BodyType.WRIST_RIGHT):
            strip_outfit(cls.get_interaction_target(interaction_instance), strip_bodytype=TurboCASUtil.BodyType.WRIST_RIGHT)
        if has_sim_body_part(cls.get_interaction_target(interaction_instance), TurboCASUtil.BodyType.INDEX_FINGER_RIGHT):
            strip_outfit(cls.get_interaction_target(interaction_instance), strip_bodytype=TurboCASUtil.BodyType.INDEX_FINGER_RIGHT)
        if has_sim_body_part(cls.get_interaction_target(interaction_instance), TurboCASUtil.BodyType.RING_FINGER_RIGHT):
            strip_outfit(cls.get_interaction_target(interaction_instance), strip_bodytype=TurboCASUtil.BodyType.RING_FINGER_RIGHT)
        if has_sim_body_part(cls.get_interaction_target(interaction_instance), TurboCASUtil.BodyType.MIDDLE_FINGER_RIGHT):
            strip_outfit(cls.get_interaction_target(interaction_instance), strip_bodytype=TurboCASUtil.BodyType.MIDDLE_FINGER_RIGHT)
        return True


class UndressActorOtherAccessoriesInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'UndressActorOtherAccessoriesInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _has_outfit_parts_to_undress(cls.get_interaction_sim(interaction_context), interaction_target, (TurboCASUtil.BodyType.CUMMERBUND,))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return strip_outfit(cls.get_interaction_target(interaction_instance), strip_bodytype=TurboCASUtil.BodyType.CUMMERBUND)

