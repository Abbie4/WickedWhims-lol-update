from enums.traits_enum import SimTrait
from turbolib.cas_util import TurboCASUtil
from turbolib.interaction_util import TurboInteractionUtil
from turbolib.sim_util import TurboSimUtil
from turbolib.world_util import TurboWorldUtil
from turbolib.wrappers.interactions import TurboSuperInteraction, TurboInteractionSetupMixin, TurboInteractionConstraintMixin, TurboInteractionBasicElementsMixin
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.nudity.notifications_handler import nudity_notification
from wickedwhims.nudity.nudity_settings import NuditySetting, get_nudity_setting, CompleteUndressingTypeSetting
from wickedwhims.nudity.permissions.test import NudityPermissionDenied, has_sim_permission_for_nudity
from wickedwhims.sxex_bridge.body import BodyState, set_sim_top_naked_state, set_sim_bottom_naked_state, is_sim_outfit_fullbody, get_sim_actual_body_state, get_sim_body_state
from wickedwhims.sxex_bridge.nudity import reset_sim_bathing_outfits
from wickedwhims.sxex_bridge.outfit import StripType, strip_outfit, dress_up_outfit
from wickedwhims.sxex_bridge.sex import is_sim_going_to_sex, is_sim_in_sex
from wickedwhims.sxex_bridge.underwear import is_sim_top_underwear, is_sim_bottom_underwear, is_underwear_outfit, set_sim_top_underwear_state, set_sim_bottom_underwear_state
from wickedwhims.utils_cas import get_modified_outfit, copy_outfit_to_special
from wickedwhims.utils_traits import has_sim_trait

class _NudityUndressOutfitTopInteraction(TurboSuperInteraction, TurboInteractionSetupMixin, TurboInteractionConstraintMixin, TurboInteractionBasicElementsMixin):
    __qualname__ = '_NudityUndressOutfitTopInteraction'

    @classmethod
    def on_constraint(cls, interaction_instance, interaction_sim, interaction_target):
        return cls.get_stand_posture_constraint()

    @classmethod
    def on_interaction_setup(cls, interaction_instance):
        if _has_permission_to_undress(cls.get_interaction_sim(interaction_instance), cls.get_interaction_context(interaction_instance)):
            return True
        cls.kill(interaction_instance)
        return False

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        sim = cls.get_interaction_sim(interaction_context)
        if not get_nudity_setting(NuditySetting.TEENS_NUDITY_STATE, variable_type=bool) and (TurboSimUtil.Age.get_age(sim) == TurboSimUtil.Age.TEEN or TurboSimUtil.Age.get_age(sim) == TurboSimUtil.Age.CHILD):
            return False
        if is_sim_in_sex(sim) or is_sim_going_to_sex(sim):
            return False
        if is_sim_outfit_fullbody(sim):
            return False
        if get_sim_body_state(sim, TurboCASUtil.BodyType.UPPER_BODY) == BodyState.OUTFIT:
            return True
        return False

    @classmethod
    def on_building_basic_elements(cls, interaction_instance, sequence):
        sim = cls.get_interaction_sim(interaction_instance)
        has_top_underwear_on = TurboSimUtil.Gender.is_female(sim) and (is_underwear_outfit(get_modified_outfit(sim)[0]) and is_sim_top_underwear(sim))
        strip_type_top = StripType.UNDERWEAR if has_top_underwear_on else StripType.NUDE
        strip_result = strip_outfit(sim, strip_type_top=strip_type_top, skip_outfit_change=True)
        if strip_result is True:
            set_sim_top_naked_state(sim, strip_type_top == StripType.NUDE)
            set_sim_top_underwear_state(sim, strip_type_top == StripType.UNDERWEAR)
            nudity_notification(text=3743260351, text_tokens=(sim,), icon=sim, sims=(sim,), is_autonomy=cls.get_interaction_source(interaction_instance) == TurboInteractionUtil.InteractionSource.AUTONOMY)
            return TurboSimUtil.CAS.get_change_outfit_element(sim, (TurboCASUtil.OutfitCategory.SPECIAL, 0), do_spin=True, interaction=interaction_instance)

    @classmethod
    def on_interaction_run(cls, interaction_instance):
        return True


