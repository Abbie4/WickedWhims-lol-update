'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from enums.tags_enum import GameTag
from turbolib.components_util import TurboComponentUtil
from turbolib.math_util import TurboMathUtil
from turbolib.object_util import TurboObjectUtil
from turbolib.resource_util import TurboResourceUtil
from turbolib.world_util import TurboWorldUtil
from turbolib.wrappers.interactions import TurboImmediateSuperInteraction, TurboInteractionStartMixin
from wickedwhims.debug.debug_controller import is_main_debug_flag_enabled
from wickedwhims.sex.autonomy._ts4_autonomy_utils import has_game_object_all_free_slots
from wickedwhims.sex.sex_location_handler import SexInteractionLocationType
from wickedwhims.utils_interfaces import display_notification
from wickedwhims.utils_objects import get_object_fixed_direction

class DisplayObjectDataInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'DisplayObjectDataInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return is_main_debug_flag_enabled()

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        target = cls.get_interaction_target(interaction_instance)
        tags_list = list()
        for tag in TurboObjectUtil.GameObject.get_game_tags(target):
            try:
                game_tag = str(GameTag(int(tag)).name)
            except:
                game_tag = str(tag)
            tags_list.append(game_tag)
        state_list = list()
        if TurboComponentUtil.has_component(target, TurboComponentUtil.ComponentType.STATE):
            for (key, value) in TurboComponentUtil.get_component(target, TurboComponentUtil.ComponentType.STATE).items():
                try:
                    state_list.append('(' + str(key.__name__) + ', ' + str(value.value) + ')')
                except:
                    pass
        object_wwid = SexInteractionLocationType.get_location_identifier(target)
        routing_surface = TurboMathUtil.Location.get_location_routing_surface(TurboObjectUtil.Position.get_location(target))
        position = TurboObjectUtil.Position.get_position(target) + get_object_fixed_direction(target)
        display_notification(text='Object WWID: ' + str(object_wwid[1]) + '\
Object WW Category: ' + str(object_wwid[0]) + '\
\
Name: ' + str(TurboObjectUtil.GameObject.get_catalog_name(target)) + '\
Class: ' + str(target.__class__.__name__) + '\
Object ID: ' + str(TurboResourceUtil.Resource.get_id(target)) + '\
Object GUID: ' + str(TurboResourceUtil.Resource.get_guid64(target)) + '\
\
X: ' + str(position.x) + '\
Y: ' + str(position.y) + '\
Z: ' + str(position.z) + '\
\
Room ID: ' + str(TurboWorldUtil.Lot.get_room_id(TurboObjectUtil.Position.get_location(target), position=position)) + '\
In Use: ' + str(TurboObjectUtil.GameObject.is_in_use(target)) + '\
All Free Slots: ' + str(has_game_object_all_free_slots(target)) + '\
Is Routable: ' + str(TurboWorldUtil.Routing.is_position_routable(routing_surface, position)) + '\
\
Tags:\
' + ', '.join(tags_list) + '\
States:\
' + ', '.join(state_list))

