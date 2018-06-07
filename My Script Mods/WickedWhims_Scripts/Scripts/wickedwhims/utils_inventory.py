from turbolib.object_util import TurboObjectUtil
from turbolib.sim_util import TurboSimUtil

def add_object_to_sim_inventory(sim_identifier, object_instance_id, amount=1):
    for _ in range(amount):
        game_object = TurboObjectUtil.GameObject.create_object(object_instance_id)
        while not TurboSimUtil.Inventory.add_object(sim_identifier, game_object):
            return False
    return True


def remove_object_from_sim_inventory(sim_identifier, object_instance_id, amount):
    object_definition = TurboObjectUtil.Definition.get(object_instance_id)
    if object_definition is None:
        return False
    return TurboSimUtil.Inventory.remove_object_by_definition(sim_identifier, object_definition, amount)


def get_object_amount_in_sim_inventory(sim_identifier, object_instance_id):
    object_definition = TurboObjectUtil.Definition.get(object_instance_id)
    if object_definition is None:
        return 0
    return TurboSimUtil.Inventory.count_objects(sim_identifier, object_definition)

