from enums.traits_enum import SimTrait
from turbolib.cas_util import TurboCASUtil
from turbolib.interaction_util import TurboInteractionUtil
from turbolib.manager_util import TurboManagerUtil
from turbolib.sim_util import TurboSimUtil
from turbolib.types_util import TurboTypesUtil
from turbolib.wrappers.interactions import TurboSuperInteraction, TurboInteractionSetupMixin, TurboInteractionConstraintMixin, TurboInteractionBasicElementsMixin, TurboInteractionStartMixin
from wickedwhims.nudity.notifications_handler import nudity_notification
from wickedwhims.nudity.nudity_settings import NuditySetting, get_nudity_setting
from wickedwhims.nudity.permissions.test import has_sim_permission_for_nudity, NudityPermissionDenied
from wickedwhims.nudity.underwear.mannequin import open_underwear_mannequin
from wickedwhims.sxex_bridge.body import BodyState, get_sim_body_state, set_sim_top_naked_state, set_sim_bottom_naked_state, get_sim_actual_body_state
from wickedwhims.sxex_bridge.outfit import StripType, strip_outfit
from wickedwhims.sxex_bridge.sex import is_sim_going_to_sex, is_sim_in_sex
from wickedwhims.sxex_bridge.underwear import set_sim_top_underwear_state, set_sim_bottom_underwear_state, is_sim_top_underwear, is_sim_bottom_underwear, is_underwear_outfit
from wickedwhims.utils_cas import get_modified_outfit
from wickedwhims.utils_traits import has_sim_trait

