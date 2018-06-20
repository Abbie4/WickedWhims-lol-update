from turbolib.events.core import register_zone_load_event_method
from turbolib.l18n_util import TurboL18NUtil
from wickedwhims.sex.animations.animations_cache import cache_animation_instance, clear_animation_data_cache
from wickedwhims.sex.animations.animations_disabler_handler import apply_disabled_sex_animations_from_dict, is_player_sex_animation_disabled
from wickedwhims.sex.autonomy.disabled_locations_handler import apply_disabled_autonomy_sex_locations_from_dict
from wickedwhims.sex.cas_cum_handler import CumLayerType, get_cum_layer_type_by_name
from wickedwhims.sex.enums.sex_gender import SexGenderType, get_sex_gender_type_by_name
from wickedwhims.sex.enums.sex_naked_type import get_sex_naked_type_by_name
from wickedwhims.sex.enums.sex_type import get_sex_category_type_by_name, SexCategoryType
from wickedwhims.sex.settings.sex_settings import SexSetting, SexGenderTypeSetting, get_sex_setting
from wickedwhims.sex.sex_location_handler import SexInteractionLocationType
from wickedwhims.utils_clips import get_clip_bytes_data, get_clip_duration, get_clip_resource_key
from wickedwhims.utils_interfaces import get_unselected_icon, get_selected_icon
from wickedwhims.utils_saves.save_disabled_animations import get_disabled_animations_save_data
from wickedwhims.utils_saves.save_disabled_locations import get_disabled_locations_save_data
from wickedwhims.utils_snippets import get_snippets_with_tag
ALL_ANIMATIONS_LIST = list()
AVAILABLE_ANIMATIONS_LIST = list()
AVAILABLE_ANIMATIONS_PER_TYPE = dict()
HIDDEN_ANIMATIONS_LIST = list()

def get_all_sex_animations():
    return ALL_ANIMATIONS_LIST


def get_available_sex_animations(sex_category_type=None):
    if sex_category_type is None:
        return AVAILABLE_ANIMATIONS_LIST
    if sex_category_type in AVAILABLE_ANIMATIONS_PER_TYPE:
        return AVAILABLE_ANIMATIONS_PER_TYPE[sex_category_type]
    return ()


def get_hidden_animations():
    return HIDDEN_ANIMATIONS_LIST


@register_zone_load_event_method(unique_id='WickedWhims', priority=2, late=True)
def _wickedwhims_load_sex_animations_on_save_load():
    apply_disabled_sex_animations_from_dict(get_disabled_animations_save_data())
    apply_disabled_autonomy_sex_locations_from_dict(get_disabled_locations_save_data())
    recollect_sex_animation_packages()


class SexAnimationActorActionInstance:
    __qualname__ = 'SexAnimationActorActionInstance'

    def __init__(self, receiving_actor_id, receiving_actor_category, receiving_actor_cum_layers, receiving_actor_cum_inside):
        self.receiving_actor_id = receiving_actor_id
        self.receiving_actor_sex_category = receiving_actor_category
        self.receiving_actor_cum_layers = receiving_actor_cum_layers
        self.receiving_actor_cum_inside = receiving_actor_cum_inside

    def get_receiving_actor_id(self):
        return self.receiving_actor_id

    def get_receiving_actor_category(self):
        return self.receiving_actor_sex_category

    def get_receiving_actor_cum_layers(self):
        return self.receiving_actor_cum_layers

    def is_receiving_actor_cum_inside(self):
        return self.receiving_actor_cum_inside

    def __repr__(self):
        cum_layers_list = ''
        for cum_layer_name in self.receiving_actor_cum_layers:
            cum_layers_list += cum_layer_name
            cum_layers_list += ', '
        return '\n    Receive Actor ID: ' + str(self.receiving_actor_id) + '\n    Receive Actor Category: ' + str(self.receiving_actor_sex_category.name) + '\n    Receive Actor Cum Layers: ' + str(cum_layers_list) + '\n    Receive Actor Cum Inside:' + str(self.receiving_actor_cum_inside)


