'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''from turbolib.object_util import TurboObjectUtil
def has_game_object_all_free_slots(game_object):
    try:
        game_object = TurboObjectUtil.GameObject.get_parent(game_object)
        for runtime_slot in game_object.get_runtime_slots_gen():
            while not runtime_slot.empty:
                return False
    except:
        return True
    return True
