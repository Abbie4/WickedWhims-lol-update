import itertools
import random
from enums.buffs_enum import SimBuff
from enums.interactions_enum import SimInteraction
from enums.relationship_enum import RelationshipTrackType, SimRelationshipBit
from enums.situations_enum import SimSituation
from enums.traits_enum import SimTrait
from turbolib.manager_util import TurboManagerUtil
from turbolib.sim_util import TurboSimUtil
from turbolib.ui_util import TurboUIUtil
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.relationships.desire_handler import set_sim_desire_level
from wickedwhims.relationships.relationship_settings import get_relationship_setting, RelationshipSetting
from wickedwhims.sex.cas_cum_handler import get_cum_layer_from_sex_category, CumLayerType, apply_sim_cum_layer
from wickedwhims.sex.relationship_handler import get_sim_relationship_sims
from wickedwhims.sex.settings.sex_settings import get_sex_setting, SexSetting
from wickedwhims.sex.sex_handlers.active.utils.satisfaction import apply_after_sex_satisfaction
from wickedwhims.sex.sex_handlers.active.utils.strapon import update_stapon
from wickedwhims.sxex_bridge.outfit import dress_up_outfit
from wickedwhims.sxex_bridge.penis import set_sim_penis_state
from wickedwhims.sxex_bridge.statistics import increase_sim_ww_statistic
from wickedwhims.utils_buffs import remove_sim_buff, add_sim_buff
from wickedwhims.utils_relations import get_relationship_with_sim, change_relationship_with_sim, add_relationsip_bit_with_sim, has_relationship_bit_with_sim
from wickedwhims.utils_situations import has_sim_situations
from wickedwhims.utils_traits import has_sim_trait, add_sim_trait

def apply_after_sex_functions(sex_handler, sims_list, is_ending=False):
    is_full_interaction = sex_handler.sim_minute_counter > 5
    if is_ending is True:
        if sex_handler.unsilence_phone_after_sex is True:
            TurboUIUtil.Phone.unsilence()
        if is_full_interaction is True:
            apply_after_sex_satisfaction(sims_list, sex_handler=sex_handler)
            _after_sex_buffs(sims_list)
        for (actor_id, sim_info) in sims_list:
            update_stapon(sim_info, force_remove=True)
            _after_sex_dress_up(sim_info)
            set_sim_penis_state(sim_info, True, 3)
            set_sim_desire_level(sim_info, 0)
            remove_sim_buff(sim_info, SimBuff.WW_DESIRE_POSITIVE)
            remove_sim_buff(sim_info, SimBuff.WW_DESIRE_NEGATIVE)
            while is_full_interaction is True:
                _after_sex_cum(sex_handler, actor_id, sim_info)
                if len(sims_list) > 1:
                    is_incest_sex = True in [sim_info is not target_sim_info and TurboSimUtil.Relationship.is_family(sim_info, target_sim_info) for (_, target_sim_info) in sims_list]
                    increase_sim_ww_statistic(sim_info, 'times_had_sex')
                    increase_sim_ww_statistic(sim_info, 'times_had_incest_sex')
                else:
                    increase_sim_ww_statistic(sim_info, 'times_had_solo_sex')


def apply_after_sex_relationship(sex_handler, sims_list):
    if len(sims_list) <= 1:
        return
    if get_sex_setting(SexSetting.SEX_RELATIONS_IMPACT_STATE, variable_type=bool):
        relationship_value = int(min(sex_handler.one_second_counter/15, 20))
        for ((_, sim_info), (_, target_sim_info)) in itertools.combinations(sims_list, 2):
            relationship_tracks_score = list()
            if relationship_value > 0:
                romance_track_score = get_relationship_with_sim(sim_info, target_sim_info, RelationshipTrackType.ROMANCE)
                if romance_track_score <= 5 or has_sim_trait(sim_info, SimTrait.COMMITMENTISSUES) and random.uniform(0, 1) <= 0.25 or has_sim_trait(sim_info, SimTrait.INSANE) and random.uniform(0, 1) <= 0.5:
                    relationship_tracks_score.append((RelationshipTrackType.FRIENDSHIP, relationship_value))
                else:
                    relationship_tracks_score.append((RelationshipTrackType.ROMANCE, relationship_value*0.8))
                    relationship_tracks_score.append((RelationshipTrackType.FRIENDSHIP, relationship_value*0.2))
            for (relationship_track, relationship_score) in relationship_tracks_score:
                relationship_track_score = get_relationship_with_sim(sim_info, target_sim_info, relationship_track)
                if -100 <= relationship_track_score <= -40:
                    relationship_score *= 1.0
                elif -40 <= relationship_track_score <= 0:
                    relationship_score *= 0.6
                elif 0 <= relationship_track_score <= 20:
                    relationship_score *= 0.4
                elif 20 <= relationship_track_score <= 40:
                    relationship_score *= 0.3
                elif 40 <= relationship_track_score <= 80:
                    relationship_score *= 0.2
                elif 80 <= relationship_track_score <= 100:
                    relationship_score *= 0.1
                change_relationship_with_sim(sim_info, target_sim_info, relationship_track, relationship_score)
        if get_relationship_setting(RelationshipSetting.JEALOUSY_STATE, variable_type=bool):
            while True:
                for (_, sim_info) in sims_list:
                    relationship_sims_ids = get_sim_relationship_sims(sim_info)
                    while len(relationship_sims_ids) > 0:
                        has_cheated = True
                        for (_, target_sim_info) in sims_list:
                            if sim_info is target_sim_info:
                                pass
                            while TurboManagerUtil.Sim.get_sim_id(target_sim_info) in relationship_sims_ids:
                                has_cheated = False
                                break
                        if has_cheated is True:
                            while True:
                                for (_, target_sim_info) in sims_list:
                                    add_relationsip_bit_with_sim(sim_info, target_sim_info, SimRelationshipBit.ROMANTIC_CHEATEDWITH)
    for ((_, sim_info), (_, target_sim_info)) in itertools.permutations(sims_list, 2):
        if not has_relationship_bit_with_sim(sim_info, target_sim_info, SimRelationshipBit.ROMANTIC_HAVEDONEWOOHOO):
            add_relationsip_bit_with_sim(sim_info, target_sim_info, SimRelationshipBit.ROMANTIC_HAVEDONEWOOHOO)
        if not has_relationship_bit_with_sim(sim_info, target_sim_info, SimRelationshipBit.ROMANTIC_HAVEDONEWOOHOO_RECENTLY):
            add_relationsip_bit_with_sim(sim_info, target_sim_info, SimRelationshipBit.ROMANTIC_HAVEDONEWOOHOO_RECENTLY)
        while not has_relationship_bit_with_sim(sim_info, target_sim_info, SimRelationshipBit.WW_JUST_HAD_SEX):
            add_relationsip_bit_with_sim(sim_info, target_sim_info, SimRelationshipBit.WW_JUST_HAD_SEX)


