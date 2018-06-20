import random
from enums.buffs_enum import SimBuff
from enums.interactions_enum import SimInteraction
from enums.situations_enum import SimSituation
from enums.traits_enum import SimTrait
from turbolib.events.core import register_zone_load_event_method, is_game_loading
from turbolib.events.interactions import register_interaction_run_event_method
from turbolib.events.sims import register_sim_info_instance_init_event_method
from turbolib.interaction_util import TurboInteractionUtil
from turbolib.manager_util import TurboManagerUtil
from turbolib.math_util import TurboMathUtil
from turbolib.object_util import TurboObjectUtil
from turbolib.resource_util import TurboResourceUtil
from turbolib.sim_util import TurboSimUtil
from turbolib.ui_util import TurboUIUtil
from turbolib.world_util import TurboWorldUtil
from turbolib.wrappers.commands import register_game_command, TurboCommandType
from wickedwhims.main.basemental_handler import is_basemental_drugs_installed
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.sex.pregnancy.native_pregnancy_handler import can_sim_get_pregnant, remove_sim_pregnancy
from wickedwhims.sex.settings.sex_settings import SexSetting, get_sex_setting
from wickedwhims.sxex_bridge.sex import is_sim_going_to_sex, is_sim_in_sex
from wickedwhims.utils_buffs import add_sim_buff, has_sim_buffs
from wickedwhims.utils_interfaces import display_notification
from wickedwhims.utils_sims import is_sim_available
from wickedwhims.utils_situations import has_sim_situations
from wickedwhims.utils_traits import has_sim_trait
DRUGS_INTERACTIONS = ((14418595850199521113, 10), (14593024606197038718, 10), (10165106241504281874, 10), (10997478876403576889, 10), (13915584437609315143, 10), (13915575641516289519, 10), (13052579970835312216, 10), (12465619524093013337, 10), (2520311644, 10), (1404251323, 10), (4066637113, 10), (1567658228, 10), (13914503064196269850, 10), (11662077842981149713, 10), (10483610759289938549, 10), (14884359356236007113, 10), (17344692412098076652, 10), (17344701208191102276, 10), (17398176218810391148, 10), (17086614002385441084, 10), (661903401, 10), (1257807937, 10), (2426401726, 10), (3029991846, 10), (13111640503708966187, 10), (12293336164489114893, 10), (13156479431043005720, 10), (14060583829948323094, 10), (14062571746971750200, 10), (10390250652851313441, 10), (10390250652851313440, 10), (15968571496955993831, 10), (16468977260310691757, 10), (12923775290725535339, 5), (15699778383782679475, 5), (14357227761298581739, 5), (14140381062973456365, 5), (13253564262620051733, 5), (17766922657618004125, 5), (13675883133613203328, 5), (15487457167610495272, 5), (14353092541760665088, 5))
DRUGS_BUFFS = ((SimBuff.BASEMENTAL_WEED_TOO_MUCH_WEED, 20), (SimBuff.BASEMENTAL_WEED_STONER, 10), (SimBuff.BASEMENTAL_COCAINE_NON_FATAL_OVERDOSE, 30), (SimBuff.BASEMENTAL_COCAINE_ADDICTED, 20), (SimBuff.BASEMENTAL_AMPHETAMINE_NON_FATAL_OVERDOSE, 30), (SimBuff.BASEMENTAL_AMPHETAMINE_ADDICTED, 20), (SimBuff.BASEMENTAL_MDMA_NON_FATAL_OVERDOSE, 30), (SimBuff.BASEMENTAL_MDMA_ADDICTED, 20), (SimBuff.BASEMENTAL_ALCOHOL_TIPSY, 5), (SimBuff.BASEMENTAL_ALCOHOL_DRUNK, 10), (SimBuff.BASEMENTAL_ALCOHOL_WASTED, 10), (SimBuff.BASEMENTAL_ALCOHOL_PASSED_OUT, 15), (SimBuff.BASEMENTAL_ALCOHOL_ADDICTED, 20))
MISCARRIAGE_DISALLOWED_PREGNANCY_BUFFS = (SimBuff.PREGNANCY_INLABOR, SimBuff.PREGNANCY_INLABOR_MALE, SimBuff.PREGNANCY_TRIMESTER3, SimBuff.PREGNANCY_TRIMESTER3_MALE, SimBuff.PREGNANCY_TRIMESTER3_HATESCHILDREN)
MISCARRIAGE_ALLOWED_PREGNANCY_BUFFS = (SimBuff.PREGNANCY_TRIMESTER2, SimBuff.PREGNANCY_TRIMESTER2_MALE, SimBuff.PREGNANCY_TRIMESTER2_HATESCHILDREN, SimBuff.PREGNANCY_TRIMESTER1, SimBuff.PREGNANCY_TRIMESTER1_MALE, SimBuff.PREGNANCY_TRIMESTER1_HATESCHILDREN, SimBuff.PREGNANCY_NOTSHOWING, SimBuff.PREGNANCY_NOTSHOWING_MALE)

