import random
from math import cos, sin
from enums.interactions_enum import SimInteraction
from turbolib.interaction_util import TurboInteractionUtil
from turbolib.manager_util import TurboManagerUtil
from turbolib.math_util import TurboMathUtil
from turbolib.object_util import TurboObjectUtil
from turbolib.sim_util import TurboSimUtil
from turbolib.world_util import TurboWorldUtil
from wickedwhims.debug.debug_controller import is_main_debug_flag_enabled
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.sex._ts4_sex_utils import apply_pressure_to_interactions_queue
from wickedwhims.sex.animations.animations_operator import get_animation_from_identifier, get_animations_max_amount_of_actors
from wickedwhims.sex.enums.sex_gender import get_sim_sex_gender, SexGenderType
from wickedwhims.sex.settings.sex_settings import SexGenderTypeSetting, SexSetting, get_sex_setting, SexAutonomyLevelSetting
from wickedwhims.sex.sex_handlers.active.active_sex_handler_updates import update_active_sex_handler
from wickedwhims.sex.sex_handlers.active.utils.after import apply_after_sex_functions, apply_after_sex_relationship
from wickedwhims.sex.sex_handlers.active.utils.before import apply_before_sex_functions
from wickedwhims.sex.sex_handlers.sex_handler import SexInteractionHandler
from wickedwhims.sex.sex_operators.active_sex_handlers_operator import queue_unregister_active_sex_handler, register_active_sex_handler, get_active_sex_handlers
from wickedwhims.sex.sex_operators.general_sex_handlers_operator import clear_sim_sex_extra_data
from wickedwhims.sex.sex_operators.pre_sex_handlers_operator import unprepare_npc_sim_from_sex
from wickedwhims.sxex_bridge.body import update_sim_body_flags
from wickedwhims.sxex_bridge.underwear import update_sim_underwear_data
from wickedwhims.utils_interfaces import display_notification


