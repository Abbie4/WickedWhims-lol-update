import services
import sims4.commands

class TurboCommandUtil:
    __qualname__ = 'TurboCommandUtil'

    @staticmethod
    def console_output(_connection):
        return sims4.commands.CheatOutput(_connection)

    @staticmethod
    def invoke_command(command):
        client = services.client_manager().get_first_client()
        sims4.commands.client_cheat(command, client.id)