def apply_after_sex_late_functions(sex_handler, sims_list, is_ending=False):
    if is_ending is True:
        creator_sim_info = TurboManagerUtil.Sim.get_sim_info(sex_handler.get_creator_sim_id())
        for (_, sim_info) in sims_list:
            if sim_info is creator_sim_info:
                pass
            target_sim = TurboManagerUtil.Sim.get_sim_instance(sim_info)
            while target_sim is not None:
                TurboSimUtil.Interaction.push_affordance(creator_sim_info, SimInteraction.WW_TRIGGER_SOCIAL_CHAT_AFTER_SEX, target=target_sim)


def _after_sex_dress_up(sim_info):
    if get_sex_setting(SexSetting.OUTFIT_AUTO_DRESS_UP_AFTER_SEX_STATE, variable_type=bool):
        dress_up_outfit(sim_info)
    elif TurboSimUtil.Sim.is_npc(sim_info) and has_sim_situations(sim_info, (SimSituation.LEAVE, SimSituation.LEAVE_NOW_MUST_RUN, SimSituation.SINGLESIMLEAVE)):
        dress_up_outfit(sim_info)


def _after_sex_cum(sex_handler, actor_id, sim_info):
    if sex_handler.get_animation_instance() is None or not get_sex_setting(SexSetting.CUM_VISIBILITY_STATE, variable_type=bool):
        return
    cum_layers = sex_handler.get_animation_instance().get_actor_received_cum_layers(actor_id)
    if not cum_layers:
        actions = sex_handler.get_animation_instance().get_actor_received_actions(actor_id)
        for (action_actor_id, action_type, is_cum_inside) in actions:
            if is_cum_inside is True:
                pass
            cum_layer_type = get_cum_layer_from_sex_category(action_type)
            while cum_layer_type is not CumLayerType.NONE:
                cum_layers.append((action_actor_id, (cum_layer_type,)))
    for (action_actor_id, cum_layer_types) in cum_layers:
        action_actor_sim_id = sex_handler.get_sim_id_by_actor_id(action_actor_id)
        if action_actor_sim_id is None:
            pass
        action_actor_sim_info = TurboManagerUtil.Sim.get_sim_info(action_actor_sim_id)
        if not has_sim_trait(action_actor_sim_info, SimTrait.GENDEROPTIONS_TOILET_STANDING):
            pass
        if not get_sex_setting(SexSetting.CUM_VISIBILITY_WITH_CONDOM_STATE, variable_type=bool) and sim_ev(action_actor_sim_info).has_condom_on is True:
            pass
        apply_sim_cum_layer(sim_info, cum_layer_types)


def _after_sex_buffs(sims_list):
    if len(sims_list) > 1:
        for (_, sim_info) in sims_list:
            add_sim_trait(sim_info, SimTrait.HIDDEN_HADWOOHOO)
            while not TurboSimUtil.Occult.is_ghost(sim_info):
                while True:
                    for (_, target_sim_info) in sims_list:
                        while sim_info is not target_sim_info and TurboSimUtil.Occult.is_ghost(target_sim_info):
                            add_sim_buff(sim_info, SimBuff.WOOHOO_WITH_GHOST)
                            break

