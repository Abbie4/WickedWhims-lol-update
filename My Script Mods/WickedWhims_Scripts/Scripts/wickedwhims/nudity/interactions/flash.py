'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from enums.buffs_enum import SimBuff
from turbolib.interaction_util import TurboInteractionUtil
from turbolib.sim_util import TurboSimUtil
from turbolib.wrappers.interactions import TurboInteractionStartMixin, TurboImmediateSuperInteraction, TurboInteractionFinishMixin, TurboInteractionSetupMixin, TurboSocialMixerInteraction, TurboBaseSuperInteraction
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.nudity.notifications_handler import nudity_notification
from wickedwhims.nudity.nudity_settings import NuditySetting, get_nudity_setting
from wickedwhims.nudity.permissions.test import has_sim_permission_for_nudity, NudityPermissionDenied
from wickedwhims.nudity.reactions.nudity_reaction import force_nudity_reaction
from wickedwhims.nudity.skill.skills_utils import apply_nudity_skill_influence, NuditySkillIncreaseReason, get_nudity_skill_points_modifier, increase_sim_nudity_skill
from wickedwhims.relationships.desire_handler import change_sim_desire_level
from wickedwhims.relationships.relationship_utils import get_sim_preferenced_genders
from wickedwhims.sxex_bridge.body import set_sim_top_naked_state, is_sim_outfit_fullbody, get_sim_body_state, BodyState, set_sim_bottom_naked_state
from wickedwhims.sxex_bridge.outfit import strip_outfit, StripType
from wickedwhims.sxex_bridge.penis import set_sim_penis_state
from wickedwhims.sxex_bridge.sex import is_sim_in_sex, is_sim_going_to_sex
from wickedwhims.sxex_bridge.statistics import increase_sim_ww_statistic
from wickedwhims.sxex_bridge.underwear import set_sim_top_underwear_state, set_sim_bottom_underwear_state
from wickedwhims.utils_buffs import has_sim_buff, add_sim_buff

class ExhibitionismUndressToFlashBoobsInteraction(TurboSocialMixerInteraction, TurboInteractionStartMixin):
    __qualname__ = 'ExhibitionismUndressToFlashBoobsInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return True

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        sim = cls.get_interaction_sim(interaction_instance)
        target = cls.get_interaction_target(interaction_instance)
        strip_result = strip_outfit(sim, strip_type_top=StripType.NUDE)
        if strip_result is True:
            set_sim_top_naked_state(sim, True)
            set_sim_top_underwear_state(sim, False)
            force_nudity_reaction(target, sim)
            return True
        return False


class ExhibitionismFlashBoobsInteraction(TurboSocialMixerInteraction, TurboInteractionSetupMixin, TurboInteractionStartMixin):
    __qualname__ = 'ExhibitionismFlashBoobsInteraction'

    @classmethod
    def on_interaction_setup(cls, interaction_instance):
        if _has_permission_to_flash(cls.get_interaction_sim(interaction_instance), cls.get_interaction_context(interaction_instance)):
            return True
        cls.kill(interaction_instance)
        return False

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        sim = cls.get_interaction_sim(interaction_context)
        if is_sim_in_sex(sim) or (is_sim_going_to_sex(sim) or is_sim_in_sex(interaction_target)) or is_sim_going_to_sex(interaction_target):
            return False
        if not get_nudity_setting(NuditySetting.TEENS_NUDITY_STATE, variable_type=bool) and TurboSimUtil.Age.get_age(sim) == TurboSimUtil.Age.TEEN:
            return False
        if is_sim_outfit_fullbody(sim):
            return False
        if get_sim_body_state(sim, 6) == BodyState.OUTFIT:
            return True
        return False

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        sim = cls.get_interaction_sim(interaction_instance)
        target = cls.get_interaction_target(interaction_instance)
        _flash_sim_result(sim, target)
        increase_sim_ww_statistic(sim, 'times_flashed_top')
        nudity_notification(text=2396534391, text_tokens=(sim, target), icon=sim, sims=(sim, target), is_autonomy=cls.get_interaction_source(interaction_instance) == TurboInteractionUtil.InteractionSource.AUTONOMY)
        return True


class ExhibitionismUndressToFlashPussyInteraction(TurboSocialMixerInteraction, TurboInteractionStartMixin):
    __qualname__ = 'ExhibitionismUndressToFlashPussyInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return True

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        sim = cls.get_interaction_sim(interaction_instance)
        target = cls.get_interaction_target(interaction_instance)
        strip_result = strip_outfit(sim, strip_type_bottom=StripType.NUDE)
        if strip_result is True:
            set_sim_bottom_naked_state(sim, True)
            set_sim_bottom_underwear_state(sim, False)
            force_nudity_reaction(target, sim)
            return True
        return False


