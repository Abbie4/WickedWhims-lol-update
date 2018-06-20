'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from turbolib.resource_util import TurboResourceUtil
from turbolib.tunable_util import TurboTunableUtil

def register_satisfaction_reward(sim_reward, cost, award_type):
    reward_instance = TurboResourceUtil.Services.get_instance(TurboResourceUtil.ResourceTypes.REWARD, int(sim_reward))
    if reward_instance is None:
        return
    immutable_slots_class = TurboResourceUtil.Collections.get_immutable_slots_class(['cost', 'award_type'])
    immutable_slots = immutable_slots_class(dict(cost=cost, award_type=award_type))
    items_dict = dict(TurboTunableUtil.Whims.get_whims_tracker_satisfaction_store_items())
    items_dict[reward_instance] = immutable_slots
    TurboTunableUtil.Whims.set_whims_tracker_satisfaction_store_items(TurboResourceUtil.Collections.get_frozen_attribute_dict(items_dict))