class ActiveSexInteractionHandler(SexInteractionHandler):
    __qualname__ = 'ActiveSexInteractionHandler'

    def __init__(self, creator_sim_id, object_identifier, gameobject_id, object_height, lot_id, location_x, location_y, location_z, location_level, location_angle, route_x, route_y, route_z, route_level, is_manual=False, is_autonomy=False):
        super().__init__(creator_sim_id, object_identifier, gameobject_id, object_height, lot_id, location_x, location_y, location_z, location_level, location_angle, route_x, route_y, route_z, route_level, is_manual=is_manual, is_autonomy=is_autonomy)
        self._hash_id_cache = None
        self.next_animation_instance = None
        self.is_canceled = False
        self.is_prepared_to_play = False
        self._prepare_to_play_count = 0
        self.is_playing = False
        self._actors_list = dict()
        self._populate_actors_list()
        self._is_npc_only_cache = None
        self.ignore_autonomy_join_sims = list()
        self.has_joining_sims = False
        self._pre_counter = 0
        self.overall_counter = 0
        self.animation_counter = 0
        self.one_second_counter = int(self.overall_counter/1000)
        self.sim_minute_counter = int(self.overall_counter/1500)
        self.is_registered = False
        self.is_ready_to_unregister = False
        self._is_restarting = False
        if get_sex_setting(SexSetting.AUTONOMY_LEVEL, variable_type=int) == SexAutonomyLevelSetting.HIGH:
            self.autonomy_actors_limit = random.randint(3, max(3, get_animations_max_amount_of_actors(self.get_object_identifier())))
        else:
            self.autonomy_actors_limit = random.randint(2, max(2, get_animations_max_amount_of_actors(self.get_object_identifier())))
        self.is_animation_paused = False
        self.is_timer_paused = False
        self.linked_sex_handler_identifier = None
        self.force_positioning_count = 0
        self.pregnancy_sex_counter = 0
        self.has_displayed_pregnancy_notification = False
        self.tried_auto_apply_birth_control = False
        self.is_at_climax = False
        self.climax_counter = 0
        self.climax_reach_value = 0
        self.go_away_sims_list = set()
        self.has_reacted_sims_list = set()
        self.unsilence_phone_after_sex = False

    def get_identifier(self):
        if self._hash_id_cache is not None:
            return self._hash_id_cache
        data_collection = list()
        for sim_id in self.get_actors_sim_id():
            data_collection.append(sim_id)
        data_collection.append(self.get_lot_id())
        data_collection = sorted(data_collection)
        hash_value = 3430008
        for item in data_collection:
            hash_value = eval(hex(1000003*hash_value & 4294967295)[:-1]) ^ item
        hash_value ^= len(data_collection)
        self._hash_id_cache = str(hash_value)
        return self._hash_id_cache

    def set_animation_instance(self, new_animation_instance, is_animation_change=False, is_manual=False):
        current_animation_instance = self.get_animation_instance()
        self.next_animation_instance = None
        super().set_animation_instance(new_animation_instance)
        if is_animation_change is True and current_animation_instance is not None and not new_animation_instance.is_matching_actors_genders(current_animation_instance):
            self.reassign_actors()
        if is_manual is True:
            self.is_timer_paused = False
            self.is_animation_paused = False

    def get_actor_animation_clip_name(self, actor_id):
        return self.get_animation_instance().get_actor(actor_id).get_animation_clip_name()

    def get_actors_sim_id(self):
        for sim_id in self._actors_list.values():
            yield sim_id

    def get_actors_amount(self):
        return len(self._actors_list)

    def get_actor_id_by_sim_id(self, actor_sim_id):
        for (actor_id, sim_id) in self._actors_list.items():
            if sim_id == actor_sim_id:
                return actor_id
        return -1

    def get_sim_id_by_actor_id(self, actor_id):
        if actor_id in self._actors_list:
            return self._actors_list[actor_id]

    def swap_actors(self, first_actor_id, second_actor_id):
        first_sim_id = self._actors_list[first_actor_id]
        second_sim_id = self._actors_list[second_actor_id]
        self._actors_list[second_actor_id] = first_sim_id
        self._actors_list[first_actor_id] = second_sim_id
        self.restart()

    def _populate_actors_list(self, force_populate=False):
        if self.get_animation_instance() is not None and (len(self._actors_list) == 0 or force_populate is True):
            self._actors_list = dict()
            for actor_data in self.get_animation_instance().get_actors():
                self._actors_list[actor_data.get_actor_id()] = None

    def is_actors_list_full(self):
        for sim_id in self._actors_list.values():
            if sim_id is None:
                return False
        return True

    def reassign_actors(self):
        current_actors_list_copy = self._actors_list.copy()
        sims_sex_gender = list()
        for sim_info in self.get_actors_sim_info_gen():
            sims_sex_gender.append((TurboManagerUtil.Sim.get_sim_id(sim_info), get_sim_sex_gender(sim_info)))
        self._populate_actors_list(force_populate=True)
        for (sim_id, sim_gender) in sims_sex_gender:
            if not self.assign_actor(sim_id, sim_gender):
                display_notification(text='Tried to assign an actor on actors reassigning and failed!', title='WickedWhims Error', is_safe=True)
                self._actors_list = current_actors_list_copy
                self.stop(hard_stop=True, is_end=True, stop_reason='Failed to reassign actors.')
                break

    def assign_actor(self, sim_id, sim_gender_sex_type):
        self._populate_actors_list()
        genders_list = self.get_animation_instance().get_actors_gender_list()
        for (actor_id, (gender, _)) in genders_list:
            if self._actors_list[actor_id] is None and sim_gender_sex_type == gender:
                self._actors_list[actor_id] = sim_id
                return True
        for (actor_id, (gender, preferenced_gender)) in genders_list:
            if self._actors_list[actor_id] is None and (gender == SexGenderType.BOTH or gender == SexGenderType.CBOTH) and preferenced_gender == sim_gender_sex_type:
                self._actors_list[actor_id] = sim_id
                return True
        for (actor_id, (gender, _)) in genders_list:
            if self._actors_list[actor_id] is None and (gender == SexGenderType.BOTH or gender == SexGenderType.CBOTH):
                self._actors_list[actor_id] = sim_id
                return True
        if get_sex_setting(SexSetting.SEX_GENDER_TYPE, variable_type=int) == SexGenderTypeSetting.ANY_BASED:
            for actor_id in self._actors_list.keys():
                if self._actors_list[actor_id] is None:
                    self._actors_list[actor_id] = sim_id
                    return True
        return False

    def has_reached_autonomy_actors_limit(self):
        return self.get_actors_amount() >= self.autonomy_actors_limit

    def get_actors_sim_info_gen(self):
        for sim_id in self._actors_list.values():
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_id)
            if sim_info is None:
                display_notification(text='Failed to identify sim with id ' + str(sim_id) + ' to properly receive its data!', title='WickedWhims Error', is_safe=True)
            yield sim_info

    def get_actors_sim_instance_gen(self):
        for sim_info in self.get_actors_sim_info_gen():
            yield TurboManagerUtil.Sim.get_sim_instance(sim_info)

    def get_sims_list(self):
        sims_list = list()
        for (actor_id, sim_id) in self._actors_list.items():
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_id)
            if sim_info is None:
                display_notification(text='Failed to identify sim with id ' + str(sim_id) + ' to properly return sims list!', title='WickedWhims Error', is_safe=True)
                return ()
            sims_list.append((actor_id, sim_info))
        return sorted(sims_list, key=lambda x: x[0])

    def is_npc_only(self):
        if self._is_npc_only_cache is not None:
            return self._is_npc_only_cache
        for sim_info in self.get_actors_sim_info_gen():
            if not TurboSimUtil.Sim.is_npc(sim_info):
                self._is_npc_only_cache = False
                return False
        self._is_npc_only_cache = True
        return True

    def get_pre_sex_handler(self, is_joining=False):
        from wickedwhims.sex.sex_handlers.pre_sex_handler import PreSexInteractionHandler
        pre_sex_handler = PreSexInteractionHandler(self.get_animation_instance().get_sex_category(), self.get_creator_sim_id(), self.get_object_identifier(), self.get_game_object_id(), self.get_object_height(), self.get_lot_id(), self.location_x, self.location_y, self.location_z, self.location_level, self.location_angle, self.route_x, self.route_y, self.route_z, self.route_level, is_manual=self.is_manual_sex(), is_autonomy=self.is_autonomy_sex(), is_joining=is_joining)
        pre_sex_handler.set_animation_instance(self.get_animation_instance())
        for sex_handler in get_active_sex_handlers():
            if sex_handler.get_identifier() == sex_handler.linked_sex_handler_identifier:
                pre_sex_handler.link_active_sex_handler(sex_handler)
                break
        for sim_id in self.get_actors_sim_id():
            pre_sex_handler.add_sim(sim_id)
        return pre_sex_handler

    def is_valid(self, skip_actors=False):
        if self.get_animation_instance() is None or self.get_object_identifier() is None:
            return False
        if skip_actors is False:
            for sim_info in self.get_actors_sim_info_gen():
                if sim_info is None or sim_ev(sim_info).active_sex_handler is None:
                    return False
        return True

    def play_if_everyone_ready(self):
        for sim_info in self.get_actors_sim_info_gen():
            if sim_ev(sim_info).has_setup_sex is False:
                return
        self.is_prepared_to_play = True
        if self.is_registered is False:
            register_active_sex_handler(self)

    def play(self, is_animation_change=False):
        if self.is_canceled is True:
            return
        if not self.is_valid():
            self.stop(hard_stop=True, stop_reason='Sex Handler detected as invalid!')
            return
        if self.get_game_object_id() != -1 and TurboObjectUtil.GameObject.get_object_with_id(self.get_game_object_id()) is None:
            self.stop(hard_stop=True, stop_reason='Game object used for sex went missing!')
            return
        sims_list = self.get_sims_list()
        is_fresh_start = self.is_playing is False
        self.is_playing = True
        self._is_restarting = False
        self.animation_counter = 0
        self.force_positioning_count = 0
        apply_before_sex_functions(self, sims_list, is_fresh_start)
        for (_, sim_info) in sims_list:
            sim = TurboManagerUtil.Sim.get_sim_instance(sim_info)
            TurboSimUtil.Interaction.cancel_queued_interaction(sim, SimInteraction.WW_SEX_ANIMATION_DEFAULT, finishing_type=TurboInteractionUtil.FinishingType.SI_FINISHED)
            target = None
            if self.get_game_object_id() != -1:
                target = TurboObjectUtil.GameObject.get_object_with_id(self.get_game_object_id())
            TurboSimUtil.Interaction.unlock_queue(sim)
            result = TurboSimUtil.Interaction.push_affordance(sim, SimInteraction.WW_SEX_ANIMATION_DEFAULT, target=target, interaction_context=TurboInteractionUtil.InteractionContext.SOURCE_SCRIPT_WITH_USER_INTENT, insert_strategy=TurboInteractionUtil.QueueInsertStrategy.LAST, priority=TurboInteractionUtil.Priority.High, run_priority=TurboInteractionUtil.Priority.High)
            if result:
                sim_ev(sim_info).is_playing_sex = True
            if is_animation_change is True:
                TurboSimUtil.Interaction.cancel_running_interaction(sim, SimInteraction.WW_SEX_ANIMATION_DEFAULT, finishing_type=TurboInteractionUtil.FinishingType.SI_FINISHED)
                apply_pressure_to_interactions_queue(sim)

    def pre_update(self, ticks):
        if self._pre_counter < 500:
            return
        if self._prepare_to_play_count >= 2:
            self.play()
            return
        for (actor_id, sim_info) in self.get_sims_list():
            sim = TurboManagerUtil.Sim.get_sim_instance(sim_info)
            if sim is not None:
                actor_data = self.get_animation_instance().get_actor(actor_id)
                TurboWorldUtil.Location.move_object_to(sim, self.get_location(), y_offset=actor_data.y_offset, orientation_offset=actor_data.facing_offset)

    def update(self, ticks):
        update_active_sex_handler(self, ticks)

    def stop(self, soft_stop=False, hard_stop=False, no_teleport=False, is_joining_stop=False, is_end=False, stop_reason=None):
        if self._is_restarting is True and hard_stop is False and is_end is False:
            return
        if stop_reason is not None and is_main_debug_flag_enabled():
            display_notification(text=str(stop_reason), title='Sex Stop Reason')
        queue_unregister_active_sex_handler(self)
        sims_list = self.get_sims_list()
        active_angle = random.randint(0, 359)
        angle_section = 360/max(1, self.get_actors_amount())
        if is_joining_stop is False:
            apply_after_sex_functions(self, sims_list, is_ending=is_end)
        apply_after_sex_relationship(self, sims_list)
        for (_, sim_info) in sims_list:
            if sim_info is None:
                continue
            clear_sim_sex_extra_data(sim_info, only_active_data=is_joining_stop)
            unprepare_npc_sim_from_sex(sim_info)
            TurboSimUtil.Interaction.unlock_queue(sim_info)
            update_sim_body_flags(sim_info)
            update_sim_underwear_data(sim_info)
            if soft_stop is False and no_teleport is False and self.get_object_identifier()[0] == 'FLOOR':
                active_angle = (active_angle + angle_section) % 360
                new_location = TurboMathUtil.Location.apply_offset(self.get_location(), x_offset=cos(active_angle)*0.4, z_offset=sin(active_angle)*0.4, orientation_offset=random.randint(0, 360))
                new_location = TurboWorldUtil.Zone.find_good_location(new_location)
                sim = TurboManagerUtil.Sim.get_sim_instance(sim_info)
                if sim is not None:
                    TurboWorldUtil.Location.move_object_to(sim, new_location)
            TurboSimUtil.Sim.reset_sim(sim_info, hard_reset_on_exception=True)
            TurboSimUtil.Interaction.push_affordance(sim_info, SimInteraction.SIM_STAND, interaction_context=TurboInteractionUtil.InteractionContext.SOURCE_POSTURE_GRAPH, insert_strategy=TurboInteractionUtil.QueueInsertStrategy.FIRST, must_run_next=True, priority=TurboInteractionUtil.Priority.Critical, run_priority=TurboInteractionUtil.Priority.Critical, skip_if_running=True)
        location_game_object = TurboObjectUtil.GameObject.get_object_with_id(self.get_game_object_id())
        if location_game_object is not None:
            TurboObjectUtil.GameObject.reset(location_game_object)

    def restart(self):
        if self._is_restarting is True:
            return
        self._is_restarting = True
        self.is_playing = False
        self.is_prepared_to_play = False
        self._pre_counter = 0
        self._prepare_to_play_count = 0
        self.animation_counter = 0
        self.force_positioning_count = 0
        self.one_second_counter = 0
        self.sim_minute_counter = 0
        for sim_info in self.get_actors_sim_info_gen():
            sim_ev(sim_info).has_setup_sex = False
            TurboSimUtil.Sim.reset_sim(sim_info)
            sim_ev(sim_info).has_setup_sex = True
            self.play_if_everyone_ready()

    def reset(self):
        pre_sex_handler = self.get_pre_sex_handler()
        self.stop(hard_stop=True, no_teleport=True, stop_reason='Reset Triggered')
        pre_sex_handler.start_sex_interaction()

    def get_save_dict(self):
        save_data = super().get_save_dict()
        actors_list = dict()
        for (actor_id, sim_id) in self._actors_list.items():
            actors_list[str(actor_id)] = sim_id
        save_data['actors_list'] = actors_list
        save_data['hash_id'] = self._hash_id_cache
        save_data['overall_counter'] = self.overall_counter
        save_data['is_ready_to_unregister'] = self.is_ready_to_unregister
        save_data['go_away_sims_list'] = list(self.go_away_sims_list)
        save_data['unsilence_phone_after_sex'] = self.unsilence_phone_after_sex
        save_data['ignore_autonomy_join_sims'] = self.ignore_autonomy_join_sims
        save_data['is_animation_paused'] = self.is_animation_paused
        save_data['is_timer_paused'] = self.is_timer_paused
        save_data['linked_sex_handler_identifier'] = self.linked_sex_handler_identifier
        return save_data

    @staticmethod
    def load_from_dict(save_data):
        actors_list = save_data.get('actors_list', dict())
        creator_sim_id = save_data.get('creator_sim', -1)
        gameobject_id = save_data.get('gameobject_id', -1)
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
        overall_counter = save_data.get('overall_counter', 0)
        is_ready_to_unregister = save_data.get('is_ready_to_unregister', False)
        go_away_sims_list = set(save_data.get('go_away_sims_list', set()))
        unsilence_phone_after_sex = save_data.get('unsilence_phone_after_sex', False)
        ignore_autonomy_join_sims = save_data.get('ignore_autonomy_join_sims', list())
        is_animation_paused = save_data.get('is_animation_paused', False)
        is_timer_paused = save_data.get('is_timer_paused', False)
        linked_sex_handler_identifier = save_data.get('linked_sex_handler_identifier', None)
        is_autonomy = save_data.get('is_autonomy', False)
        is_manual = save_data.get('is_manual', False)
        animation_identifier = save_data.get('animation_identifier', '-1')
        animation_instance = get_animation_from_identifier(animation_identifier)
        hash_id = save_data.get('hash_id', None)
        active_sex_handler = ActiveSexInteractionHandler(creator_sim_id, object_identifier, gameobject_id, object_height, lot_id, location_x, location_y, location_z, location_level, location_angle, route_x, route_y, route_z, route_level, is_manual=is_manual, is_autonomy=is_autonomy)
        actors_data = dict()
        for (actor_id, sim_id) in actors_list.items():
            actors_data[int(actor_id)] = int(sim_id)
        active_sex_handler._actors_list = actors_data
        active_sex_handler.set_animation_instance(animation_instance)
        active_sex_handler.overall_counter = overall_counter
        active_sex_handler.is_ready_to_unregister = is_ready_to_unregister
        active_sex_handler.go_away_sims_list = go_away_sims_list
        active_sex_handler.unsilence_phone_after_sex = unsilence_phone_after_sex
        active_sex_handler.ignore_autonomy_join_sims = ignore_autonomy_join_sims
        active_sex_handler._hash_id_cache = hash_id
        active_sex_handler.is_animation_paused = is_animation_paused
        active_sex_handler.is_timer_paused = is_timer_paused
        active_sex_handler.linked_sex_handler_identifier = linked_sex_handler_identifier
        return active_sex_handler

    def get_string_data(self):
        basic_data = super().get_string_data()
        return basic_data + '\n Identifier: ' + str(self.get_identifier()) + '\n Is Playing: ' + str(self.is_playing) + '\n Is Prepared To Play: ' + str(self.is_prepared_to_play) + '\n Prepare To Play Count: ' + str(self._prepare_to_play_count) + '\n Counter: ' + str(self.animation_counter) + '\n Overall Counter: ' + str(self.overall_counter) + '\n Is Animation Paused: ' + str(self.is_animation_paused) + '\n Is Timer Paused: ' + str(self.is_timer_paused) + '\n Is Registered: ' + str(self.is_registered) + '\n Is Ready To Unregistered: ' + str(self.is_ready_to_unregister) + '\n Is Restarting: ' + str(self._is_restarting) + '\n Force Position Count: ' + str(self.force_positioning_count) + '\n Pregnancy Counter: ' + str(self.pregnancy_sex_counter) + '\n Autonomy Actors Limit: ' + str(self.autonomy_actors_limit) + '\n Is At Climaxed: ' + str(self.is_at_climax) + '\n Climax Counter: ' + str(self.climax_counter) + '\n Unsilence Phone After Sex: ' + str(self.unsilence_phone_after_sex) + '\n Forced From Privacy Sims List: ' + str(self.go_away_sims_list)