class ExhibitionismFlashPussyInteraction(TurboSocialMixerInteraction, TurboInteractionSetupMixin, TurboInteractionStartMixin):
    __qualname__ = 'ExhibitionismFlashPussyInteraction'

    @classmethod
    def on_interaction_setup(cls, interaction_instance):
        if _has_permission_to_flash(cls.get_interaction_sim(interaction_instance), cls.get_interaction_context(interaction_instance)):
            return True
        cls.kill(interaction_instance)
        return False

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        sim = cls.get_interaction_sim(interaction_context)
        if is_sim_in_sex(sim) or (is_sim_going_to_sex(sim) or is_sim_in_sex(interaction_target)) or is_sim_going_to_sex(interaction_target):
            return False
        if not get_nudity_setting(NuditySetting.TEENS_NUDITY_STATE, variable_type=bool) and TurboSimUtil.Age.get_age(sim) == TurboSimUtil.Age.TEEN:
            return False
        if is_sim_outfit_fullbody(sim):
            return False
        if get_sim_body_state(sim, 7) == BodyState.OUTFIT:
            return True
        return False

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        sim = cls.get_interaction_sim(interaction_instance)
        target = cls.get_interaction_target(interaction_instance)
        _flash_sim_result(sim, target)
        increase_sim_ww_statistic(sim, 'times_flashed_bottom')
        nudity_notification(text=3499180400, text_tokens=(sim, target), icon=sim, sims=(sim, target), is_autonomy=cls.get_interaction_source(interaction_instance) == TurboInteractionUtil.InteractionSource.AUTONOMY)
        return True


class ExhibitionismUndressToFlashDickInteraction(TurboSocialMixerInteraction, TurboInteractionStartMixin):
    __qualname__ = 'ExhibitionismUndressToFlashDickInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return True

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        sim = cls.get_interaction_sim(interaction_instance)
        target = cls.get_interaction_target(interaction_instance)
        strip_result = strip_outfit(sim, strip_type_bottom=StripType.NUDE)
        if strip_result is True:
            set_sim_bottom_naked_state(sim, True)
            set_sim_bottom_underwear_state(sim, False)
            force_nudity_reaction(target, sim)
            return True
        return False


class ExhibitionismFlashDickInteraction(TurboSocialMixerInteraction, TurboInteractionSetupMixin, TurboInteractionStartMixin):
    __qualname__ = 'ExhibitionismFlashDickInteraction'

    @classmethod
    def on_interaction_setup(cls, interaction_instance):
        if _has_permission_to_flash(cls.get_interaction_sim(interaction_instance), cls.get_interaction_context(interaction_instance)):
            return True
        cls.kill(interaction_instance)
        return False

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        sim = cls.get_interaction_sim(interaction_context)
        if is_sim_in_sex(sim) or (is_sim_going_to_sex(sim) or is_sim_in_sex(interaction_target)) or is_sim_going_to_sex(interaction_target):
            return False
        if not get_nudity_setting(NuditySetting.TEENS_NUDITY_STATE, variable_type=bool) and TurboSimUtil.Age.get_age(sim) == TurboSimUtil.Age.TEEN:
            return False
        if is_sim_outfit_fullbody(sim):
            return False
        if get_sim_body_state(sim, 7) == BodyState.OUTFIT:
            return True
        return False

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        sim = cls.get_interaction_sim(interaction_instance)
        target = cls.get_interaction_target(interaction_instance)
        _flash_sim_result(sim, target)
        increase_sim_ww_statistic(sim, 'times_flashed_bottom')
        set_sim_penis_state(sim, True, 5)
        nudity_notification(text=1399400780, text_tokens=(sim, target), icon=sim, sims=(sim, target), is_autonomy=cls.get_interaction_source(interaction_instance) == TurboInteractionUtil.InteractionSource.AUTONOMY)
        return True


class ExhibitionismUndressToFlashButtInteraction(TurboSocialMixerInteraction, TurboInteractionStartMixin):
    __qualname__ = 'ExhibitionismUndressToFlashButtInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return True

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        sim = cls.get_interaction_sim(interaction_instance)
        target = cls.get_interaction_target(interaction_instance)
        strip_result = strip_outfit(sim, strip_type_bottom=StripType.NUDE)
        if strip_result is True:
            set_sim_bottom_naked_state(sim, True)
            set_sim_bottom_underwear_state(sim, False)
            force_nudity_reaction(target, sim)
            return True
        return False


class ExhibitionismFlashButtInteraction(TurboSocialMixerInteraction, TurboInteractionSetupMixin, TurboInteractionStartMixin):
    __qualname__ = 'ExhibitionismFlashButtInteraction'

    @classmethod
    def on_interaction_setup(cls, interaction_instance):
        if _has_permission_to_flash(cls.get_interaction_sim(interaction_instance), cls.get_interaction_context(interaction_instance)):
            return True
        cls.kill(interaction_instance)
        return False

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        sim = cls.get_interaction_sim(interaction_context)
        if is_sim_in_sex(sim) or (is_sim_going_to_sex(sim) or is_sim_in_sex(interaction_target)) or is_sim_going_to_sex(interaction_target):
            return False
        if not get_nudity_setting(NuditySetting.TEENS_NUDITY_STATE, variable_type=bool) and TurboSimUtil.Age.get_age(sim) == TurboSimUtil.Age.TEEN:
            return False
        if is_sim_outfit_fullbody(sim):
            return False
        if get_sim_body_state(sim, 7) == BodyState.OUTFIT:
            return True
        return False

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        sim = cls.get_interaction_sim(interaction_instance)
        target = cls.get_interaction_target(interaction_instance)
        _flash_sim_result(sim, target)
        increase_sim_ww_statistic(sim, 'times_flashed_bottom')
        nudity_notification(text=4243459940, text_tokens=(sim, target), icon=sim, sims=(sim, target), is_autonomy=cls.get_interaction_source(interaction_instance) == TurboInteractionUtil.InteractionSource.AUTONOMY)
        return True