class NaturismUndressOutfitTopInteraction(_NudityUndressOutfitTopInteraction):
    __qualname__ = 'NaturismUndressOutfitTopInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        sim = cls.get_interaction_sim(interaction_context)
        if has_sim_trait(sim, SimTrait.WW_EXHIBITIONIST):
            return False
        return super().on_interaction_test(interaction_context, interaction_target)


class ExhibitionismUndressOutfitTopInteraction(_NudityUndressOutfitTopInteraction):
    __qualname__ = 'ExhibitionismUndressOutfitTopInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        sim = cls.get_interaction_sim(interaction_context)
        if not has_sim_trait(sim, SimTrait.WW_EXHIBITIONIST):
            return False
        return super().on_interaction_test(interaction_context, interaction_target)


class _NudityUndressOutfitBottomInteraction(TurboSuperInteraction, TurboInteractionSetupMixin, TurboInteractionConstraintMixin, TurboInteractionBasicElementsMixin):
    __qualname__ = '_NudityUndressOutfitBottomInteraction'

    @classmethod
    def on_constraint(cls, interaction_instance, interaction_sim, interaction_target):
        return cls.get_stand_posture_constraint()

    @classmethod
    def on_interaction_setup(cls, interaction_instance):
        if _has_permission_to_undress(cls.get_interaction_sim(interaction_instance), cls.get_interaction_context(interaction_instance)):
            return True
        cls.kill(interaction_instance)
        return False

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        sim = cls.get_interaction_sim(interaction_context)
        if not get_nudity_setting(NuditySetting.TEENS_NUDITY_STATE, variable_type=bool) and (TurboSimUtil.Age.get_age(sim) == TurboSimUtil.Age.TEEN or TurboSimUtil.Age.get_age(sim) == TurboSimUtil.Age.CHILD):
            return False
        if is_sim_in_sex(sim) or is_sim_going_to_sex(sim):
            return False
        if is_sim_outfit_fullbody(sim):
            return False
        if get_sim_body_state(sim, TurboCASUtil.BodyType.LOWER_BODY) == BodyState.OUTFIT:
            return True
        return False

    @classmethod
    def on_building_basic_elements(cls, interaction_instance, sequence):
        sim = cls.get_interaction_sim(interaction_instance)
        has_bottom_underwear_on = is_underwear_outfit(get_modified_outfit(sim)[0]) and is_sim_bottom_underwear(sim)
        strip_type_bottom = StripType.UNDERWEAR if has_bottom_underwear_on else StripType.NUDE
        strip_result = strip_outfit(sim, strip_type_bottom=strip_type_bottom, skip_outfit_change=True)
        if strip_result is True:
            set_sim_bottom_naked_state(sim, strip_type_bottom == StripType.NUDE)
            set_sim_bottom_underwear_state(sim, strip_type_bottom == StripType.UNDERWEAR)
            nudity_notification(text=3069021969, text_tokens=(sim,), icon=sim, sims=(sim,), is_autonomy=cls.get_interaction_source(interaction_instance) == TurboInteractionUtil.InteractionSource.AUTONOMY)
            return TurboSimUtil.CAS.get_change_outfit_element(sim, (TurboCASUtil.OutfitCategory.SPECIAL, 0), do_spin=True, interaction=interaction_instance)

    @classmethod
    def on_interaction_run(cls, interaction_instance):
        return True


class NaturismUndressOutfitBottomInteraction(_NudityUndressOutfitBottomInteraction):
    __qualname__ = 'NaturismUndressOutfitBottomInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        sim = cls.get_interaction_sim(interaction_context)
        if has_sim_trait(sim, SimTrait.WW_EXHIBITIONIST):
            return False
        return super().on_interaction_test(interaction_context, interaction_target)


