from turbolib.interaction_util import TurboInteractionUtil
from turbolib.l18n_util import TurboL18NUtil
from turbolib.manager_util import TurboManagerUtil
from turbolib.object_util import TurboObjectUtil
from turbolib.sim_util import TurboSimUtil
from turbolib.wrappers.interactions import TurboBaseSuperInteraction, TurboInteractionCancelMixin, TurboInteractionNameMixin, TurboInteractionASMMixin, TurboInteractionConstraintMixin
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.utils_interfaces import display_notification

class DefaultAnimationsInteraction(TurboBaseSuperInteraction, TurboInteractionCancelMixin, TurboInteractionASMMixin, TurboInteractionNameMixin, TurboInteractionConstraintMixin):
    __qualname__ = 'DefaultAnimationsInteraction'

    @classmethod
    def on_constraint(cls, interaction_instance, interaction_sim, interaction_target):
        return cls.get_stand_posture_constraint()

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return True

    @classmethod
    def on_interaction_asm_setup(cls, interaction_instance, interaction_asm):
        sim = TurboInteractionUtil.get_interaction_sim(interaction_instance)
        active_sex_handler = sim_ev(sim).active_sex_handler
        if active_sex_handler is None:
            cls.cancel_interaction(interaction_instance, finishing_type=TurboInteractionUtil.FinishingType.NATURAL)
            display_notification(text='Missing Active Sex Handler Instance!', title='WickedWhims Error', secondary_icon=sim, is_safe=True)
            return False
        if TurboManagerUtil.Sim.get_sim_id(sim) != active_sex_handler.get_creator_sim_id():
            return True
        game_object_target = TurboObjectUtil.GameObject.get_object_with_id(active_sex_handler.get_game_object_id())
        actors_list = active_sex_handler.get_sims_list()
        for i in range(len(actors_list)):
            actor_id = actors_list[i][0]
            actor_sim = TurboManagerUtil.Sim.get_sim_instance(actors_list[i][1])
            interaction_asm.set_parameter('animation_name_a' + str(i), active_sex_handler.get_actor_animation_clip_name(actor_id))
            interaction_asm.set_actor('a' + str(i), actor_sim)
        if game_object_target is not None:
            interaction_asm.set_parameter('object_animation_name', active_sex_handler.get_animation_instance().get_object_animation_clip_name())
            interaction_asm.set_actor('o', game_object_target)
        interaction_asm.enter()
        return True

    @classmethod
    def get_interaction_name(cls, interaction_instance):
        sim = TurboInteractionUtil.get_interaction_sim(interaction_instance)
        active_sex_handler = sim_ev(sim).active_sex_handler
        if active_sex_handler is None:
            return TurboL18NUtil.get_localized_string(2175203501)
        return TurboL18NUtil.get_localized_string(2667173688, tokens=(active_sex_handler.get_animation_instance().get_display_name(string_hash=True), active_sex_handler.get_animation_instance().get_author()))

    @classmethod
    def on_interaction_cancel(cls, interaction_instance, finishing_type):
        sim = TurboInteractionUtil.get_interaction_sim(interaction_instance)
        if finishing_type == TurboInteractionUtil.FinishingType.USER_CANCEL:
            if sim_ev(sim).active_sex_handler is not None:
                sim_ev(sim).active_sex_handler.is_canceled = True
                sim_ev(sim).active_sex_handler.stop(is_end=True, stop_reason='On interaction cancel: ' + finishing_type.name)
            else:
                TurboSimUtil.Sim.reset_sim(sim, hard_reset_on_exception=True)
        elif finishing_type == TurboInteractionUtil.FinishingType.NATURAL and sim_ev(sim).active_sex_handler is not None:
            if sim_ev(sim).active_sex_handler.is_canceled is True:
                sim_ev(sim).active_sex_handler.stop(is_end=True, stop_reason='On interaction cancel: ' + finishing_type.name)

