import random
from enums.interactions_enum import SimInteraction
from enums.traits_enum import SimTrait
from turbolib.interaction_util import TurboInteractionUtil
from turbolib.sim_util import TurboSimUtil
from turbolib.types_util import TurboTypesUtil
from turbolib.world_util import TurboWorldUtil
from turbolib.wrappers.interactions import TurboSocialMixerInteraction, TurboInteractionStartMixin
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.nudity.nudity_settings import NuditySetting, get_nudity_setting
from wickedwhims.nudity.permissions.test import has_sim_permission_for_nudity
from wickedwhims.nudity.skill.skills_utils import get_sim_nudity_skill_level, apply_nudity_skill_influence, increase_sim_nudity_skill, get_nudity_skill_points_modifier, NuditySkillIncreaseReason, is_sim_exhibitionist
from wickedwhims.relationships.desire_handler import change_sim_desire_level
from wickedwhims.relationships.relationship_utils import get_sim_preferenced_genders
from wickedwhims.sxex_bridge.body import BodyState, get_sim_body_state, is_sim_outfit_fullbody
from wickedwhims.sxex_bridge.sex import is_sim_going_to_sex, is_sim_in_sex
from wickedwhims.sxex_bridge.statistics import increase_sim_ww_statistic
from wickedwhims.sxex_bridge.underwear import set_sim_top_underwear_state, set_sim_bottom_underwear_state
from wickedwhims.utils_traits import add_sim_trait


class _NuditySocialComplimentSexyBodyInteraction(TurboSocialMixerInteraction, TurboInteractionStartMixin):
    __qualname__ = '_NuditySocialComplimentSexyBodyInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        sim = cls.get_interaction_sim(interaction_context)
        if not get_nudity_setting(NuditySetting.TEENS_NUDITY_STATE, variable_type=bool) and (TurboSimUtil.Age.get_age(sim) == TurboSimUtil.Age.TEEN or TurboSimUtil.Age.get_age(sim) == TurboSimUtil.Age.CHILD):
            return False
        nudity_skill_level = get_sim_nudity_skill_level(sim)
        if nudity_skill_level < 2:
            return False
        if is_sim_in_sex(sim) or (is_sim_going_to_sex(sim) or is_sim_in_sex(interaction_target)) or is_sim_going_to_sex(interaction_target):
            return False
        return True

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        sim = cls.get_interaction_sim(interaction_instance)
        target = cls.get_interaction_target(interaction_instance)
        if TurboSimUtil.Sim.is_npc(target):
            apply_nudity_skill_influence(target, 0.1, overall_limit=4.1)
        else:
            increase_sim_nudity_skill(target, get_nudity_skill_points_modifier(NuditySkillIncreaseReason.SOCIAL_COMPLIMENT), extra_fatigue=2.5)
        if TurboSimUtil.Gender.get_gender(sim) in get_sim_preferenced_genders(target):
            change_sim_desire_level(target, 10)
            change_sim_desire_level(sim, 5)
        increase_sim_ww_statistic(sim, 'times_talked_exhibitionism')
        return True


class NaturismSocialComplimentSexyBodyInteraction(_NuditySocialComplimentSexyBodyInteraction):
    __qualname__ = 'NaturismSocialComplimentSexyBodyInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        sim = cls.get_interaction_sim(interaction_context)
        if is_sim_exhibitionist(sim):
            return False
        return super().on_interaction_test(interaction_context, interaction_target)


class ExhibitionismSocialComplimentSexyBodyInteraction(_NuditySocialComplimentSexyBodyInteraction):
    __qualname__ = 'ExhibitionismSocialComplimentSexyBodyInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        sim = cls.get_interaction_sim(interaction_context)
        if not is_sim_exhibitionist(sim):
            return False
        return super().on_interaction_test(interaction_context, interaction_target)