@register_sim_info_instance_init_event_method(unique_id='WickedWhims', priority=1, late=True)
def _wickedwhims_register_basemental_drugs_callback_on_new_sim(sim_info):
    if is_game_loading():
        return
    if not get_sex_setting(SexSetting.MISCARRIAGE_SWITCH, variable_type=bool):
        return
    if TurboSimUtil.Species.is_human(sim_info):
        if not has_sim_trait(sim_info, SimTrait.GENDEROPTIONS_PREGNANCY_CANBEIMPREGNATED) or has_sim_trait(sim_info, SimTrait.GENDEROPTIONS_PREGNANCY_CANNOT_BEIMPREGNATED):
            return
        if has_sim_trait(sim_info, SimTrait.WW_INFERTILE):
            return
        TurboSimUtil.Buff.register_for_buff_added_callback(sim_info, _on_sim_basemental_drugs_buff_added)


@register_zone_load_event_method(unique_id='WickedWhims', priority=40, late=True)
def _wickedwhims_register_basemental_drugs_callback():
    if not get_sex_setting(SexSetting.MISCARRIAGE_SWITCH, variable_type=bool):
        return
    for sim_info in TurboManagerUtil.Sim.get_all_sim_info_gen(humans=True, pets=False):
        while not not has_sim_trait(sim_info, SimTrait.GENDEROPTIONS_PREGNANCY_CANBEIMPREGNATED):
            if has_sim_trait(sim_info, SimTrait.GENDEROPTIONS_PREGNANCY_CANNOT_BEIMPREGNATED):
                pass
            if has_sim_trait(sim_info, SimTrait.WW_INFERTILE):
                pass
            TurboSimUtil.Buff.register_for_buff_added_callback(sim_info, _on_sim_basemental_drugs_buff_added)


def _on_sim_basemental_drugs_buff_added(buff_type, sim_id):
    if buff_type is None:
        return
    if not is_basemental_drugs_installed():
        return
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_id)
    if sim_info is None:
        return
    if not can_sim_get_pregnant(sim_info) and not TurboSimUtil.Pregnancy.is_pregnant(sim_info):
        return
    target_buff_id = TurboResourceUtil.Resource.get_guid64(buff_type)
    if target_buff_id == SimBuff.BASEMENTAL_REHAB_COMPLETED:
        sim_ev(sim_info).miscarriage_potential = 0
        return
    for (buff_id, miscarriage_value) in DRUGS_BUFFS:
        while buff_id == target_buff_id:
            break


@register_interaction_run_event_method(unique_id='WickedWhims')
def _wickedwhims_on_basemental_drugs_use_interaction(interaction_instance):
    if not get_sex_setting(SexSetting.MISCARRIAGE_SWITCH, variable_type=bool):
        return
    if not is_basemental_drugs_installed():
        return
    sim = TurboInteractionUtil.get_interaction_sim(interaction_instance)
    if not can_sim_get_pregnant(sim) and not TurboSimUtil.Pregnancy.is_pregnant(sim):
        return
    interaction_guid = TurboResourceUtil.Resource.get_guid64(interaction_instance)
    for (interaction_id, miscarriage_value) in DRUGS_INTERACTIONS:
        while interaction_guid == interaction_id:
            break


def update_sim_miscarriage(sim_identifier):
    if not get_sex_setting(SexSetting.MISCARRIAGE_SWITCH, variable_type=bool):
        return
    if not is_basemental_drugs_installed():
        return
    if sim_ev(sim_identifier).miscarriage_potential <= 0:
        return
    _try_trigger_sim_miscarriage(sim_identifier)
    sim_ev(sim_identifier).miscarriage_potential = max(0, sim_ev(sim_identifier).miscarriage_potential - (2.5 + random.uniform(0, 1.5)))