class SexAnimationActorInstance:
    __qualname__ = 'SexAnimationActorInstance'

    def __init__(self, actor_id, animation_clip_name, sex_category, gender_type, preferenced_gender_type, naked_type, force_nude_hands, force_nude_feet, allow_strapon, actor_actions, y_offset=0, facing_offset=0):
        self.actor_id = actor_id
        self.animation_clip_name = animation_clip_name
        self.sex_category = sex_category
        self.gender_type = gender_type
        self.preferenced_gender_type = preferenced_gender_type
        self.naked_type = naked_type
        self.force_nude_hands = force_nude_hands
        self.force_nude_feet = force_nude_feet
        self.allow_strapon = allow_strapon
        self.actor_actions = actor_actions
        self.y_offset = y_offset
        self.facing_offset = facing_offset
        self.temp_x_offset = 0
        self.temp_y_offset = 0
        self.temp_z_offset = 0
        self.temp_facing_offset = 0

    def get_actor_id(self):
        return self.actor_id

    def get_animation_clip_name(self):
        return self.animation_clip_name

    def get_sex_category(self):
        return self.sex_category

    def get_gender_type(self, default_gender=False):
        if default_gender is True:
            return self.gender_type
        if get_sex_setting(SexSetting.SEX_GENDER_TYPE, variable_type=int) == SexGenderTypeSetting.ANY_BASED:
            if self.gender_type == SexGenderType.CMALE or self.gender_type == SexGenderType.CFEMALE or self.gender_type == SexGenderType.CBOTH:
                return SexGenderType.CBOTH
            return SexGenderType.BOTH
        if self.gender_type == SexGenderType.CFEMALE and get_sex_setting(SexSetting.GENDER_RECOGNITION_FEMALE_TO_BOTH_STATE, variable_type=bool):
            return SexGenderType.CBOTH
        if self.gender_type == SexGenderType.CMALE and get_sex_setting(SexSetting.GENDER_RECOGNITION_MALE_TO_BOTH_STATE, variable_type=bool):
            return SexGenderType.CBOTH
        if self.gender_type == SexGenderType.FEMALE and get_sex_setting(SexSetting.GENDER_RECOGNITION_FEMALE_TO_BOTH_STATE, variable_type=bool):
            return SexGenderType.BOTH
        if self.gender_type == SexGenderType.MALE and get_sex_setting(SexSetting.GENDER_RECOGNITION_MALE_TO_BOTH_STATE, variable_type=bool):
            return SexGenderType.BOTH
        return self.gender_type

    def get_preferenced_gender_type(self):
        pref_gender = self.preferenced_gender_type
        if pref_gender == SexGenderType.NONE:
            pref_gender = self.get_gender_type(default_gender=True)
            if pref_gender == SexGenderType.BOTH or pref_gender == SexGenderType.CBOTH:
                pref_gender = SexGenderType.NONE
        return pref_gender

    def get_final_gender_type(self):
        gender_type = self.get_gender_type()
        if gender_type == SexGenderType.CBOTH:
            pref_gender_type = self.get_preferenced_gender_type()
            if pref_gender_type == SexGenderType.NONE:
                return SexGenderType.CBOTH
            return pref_gender_type
        if gender_type == SexGenderType.BOTH:
            pref_gender_type = self.get_preferenced_gender_type()
            if pref_gender_type == SexGenderType.NONE:
                return SexGenderType.BOTH
            return pref_gender_type
        return gender_type

    def get_naked_type(self):
        return self.naked_type

    def is_forcing_nude_hands(self):
        return self.force_nude_hands

    def is_forcing_nude_feet(self):
        return self.force_nude_feet

    def is_allowing_strapon(self):
        return self.allow_strapon

    def get_actor_actions(self):
        return self.actor_actions

    def get_y_position_offset(self):
        return self.y_offset

    def get_facing_position_offset(self):
        return self.facing_offset

    def __repr__(self):
        interactions_display_data = ''
        for interaction in self.actor_actions:
            interactions_display_data += str(interaction)
        return '\n  Actor ID: ' + str(self.actor_id) + '\n  Animation Name: ' + str(self.animation_clip_name) + '\n  Animation Type: ' + str(self.sex_category.name) + '\n  Animation Pref Genders: ' + str(self.preferenced_gender_type.name) + '\n  Animation Genders: ' + str(self.gender_type.name) + '\n  Naked Type: ' + str(self.naked_type.name) + '\n  Froce Nude Hands: ' + str(self.force_nude_hands) + '\n  Froce Nude Feet: ' + str(self.force_nude_feet) + '\n  Allow Strapon Flag: ' + str(self.allow_strapon) + '\n  Y Offset: ' + str(self.y_offset) + '\n  Facing Offset: ' + str(self.facing_offset) + '\n   Interactions:' + interactions_display_data


