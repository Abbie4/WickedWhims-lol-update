import routing
import routing.connectivity
from animation.animation_utils import flush_all_animations
from animation.posture_manifest_constants import STAND_OR_MOVING_STAND_CONSTRAINT, STAND_CONSTRAINT
from element_utils import build_critical_section
from event_testing.results import TestResult
from interactions.base.immediate_interaction import ImmediateSuperInteraction
from interactions.base.interaction import Interaction
from interactions.base.mixer_interaction import MixerInteraction
from interactions.base.super_interaction import SuperInteraction
from interactions.constraints import Circle
from interactions.context import InteractionContext
from interactions.social.social_mixer_interaction import SocialMixerInteraction
from objects.terrain import TerrainInteractionMixin, TravelMixin
from server.pick_info import PickType
from sims4.utils import flexmethod
from turbolib.interaction_util import TurboInteractionUtil
from turbolib.math_util import TurboMathUtil


class _TurboBaseInteractionUtil:
    __qualname__ = '_TurboBaseInteractionUtil'

    @classmethod
    def get_interaction_sim(cls, interaction_context_or_instance):
        return interaction_context_or_instance.sim

    @classmethod
    def get_interaction_target(cls, interaction_context_or_instance):
        if isinstance(interaction_context_or_instance, Interaction):
            return interaction_context_or_instance.target

    @classmethod
    def get_interaction_context(cls, interaction_context_or_instance):
        if isinstance(interaction_context_or_instance, InteractionContext):
            return interaction_context_or_instance
        return interaction_context_or_instance.context

    @classmethod
    def get_interaction_source(cls, interaction_context_or_instance):
        if isinstance(interaction_context_or_instance, InteractionContext):
            return interaction_context_or_instance.source
        return interaction_context_or_instance.context.source

    @classmethod
    def cancel_interaction(cls, interaction_instance, finishing_type=TurboInteractionUtil.FinishingType.NATURAL):
        interaction_instance.cancel(finishing_type, '_TurboBaseInteractionUtil.cancel_interaction')

    @classmethod
    def kill_interaction(cls, interaction_context_or_instance):
        if isinstance(interaction_context_or_instance, Interaction):
            interaction_context_or_instance.kill()


class _TurboConstraintUtil:
    __qualname__ = '_TurboConstraintUtil'

    @classmethod
    def get_stand_or_move_stand_posture_constraint(cls):
        return STAND_OR_MOVING_STAND_CONSTRAINT

    @classmethod
    def get_stand_posture_constraint(cls):
        return STAND_CONSTRAINT

    @classmethod
    def get_circle_constraint(cls, origin_position, radius, routing_surface, ideal_radius=None, ideal_radius_width=0):
        return Circle(origin_position, radius, routing_surface, ideal_radius=ideal_radius, ideal_radius_width=ideal_radius_width)

    @classmethod
    def combine_constraints(cls, constraints):
        total_constraints = None
        for constraint in constraints:
            if total_constraints is None:
                total_constraints = constraint
            else:
                total_constraints.intersect(constraint)
        return total_constraints


class _TurboInteraction(Interaction, _TurboBaseInteractionUtil):
    __qualname__ = '_TurboInteraction'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if issubclass(self.__class__, TurboInteractionInitMixin):
            self.on_interaction_init(self)

    @classmethod
    def _test(cls, target, context, **kwargs):
        interaction_test_result = cls.on_interaction_test(context, target)
        if interaction_test_result:
            return TestResult.TRUE
        return TestResult.NONE

    def _trigger_interaction_start_event(self):
        super()._trigger_interaction_start_event()
        if issubclass(self.__class__, TurboInteractionStartMixin):
            self.on_interaction_start(self)

    def setup_asm_default(self, asm, *args, **kwargs):
        if issubclass(self.__class__, TurboInteractionASMMixin):
            return self.on_interaction_asm_setup(self, asm)
        return super().setup_asm_default(asm, *args, **kwargs)

    def cancel(self, finishing_type, cancel_reason_msg, **kwargs):
        if issubclass(self.__class__, TurboInteractionCancelMixin):
            self.on_interaction_cancel(self, finishing_type)
        return super().cancel(finishing_type, cancel_reason_msg, **kwargs)

    def _post_perform(self):
        if issubclass(self.__class__, TurboInteractionFinishMixin):
            self.on_interaction_finish(self)
        return super()._post_perform()


class TurboBaseSuperInteraction(_TurboInteraction, SuperInteraction):
    __qualname__ = 'TurboBaseSuperInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        raise NotImplementedError


