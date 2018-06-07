from turbolib.events.interactions import manual_register_interaction_run_event_method, manual_register_interaction_queue_event_method, manual_register_interaction_outcome_event_method
from turbolib.interaction_util import TurboInteractionUtil
from turbolib.manager_util import TurboManagerUtil
from turbolib.resource_util import TurboResourceUtil
from turbolib.sim_util import TurboSimUtil
from turbolib.wrappers.commands import TurboCommandType, register_game_command
from wickedwhims.debug.debug_controller import enable_main_debug_flag
from wickedwhims.utils_interfaces import display_notification

@register_game_command('ww.test', command_type=TurboCommandType.LIVE)
def _wickedwhims_command_debug_test(output=None):
    output('Hello World!')


@register_game_command('ww.enabledebug', 'ww.enable_debug', command_type=TurboCommandType.LIVE)
def _wickedwhims_command_enable_debug(output=None):
    enable_main_debug_flag()
    output('Debug mode enabled.')


@register_game_command('ww.display_sex', command_type=TurboCommandType.LIVE)
def _wickedwhims_command_display_sex_debug(output=None):
    from wickedwhims.sex.sex_operators.active_sex_handlers_operator import get_active_sex_handlers
    for sex_handler in get_active_sex_handlers():
        output(sex_handler.get_string_data() + '\n---------------------------------------\n')


@register_game_command('ww.enable_run_listener', command_type=TurboCommandType.LIVE)
def _wickedwhims_command_enable_run_debug():

    def _wickedwhims_debug_interaction_run_event(interaction_instance):
        sim = TurboInteractionUtil.get_interaction_sim(interaction_instance)
        interaction_guid = TurboResourceUtil.Resource.get_guid64(interaction_instance)
        display_notification(text='ID: ' + str(interaction_guid) + '\nData: ' + interaction_instance.__class__.__name__.lower(), title='Interaction Run', secondary_icon=sim)

    manual_register_interaction_run_event_method(_wickedwhims_debug_interaction_run_event, unique_id='WickedWhims')


@register_game_command('ww.enable_queue_listener', command_type=TurboCommandType.LIVE)
def _wickedwhims_command_enable_queue_debug():

    def _wickedwhims_debug_interaction_queue_event(interaction_instance):
        sim = TurboInteractionUtil.get_interaction_sim(interaction_instance)
        interaction_guid = TurboResourceUtil.Resource.get_guid64(interaction_instance)
        display_notification(text='ID: ' + str(interaction_guid) + '\nData: ' + str(interaction_instance.__class__.__name__).lower(), title='Interaction Queue', secondary_icon=sim)

    manual_register_interaction_queue_event_method(_wickedwhims_debug_interaction_queue_event, unique_id='WickedWhims')


@register_game_command('ww.enable_outcome_listener', command_type=TurboCommandType.LIVE)
def _wickedwhims_command_enable_outcome_debug():

    def _wickedwhims_debug_interaction_outcome_event(interaction_instance, outcome_result):
        sim = TurboInteractionUtil.get_interaction_sim(interaction_instance)
        interaction_guid = TurboResourceUtil.Resource.get_guid64(interaction_instance)
        display_notification(text='ID: ' + str(interaction_guid) + '\nData: ' + interaction_instance.__class__.__name__.lower() + '\nOutcome: ' + str(outcome_result), title='Interaction Outcome', secondary_icon=sim)

    manual_register_interaction_outcome_event_method(_wickedwhims_debug_interaction_outcome_event, unique_id='WickedWhims')


@register_game_command('ww.push_interaction', command_type=TurboCommandType.LIVE)
def _wickedwhims_command_push_interactions_debug(*args, output=None):
    sim = TurboManagerUtil.Sim.get_active_sim()
    TurboSimUtil.Interaction.push_affordance(sim, int(args[0]), interaction_context=TurboInteractionUtil.InteractionContext.SOURCE_SCRIPT, insert_strategy=TurboInteractionUtil.QueueInsertStrategy.NEXT, must_run_next=True, priority=TurboInteractionUtil.Priority.High, run_priority=TurboInteractionUtil.Priority.High)
    output('Interaction pushed.')

