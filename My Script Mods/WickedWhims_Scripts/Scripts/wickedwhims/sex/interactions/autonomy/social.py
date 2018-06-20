from enums.interactions_enum import SimInteraction
from turbolib.interaction_util import TurboInteractionUtil
from turbolib.sim_util import TurboSimUtil
from turbolib.ui_util import TurboUIUtil
from turbolib.wrappers.interactions import TurboInteractionStartMixin, TurboSocialMixerInteraction, TurboInteractionCancelMixin, TurboInteractionInitMixin, TurboImmediateSuperInteraction
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.sex.sex_operators.general_sex_handlers_operator import clear_sim_sex_extra_data
from wickedwhims.utils_interfaces import display_drama_dialog

class AutonomyAskForSexSocialMixerInteraction(TurboSocialMixerInteraction, TurboInteractionInitMixin, TurboInteractionStartMixin, TurboInteractionCancelMixin):
    __qualname__ = 'AutonomyAskForSexSocialMixerInteraction'

    @classmethod
    def on_interaction_init(cls, interaction_instance):
        interaction_instance.has_attempted_asking_for_sex_autonomy = False

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return True

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        interaction_instance.has_attempted_asking_for_sex_autonomy = True

    @classmethod
    def on_interaction_cancel(cls, interaction_instance, interaction_finishing_type):
        if interaction_finishing_type == TurboInteractionUtil.FinishingType.USER_CANCEL or interaction_instance.has_attempted_asking_for_sex_autonomy is False:
            pre_sex_handler = sim_ev(cls.get_interaction_sim(interaction_instance)).active_pre_sex_handler
            if pre_sex_handler is not None:
                while True:
                    for sim_info in pre_sex_handler.get_actors_sim_info_gen():
                        clear_sim_sex_extra_data(sim_info)


class AutonomyAskForSexSocialOutcomeInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'AutonomyAskForSexSocialOutcomeInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return True

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        sim = cls.get_interaction_sim(interaction_instance)
        target = cls.get_interaction_target(interaction_instance)
        pre_sex_handler = sim_ev(sim).active_pre_sex_handler
        if pre_sex_handler is None or target is None:
            clear_sim_sex_extra_data(sim)
            if target is not None:
                clear_sim_sex_extra_data(target)
            return False

        def _ask_for_sex_callback(dialog):
            if not TurboUIUtil.DramaDialog.get_response_result(dialog):
                pre_sex_handler.set_as_failure()
            else:
                pre_sex_handler.set_as_success()
            TurboSimUtil.Interaction.push_affordance(sim, SimInteraction.WW_TRIGGER_SOCIAL_ASK_FOR_SEX_DEFAULT, target=target, skip_if_running=True)
            return True

        display_drama_dialog(target, sim, text=1638454846, text_tokens=(sim, target), ok_text=3398494028, cancel_text=3364226930, callback=_ask_for_sex_callback)
        return True

