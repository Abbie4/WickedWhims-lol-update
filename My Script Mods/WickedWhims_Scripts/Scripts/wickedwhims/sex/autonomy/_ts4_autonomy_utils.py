from turbolib.object_util import TurboObjectUtil

def has_game_object_all_free_slots(game_object):
    try:
        game_object = TurboObjectUtil.GameObject.get_parent(game_object)
        for runtime_slot in game_object.get_runtime_slots_gen():
            while not runtime_slot.empty:
                return False
    except:
        return True
    return True