class ExhibitionismUndressOutfitBottomInteraction(_NudityUndressOutfitBottomInteraction):
    __qualname__ = 'ExhibitionismUndressOutfitBottomInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        sim = cls.get_interaction_sim(interaction_context)
        if not has_sim_trait(sim, SimTrait.WW_EXHIBITIONIST):
            return False
        return super().on_interaction_test(interaction_context, interaction_target)


class _NudityUndressOutfitShoesInteraction(TurboSuperInteraction, TurboInteractionSetupMixin, TurboInteractionConstraintMixin, TurboInteractionBasicElementsMixin):
    __qualname__ = '_NudityUndressOutfitShoesInteraction'

    @classmethod
    def on_constraint(cls, interaction_instance, interaction_sim, interaction_target):
        return cls.get_stand_posture_constraint()

    @classmethod
    def on_interaction_setup(cls, interaction_instance):
        return True

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        sim = cls.get_interaction_sim(interaction_context)
        if is_sim_in_sex(sim) or is_sim_going_to_sex(sim):
            return False
        if get_sim_body_state(sim, TurboCASUtil.BodyType.SHOES) == BodyState.OUTFIT:
            return True
        return False

    @classmethod
    def on_building_basic_elements(cls, interaction_instance, sequence):
        sim = cls.get_interaction_sim(interaction_instance)
        strip_result = strip_outfit(sim, strip_bodytype=8, skip_outfit_change=True)
        if strip_result is True:
            nudity_notification(text=4281967896, text_tokens=(sim,), icon=sim, sims=(sim,), is_autonomy=cls.get_interaction_source(interaction_instance) == TurboInteractionUtil.InteractionSource.AUTONOMY)
            return TurboSimUtil.CAS.get_change_outfit_element(sim, (TurboCASUtil.OutfitCategory.SPECIAL, 0), do_spin=True, interaction=interaction_instance)

    @classmethod
    def on_interaction_run(cls, interaction_instance):
        return True


class NaturismUndressOutfitShoesInteraction(_NudityUndressOutfitShoesInteraction):
    __qualname__ = 'NaturismUndressOutfitShoesInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        sim = cls.get_interaction_sim(interaction_context)
        if has_sim_trait(sim, SimTrait.WW_EXHIBITIONIST):
            return False
        return super().on_interaction_test(interaction_context, interaction_target)


class ExhibitionismUndressOutfitShoesInteraction(_NudityUndressOutfitShoesInteraction):
    __qualname__ = 'ExhibitionismUndressOutfitShoesInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        sim = cls.get_interaction_sim(interaction_context)
        if not has_sim_trait(sim, SimTrait.WW_EXHIBITIONIST):
            return False
        return super().on_interaction_test(interaction_context, interaction_target)


