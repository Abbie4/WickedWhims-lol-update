from turbolib.sim_util import TurboSimUtil
from turbolib.world_util import TurboWorldUtil
from turbolib.wrappers.interactions import TurboSuperInteraction, TurboInteractionConstraintMixin

class GoToHouseInteraction(TurboSuperInteraction, TurboInteractionConstraintMixin):
    __qualname__ = 'GoToHouseInteraction'

    @classmethod
    def on_constraint(cls, interaction_instance, interaction_sim, interaction_target):
        house_position = TurboWorldUtil.Lot.get_spawn_position() or TurboWorldUtil.Lot.get_active_lot_corners()[0]
        if house_position is None:
            return
        circle_constraint = cls.get_circle_constraint(house_position, 1.5, TurboSimUtil.Location.get_routing_surface(interaction_sim), ideal_radius=1, ideal_radius_width=0.5)
        posture_constraint = cls.get_stand_or_move_stand_posture_constraint()
        return cls.combine_constraints((circle_constraint, posture_constraint))

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return True

    @classmethod
    def on_interaction_run(cls, interaction_instance):
        return True