class SexAnimationInstance:
    __qualname__ = 'SexAnimationInstance'

    def __init__(self, animation_id, display_name, author, object_animation_clip_name, animation_stage_name, locations, sex_category, duration, duration_loops, animation_next_stages, allowed_for_random, actors, custom_locations=()):
        self.is_valid = True
        self.animation_id = animation_id
        self.display_name = display_name
        self.author = author
        self.sex_category = sex_category
        self.locations = locations
        self.custom_locations = custom_locations
        self.object_animation_clip_name = object_animation_clip_name
        self.actors = actors
        self.animation_stage_name = animation_stage_name
        self.animation_next_stages = animation_next_stages
        self.allowed_for_random = allowed_for_random
        self.identifier_cache = None
        self.single_loop_duration_cache = -1
        if self.get_single_loop_duration() <= 0:
            self.is_valid = False
            return
        if duration > 0:
            self.duration = max(1, int(min(60, duration)/self.get_single_loop_duration()))*self.get_single_loop_duration()
        elif duration_loops > 0:
            self.duration = int(self.get_single_loop_duration()*duration_loops)
        else:
            self.is_valid = False

    def is_valid_animation(self):
        return self.is_valid

    def get_animation_id(self):
        return self.animation_id

    def get_identifier(self):
        if self.identifier_cache is not None:
            return self.identifier_cache
        id_data = [str(self.get_display_name(string_hash=True)), str(self.author), str(int(self.sex_category)), str(len(self.actors))]
        ord3 = lambda x: '%.3d' % ord(x)
        locs_data = str(''.join(map(ord3, ''.join(self.locations))))
        id_data.append(str(locs_data))
        customlocs_data = str(''.join(map(ord3, ''.join(str(i) for i in self.custom_locations))))
        id_data.append(str(customlocs_data))
        hash_id = str(''.join(map(ord3, ''.join(id_data))))
        self.identifier_cache = hash_id
        return hash_id

    def get_display_name(self, string_hash=False):
        if string_hash is True and not isinstance(self.display_name, str):
            return TurboL18NUtil.get_localized_string_id(self.display_name)
        return self.display_name

    def get_author(self):
        return self.author

    def get_sex_category(self):
        return self.sex_category

    def get_duration(self):
        return self.duration

    def get_duration_milliseconds(self):
        return self.duration*1000

    def get_single_loop_duration(self):
        if self.single_loop_duration_cache != -1:
            return self.single_loop_duration_cache
        if not self.get_actors():
            return 0
        actor_data = self.get_actors()[0]
        clip_resource_key = get_clip_resource_key(actor_data.get_animation_clip_name())
        clip_data = get_clip_bytes_data(clip_resource_key)
        self.single_loop_duration_cache = get_clip_duration(clip_data)
        return self.single_loop_duration_cache

    def get_locations(self):
        return self.locations

    def get_custom_locations(self):
        return self.custom_locations

    def get_object_animation_clip_name(self):
        return self.object_animation_clip_name

    def can_be_used_with_object(self, object_identifier):
        if object_identifier[0] is not None:
            for location in self.get_locations():
                if str(location) == str(object_identifier[0]):
                    return True
        for custom_location in self.get_custom_locations():
            if str(custom_location) == str(object_identifier[1]):
                return True
        return False

    def get_actors(self):
        return self.actors

    def get_actor(self, actor_id):
        for actor in self.get_actors():
            if actor.get_actor_id() == actor_id:
                return actor

    def get_actor_received_actions(self, actor_id):
        received_actons = list()
        for actor in self.get_actors():
            if actor.get_actor_id() == actor_id:
                continue
            for action in actor.get_actor_actions():
                if action.get_receiving_actor_id() == actor_id:
                    received_actons.append((actor.get_actor_id(), action.get_receiving_actor_category(), action.is_receiving_actor_cum_inside()))
        return received_actons

    def get_actor_received_cum_layers(self, actor_id):
        received_cum = list()
        for actor in self.get_actors():
            if actor.get_actor_id() == actor_id:
                continue
            for action in actor.get_actor_actions():
                if action.get_receiving_actor_id() == actor_id and action.get_receiving_actor_cum_layers():
                    received_cum.append((actor.get_actor_id(), action.get_receiving_actor_cum_layers()))
        return received_cum

    def get_actors_gender_list(self):
        genders = list()
        for actor_data in self.get_actors():
            genders.append((actor_data.get_actor_id(), (actor_data.get_gender_type(), actor_data.get_preferenced_gender_type())))
        return sorted(genders, key=lambda x: int(x[1][0]))

    def is_matching_actors_genders(self, compare_animation_instance):
        if len(self.get_actors()) != len(compare_animation_instance.get_actors()):
            return False
        animation_1_genders = [(actor_data.get_actor_id(), actor_data.get_gender_type()) for actor_data in self.get_actors()]
        animation_2_genders = [(actor_data.get_actor_id(), actor_data.get_gender_type()) for actor_data in compare_animation_instance.get_actors()]
        for i in range(len(self.get_actors())):
            animation_1_gender = animation_1_genders[i]
            animation_2_gender = animation_2_genders[i]
            if animation_1_gender != animation_2_gender and animation_1_gender != SexGenderType.BOTH and animation_1_gender != SexGenderType.CBOTH and animation_2_gender != SexGenderType.BOTH and animation_2_gender != SexGenderType.CBOTH:
                return False
        return True

    def get_stage_name(self):
        return self.animation_stage_name

    def get_next_stages(self):
        return self.animation_next_stages

    def is_allowed_for_random(self):
        return self.allowed_for_random

    def get_picker_row(self, display_selected=False):
        display_icon = get_unselected_icon()
        if display_selected is True:
            display_icon = get_selected_icon()
        from wickedwhims.sex.animations.animations_operator import ListAnimationPickerRow
        return ListAnimationPickerRow(self.get_animation_id(), self.get_display_name(), TurboL18NUtil.get_localized_string(881372436, tokens=(self.get_author(),)), icon=display_icon, skip_tooltip=True, tag=self)

    def __repr__(self):
        locations_list = ''
        for location_name in self.locations:
            locations_list += location_name
            locations_list += ', '
        custom_locations_list = ''
        for location_id in self.custom_locations:
            custom_locations_list += str(location_id)
            custom_locations_list += ', '
        actors_display_data = ''
        for actor in self.get_actors():
            actors_display_data += str(actor)
        return 'ID: ' + str(self.get_identifier()) + '\nAuthor: ' + str(self.author) + '\nStage Name: ' + str(self.animation_stage_name) + '\nLocations: ' + str(locations_list) + '\nCustom Locations: ' + str(custom_locations_list) + '\nCategory: ' + str(self.sex_category.name) + '\nLength: ' + str(self.duration) + '\nNext Stages: ' + str(self.animation_next_stages) + '\n Actors: ' + actors_display_data