class TurboSuperInteraction(TurboBaseSuperInteraction):
    __qualname__ = 'TurboSuperInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        raise NotImplementedError

    def _run_interaction_gen(self, timeline):
        super()._run_interaction_gen(timeline)
        return self.on_interaction_run(self)

    @classmethod
    def on_interaction_run(cls, interaction_instance):
        raise NotImplementedError


class TurboImmediateSuperInteraction(_TurboInteraction, ImmediateSuperInteraction):
    __qualname__ = 'TurboImmediateSuperInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        raise NotImplementedError


class TurboTerrainImmediateSuperInteraction(_TurboInteraction, TravelMixin, TerrainInteractionMixin, ImmediateSuperInteraction):
    __qualname__ = 'TurboTerrainImmediateSuperInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        raise NotImplementedError

    @classmethod
    def is_terrain_location_valid(cls, interaction_target, interaction_context):
        (position, surface) = cls._get_position_and_surface(interaction_target, interaction_context)
        if position is None:
            return False
        if interaction_context.pick is not None and (interaction_context.pick.pick_type is not None and (interaction_context.pick.pick_type != PickType.PICK_TERRAIN and interaction_context.pick.pick_type != PickType.PICK_FLOOR)) and interaction_context.pick.pick_type != PickType.PICK_POOL_SURFACE:
            return False
        if surface is None:
            return False
        routing_location = routing.Location(position, TurboMathUtil.Orientation.get_quaternion_identity(), surface)
        if not routing.test_connectivity_permissions_for_handle(routing.connectivity.Handle(routing_location), interaction_context.sim.routing_context):
            return False
        return True


class TurboMixerInteraction(_TurboInteraction, MixerInteraction):
    __qualname__ = 'TurboMixerInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        raise NotImplementedError


class TurboSocialMixerInteraction(_TurboInteraction, SocialMixerInteraction):
    __qualname__ = 'TurboSocialMixerInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        raise NotImplementedError


class TurboInteractionInitMixin:
    __qualname__ = 'TurboInteractionInitMixin'

    @classmethod
    def on_interaction_init(cls, interaction_instance):
        raise NotImplementedError


class TurboInteractionSetupMixin(Interaction):
    __qualname__ = 'TurboInteractionSetupMixin'

    def _setup_gen(self, timeline):
        result = super()._setup_gen(timeline)
        if result:
            self.on_interaction_setup(self)
        return result

    @classmethod
    def on_interaction_setup(cls, interaction_instance):
        raise NotImplementedError


class TurboInteractionBasicElementsMixin(SuperInteraction):
    __qualname__ = 'TurboInteractionBasicElementsMixin'

    def build_basic_elements(self, *args, sequence=(), **kwargs):
        sequence = super().build_basic_elements(sequence=sequence)
        return build_critical_section(sequence, self.on_building_basic_elements(self, sequence), flush_all_animations)

    @classmethod
    def on_building_basic_elements(cls, interaction_instance, sequence):
        raise NotImplementedError


class TurboInteractionConstraintMixin(SuperInteraction, _TurboConstraintUtil):
    __qualname__ = 'TurboInteractionConstraintMixin'

    @flexmethod
    def _constraint_gen(self, inst, sim, target, *args, **kwargs):
        yield self.on_constraint(inst if inst is not None else self, sim, target)

    @classmethod
    def on_constraint(cls, interaction_instance, interaction_sim, interaction_target):
        raise NotImplementedError


class TurboInteractionConstraintResetMixin(SuperInteraction, _TurboConstraintUtil):
    __qualname__ = 'TurboInteractionConstraintResetMixin'

    @flexmethod
    def _constraint_gen(self, *args, **kwargs):
        return ()


class TurboInteractionASMMixin:
    __qualname__ = 'TurboInteractionASMMixin'

    @classmethod
    def on_interaction_asm_setup(cls, interaction_instance, interaction_asm):
        raise NotImplementedError


class TurboInteractionNameMixin:
    __qualname__ = 'TurboInteractionNameMixin'

    @flexmethod
    def get_name(self, inst, *_, **__):
        inst_or_cls = inst if inst is not None else self
        return self.get_interaction_name(inst_or_cls)

    @classmethod
    def get_interaction_name(cls, interaction_instance):
        raise NotImplementedError


class TurboInteractionStartMixin:
    __qualname__ = 'TurboInteractionStartMixin'

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        raise NotImplementedError


class TurboInteractionCancelMixin:
    __qualname__ = 'TurboInteractionCancelMixin'

    @classmethod
    def on_interaction_cancel(cls, interaction_instance, finishing_type):
        raise NotImplementedError


class TurboInteractionFinishMixin:
    __qualname__ = 'TurboInteractionFinishMixin'

    @classmethod
    def on_interaction_finish(cls, interaction_instance):
        raise NotImplementedError

