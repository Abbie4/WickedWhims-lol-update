'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
import random
from enums.interactions_enum import SimInteraction
from enums.situations_enum import SimSituation
from enums.traits_enum import SimTrait
from enums.vanues_enum import VenueType
from turbolib.interaction_util import TurboInteractionUtil
from turbolib.manager_util import TurboManagerUtil
from turbolib.math_util import TurboMathUtil
from turbolib.sim_util import TurboSimUtil
from turbolib.world_util import TurboWorldUtil
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.main.tick_handler import register_on_game_update_method
from wickedwhims.nudity.nudity_settings import NuditySetting, get_nudity_setting, NudityAutonomyTypeSetting
from wickedwhims.nudity.outfit_utils import get_sim_outfit_level, OutfitLevel
from wickedwhims.nudity.permissions.test import has_sim_permission_for_nudity
from wickedwhims.nudity.skill.skills_utils import is_sim_naturist, is_sim_exhibitionist
from wickedwhims.sxex_bridge.body import is_sim_outfit_fullbody, get_sim_actual_body_state, BodyState
from wickedwhims.sxex_bridge.sex import is_sim_going_to_sex, is_sim_in_sex
from wickedwhims.sxex_bridge.underwear import set_sim_bottom_underwear_state, set_sim_top_underwear_state
from wickedwhims.utils_autonomy import is_sim_allowed_for_autonomy
from wickedwhims.utils_sims import is_sim_available
from wickedwhims.utils_situations import has_sim_situations
from wickedwhims.utils_traits import has_sim_traits

@register_on_game_update_method(interval=10000)
def _trigger_nudity_autonomy_on_game_update():
    if not get_nudity_setting(NuditySetting.NUDITY_SWITCH_STATE, variable_type=bool):
        return
    if get_nudity_setting(NuditySetting.AUTONOMY_TYPE, variable_type=int) == NudityAutonomyTypeSetting.DISABLED:
        return
    is_special_lot = TurboWorldUtil.Venue.get_current_venue_type() in (VenueType.BAR, VenueType.LOUNGE, VenueType.CLUB)
    for sim in TurboManagerUtil.Sim.get_all_sim_instance_gen(humans=True, pets=False):
        if TurboSimUtil.Age.is_younger_than(sim, TurboSimUtil.Age.CHILD):
            pass
        if not get_nudity_setting(NuditySetting.TEENS_NUDITY_STATE, variable_type=bool) and (TurboSimUtil.Age.get_age(sim) == TurboSimUtil.Age.TEEN or TurboSimUtil.Age.get_age(sim) == TurboSimUtil.Age.CHILD):
            pass
        if TurboWorldUtil.Time.get_absolute_ticks() <= sim_ev(sim).last_nudity_autonomy:
            pass
        if get_nudity_setting(NuditySetting.AUTONOMY_TYPE, variable_type=int) == NudityAutonomyTypeSetting.NPC_ONLY and TurboSimUtil.Sim.is_player(sim):
            pass
        if not is_sim_allowed_for_autonomy(sim):
            pass
        if not _is_sim_ready_to_undress(sim):
            sim_ev(sim).last_nudity_autonomy = TurboWorldUtil.Time.get_absolute_ticks() + 30000
        is_sim_on_lot = TurboWorldUtil.Lot.is_position_on_active_lot(TurboSimUtil.Location.get_position(sim))
        has_child_sims_on_lot = False
        for target in TurboManagerUtil.Sim.get_all_sim_instance_gen(humans=True, pets=False):
            if sim is target:
                pass
            if is_special_lot is False and TurboSimUtil.Age.is_younger_than(target, TurboSimUtil.Age.CHILD):
                has_child_sims_on_lot = True
                break
            while get_sim_outfit_level(target) == OutfitLevel.NUDE:
                if is_sim_on_lot is True and TurboWorldUtil.Lot.is_position_on_active_lot(TurboSimUtil.Location.get_position(target)) or TurboMathUtil.Position.get_distance(TurboSimUtil.Location.get_position(sim), TurboSimUtil.Location.get_position(target)) <= 12:
                    pass
        if has_child_sims_on_lot is True:
            sim_ev(sim).last_nudity_autonomy = TurboWorldUtil.Time.get_absolute_ticks() + 30000
        if is_sim_exhibitionist(sim):
            pass
        if random.uniform(0, 1) > sim_ev(sim).nudity_autonomy_chance:
            sim_ev(sim).last_nudity_autonomy = TurboWorldUtil.Time.get_absolute_ticks() + 25000
        while trigger_nudity_autonomy(sim):
            sim_ev(sim).last_nudity_autonomy = TurboWorldUtil.Time.get_absolute_ticks() + 55000
            sim_ev(sim).nudity_autonomy_chance = 0.05
            return