class _NuditySocialTalkAboutNudityInteraction(TurboSocialMixerInteraction, TurboInteractionStartMixin):
    __qualname__ = '_NuditySocialTalkAboutNudityInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        sim = cls.get_interaction_sim(interaction_context)
        if not get_nudity_setting(NuditySetting.TEENS_NUDITY_STATE, variable_type=bool) and (TurboSimUtil.Age.get_age(sim) == TurboSimUtil.Age.TEEN or TurboSimUtil.Age.get_age(sim) == TurboSimUtil.Age.CHILD):
            return False
        if is_sim_in_sex(sim) or (is_sim_going_to_sex(sim) or is_sim_in_sex(interaction_target)) or is_sim_going_to_sex(interaction_target):
            return False
        return True

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        sim = cls.get_interaction_sim(interaction_instance)
        target = cls.get_interaction_target(interaction_instance)
        sim_skill_level = get_sim_nudity_skill_level(sim)
        target_skill_level = get_sim_nudity_skill_level(target)
        if sim_skill_level > target_skill_level:
            if TurboSimUtil.Sim.is_npc(target):
                apply_nudity_skill_influence(target, sim_skill_level/100, overall_limit=2.5)
            else:
                increase_sim_nudity_skill(target, sim_skill_level, extra_fatigue=2.5)
        elif sim_skill_level < target_skill_level:
            if TurboSimUtil.Sim.is_npc(sim):
                apply_nudity_skill_influence(sim, target_skill_level/100, overall_limit=2.5)
            else:
                increase_sim_nudity_skill(sim, target_skill_level, extra_fatigue=2.5)
        if TurboSimUtil.Gender.get_gender(sim) in get_sim_preferenced_genders(target):
            change_sim_desire_level(target, 5)
        if TurboSimUtil.Gender.get_gender(target) in get_sim_preferenced_genders(sim):
            change_sim_desire_level(sim, 5)
        increase_sim_ww_statistic(sim, 'times_talked_exhibitionism')
        increase_sim_ww_statistic(target, 'times_talked_exhibitionism')
        return True


class NaturismSocialTalkAboutNudityInteraction(_NuditySocialTalkAboutNudityInteraction):
    __qualname__ = 'NaturismSocialTalkAboutNudityInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        sim = cls.get_interaction_sim(interaction_context)
        if is_sim_exhibitionist(sim):
            return False
        return super().on_interaction_test(interaction_context, interaction_target)


class ExhibitionismSocialTalkAboutNudityInteraction(_NuditySocialTalkAboutNudityInteraction):
    __qualname__ = 'ExhibitionismSocialTalkAboutNudityInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        sim = cls.get_interaction_sim(interaction_context)
        if not is_sim_exhibitionist(sim):
            return False
        return super().on_interaction_test(interaction_context, interaction_target)


class _NuditySocialConvinceToNudityInteraction(TurboSocialMixerInteraction, TurboInteractionStartMixin):
    __qualname__ = '_NuditySocialConvinceToNudityInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        sim = cls.get_interaction_sim(interaction_context)
        if not get_nudity_setting(NuditySetting.TEENS_NUDITY_STATE, variable_type=bool) and (TurboSimUtil.Age.get_age(sim) == TurboSimUtil.Age.TEEN or TurboSimUtil.Age.get_age(sim) == TurboSimUtil.Age.CHILD):
            return False
        nudity_skill_level = get_sim_nudity_skill_level(sim)
        if nudity_skill_level < 4:
            return False
        if is_sim_in_sex(sim) or (is_sim_going_to_sex(sim) or is_sim_in_sex(interaction_target)) or is_sim_going_to_sex(interaction_target):
            return False
        return True

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        sim = cls.get_interaction_sim(interaction_instance)
        target = cls.get_interaction_target(interaction_instance)
        sim_skill_level = get_sim_nudity_skill_level(sim)
        if TurboSimUtil.Sim.is_npc(target):
            apply_nudity_skill_influence(target, 0.05*sim_skill_level, overall_limit=7.1)
            if random.uniform(0, 1) <= 0.1:
                add_sim_trait(target, SimTrait.WW_EXHIBITIONIST)
        else:
            increase_sim_nudity_skill(target, get_nudity_skill_points_modifier(NuditySkillIncreaseReason.SOCIAL_CONVINCE), extra_fatigue=3.1)
        if TurboSimUtil.Gender.get_gender(sim) in get_sim_preferenced_genders(target):
            change_sim_desire_level(target, 10)
            change_sim_desire_level(sim, 5)
        increase_sim_ww_statistic(sim, 'times_talked_exhibitionism')
        increase_sim_ww_statistic(target, 'times_talked_exhibitionism')
        return True


