'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from turbolib.resource_util import TurboResourceUtil
from turbolib.types_util import TurboTypesUtil
from turbolib.wrappers.interactions import TurboImmediateSuperInteraction, TurboInteractionStartMixin
from wickedwhims.sex.autonomy.disabled_locations_handler import update_disabled_sex_locations_data, switch_autonomy_sex_disabled_location, is_autonomy_sex_locations_disabled

class CheatEnableAutonomySexLocationInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'CheatEnableAutonomySexLocationInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        if interaction_target is None or not TurboTypesUtil.Objects.is_game_object(interaction_target):
            return False
        target_id = TurboResourceUtil.Resource.get_id(interaction_target)
        return is_autonomy_sex_locations_disabled(target_id)

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        switch_autonomy_sex_disabled_location(TurboResourceUtil.Resource.get_id(cls.get_interaction_target(interaction_instance)))
        update_disabled_sex_locations_data()
        return True

class CheatDisableAutonomySexLocationInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'CheatDisableAutonomySexLocationInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        if interaction_target is None or not TurboTypesUtil.Objects.is_game_object(interaction_target):
            return False
        target_id = TurboResourceUtil.Resource.get_id(interaction_target)
        return not is_autonomy_sex_locations_disabled(target_id)

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        switch_autonomy_sex_disabled_location(TurboResourceUtil.Resource.get_id(cls.get_interaction_target(interaction_instance)))
        update_disabled_sex_locations_data()
        return True

