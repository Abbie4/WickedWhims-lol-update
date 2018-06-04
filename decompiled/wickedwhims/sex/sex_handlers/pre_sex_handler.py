'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from turbolib.manager_util import TurboManagerUtil
from turbolib.sim_util import TurboSimUtil
from turbolib.world_util import TurboWorldUtil
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.sex.animations.animations_operator import get_animation_from_identifier
from wickedwhims.sex.enums.sex_gender import get_sim_sex_gender
from wickedwhims.sex.enums.sex_type import get_sex_category_type_by_name
from wickedwhims.sex.sex_handlers.active.active_sex_handler import ActiveSexInteractionHandler
from wickedwhims.sex.sex_handlers.sex_handler import SexInteractionHandler
from wickedwhims.sex.sex_handlers.sex_handler_utils import get_sim_sex_state_snapshot
from wickedwhims.sex.sex_operators.general_sex_handlers_operator import clear_sim_sex_extra_data
from wickedwhims.utils_interfaces import display_notification

class PreSexInteractionHandler(SexInteractionHandler):
    __qualname__ = 'PreSexInteractionHandler'

    def __init__(self, interaction_type, creator_sim_id, object_identifier, gameobject_id, object_height, lot_id, location_x, location_y, location_z, location_level, location_angle, route_x, route_y, route_z, route_level, is_manual=False, is_autonomy=False, is_joining=False):
        super().__init__(creator_sim_id, object_identifier, gameobject_id, object_height, lot_id, location_x, location_y, location_z, location_level, location_angle, route_x, route_y, route_z, route_level, is_manual=is_manual, is_autonomy=is_autonomy)
        self._hash_id_cache = ''
        self._interaction_type = interaction_type
        self._sims_ids_list = list()
        self.add_sim(creator_sim_id)
        self._is_animation_paused = False
        self._is_timer_paused = False
        self._linked_sex_handler_identifier = None
        self._is_joining = is_joining
        self._is_failure = False
        self._is_success = False

    def get_identifier(self):
        if self._hash_id_cache is not None:
            return self._hash_id_cache
        data_collection = list()
        for sim_id in self._sims_ids_list:
            data_collection.append(sim_id)
        data_collection.append(self.get_lot_id())
        data_collection = sorted(data_collection)
        hash_value = 3430008
        for item in data_collection:
            hash_value = eval(hex(1000003*hash_value & 4294967295)[:-1]) ^ item
        hash_value ^= len(data_collection)
        hash_value = str(hash_value)
        self._hash_id_cache = str(hash_value)
        return hash_value

    def get_interaction_type(self):
        return self._interaction_type

    def set_interaction_type(self, interaction_type):
        self._interaction_type = interaction_type

    def set_animation_instance(self, animation_instance):
        self._interaction_type = animation_instance.get_sex_category()
        super().set_animation_instance(animation_instance)

    def get_sims_amount(self):
        return len(self._sims_ids_list)

    def add_sim(self, sim):
        sim_id = TurboManagerUtil.Sim.get_sim_id(sim)
        if sim_id in self._sims_ids_list:
            return
        self._sims_ids_list.append(sim_id)

    def get_second_sim_id(self):
        for sim_id in self._sims_ids_list:
            while sim_id != self.get_creator_sim_id():
                return int(sim_id)
        return -1

    def get_actors_sim_info_gen(self):
        for sim_id in self._sims_ids_list:
            yield TurboManagerUtil.Sim.get_sim_info(sim_id)

    def get_actors_sim_instance_gen(self):
        for sim_info in self.get_actors_sim_info_gen():
            yield TurboManagerUtil.Sim.get_sim_instance(sim_info)

    def is_npc_only(self):
        for sim_info in self.get_actors_sim_info_gen():
            while TurboSimUtil.Sim.is_player(sim_info):
                return False
        return True

    def are_all_sims_ready(self):
        for sim_info in self.get_actors_sim_info_gen():
            while sim_ev(sim_info).is_ready_to_sex is False:
                return False
        return True

    def _get_active_sex_handler(self):
        active_sex_handler = ActiveSexInteractionHandler(self.get_creator_sim_id(), self.get_object_identifier(), self.get_game_object_id(), self.get_object_height(), self.get_lot_id(), self.location_x, self.location_y, self.location_z, self.location_level, self.location_angle, self.route_x, self.route_y, self.route_z, self.route_level, is_autonomy=self.is_autonomy_sex())
        active_sex_handler.is_timer_paused = self._is_timer_paused
        active_sex_handler.is_animation_paused = self._is_animation_paused
        active_sex_handler.linked_sex_handler_identifier = self._linked_sex_handler_identifier
        active_sex_handler.set_animation_instance(self.get_animation_instance())
        if active_sex_handler.get_animation_instance() is None:
            display_notification(text='Tried creating sex interaction without animation data!\
\
This not an intended behaviour and it should be reported.', title='WickedWhims Error', is_safe=True)
            return
        from wickedwhims.sex.sex_operators.active_sex_handlers_operator import queue_unregister_active_sex_handler
        for sim_info in self.get_actors_sim_info_gen():
            old_sex_handler = sim_ev(sim_info).active_sex_handler
            if old_sex_handler is not None:
                queue_unregister_active_sex_handler(old_sex_handler)
            if not active_sex_handler.assign_actor(TurboManagerUtil.Sim.get_sim_id(sim_info), get_sim_sex_gender(sim_info)):
                display_notification(text='Tried to assign actor on sex handler creation and failed!', title='WickedWhims Error', is_safe=True)
                return
            sim_ev(sim_info).sim_sex_state_snapshot = get_sim_sex_state_snapshot(sim_info)
            sim_ev(sim_info).sim_immutable_sex_state_snapshot = get_sim_sex_state_snapshot(sim_info)
        if not active_sex_handler.is_actors_list_full():
            display_notification(text='Sex handler is missing actors for selected animation!\
\
Remember the selected animation name, used sims (genders) and settings (gender settings) when reporting this problem!', title='WickedWhims Error', is_safe=True)
            return
        return active_sex_handler

    def start_sex_interaction(self):
        active_sex_handler = self._get_active_sex_handler()
        for sim_info in self.get_actors_sim_info_gen():
            if active_sex_handler is None:
                clear_sim_sex_extra_data(sim_info)
            sim_ev(sim_info).active_sex_handler_identifier = active_sex_handler.get_identifier()
            sim_ev(sim_info).active_sex_handler = active_sex_handler
            if self.is_autonomy_sex():
                sim_ev(sim_info).last_sex_autonomy = TurboWorldUtil.Time.get_absolute_ticks()
            clear_sim_sex_extra_data(sim_info, only_pre_active_data=True)
            TurboSimUtil.Sim.reset_sim(sim_info)
            sim_ev(sim_info).has_setup_sex = True
            active_sex_handler.play_if_everyone_ready()

    def is_valid(self):
        if self.get_animation_instance() is None or self.get_object_identifier() is None:
            return False
        return True

    def pause_animation(self):
        self._is_animation_paused = True

    def pause_timer(self):
        self._is_timer_paused = True

    def link_active_sex_handler(self, active_sex_handler):
        self._linked_sex_handler_identifier = active_sex_handler.get_identifier()

    def is_joining_sex(self):
        return self._is_joining

    def set_as_success(self):
        self._is_success = True

    def is_success_sex(self):
        return self._is_success

    def set_as_failure(self):
        self._is_failure = True

    def is_failure_sex(self):
        return self._is_failure

    def get_save_dict(self):
        save_data = super().get_save_dict()
        save_data['hash_id'] = self._hash_id_cache
        save_data['interaction_type'] = self._interaction_type.name
        save_data['sims_list'] = self._sims_ids_list
        save_data['is_animation_paused'] = self._is_animation_paused
        save_data['is_timer_paused'] = self._is_timer_paused
        save_data['linked_sex_handler_identifier'] = self._linked_sex_handler_identifier
        save_data['is_joining'] = self._is_joining
        save_data['is_success'] = self._is_success
        save_data['is_failure'] = self._is_failure
        return save_data

    @staticmethod
    def load_from_dict(save_data):
        interaction_type = get_sex_category_type_by_name(save_data.get('interaction_type', 'NONE'))
        creator_sim_id = save_data.get('creator_sim', -1)
        game_object_id = save_data.get('gameobject_id', -1)
        object_identifier_name = save_data.get('object_identifier_name', None)
        object_identifier_guid = save_data.get('object_identifier_guid', -1)
        object_identifier = (object_identifier_name, object_identifier_guid)
        object_height = save_data.get('object_height', 0)
        lot_id = save_data.get('lot_id', -1)
        location_x = save_data.get('location_x', 0)
        location_y = save_data.get('location_y', 0)
        location_z = save_data.get('location_z', 0)
        location_level = save_data.get('location_level', 0)
        location_angle = save_data.get('location_angle', 0)
        route_x = save_data.get('route_x', 0)
        route_y = save_data.get('route_y', 0)
        route_z = save_data.get('route_z', 0)
        route_level = save_data.get('route_level', 0)
        is_animation_paused = save_data.get('is_animation_paused', False)
        is_timer_paused = save_data.get('is_timer_paused', False)
        linked_sex_handler_identifier = save_data.get('linked_sex_handler_identifier', None)
        is_autonomy = save_data.get('is_autonomy', False)
        is_manual = save_data.get('is_manual', False)
        is_joining = save_data.get('is_joining', False)
        is_success = save_data.get('is_success', False)
        is_failure = save_data.get('is_failure', False)
        animation_identifier = save_data.get('animation_identifier', '-1')
        animation_instance = get_animation_from_identifier(animation_identifier)
        if animation_instance is None:
            return
        hash_id = save_data.get('hash_id', None)
        pre_sex_handler = PreSexInteractionHandler(interaction_type, creator_sim_id, object_identifier, game_object_id, object_height, lot_id, location_x, location_y, location_z, location_level, location_angle, route_x, route_y, route_z, route_level, is_manual=is_manual, is_autonomy=is_autonomy, is_joining=is_joining)
        pre_sex_handler.set_animation_instance(animation_instance)
        if is_animation_paused is True:
            pre_sex_handler.pause_animation()
        if is_timer_paused is True:
            pre_sex_handler.pause_timer()
        if is_success is True:
            pre_sex_handler.set_as_success()
        if is_failure is True:
            pre_sex_handler.set_as_failure()
        pre_sex_handler._linked_sex_handler_identifier = linked_sex_handler_identifier
        saved_sims_ids = save_data.get('sims_list', list())
        for sim_id in saved_sims_ids:
            pre_sex_handler.add_sim(sim_id)
        pre_sex_handler._hash_id_cache = hash_id
        return pre_sex_handler

    def get_string_data(self):
        basic_data = super().get_string_data()
        return basic_data + '\
 Interaction Type: ' + str(self._interaction_type.name) + '\
 Sims List: ' + str(', '.join(str(v) for v in self._sims_ids_list))