class NaturismSocialConvinceToNudityInteraction(_NuditySocialConvinceToNudityInteraction):
    __qualname__ = 'NaturismSocialConvinceToNudityInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        sim = cls.get_interaction_sim(interaction_context)
        if is_sim_exhibitionist(sim):
            return False
        return super().on_interaction_test(interaction_context, interaction_target)


class ExhibitionismSocialConvinceToNudityInteraction(_NuditySocialConvinceToNudityInteraction):
    __qualname__ = 'ExhibitionismSocialConvinceToNudityInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        sim = cls.get_interaction_sim(interaction_context)
        if not is_sim_exhibitionist(sim):
            return False
        return super().on_interaction_test(interaction_context, interaction_target)


class _NuditySocialAskToGetNakedInteraction(TurboSocialMixerInteraction, TurboInteractionStartMixin):
    __qualname__ = '_NuditySocialAskToGetNakedInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        if not TurboTypesUtil.Sims.is_sim(interaction_target):
            return False
        sim = cls.get_interaction_sim(interaction_context)
        if not get_nudity_setting(NuditySetting.TEENS_NUDITY_STATE, variable_type=bool) and (TurboSimUtil.Age.get_age(sim) == TurboSimUtil.Age.TEEN or TurboSimUtil.Age.get_age(sim) == TurboSimUtil.Age.CHILD or TurboSimUtil.Age.get_age(interaction_target) == TurboSimUtil.Age.TEEN or TurboSimUtil.Age.get_age(interaction_target) == TurboSimUtil.Age.CHILD):
            return False
        skill_level = get_sim_nudity_skill_level(sim)
        if skill_level <= 1:
            return False
        if is_sim_in_sex(sim) or (is_sim_going_to_sex(sim) or is_sim_in_sex(interaction_target)) or is_sim_going_to_sex(interaction_target):
            return False
        if not has_sim_permission_for_nudity(sim)[0]:
            return False
        if is_sim_outfit_fullbody(interaction_target):
            return True
        if get_sim_body_state(interaction_target, 6) == BodyState.OUTFIT:
            return True
        if get_sim_body_state(interaction_target, 7) == BodyState.OUTFIT:
            return True
        return False

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        target = cls.get_interaction_target(interaction_instance)
        (has_permission, _) = has_sim_permission_for_nudity(target, nudity_setting_test=True)
        if has_permission is False:
            return False
        if is_sim_outfit_fullbody(target):
            set_sim_top_underwear_state(target, False)
            set_sim_bottom_underwear_state(target, False)
            TurboSimUtil.Interaction.push_affordance(target, SimInteraction.WW_EXHIBITIONISM_UNDRESS_OUTFIT if is_sim_exhibitionist(target) else SimInteraction.WW_NATURISM_UNDRESS_OUTFIT, interaction_context=TurboInteractionUtil.InteractionContext.SOURCE_SCRIPT, insert_strategy=TurboInteractionUtil.QueueInsertStrategy.NEXT, must_run_next=True, priority=TurboInteractionUtil.Priority.High)
            return True
        if get_sim_body_state(target, 6) != BodyState.NUDE:
            set_sim_top_underwear_state(target, False)
            TurboSimUtil.Interaction.push_affordance(target, SimInteraction.WW_EXHIBITIONISM_UNDRESS_OUTFIT_TOP if is_sim_exhibitionist(target) else SimInteraction.WW_NATURISM_UNDRESS_OUTFIT_TOP, interaction_context=TurboInteractionUtil.InteractionContext.SOURCE_SCRIPT, insert_strategy=TurboInteractionUtil.QueueInsertStrategy.NEXT, must_run_next=True, priority=TurboInteractionUtil.Priority.High)
            return True
        if get_sim_body_state(target, 7) != BodyState.NUDE:
            set_sim_bottom_underwear_state(target, False)
            TurboSimUtil.Interaction.push_affordance(target, SimInteraction.WW_EXHIBITIONISM_UNDRESS_OUTFIT_BOTTOM if is_sim_exhibitionist(target) else SimInteraction.WW_NATURISM_UNDRESS_OUTFIT_BOTTOM, interaction_context=TurboInteractionUtil.InteractionContext.SOURCE_SCRIPT, insert_strategy=TurboInteractionUtil.QueueInsertStrategy.NEXT, must_run_next=True, priority=TurboInteractionUtil.Priority.High)
            return True
        return False