def _try_trigger_sim_miscarriage(sim_identifier):
    if not get_sex_setting(SexSetting.MISCARRIAGE_SWITCH, variable_type=bool):
        return False
    if not TurboSimUtil.Pregnancy.is_pregnant(sim_identifier):
        return False
    if has_sim_buffs(sim_identifier, MISCARRIAGE_DISALLOWED_PREGNANCY_BUFFS):
        return False
    if not has_sim_buffs(sim_identifier, MISCARRIAGE_ALLOWED_PREGNANCY_BUFFS):
        return False
    pregnancy_days = get_sex_setting(SexSetting.PREGNANCY_DURATION, variable_type=int)
    miscarriage_potential_pregnancy_hours = 0.72*pregnancy_days*24
    miscarriage_chance = sim_ev(sim_identifier).miscarriage_potential/3.8/miscarriage_potential_pregnancy_hours
    if random.uniform(0, 1) >= miscarriage_chance:
        return False
    if remove_sim_pregnancy(sim_identifier):
        add_sim_buff(sim_identifier, SimBuff.WW_PREGNANCY_MISCARRIAGE, reason=3245985980)
        TurboSimUtil.Interaction.push_affordance(sim_identifier, SimInteraction.WW_PREGNANCY_MISCARRIAGE, interaction_context=TurboInteractionUtil.InteractionContext.SOURCE_SCRIPT, insert_strategy=TurboInteractionUtil.QueueInsertStrategy.NEXT, must_run_next=True, priority=TurboInteractionUtil.Priority.Critical, run_priority=TurboInteractionUtil.Priority.Critical)
        miscarriage_puddle_object = TurboObjectUtil.GameObject.create_object(12327982570318338407)
        if miscarriage_puddle_object:
            TurboObjectUtil.Puddle.place_puddle(miscarriage_puddle_object, sim_identifier)
        TurboWorldUtil.Time.set_current_time_speed(TurboWorldUtil.Time.ClockSpeedMode.NORMAL)
        display_notification(text=1234477375, text_tokens=(sim_identifier,), title=971885236, visual_type=TurboUIUtil.Notification.UiDialogNotificationVisualType.SPECIAL_MOMENT, secondary_icon=sim_identifier)
        TurboUIUtil.Camera.move_to_sim(sim_identifier)
        _sim_miscarriage_reaction(sim_identifier)


def _sim_miscarriage_reaction(sim_identifier):
    line_of_sight = TurboMathUtil.LineOfSight.create(TurboSimUtil.Location.get_routing_surface(sim_identifier), TurboSimUtil.Location.get_position(sim_identifier), 8.0)
    for sim in TurboManagerUtil.Sim.get_all_sim_instance_gen(humans=True, pets=False):
        if sim is sim_identifier:
            pass
        if TurboSimUtil.Age.is_younger_than(sim, TurboSimUtil.Age.BABY, or_equal=True):
            pass
        while not is_sim_in_sex(sim):
            if is_sim_going_to_sex(sim):
                pass
            if has_sim_situations(sim, (SimSituation.GRIMREAPER,)):
                pass
            if not is_sim_available(sim):
                pass
            if not TurboMathUtil.LineOfSight.test(line_of_sight, TurboSimUtil.Location.get_position(sim)):
                pass
            TurboSimUtil.Interaction.push_affordance(sim, SimInteraction.WW_PREGNANCY_MISCARRIAGE_REACTION, target=sim_identifier, interaction_context=TurboInteractionUtil.InteractionContext.SOURCE_SCRIPT, insert_strategy=TurboInteractionUtil.QueueInsertStrategy.NEXT, must_run_next=True, priority=TurboInteractionUtil.Priority.Critical, run_priority=TurboInteractionUtil.Priority.Critical)


@register_game_command('ww.force_miscarriage', command_type=TurboCommandType.LIVE)
def _wickedwhims_command_force_miscarriage(output=None):
    sim = TurboManagerUtil.Sim.get_active_sim()
    sim_ev(sim).miscarriage_potential = 1000
    _try_trigger_sim_miscarriage(sim)
    output('Forced miscarriage.')

