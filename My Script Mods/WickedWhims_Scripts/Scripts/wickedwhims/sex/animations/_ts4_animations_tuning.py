import services
from sims4.localization import TunableLocalizedString
from sims4.resources import Types
from sims4.tuning.instances import HashedTunedInstanceMetaclass
from sims4.tuning.tunable import HasTunableFactory, AutoFactoryInit, Tunable, TunableList

class _WickedWhimsActorInteractionData(HasTunableFactory, AutoFactoryInit):
    __qualname__ = '_WickedWhimsActorInteractionData'
    FACTORY_TUNABLES = {'receiving_actor_id': Tunable(tunable_type=int, default=0), 'receiving_actor_category': Tunable(tunable_type=str, default=''), 'receiving_actor_cum_layers': Tunable(tunable_type=str, default=''), 'receiving_actor_cum_inside': Tunable(tunable_type=int, default=1), 'receiving_actor_cum_layer': Tunable(tunable_type=str, default='')}


class _WickedWhimsAnimationActor(HasTunableFactory, AutoFactoryInit):
    __qualname__ = '_WickedWhimsAnimationActor'
    FACTORY_TUNABLES = {'actor_id': Tunable(tunable_type=int, default=0), 'animation_clip_name': Tunable(tunable_type=str, default=''), 'animation_type': Tunable(tunable_type=str, default=''), 'animation_genders': Tunable(tunable_type=str, default=''), 'animation_pref_gender': Tunable(tunable_type=str, default=''), 'animation_naked_type': Tunable(tunable_type=str, default=''), 'animation_force_nude_hands': Tunable(tunable_type=int, default=0), 'animation_force_nude_feet': Tunable(tunable_type=int, default=0), 'animation_allow_strapon': Tunable(tunable_type=int, default=0), 'animation_y_offset': Tunable(tunable_type=float, default=0), 'animation_facing_offset': Tunable(tunable_type=float, default=0), 'actor_interactions': TunableList(tunable=_WickedWhimsActorInteractionData.TunableFactory()), 'animation_name': Tunable(tunable_type=str, default=''), 'animation_naked_flags': Tunable(tunable_type=str, default='')}


class _WickedWhimsAnimationData(HasTunableFactory, AutoFactoryInit):
    __qualname__ = '_WickedWhimsAnimationData'
    FACTORY_TUNABLES = {'animation_display_name': TunableLocalizedString(default=None), 'animation_raw_display_name': Tunable(tunable_type=str, default=''), 'animation_author': Tunable(tunable_type=str, default=''), 'animation_locations': Tunable(tunable_type=str, default='NONE'), 'animation_custom_locations': Tunable(tunable_type=str, default=''), 'object_animation_clip_name': Tunable(tunable_type=str, default=''), 'animation_category': Tunable(tunable_type=str, default=''), 'animation_loops': Tunable(tunable_type=int, default=0), 'animation_stage_name': Tunable(tunable_type=str, default=''), 'animation_next_stages': Tunable(tunable_type=str, default=''), 'animation_allowed_for_random': Tunable(tunable_type=int, default=1), 'animation_hidden': Tunable(tunable_type=int, default=0), 'animation_actors_list': TunableList(tunable=_WickedWhimsAnimationActor.TunableFactory()), 'animation_length': Tunable(tunable_type=int, default=0)}


class _WickedWhimsAnimationPackage(metaclass=HashedTunedInstanceMetaclass, manager=services.get_instance_manager(Types.SNIPPET)):
    __qualname__ = '_WickedWhimsAnimationPackage'
    INSTANCE_TUNABLES = {'wickedwhims_animations': Tunable(tunable_type=int, default=1), 'animations_list': TunableList(tunable=_WickedWhimsAnimationData.TunableFactory()), 'wickedwoohoo_animations': Tunable(tunable_type=int, default=1)}

