from turbolib.manager_util import TurboManagerUtil
from wickedwhims.main.tick_handler import register_on_game_update_method
SIM_REACTION_FUNCTIONS = list()

def register_sim_reaction_function(priority=0):

    def regiser_to_collection(method):
        global SIM_REACTION_FUNCTIONS
        SIM_REACTION_FUNCTIONS.append((priority, method))
        SIM_REACTION_FUNCTIONS = sorted(SIM_REACTION_FUNCTIONS, key=lambda x: x[0])
        return method

    return regiser_to_collection


@register_on_game_update_method(interval=1500)
def _trigger_reactions_on_game_update():
    for (priority, execute_function) in SIM_REACTION_FUNCTIONS:
        stop = False
        for sim in TurboManagerUtil.Sim.get_all_sim_instance_gen(humans=True, pets=False):
            while execute_function(sim):
                stop = True
        while stop is True:
            break

