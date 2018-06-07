'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''from interactions.context import QueueInsertStrategy, InteractionSourcefrom interactions.interaction_finisher import FinishingTypefrom interactions.priority import can_displace, Priority
class TurboInteractionUtil:
    __qualname__ = 'TurboInteractionUtil'

    class Priority:
        __qualname__ = 'TurboInteractionUtil.Priority'

        def _get_priority(*args):
            try:
                return Priority(args[0])
            except:
                return

        Low = _get_priority(1)
        High = _get_priority(2)
        Critical = _get_priority(3)

    class QueueInsertStrategy:
        __qualname__ = 'TurboInteractionUtil.QueueInsertStrategy'

        def _get_queue_insert_strategy(*args):
            try:
                return QueueInsertStrategy(args[0])
            except:
                return

        LAST = _get_queue_insert_strategy(0)
        NEXT = _get_queue_insert_strategy(1)
        FIRST = _get_queue_insert_strategy(2)

    class FinishingType:
        __qualname__ = 'TurboInteractionUtil.FinishingType'

        def _get_finishing_type(*args):
            try:
                return FinishingType(args[0])
            except:
                return FinishingType.UNKNOWN

        KILLED = _get_finishing_type(0)
        AUTO_EXIT = _get_finishing_type(1)
        DISPLACED = _get_finishing_type(2)
        NATURAL = _get_finishing_type(3)
        RESET = _get_finishing_type(4)
        USER_CANCEL = _get_finishing_type(5)
        SI_FINISHED = _get_finishing_type(6)
        TARGET_DELETED = _get_finishing_type(7)
        FAILED_TESTS = _get_finishing_type(8)
        TRANSITION_FAILURE = _get_finishing_type(9)
        INTERACTION_INCOMPATIBILITY = _get_finishing_type(10)
        INTERACTION_QUEUE = _get_finishing_type(11)
        PRIORITY = _get_finishing_type(12)
        SOCIALS = _get_finishing_type(13)
        WAIT_IN_LINE = _get_finishing_type(14)
        OBJECT_CHANGED = _get_finishing_type(15)
        SITUATIONS = _get_finishing_type(16)
        CRAFTING = _get_finishing_type(17)
        LIABILITY = _get_finishing_type(18)
        DIALOG = _get_finishing_type(19)
        CONDITIONAL_EXIT = _get_finishing_type(20)
        FIRE = _get_finishing_type(21)
        WEDDING = _get_finishing_type(22)
        UNKNOWN = _get_finishing_type(23)

    class InteractionSource:
        __qualname__ = 'TurboInteractionUtil.InteractionSource'

        def _get_interaction_source(*args):
            try:
                return InteractionSource(args[0])
            except:
                return

        PIE_MENU = _get_interaction_source(0)
        AUTONOMY = _get_interaction_source(1)
        BODY_CANCEL_AOP = _get_interaction_source(2)
        CARRY_CANCEL_AOP = _get_interaction_source(3)
        SCRIPT = _get_interaction_source(4)
        UNIT_TEST = _get_interaction_source(5)
        POSTURE_GRAPH = _get_interaction_source(6)
        SOCIAL_ADJUSTMENT = _get_interaction_source(7)
        REACTION = _get_interaction_source(8)
        GET_COMFORTABLE = _get_interaction_source(9)
        SCRIPT_WITH_USER_INTENT = _get_interaction_source(10)

    class InteractionContext:
        __qualname__ = 'TurboInteractionUtil.InteractionContext'

        def _get_interaction_source(*args):
            try:
                return InteractionSource(args[0])
            except:
                return

        SOURCE_PIE_MENU = _get_interaction_source(0)
        SOURCE_AUTONOMY = _get_interaction_source(1)
        SOURCE_BODY_CANCEL_AOP = _get_interaction_source(2)
        SOURCE_CARRY_CANCEL_AOP = _get_interaction_source(3)
        SOURCE_SCRIPT = _get_interaction_source(4)
        SOURCE_UNIT_TEST = _get_interaction_source(5)
        SOURCE_SOCIAL_ADJUSTMENT = _get_interaction_source(7)
        SOURCE_REACTION = _get_interaction_source(8)
        SOURCE_GET_COMFORTABLE = _get_interaction_source(9)
        SOURCE_SCRIPT_WITH_USER_INTENT = _get_interaction_source(10)
        SOURCE_POSTURE_GRAPH = _get_interaction_source(6)
        TRANSITIONAL_SOURCES = frozenset((SOURCE_SOCIAL_ADJUSTMENT, SOURCE_GET_COMFORTABLE, SOURCE_POSTURE_GRAPH))

    @staticmethod
    def get_interaction_sim(interaction_instance):
        return interaction_instance.sim

    @staticmethod
    def get_interaction_target(interaction_instance):
        return interaction_instance.target

    @staticmethod
    def get_affordance_tags(interaction_instance):
        return interaction_instance.get_category_tags()

    @staticmethod
    def get_interaction_start_time(interaction_instance):
        return interaction_instance.start_time

    @staticmethod
    def can_interaction_fallback_to_mixer_interaction(sim, interaction):
        if interaction is None:
            return True
        for running_interaction in sim.si_state:
            if running_interaction.is_guaranteed():
                pass
            if not can_displace(interaction, running_interaction):
                pass
            if not sim.si_state.are_sis_compatible(running_interaction, interaction):
                pass
        return False

    @staticmethod
    def kill_interaction(interaction_instance):
        interaction_instance.kill()

    @staticmethod
    def get_interaction_from_enqueue_result(enqueue_result):
        return enqueue_result.interaction
