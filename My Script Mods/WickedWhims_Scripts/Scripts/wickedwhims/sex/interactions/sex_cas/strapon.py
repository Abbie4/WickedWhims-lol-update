from enums.traits_enum import SimTrait
from turbolib.manager_util import TurboManagerUtil
from turbolib.sim_util import TurboSimUtil
from turbolib.types_util import TurboTypesUtil
from turbolib.wrappers.interactions import TurboSuperInteraction, TurboImmediateSuperInteraction, TurboInteractionStartMixin
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.nudity.nudity_settings import NuditySetting, get_nudity_setting
from wickedwhims.sex.sex_handlers.active.utils.strapon import update_stapon
from wickedwhims.sex.strapon.mannequin import open_strapon_mannequin
from wickedwhims.sex.strapon.operator import has_loaded_strapon, is_strapon_on_sim
from wickedwhims.sxex_bridge.outfit import StripType, strip_outfit
from wickedwhims.sxex_bridge.sex import is_sim_going_to_sex, is_sim_in_sex
from wickedwhims.utils_traits import has_sim_trait

class ChangeSimStraponInteraction(TurboSuperInteraction):
    __qualname__ = 'ChangeSimStraponInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        if not TurboTypesUtil.Sims.is_sim(interaction_target):
            return False
        if has_sim_trait(interaction_target, SimTrait.GENDEROPTIONS_TOILET_STANDING):
            return False
        sim = cls.get_interaction_sim(interaction_context)
        if is_sim_in_sex(sim) or (is_sim_going_to_sex(sim) or is_sim_in_sex(interaction_target)) or is_sim_going_to_sex(interaction_target):
            return False
        if not get_nudity_setting(NuditySetting.TEENS_NUDITY_STATE, variable_type=bool) and TurboSimUtil.Age.get_age(interaction_target) == TurboSimUtil.Age.TEEN:
            return False
        if not has_loaded_strapon():
            return False
        return True

    @classmethod
    def on_interaction_run(cls, interaction_instance):
        open_strapon_mannequin(cls.get_interaction_target(interaction_instance))
        return True


class AllowStraponInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'AllowStraponInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        if interaction_target is None or not TurboTypesUtil.Sims.is_sim(interaction_target):
            return False
        sim = cls.get_interaction_sim(interaction_context)
        if sim_ev(sim).active_sex_handler is None or sim_ev(interaction_target).active_sex_handler is None:
            return False
        if sim_ev(sim).active_sex_handler is not sim_ev(interaction_target).active_sex_handler:
            return False
        if has_sim_trait(interaction_target, SimTrait.GENDEROPTIONS_TOILET_STANDING):
            return False
        if not has_loaded_strapon():
            return False
        if sim_ev(interaction_target).is_strapon_allowed is False:
            return True
        return False

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        target = cls.get_interaction_target(interaction_instance)
        sim_ev(target).is_strapon_allowed = True
        active_sex_handler = sim_ev(target).active_sex_handler
        if active_sex_handler is not None:
            actor_data = active_sex_handler.get_animation_instance().get_actor(active_sex_handler.get_actor_id_by_sim_id(TurboManagerUtil.Sim.get_sim_id(target)))
            update_stapon(target, actor_data=actor_data)
        return True


class DisallowStraponInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'DisallowStraponInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        if interaction_target is None or not TurboTypesUtil.Sims.is_sim(interaction_target):
            return False
        sim = cls.get_interaction_sim(interaction_context)
        if sim_ev(sim).active_sex_handler is None or sim_ev(interaction_target).active_sex_handler is None:
            return False
        if sim_ev(sim).active_sex_handler is not sim_ev(interaction_target).active_sex_handler:
            return False
        if has_sim_trait(interaction_target, SimTrait.GENDEROPTIONS_TOILET_STANDING):
            return False
        if not has_loaded_strapon():
            return False
        if sim_ev(interaction_target).is_strapon_allowed is True:
            return True
        return False

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        target = cls.get_interaction_target(interaction_instance)
        sim_ev(target).is_strapon_allowed = False
        if is_strapon_on_sim(target):
            strip_outfit(target, strip_type_bottom=StripType.NUDE)
        return True