class _NudityUndressOutfitInteraction(TurboSuperInteraction, TurboInteractionSetupMixin, TurboInteractionConstraintMixin, TurboInteractionBasicElementsMixin):
    __qualname__ = '_NudityUndressOutfitInteraction'

    @classmethod
    def on_constraint(cls, interaction_instance, interaction_sim, interaction_target):
        return cls.get_stand_posture_constraint()

    @classmethod
    def on_interaction_setup(cls, interaction_instance):
        if _has_permission_to_undress(cls.get_interaction_sim(interaction_instance), cls.get_interaction_context(interaction_instance)):
            return True
        cls.kill(interaction_instance)
        return False

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        sim = cls.get_interaction_sim(interaction_context)
        if not get_nudity_setting(NuditySetting.TEENS_NUDITY_STATE, variable_type=bool) and (TurboSimUtil.Age.get_age(sim) == TurboSimUtil.Age.TEEN or TurboSimUtil.Age.get_age(sim) == TurboSimUtil.Age.CHILD):
            return False
        if is_sim_in_sex(sim) or is_sim_going_to_sex(sim):
            return False
        if is_sim_outfit_fullbody(sim):
            return True
        if get_sim_body_state(sim, TurboCASUtil.BodyType.UPPER_BODY) == BodyState.OUTFIT and get_sim_body_state(sim, TurboCASUtil.BodyType.LOWER_BODY) == BodyState.OUTFIT:
            return True
        return False

    @classmethod
    def on_building_basic_elements(cls, interaction_instance, sequence):
        sim = cls.get_interaction_sim(interaction_instance)
        has_top_underwear_on = TurboSimUtil.Gender.is_female(sim) and (is_underwear_outfit(get_modified_outfit(sim)[0]) and is_sim_top_underwear(sim))
        has_bottom_underwear_on = is_underwear_outfit(get_modified_outfit(sim)[0]) and is_sim_bottom_underwear(sim)
        strip_type_top = StripType.UNDERWEAR if has_top_underwear_on else StripType.NUDE
        strip_type_bottom = StripType.UNDERWEAR if has_bottom_underwear_on else StripType.NUDE
        strip_result = strip_outfit(sim, strip_type_top=strip_type_top, strip_type_bottom=strip_type_bottom, skip_outfit_change=True)
        if strip_result is True:
            set_sim_top_naked_state(sim, strip_type_top == StripType.NUDE)
            set_sim_bottom_naked_state(sim, strip_type_bottom == StripType.NUDE)
            set_sim_top_underwear_state(sim, strip_type_top == StripType.UNDERWEAR)
            set_sim_bottom_underwear_state(sim, strip_type_bottom == StripType.UNDERWEAR)
            nudity_notification(text=2191667249, text_tokens=(sim,), icon=sim, sims=(sim,), is_autonomy=cls.get_interaction_source(interaction_instance) == TurboInteractionUtil.InteractionSource.AUTONOMY)
            return TurboSimUtil.CAS.get_change_outfit_element(sim, (TurboCASUtil.OutfitCategory.SPECIAL, 0), do_spin=True, interaction=interaction_instance)

    @classmethod
    def on_interaction_run(cls, interaction_instance):
        return True


class NaturismUndressOutfitInteraction(_NudityUndressOutfitInteraction):
    __qualname__ = 'NaturismUndressOutfitInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        sim = cls.get_interaction_sim(interaction_context)
        if has_sim_trait(sim, SimTrait.WW_EXHIBITIONIST):
            return False
        return super().on_interaction_test(interaction_context, interaction_target)


class ExhibitionismUndressOutfitInteraction(_NudityUndressOutfitInteraction):
    __qualname__ = 'ExhibitionismUndressOutfitInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        sim = cls.get_interaction_sim(interaction_context)
        if not has_sim_trait(sim, SimTrait.WW_EXHIBITIONIST):
            return False
        return super().on_interaction_test(interaction_context, interaction_target)