class NudityChangeUnderwearInteraction(TurboSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'NudityChangeUnderwearInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        if not TurboTypesUtil.Sims.is_sim(interaction_target):
            return False
        if not get_nudity_setting(NuditySetting.UNDERWEAR_SWITCH_STATE, variable_type=bool) or has_sim_trait(interaction_target, SimTrait.WW_NO_UNDERWEAR):
            return False
        sim = cls.get_interaction_sim(interaction_context)
        if is_sim_in_sex(sim) or (is_sim_going_to_sex(sim) or is_sim_in_sex(interaction_target)) or is_sim_going_to_sex(interaction_target):
            return False
        if not get_nudity_setting(NuditySetting.TEENS_NUDITY_STATE, variable_type=bool) and TurboSimUtil.Age.get_age(interaction_target) == TurboSimUtil.Age.TEEN:
            return False
        return True

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        open_underwear_mannequin(cls.get_interaction_target(interaction_instance))
        return True

    @classmethod
    def on_interaction_run(cls, interaction_instance):
        return True


class _NudityUndressUnderwearTopInteraction(TurboSuperInteraction, TurboInteractionSetupMixin, TurboInteractionConstraintMixin, TurboInteractionBasicElementsMixin):
    __qualname__ = '_NudityUndressUnderwearTopInteraction'

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
        if not get_nudity_setting(NuditySetting.UNDERWEAR_SWITCH_STATE, variable_type=bool) or has_sim_trait(sim, SimTrait.WW_NO_UNDERWEAR):
            return False
        if not get_nudity_setting(NuditySetting.TEENS_NUDITY_STATE, variable_type=bool) and TurboSimUtil.Age.get_age(sim) == TurboSimUtil.Age.TEEN:
            return False
        if is_sim_in_sex(sim) or is_sim_going_to_sex(sim):
            return False
        if TurboSimUtil.Gender.is_male(sim):
            return False
        if get_sim_body_state(sim, TurboCASUtil.BodyType.UPPER_BODY) == BodyState.UNDERWEAR:
            return True
        return False

    @classmethod
    def on_building_basic_elements(cls, interaction_instance, sequence):
        sim = cls.get_interaction_sim(interaction_instance)
        strip_result = strip_outfit(sim, strip_type_top=StripType.NUDE, skip_outfit_change=True, save_original=False)
        if strip_result is True:
            set_sim_top_naked_state(sim, True)
            set_sim_top_underwear_state(sim, False)
            nudity_notification(text=1357018163, text_tokens=(sim,), icon=sim, sims=(sim,), is_autonomy=cls.get_interaction_source(interaction_instance) == TurboInteractionUtil.InteractionSource.AUTONOMY)
            return TurboSimUtil.CAS.get_change_outfit_element(sim, (TurboCASUtil.OutfitCategory.SPECIAL, 0), do_spin=True, interaction=interaction_instance)

    @classmethod
    def on_interaction_run(cls, interaction_instance):
        return True


class NaturismUndressUnderwearTopInteraction(_NudityUndressUnderwearTopInteraction):
    __qualname__ = 'NaturismUndressUnderwearTopInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        sim = cls.get_interaction_sim(interaction_context)
        if has_sim_trait(sim, SimTrait.WW_EXHIBITIONIST):
            return False
        return super().on_interaction_test(interaction_context, interaction_target)


class ExhibitionismUndressUnderwearTopInteraction(_NudityUndressUnderwearTopInteraction):
    __qualname__ = 'ExhibitionismUndressUnderwearTopInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        sim = cls.get_interaction_sim(interaction_context)
        if not has_sim_trait(sim, SimTrait.WW_EXHIBITIONIST):
            return False
        return super().on_interaction_test(interaction_context, interaction_target)


class _NudityUndressUnderwearBottomInteraction(TurboSuperInteraction, TurboInteractionSetupMixin, TurboInteractionConstraintMixin, TurboInteractionBasicElementsMixin):
    __qualname__ = '_NudityUndressUnderwearBottomInteraction'

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
        if not get_nudity_setting(NuditySetting.UNDERWEAR_SWITCH_STATE, variable_type=bool) or has_sim_trait(sim, SimTrait.WW_NO_UNDERWEAR):
            return False
        if not get_nudity_setting(NuditySetting.TEENS_NUDITY_STATE, variable_type=bool) and TurboSimUtil.Age.get_age(sim) == TurboSimUtil.Age.TEEN:
            return False
        if is_sim_in_sex(sim) or is_sim_going_to_sex(sim):
            return False
        if TurboSimUtil.Gender.is_male(sim):
            return False
        if get_sim_body_state(sim, TurboCASUtil.BodyType.LOWER_BODY) == BodyState.UNDERWEAR:
            return True
        return False

    @classmethod
    def on_building_basic_elements(cls, interaction_instance, sequence):
        sim = cls.get_interaction_sim(interaction_instance)
        strip_result = strip_outfit(sim, strip_type_bottom=StripType.NUDE, skip_outfit_change=True, save_original=False)
        if strip_result is True:
            set_sim_bottom_naked_state(sim, True)
            set_sim_bottom_underwear_state(sim, False)
            nudity_notification(text=3100688268, text_tokens=(sim,), icon=sim, sims=(sim,), is_autonomy=cls.get_interaction_source(interaction_instance) == TurboInteractionUtil.InteractionSource.AUTONOMY)
            return TurboSimUtil.CAS.get_change_outfit_element(sim, (TurboCASUtil.OutfitCategory.SPECIAL, 0), do_spin=True, interaction=interaction_instance)

    @classmethod
    def on_interaction_run(cls, interaction_instance):
        return True


class NaturismUndressUnderwearBottomInteraction(_NudityUndressUnderwearBottomInteraction):
    __qualname__ = 'NaturismUndressUnderwearBottomInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        sim = cls.get_interaction_sim(interaction_context)
        if has_sim_trait(sim, SimTrait.WW_EXHIBITIONIST):
            return False
        return super().on_interaction_test(interaction_context, interaction_target)


class ExhibitionismUndressUnderwearBottomInteraction(_NudityUndressUnderwearBottomInteraction):
    __qualname__ = 'ExhibitionismUndressUnderwearBottomInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        sim = cls.get_interaction_sim(interaction_context)
        if not has_sim_trait(sim, SimTrait.WW_EXHIBITIONIST):
            return False
        return super().on_interaction_test(interaction_context, interaction_target)


class _NudityUndressUnderwearInteraction(TurboSuperInteraction, TurboInteractionSetupMixin, TurboInteractionConstraintMixin, TurboInteractionBasicElementsMixin):
    __qualname__ = '_NudityUndressUnderwearInteraction'

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
        if not get_nudity_setting(NuditySetting.UNDERWEAR_SWITCH_STATE, variable_type=bool) or has_sim_trait(sim, SimTrait.WW_NO_UNDERWEAR):
            return False
        if not get_nudity_setting(NuditySetting.TEENS_NUDITY_STATE, variable_type=bool) and TurboSimUtil.Age.get_age(sim) == TurboSimUtil.Age.TEEN:
            return False
        if is_sim_in_sex(sim) or is_sim_going_to_sex(sim):
            return False
        if TurboSimUtil.Gender.is_male(sim):
            return get_sim_body_state(sim, TurboCASUtil.BodyType.LOWER_BODY) == BodyState.UNDERWEAR
        return get_sim_body_state(sim, TurboCASUtil.BodyType.UPPER_BODY) == BodyState.UNDERWEAR and get_sim_body_state(sim, TurboCASUtil.BodyType.LOWER_BODY) == BodyState.UNDERWEAR

    @classmethod
    def on_building_basic_elements(cls, interaction_instance, sequence):
        sim = cls.get_interaction_sim(interaction_instance)
        top_body_state = get_sim_body_state(sim, TurboCASUtil.BodyType.UPPER_BODY)
        bottom_body_state = get_sim_body_state(sim, TurboCASUtil.BodyType.LOWER_BODY)
        strip_type_top = StripType.NUDE if top_body_state == BodyState.UNDERWEAR else StripType.NONE
        strip_type_bottom = StripType.NUDE if bottom_body_state == BodyState.UNDERWEAR else StripType.NONE
        strip_result = strip_outfit(sim, strip_type_top=strip_type_top, strip_type_bottom=strip_type_bottom, skip_outfit_change=True, save_original=False)
        if strip_result is True:
            set_sim_top_naked_state(sim, True)
            set_sim_bottom_naked_state(sim, True)
            set_sim_top_underwear_state(sim, False)
            set_sim_bottom_underwear_state(sim, False)
            nudity_notification(text=3110156917, text_tokens=(sim,), icon=sim, sims=(sim,), is_autonomy=cls.get_interaction_source(interaction_instance) == TurboInteractionUtil.InteractionSource.AUTONOMY)
            return TurboSimUtil.CAS.get_change_outfit_element(sim, (TurboCASUtil.OutfitCategory.SPECIAL, 0), do_spin=True, interaction=interaction_instance)

    @classmethod
    def on_interaction_run(cls, interaction_instance):
        return True


class NaturismUndressUnderwearInteraction(_NudityUndressUnderwearInteraction):
    __qualname__ = 'NaturismUndressUnderwearInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        sim = cls.get_interaction_sim(interaction_context)
        if has_sim_trait(sim, SimTrait.WW_EXHIBITIONIST):
            return False
        return super().on_interaction_test(interaction_context, interaction_target)


class ExhibitionismUndressUnderwearInteraction(_NudityUndressUnderwearInteraction):
    __qualname__ = 'ExhibitionismUndressUnderwearInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        sim = cls.get_interaction_sim(interaction_context)
        if not has_sim_trait(sim, SimTrait.WW_EXHIBITIONIST):
            return False
        return super().on_interaction_test(interaction_context, interaction_target)


class _NudityPutOnUnderwearInteraction(TurboSuperInteraction, TurboInteractionSetupMixin, TurboInteractionConstraintMixin, TurboInteractionBasicElementsMixin):
    __qualname__ = '_NudityPutOnUnderwearInteraction'

    @classmethod
    def on_constraint(cls, interaction_instance, interaction_sim, interaction_target):
        return cls.get_stand_posture_constraint()

    @classmethod
    def on_interaction_setup(cls, interaction_instance):
        return True

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        sim = cls.get_interaction_sim(interaction_context)
        if not get_nudity_setting(NuditySetting.UNDERWEAR_SWITCH_STATE, variable_type=bool) or has_sim_trait(sim, SimTrait.WW_NO_UNDERWEAR):
            return False
        if is_sim_in_sex(sim) or is_sim_going_to_sex(sim):
            return False
        if TurboSimUtil.Gender.is_male(sim):
            return False
        if is_underwear_outfit(get_modified_outfit(sim)[0]) and (not is_sim_bottom_underwear(sim) or TurboSimUtil.Gender.is_female(sim) and not is_sim_top_underwear(sim)):
            return True
        return False

    @classmethod
    def on_building_basic_elements(cls, interaction_instance, sequence):
        sim = cls.get_interaction_sim(interaction_instance)
        put_sim_underwear_on(sim, skip_outfit_change=True)
        nudity_notification(text=1950586772, text_tokens=(sim,), icon=sim, sims=(sim,), is_autonomy=cls.get_interaction_source(interaction_instance) == TurboInteractionUtil.InteractionSource.AUTONOMY)
        return TurboSimUtil.CAS.get_change_outfit_element(sim, (TurboCASUtil.OutfitCategory.SPECIAL, 0), do_spin=True, interaction=interaction_instance)

    @classmethod
    def on_interaction_run(cls, interaction_instance):
        return True


class NaturismPutOnUnderwearInteraction(_NudityPutOnUnderwearInteraction):
    __qualname__ = 'NaturismPutOnUnderwearInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        sim = cls.get_interaction_sim(interaction_context)
        if has_sim_trait(sim, SimTrait.WW_EXHIBITIONIST):
            return False
        return super().on_interaction_test(interaction_context, interaction_target)


class ExhibitionismPutOnUnderwearInteraction(_NudityPutOnUnderwearInteraction):
    __qualname__ = 'ExhibitionismPutOnUnderwearInteraction'

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
        if denied_permission == NudityPermissionDenied.NOT_AT_HOME:
            text_tokens.append(2434379342)
        elif denied_permission == NudityPermissionDenied.OUTSIDE:
            text_tokens.append(14125364)
        else:
            while denied_permission == NudityPermissionDenied.TOO_MANY_SIMS_AROUND:
                text_tokens.append(902300171)
    for _ in range(11 - len(text_tokens)):
        text_tokens.append(0)
    nudity_notification(text=2447814946, text_tokens=text_tokens, icon=interaction_sim, sims=(interaction_sim,), is_autonomy=is_autonomy)
    return False


def put_sim_underwear_on(sim_identifier, skip_outfit_change=False):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    set_sim_top_naked_state(sim_info, False)
    set_sim_bottom_naked_state(sim_info, False)
    set_sim_top_underwear_state(sim_info, True)
    set_sim_bottom_underwear_state(sim_info, True)
    top_outfit_type = StripType.UNDERWEAR if TurboSimUtil.Gender.is_female(sim_info) and get_sim_body_state(sim_info, 6) == BodyState.NUDE else StripType.NONE
    bottom_outfit_type = StripType.UNDERWEAR if get_sim_actual_body_state(sim_info, 7) == BodyState.NUDE else StripType.NONE
    strip_outfit(sim_info, strip_type_top=top_outfit_type, strip_type_bottom=bottom_outfit_type, skip_outfit_change=skip_outfit_change, save_original=False)