class NaturismSocialAskToGetNakedInteraction(_NuditySocialAskToGetNakedInteraction):
    __qualname__ = 'NaturismSocialAskToGetNakedInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        sim = cls.get_interaction_sim(interaction_context)
        if is_sim_exhibitionist(sim):
            return False
        return super().on_interaction_test(interaction_context, interaction_target)


class ExhibitionismSocialAskToGetNakedInteraction(_NuditySocialAskToGetNakedInteraction):
    __qualname__ = 'ExhibitionismSocialAskToGetNakedInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        sim = cls.get_interaction_sim(interaction_context)
        if not is_sim_exhibitionist(sim):
            return False
        return super().on_interaction_test(interaction_context, interaction_target)


class _NuditySocialAskToDressUpInteraction(TurboSocialMixerInteraction, TurboInteractionStartMixin):
    __qualname__ = '_NuditySocialAskToDressUpInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        if not TurboTypesUtil.Sims.is_sim(interaction_target):
            return False
        sim = cls.get_interaction_sim(interaction_context)
        if is_sim_in_sex(sim) or (is_sim_going_to_sex(sim) or is_sim_in_sex(interaction_target)) or is_sim_going_to_sex(interaction_target):
            return False
        if get_sim_body_state(interaction_target, 6) != BodyState.OUTFIT:
            return True
        if get_sim_body_state(interaction_target, 7) != BodyState.OUTFIT:
            return True
        return False

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        target = cls.get_interaction_target(interaction_instance)
        result = TurboSimUtil.Interaction.push_affordance(target, SimInteraction.WW_EXHIBITIONISM_FORCE_DRESS_UP if is_sim_exhibitionist(target) else SimInteraction.WW_NATURISM_FORCE_DRESS_UP, interaction_context=TurboInteractionUtil.InteractionContext.SOURCE_AUTONOMY, insert_strategy=TurboInteractionUtil.QueueInsertStrategy.NEXT, must_run_next=True, run_priority=TurboInteractionUtil.Priority.High, priority=TurboInteractionUtil.Priority.High, skip_if_running=True)
        if result:
            sim_ev(target).last_nudity_autonomy = TurboWorldUtil.Time.get_absolute_ticks() + 360000
        return True


class NaturismSocialAskToDressUpInteraction(_NuditySocialAskToDressUpInteraction):
    __qualname__ = 'NaturismSocialAskToDressUpInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        sim = cls.get_interaction_sim(interaction_context)
        if is_sim_exhibitionist(sim):
            return False
        return super().on_interaction_test(interaction_context, interaction_target)


class ExhibitionismSocialAskToDressUpInteraction(_NuditySocialAskToDressUpInteraction):
    __qualname__ = 'ExhibitionismSocialAskToDressUpInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        sim = cls.get_interaction_sim(interaction_context)
        if not is_sim_exhibitionist(sim):
            return False
        return super().on_interaction_test(interaction_context, interaction_target)

