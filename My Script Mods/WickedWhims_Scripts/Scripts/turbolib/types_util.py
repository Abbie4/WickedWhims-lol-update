from buffs.buff import Buff
from objects.doors.door import Door
from objects.game_object import GameObject
from objects.terrain import Terrain
from sims.self_interactions import NPCLeaveLotInteraction
from sims.sim import Sim
from sims4.math import Location

class TurboTypesUtil:
    __qualname__ = 'TurboTypesUtil'

    class Sims:
        __qualname__ = 'TurboTypesUtil.Sims'

        @staticmethod
        def is_sim(obj):
            return isinstance(obj, Sim)

    class Objects:
        __qualname__ = 'TurboTypesUtil.Objects'

        @staticmethod
        def is_game_object(obj):
            return isinstance(obj, GameObject)

        @staticmethod
        def is_terrain(obj):
            return isinstance(obj, Terrain)

        @staticmethod
        def is_door(obj):
            return isinstance(obj, Door)

    class Data:
        __qualname__ = 'TurboTypesUtil.Data'

        @staticmethod
        def is_buff(obj):
            return isinstance(obj, Buff)

        @staticmethod
        def is_location(obj):
            return isinstance(obj, Location)

    class Interactions:
        __qualname__ = 'TurboTypesUtil.Interactions'

        @staticmethod
        def is_npc_leave_lot_interaction(interaction):
            return isinstance(interaction, NPCLeaveLotInteraction)