class _NudityUndressToNudeInteraction(TurboSuperInteraction, TurboInteractionSetupMixin, TurboInteractionConstraintMixin, TurboInteractionBasicElementsMixin):
    __qualname__ = '_NudityUndressToNudeInteraction'

    @classmethod
    def on_constraint(cls, interaction_instance, interaction_sim, interaction_target):
        return cls.get_stand_posture_constraint()

    @classmethod
    def on_interaction_setup(cls, interaction_instance):
        if _has_permission_to_undress(cls.get_interaction_sim(interaction_instance), cls.get_interaction_context(interaction_instance)):
            return True
        cls.kill(interaction_instance)
        return False

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        sim = cls.get_interaction_sim(interaction_context)
        if not get_nudity_setting(NuditySetting.TEENS_NUDITY_STATE, variable_type=bool) and (TurboSimUtil.Age.get_age(sim) == TurboSimUtil.Age.TEEN or TurboSimUtil.Age.get_age(sim) == TurboSimUtil.Age.CHILD):
            return False
        if is_sim_in_sex(sim) or is_sim_going_to_sex(sim):
            return False
        if is_sim_outfit_fullbody(sim):
            return True
        if get_sim_body_state(sim, TurboCASUtil.BodyType.UPPER_BODY) != BodyState.NUDE or get_sim_body_state(sim, TurboCASUtil.BodyType.LOWER_BODY) != BodyState.NUDE or get_sim_body_state(sim, TurboCASUtil.BodyType.SHOES) == BodyState.OUTFIT:
            return True
        return False

    @classmethod
    def on_building_basic_elements(cls, interaction_instance, sequence):
        sim = cls.get_interaction_sim(interaction_instance)
        if get_nudity_setting(NuditySetting.COMPLETE_UNDRESSING_TYPE, variable_type=int) == CompleteUndressingTypeSetting.DEFAULT:
            reset_sim_bathing_outfits(sim)
            strip_result = copy_outfit_to_special(sim, set_special_outfit=False, outfit_category_and_index=(TurboCASUtil.OutfitCategory.BATHING, 0), override_outfit_parts={115: sim_ev(sim).nude_outfit_parts[115]})
        else:
            strip_result = copy_outfit_to_special(sim, set_special_outfit=False, outfit_category_and_index=get_modified_outfit(sim), override_outfit_parts={TurboCASUtil.BodyType.UPPER_BODY: sim_ev(sim).nude_outfit_parts[TurboCASUtil.BodyType.UPPER_BODY], TurboCASUtil.BodyType.LOWER_BODY: sim_ev(sim).nude_outfit_parts[TurboCASUtil.BodyType.LOWER_BODY], TurboCASUtil.BodyType.SHOES: sim_ev(sim).nude_outfit_parts[TurboCASUtil.BodyType.SHOES], TurboCASUtil.BodyType.FULL_BODY: 0, TurboCASUtil.BodyType.HAT: 0, TurboCASUtil.BodyType.CUMMERBUND: 0, TurboCASUtil.BodyType.EARRINGS: 0, TurboCASUtil.BodyType.GLASSES: 0, TurboCASUtil.BodyType.NECKLACE: 0, TurboCASUtil.BodyType.GLOVES: 0, TurboCASUtil.BodyType.WRIST_LEFT: 0, TurboCASUtil.BodyType.WRIST_RIGHT: 0, TurboCASUtil.BodyType.SOCKS: 0, TurboCASUtil.BodyType.TIGHTS: 0, 115: sim_ev(sim).nude_outfit_parts[115]})
        if strip_result is True:
            set_sim_top_naked_state(sim, True)
            set_sim_bottom_naked_state(sim, True)
            set_sim_top_underwear_state(sim, False)
            set_sim_bottom_underwear_state(sim, False)
            nudity_notification(text=2191667249, text_tokens=(sim,), icon=sim, sims=(sim,), is_autonomy=cls.get_interaction_source(interaction_instance) == TurboInteractionUtil.InteractionSource.AUTONOMY)
            return TurboSimUtil.CAS.get_change_outfit_element(sim, (TurboCASUtil.OutfitCategory.SPECIAL, 0), do_spin=True, interaction=interaction_instance, dirty_outfit=True)

    @classmethod
    def on_interaction_run(cls, interaction_instance):
        return True


class NaturismUndressToNudeInteraction(_NudityUndressToNudeInteraction):
    __qualname__ = 'NaturismUndressToNudeInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        sim = cls.get_interaction_sim(interaction_context)
        if has_sim_trait(sim, SimTrait.WW_EXHIBITIONIST):
            return False
        return super().on_interaction_test(interaction_context, interaction_target)


class ExhibitionismUndressToNudeInteraction(_NudityUndressToNudeInteraction):
    __qualname__ = 'ExhibitionismUndressToNudeInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        sim = cls.get_interaction_sim(interaction_context)
        if not has_sim_trait(sim, SimTrait.WW_EXHIBITIONIST):
            return False
        return super().on_interaction_test(interaction_context, interaction_target)


