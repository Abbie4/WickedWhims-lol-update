import inspect
from functools import wraps
import sims4
from sims4.commands import Command, CommandType
from turbolib.special.custom_exception_watcher import exception_watch

class TurboCommandType:
    __qualname__ = 'TurboCommandType'
    DEBUG = CommandType.DebugOnly
    AUTOMATION = CommandType.Automation
    CHEAT = CommandType.Cheat
    LIVE = CommandType.Live


def register_game_command(*aliases, command_type=TurboCommandType.LIVE):

    def regiser_in_game(method):
        command_class = Command(command_type=command_type, *aliases)

        @wraps(method)
        def command_exception_wrap(*args, _connection=None):
            function_args = inspect.getfullargspec(method)
            kwargs = dict()
            if 'output' in function_args.args or 'output' in function_args.kwonlyargs:
                kwargs['output'] = sims4.commands.CheatOutput(_connection)

            @exception_watch()
            def command_wrap():
                method(*args, **kwargs)

            command_wrap()

        command_class(command_exception_wrap)
        return method

    return regiser_in_game

