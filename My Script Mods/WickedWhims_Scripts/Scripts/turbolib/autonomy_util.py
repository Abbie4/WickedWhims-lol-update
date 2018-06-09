
class TurboAutonomyUtil:
    __qualname__ = 'TurboAutonomyUtil'

    class ObjectPreferenceTag:
        __qualname__ = 'TurboAutonomyUtil.ObjectPreferenceTag'
        LOVESEAT = 0
        BED = 1
        STUFFED_ANIMAL = 2
        INSTRUMENT = 3
        COMPUTER = 4
        FOOD = 5
        DRINK = 6
        TENT = 7
        FOOD_BOWL = 8
        PET_SLEEP_OBJECT = 9

    class RoleStates:
        __qualname__ = 'TurboAutonomyUtil.RoleStates'

        @staticmethod
        def is_rolestate_allowing_player_sims(role_state_instance):
            return not role_state_instance._portal_disallowance_tags

        @staticmethod
        def is_rolestate_allowing_npc_sims(role_state_instance):
            return not role_state_instance._portal_disallowance_tags and role_state_instance._allow_npc_routing_on_active_lot