def _is_sim_ready_to_undress(sim):
    if is_sim_in_sex(sim) or is_sim_going_to_sex(sim):
        return False
    if get_sim_actual_body_state(sim, 6) == BodyState.NUDE and get_sim_actual_body_state(sim, 7) == BodyState.NUDE:
        return False
    if has_sim_traits(sim, (SimTrait.HIDDEN_ISEVENTNPC_CHALLENGE,)):
        return False
    if has_sim_situations(sim, (SimSituation.BARISTA_VENUE, SimSituation.HIREDNPC_BARISTA, SimSituation.BARBARTENDER, SimSituation.BARTENDER_RESTAURANT, SimSituation.HIREDNPC_BARTENDER, SimSituation.HIREDNPC_CATERER, SimSituation.HIREDNPC_CATERER_VEGETARIAN, SimSituation.HIREDNPC_DJ, SimSituation.HIREDNPC_DJ_LEVEL10, SimSituation.SINGLEJOB_CLUB_DJ, SimSituation.SINGLEJOB_CLUB_DJ_LEVEL10, SimSituation.HIREDNPC_ENTERTAINER_GUITAR, SimSituation.HIREDNPC_ENTERTAINER_MICCOMEDY, SimSituation.HIREDNPC_ENTERTAINER_ORGAN, SimSituation.HIREDNPC_ENTERTAINER_PIANO, SimSituation.HIREDNPC_ENTERTAINER_VIOLIN, SimSituation.BUTLER_SITUATION, SimSituation.GARDENER_SERVICE_SITUATION, SimSituation.NANNY_SITUATION, SimSituation.GYMTRAINER_VENUE, SimSituation.LANDLORD, SimSituation.LIBRARYVENUE_LIBRARIAN, SimSituation.MAID_SITUATION, SimSituation.MAILMAN_SITUATION, SimSituation.PIZZADELIVERY_NEW, SimSituation.FORESTRANGER_VACATIONARRIVAL, SimSituation.REFLEXOLOGIST_VENUE, SimSituation.REPAIR_SITUATION, SimSituation.TRAGICCLOWN, SimSituation.YOGAINSTRUCTOR_VENUE, SimSituation.MASSAGETHERAPIST_VENUE, SimSituation.MASSAGETHERAPIST_SERVICECALL, SimSituation.CHEFSITUATION, SimSituation.HOST_1, SimSituation.RESTAURANT_WAITSTAFF, SimSituation.RESTAURANTDINER_SUB_NPC_CRITIC, SimSituation.RETAILEMPLOYEE_HARDWORKER, SimSituation.RETAILEMPLOYEE_NPCSTORE_HARDWORKER, SimSituation.SINGLEJOB_COWORKER_RETAILEMPLOYEE, SimSituation.HIREDNPC_STALLVENDOR, SimSituation.HIREDNPC_VENDORSTALL, SimSituation.OPENSTREETS_STALLVENDOR, SimSituation.CAREER_DOCTOR_NPC_DOCTOR, SimSituation.CAREER_DOCTOR_NPC_ASSISTANT, SimSituation.CAREER_DOCTOR_NPC_DOCTOR_DIAGNOSER, SimSituation.CAREER_DOCTOR_NPC_NURSE, SimSituation.CAREER_DOCTOR_NPC_PATIENT_ADMITTED, SimSituation.DETECTIVE_APB, SimSituation.DETECTIVE_APBNEUTRAL, SimSituation.CAREER_DETECTIVE_APBPLAYER, SimSituation.SINGLEJOB_COWORKER_SCIENTIST, SimSituation.SINGLEJOB_COWORKER_SCIENTIST_FRONTDESK, SimSituation.CAREEREVENTSITUATIONS_SCIENTISTCAREER_MAIN, SimSituation.GRIMREAPER, SimSituation.FIRE, SimSituation.BABYBIRTH_HOSPITAL, SimSituation.PARK_CHILDPLAYING, SimSituation.CAREGIVER_TODDLER, SimSituation.DATE, SimSituation.DATE_TEEN)):
        return False
    if not is_sim_available(sim):
        return False
    if not has_sim_permission_for_nudity(sim)[0]:
        return False
    return True