def _has_permission_to_undress(interaction_sim, interaction_context):
    (has_permission, denied_permissions) = has_sim_permission_for_nudity(interaction_sim, nudity_setting_test=True)
    if has_permission is True:
        return True
    is_autonomy = interaction_context == TurboInteractionUtil.InteractionSource.AUTONOMY
    if is_autonomy is True:
        return False
    text_tokens = [interaction_sim]
    for denied_permission in denied_permissions:
        if denied_permission is None:
            continue
        if denied_permission == NudityPermissionDenied.NOT_AT_HOME:
            text_tokens.append(2434379342)
        elif denied_permission == NudityPermissionDenied.OUTSIDE:
            text_tokens.append(14125364)
        else:
            if denied_permission == NudityPermissionDenied.TOO_MANY_SIMS_AROUND:
                text_tokens.append(902300171)
    for _ in range(11 - len(text_tokens)):
        text_tokens.append(0)
    nudity_notification(text=3224264085, text_tokens=text_tokens, icon=interaction_sim, sims=(interaction_sim,), is_autonomy=is_autonomy)
    return False


class _NudityDressUpOutfitInteraction(TurboSuperInteraction, TurboInteractionConstraintMixin, TurboInteractionBasicElementsMixin):
    __qualname__ = '_NudityDressUpOutfitInteraction'

    @classmethod
    def on_constraint(cls, interaction_instance, interaction_sim, interaction_target):
        return cls.get_stand_posture_constraint()

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        sim = cls.get_interaction_sim(interaction_context)
        if is_sim_outfit_fullbody(sim):
            return False
        if is_sim_in_sex(sim) or is_sim_going_to_sex(sim):
            return False
        if TurboSimUtil.CAS.get_current_outfit(sim)[0] == TurboCASUtil.OutfitCategory.BATHING:
            return True
        if get_sim_actual_body_state(sim, 6) != BodyState.OUTFIT or get_sim_actual_body_state(sim, 7) != BodyState.OUTFIT:
            return True
        return False

    @classmethod
    def on_building_basic_elements(cls, interaction_instance, sequence):
        sim = cls.get_interaction_sim(interaction_instance)
        is_autonomy = cls.get_interaction_source(interaction_instance) == TurboInteractionUtil.InteractionSource.AUTONOMY
        if TurboSimUtil.Sim.is_player(sim) and is_autonomy:
            text_tokens = [sim]
            if is_autonomy is True and sim_ev(sim).last_nudity_denied_permissions is not None:
                for denied_permission in sim_ev(sim).last_nudity_denied_permissions:
                    if denied_permission == NudityPermissionDenied.NOT_AT_HOME:
                        text_tokens.append(2434379342)
                    elif denied_permission == NudityPermissionDenied.OUTSIDE:
                        text_tokens.append(14125364)
                    else:
                        if denied_permission == NudityPermissionDenied.TOO_MANY_SIMS_AROUND:
                            text_tokens.append(902300171)
            for _ in range(11 - len(text_tokens)):
                text_tokens.append(0)
            nudity_notification(text=2998371344, text_tokens=text_tokens, icon=sim, sims=(sim,), is_autonomy=is_autonomy)
        sim_ev(sim).last_nudity_denied_permissions = None
        outfit_category_and_index = dress_up_outfit(sim, skip_outfit_change=True)
        return TurboSimUtil.CAS.get_change_outfit_element(sim, outfit_category_and_index, do_spin=True, interaction=interaction_instance, dirty_outfit=True)

    @classmethod
    def on_interaction_run(cls, interaction_instance):
        sim = cls.get_interaction_sim(interaction_instance)
        sim_ev(sim).last_nudity_autonomy = TurboWorldUtil.Time.get_absolute_ticks() + 360000
        return True


class NaturismDressUpOutfitInteraction(_NudityDressUpOutfitInteraction):
    __qualname__ = 'NaturismDressUpOutfitInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        sim = cls.get_interaction_sim(interaction_context)
        if has_sim_trait(sim, SimTrait.WW_EXHIBITIONIST):
            return False
        return super().on_interaction_test(interaction_context, interaction_target)


class ExhibitionismDressUpOutfitInteraction(_NudityDressUpOutfitInteraction):
    __qualname__ = 'ExhibitionismDressUpOutfitInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        sim = cls.get_interaction_sim(interaction_context)
        if not has_sim_trait(sim, SimTrait.WW_EXHIBITIONIST):
            return False
        return super().on_interaction_test(interaction_context, interaction_target)