class ExhibitionismUndressToFlashEverythingInteraction(TurboSocialMixerInteraction, TurboInteractionStartMixin):
    __qualname__ = 'ExhibitionismUndressToFlashEverythingInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return True

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        sim = cls.get_interaction_sim(interaction_instance)
        target = cls.get_interaction_target(interaction_instance)
        strip_result = strip_outfit(sim, strip_type_top=StripType.NUDE, strip_type_bottom=StripType.NUDE)
        if strip_result is True:
            set_sim_top_naked_state(sim, True)
            set_sim_bottom_naked_state(sim, True)
            set_sim_top_underwear_state(sim, False)
            set_sim_bottom_underwear_state(sim, False)
            force_nudity_reaction(target, sim)
            return True
        return False


class ExhibitionismFlashEverythingInteraction(TurboSocialMixerInteraction, TurboInteractionSetupMixin, TurboInteractionStartMixin):
    __qualname__ = 'ExhibitionismFlashEverythingInteraction'

    @classmethod
    def on_interaction_setup(cls, interaction_instance):
        if _has_permission_to_flash(cls.get_interaction_sim(interaction_instance), cls.get_interaction_context(interaction_instance)):
            return True
        cls.kill(interaction_instance)
        return False

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        sim = cls.get_interaction_sim(interaction_context)
        if is_sim_in_sex(sim) or (is_sim_going_to_sex(sim) or is_sim_in_sex(interaction_target)) or is_sim_going_to_sex(interaction_target):
            return False
        if not get_nudity_setting(NuditySetting.TEENS_NUDITY_STATE, variable_type=bool) and TurboSimUtil.Age.get_age(sim) == TurboSimUtil.Age.TEEN:
            return False
        if get_sim_body_state(sim, 6) == BodyState.OUTFIT and get_sim_body_state(sim, 7) == BodyState.OUTFIT:
            return True
        return False

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        sim = cls.get_interaction_sim(interaction_instance)
        target = cls.get_interaction_target(interaction_instance)
        _flash_sim_result(sim, target)
        increase_sim_ww_statistic(sim, 'times_flashed_full')
        nudity_notification(text=3983588816, text_tokens=(sim, target), icon=sim, sims=(sim, target), is_autonomy=cls.get_interaction_source(interaction_instance) == TurboInteractionUtil.InteractionSource.AUTONOMY)
        return True


def _has_permission_to_flash(interaction_sim, interaction_source):
    (has_permission, denied_permissions) = has_sim_permission_for_nudity(interaction_sim, nudity_setting_test=True)
    if has_permission is True:
        return True
    is_autonomy = interaction_source == TurboInteractionUtil.InteractionSource.AUTONOMY
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
    nudity_notification(text=72156750, text_tokens=text_tokens, icon=interaction_sim, sims=(interaction_sim,), is_autonomy=is_autonomy)
    return False


def _flash_sim_result(sim, target):
    sim_ev(sim).is_flashing = True
    increase_sim_nudity_skill(sim, get_nudity_skill_points_modifier(NuditySkillIncreaseReason.FLASHING_BODY), extra_fatigue=5.0)
    is_prefered_gender = TurboSimUtil.Gender.get_gender(sim) in get_sim_preferenced_genders(target)
    if is_prefered_gender is True:
        apply_nudity_skill_influence(target, 0.05, overall_limit=6.5)
        change_sim_desire_level(target, 10)
        change_sim_desire_level(sim, 4.5)
    if not has_sim_buff(sim, SimBuff.WW_NUDITY_HAS_FLASHED):
        add_sim_buff(sim, SimBuff.WW_NUDITY_HAS_FLASHED)


class ExhibitionismFlashShowOffInteraction(TurboBaseSuperInteraction, TurboInteractionFinishMixin):
    __qualname__ = 'ExhibitionismFlashShowOffInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return True

    @classmethod
    def on_interaction_finish(cls, interaction_instance):
        sim_ev(cls.get_interaction_sim(interaction_instance)).is_flashing = False


class ExhibitionismStreakInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'ExhibitionismStreakInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        sim = cls.get_interaction_sim(interaction_context)
        if is_sim_in_sex(sim) or is_sim_going_to_sex(sim):
            return False
        return True

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return True