def collect_sex_animation_packages():
    global ALL_ANIMATIONS_LIST, AVAILABLE_ANIMATIONS_LIST, AVAILABLE_ANIMATIONS_PER_TYPE, HIDDEN_ANIMATIONS_LIST
    animations_packages_list = get_snippets_with_tag('wickedwhims_animations', 'wickedwoohoo_animations')
    all_animations_list = list()
    available_animations_list = list()
    available_animations_per_type = dict()
    hidden_animations_list = list()
    for animation_package in animations_packages_list:
        for package_animation in animation_package.animations_list:
            if package_animation.animation_actors_list:
                if len(package_animation.animation_actors_list) > 10:
                    continue
                display_name = package_animation.animation_display_name or str(package_animation.animation_raw_display_name)
                author = str(package_animation.animation_author)
                sex_category = get_sex_category_type_by_name(package_animation.animation_category)
                if sex_category == SexCategoryType.NONE:
                    continue
                duration = int(package_animation.animation_length)
                duration_loops = int(package_animation.animation_loops)
                locations = _parse_sex_animation_locations(package_animation.animation_locations)
                custom_locations = _parse_sex_animation_custom_locations(package_animation.animation_custom_locations)
                if not locations and not custom_locations:
                    continue
                object_animation_clip_name = str(package_animation.object_animation_clip_name)
                stage_name = str(package_animation.animation_stage_name).strip().lower()
                next_stages = _parse_sex_animation_stages_list(package_animation.animation_next_stages, exclude_stages=(stage_name,))
                allowed_for_random = bool(package_animation.animation_allowed_for_random)
                is_hidden = bool(package_animation.animation_hidden)
                animation_actors = list()
                for animation_actor in package_animation.animation_actors_list:
                    actor_interactions = list()
                    for actor_interaction in animation_actor.actor_interactions:
                        receiving_actor_id = int(actor_interaction.receiving_actor_id)
                        receiving_actor_category = get_sex_category_type_by_name(actor_interaction.receiving_actor_category)
                        receiving_actor_cum_layers = _parse_cum_layer_types(actor_interaction.receiving_actor_cum_layers or actor_interaction.receiving_actor_cum_layer)
                        receiving_actor_cum_inside = bool(actor_interaction.receiving_actor_cum_inside)
                        animation_actor_action_instance = SexAnimationActorActionInstance(receiving_actor_id, receiving_actor_category, receiving_actor_cum_layers, receiving_actor_cum_inside)
                        actor_interactions.append(animation_actor_action_instance)
                    actor_interactions = tuple(actor_interactions)
                    actor_id = int(animation_actor.actor_id)
                    animation_clip_name = str(animation_actor.animation_clip_name or animation_actor.animation_name)
                    actor_sex_category = get_sex_category_type_by_name(animation_actor.animation_type)
                    gender_type = get_sex_gender_type_by_name(animation_actor.animation_genders)
                    preferenced_gender_type = get_sex_gender_type_by_name(animation_actor.animation_pref_gender)
                    naked_type = get_sex_naked_type_by_name(animation_actor.animation_naked_type or animation_actor.animation_naked_flags)
                    force_nude_hands = bool(animation_actor.animation_force_nude_hands)
                    force_nude_feet = bool(animation_actor.animation_force_nude_feet)
                    allow_strapon = bool(animation_actor.animation_allow_strapon)
                    y_offset = animation_actor.animation_y_offset
                    facing_offset = animation_actor.animation_facing_offset
                    animation_actor_instance = SexAnimationActorInstance(actor_id, animation_clip_name, actor_sex_category, gender_type, preferenced_gender_type, naked_type, force_nude_hands, force_nude_feet, allow_strapon, actor_interactions, y_offset, facing_offset)
                    animation_actors.append(animation_actor_instance)
                animation_actors = _fix_animation_actors_order(animation_actors)
                animation_actors = tuple(animation_actors)
                animation_instance = SexAnimationInstance(len(available_animations_list), display_name, author, object_animation_clip_name, stage_name, locations, sex_category, duration, duration_loops, next_stages, allowed_for_random, animation_actors, custom_locations=custom_locations)
                if not animation_instance.is_valid_animation():
                    continue
                if is_hidden is True:
                    hidden_animations_list.append(animation_instance)
                else:
                    all_animations_list.append(animation_instance)
                    animation_identifier = animation_instance.get_identifier()
                    if not is_player_sex_animation_disabled(animation_identifier):
                        available_animations_list.append(animation_instance)
                        if sex_category not in available_animations_per_type:
                            available_animations_per_type[sex_category] = list()
                        available_animations_per_type[sex_category].append(animation_instance)
                        cache_animation_instance(animation_instance)
    all_animations_list = sorted(all_animations_list, key=lambda x: x.get_author())
    available_animations_list = sorted(available_animations_list, key=lambda x: x.get_author())
    for key in available_animations_per_type.keys():
        available_animations_per_type[key] = sorted(available_animations_per_type[key], key=lambda x: x.get_author())
    ALL_ANIMATIONS_LIST = all_animations_list
    AVAILABLE_ANIMATIONS_LIST = available_animations_list
    AVAILABLE_ANIMATIONS_PER_TYPE = available_animations_per_type
    HIDDEN_ANIMATIONS_LIST = hidden_animations_list


