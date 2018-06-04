'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
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