def trigger_nudity_autonomy(sim):
    if is_sim_naturist(sim):
        if is_sim_outfit_fullbody(sim):
            set_sim_top_underwear_state(sim, False)
            set_sim_bottom_underwear_state(sim, False)
            return TurboSimUtil.Interaction.push_affordance(sim, SimInteraction.WW_NATURISM_UNDRESS_OUTFIT, interaction_context=TurboInteractionUtil.InteractionContext.SOURCE_AUTONOMY, insert_strategy=TurboInteractionUtil.QueueInsertStrategy.NEXT, priority=TurboInteractionUtil.Priority.High, run_priority=TurboInteractionUtil.Priority.High, skip_if_running=True)
        top_outfit_state = get_sim_actual_body_state(sim, 6) == BodyState.OUTFIT
        if top_outfit_state is True:
            set_sim_top_underwear_state(sim, False)
            return TurboSimUtil.Interaction.push_affordance(sim, SimInteraction.WW_NATURISM_UNDRESS_OUTFIT_TOP, interaction_context=TurboInteractionUtil.InteractionContext.SOURCE_AUTONOMY, insert_strategy=TurboInteractionUtil.QueueInsertStrategy.NEXT, priority=TurboInteractionUtil.Priority.High, run_priority=TurboInteractionUtil.Priority.High, skip_if_running=True)
        bottom_outfit_state = get_sim_actual_body_state(sim, 7) == BodyState.OUTFIT
        if bottom_outfit_state is True:
            set_sim_bottom_underwear_state(sim, False)
            return TurboSimUtil.Interaction.push_affordance(sim, SimInteraction.WW_NATURISM_UNDRESS_OUTFIT_BOTTOM, interaction_context=TurboInteractionUtil.InteractionContext.SOURCE_AUTONOMY, insert_strategy=TurboInteractionUtil.QueueInsertStrategy.NEXT, priority=TurboInteractionUtil.Priority.High, run_priority=TurboInteractionUtil.Priority.High, skip_if_running=True)
        return False
    else:
        if is_sim_outfit_fullbody(sim):
            set_sim_top_underwear_state(sim, False)
            set_sim_bottom_underwear_state(sim, False)
            return TurboSimUtil.Interaction.push_affordance(sim, SimInteraction.WW_EXHIBITIONISM_UNDRESS_OUTFIT, interaction_context=TurboInteractionUtil.InteractionContext.SOURCE_AUTONOMY, insert_strategy=TurboInteractionUtil.QueueInsertStrategy.NEXT, priority=TurboInteractionUtil.Priority.High, run_priority=TurboInteractionUtil.Priority.High, skip_if_running=True)
        top_outfit_state = get_sim_actual_body_state(sim, 6) == BodyState.OUTFIT
        if top_outfit_state is True:
            set_sim_top_underwear_state(sim, False)
            return TurboSimUtil.Interaction.push_affordance(sim, SimInteraction.WW_EXHIBITIONISM_UNDRESS_OUTFIT_TOP, interaction_context=TurboInteractionUtil.InteractionContext.SOURCE_AUTONOMY, insert_strategy=TurboInteractionUtil.QueueInsertStrategy.NEXT, priority=TurboInteractionUtil.Priority.High, run_priority=TurboInteractionUtil.Priority.High, skip_if_running=True)
        bottom_outfit_state = get_sim_actual_body_state(sim, 7) == BodyState.OUTFIT
        if bottom_outfit_state is True:
            set_sim_bottom_underwear_state(sim, False)
            return TurboSimUtil.Interaction.push_affordance(sim, SimInteraction.WW_EXHIBITIONISM_UNDRESS_OUTFIT_BOTTOM, interaction_context=TurboInteractionUtil.InteractionContext.SOURCE_AUTONOMY, insert_strategy=TurboInteractionUtil.QueueInsertStrategy.NEXT, priority=TurboInteractionUtil.Priority.High, run_priority=TurboInteractionUtil.Priority.High, skip_if_running=True)
        return False