def _fix_animation_actors_order(animation_actors):
    animation_actors = sorted(animation_actors, key=lambda x: int(x.get_gender_type(default_gender=True)))
    new_actor_id = 0
    actors_id_dict = dict()
    for actor in animation_actors:
        actors_id_dict[actor.get_actor_id()] = new_actor_id
        new_actor_id += 1
    for actor in animation_actors:
        actor.actor_id = actors_id_dict[actor.actor_id]
        for actor_action in actor.get_actor_actions():
            if actor_action.receiving_actor_id not in actors_id_dict:
                continue
            actor_action.receiving_actor_id = actors_id_dict[actor_action.receiving_actor_id]
    return animation_actors


def recollect_sex_animation_packages():
    global ALL_ANIMATIONS_LIST, AVAILABLE_ANIMATIONS_LIST, AVAILABLE_ANIMATIONS_PER_TYPE
    ALL_ANIMATIONS_LIST = list()
    AVAILABLE_ANIMATIONS_LIST = list()
    AVAILABLE_ANIMATIONS_PER_TYPE = list()
    clear_animation_data_cache()
    collect_sex_animation_packages()


def get_unique_sex_animations_authors():
    authors_list = list()
    for animation_instance in get_available_sex_animations():
        if animation_instance.get_author() not in authors_list:
            authors_list.append(animation_instance.get_author())
    authors_list.sort()
    authors_list_text = ', '.join(authors_list)
    return authors_list_text


def _parse_sex_animation_locations(locations_names):
    if len(locations_names) <= 0:
        return ()
    if ',' not in locations_names:
        location_data = SexInteractionLocationType.verify_location_type(str(locations_names).strip())
        if location_data is None:
            return ()
        return (location_data,)
    locations_list = list()
    locations_names = locations_names.split(',')
    for location_name in locations_names:
        location_name = str(location_name).strip()
        if not location_name:
            continue
        location_data = SexInteractionLocationType.verify_location_type(location_name.strip())
        if location_data is not None:
            if location_data == 'NONE':
                continue
            locations_list.append(location_data)
    return tuple(locations_list)


def _parse_sex_animation_custom_locations(locations_ids):
    if len(locations_ids) <= 0:
        return ()
    if ',' not in locations_ids:
        try:
            return (int(locations_ids.strip()),)
        except ValueError:
            return ()
    locations_list = list()
    locations_names = locations_ids.split(',')
    for location_id in locations_names:
        location_id = location_id.strip()
        if not location_id:
            continue
        try:
            locations_list.append(int(location_id))
        except ValueError:
            continue
    return tuple(locations_list)


def _parse_sex_animation_stages_list(stages_names, exclude_stages=()):
    if len(stages_names) <= 0:
        return ()
    if ',' not in stages_names:
        stage_name = str(stages_names).strip().lower()
        if stage_name in exclude_stages:
            return ()
        return (stage_name,)
    stages_list = set()
    stages_names_list = stages_names.split(',')
    for stage_name in stages_names_list:
        stage_name = str(stage_name).strip().lower()
        if not stage_name:
            continue
        if stage_name in exclude_stages:
            continue
        stages_list.add(stage_name)
    return tuple(stages_list)


def _parse_cum_layer_types(names):
    if len(names) <= 0:
        return ()
    if ',' not in names:
        return (get_cum_layer_type_by_name(names.strip()),)
    cum_layers_list = set()
    names = names.split(',')
    for cum_layer_name in names:
        cum_layer_name = cum_layer_name.strip()
        if not cum_layer_name:
            continue
        cum_layer_type = get_cum_layer_type_by_name(cum_layer_name)
        if cum_layer_type == CumLayerType.NONE:
            continue
        cum_layers_list.add(cum_layer_type)
    return tuple(cum_layers_list)

