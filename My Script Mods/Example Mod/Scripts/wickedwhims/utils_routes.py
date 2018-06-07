'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''from turbolib.sim_util import TurboSimUtilfrom turbolib.world_util import TurboWorldUtilfrom wickedwhims.utils_rolestates import has_sim_full_permission_role
def is_sim_allowed_on_active_lot(sim_identifier):
    household = TurboSimUtil.Household.get_household(sim_identifier)
    if household is not None and TurboWorldUtil.Household.get_household_zone_id(household) == TurboWorldUtil.Zone.get_current_zone_id():
        return True
    if TurboWorldUtil.Zone.is_sim_renting_zone_id(sim_identifier, TurboWorldUtil.Zone.get_current_zone_id()):
        return True
    if TurboSimUtil.Sim.is_player(sim_identifier):
        venue_instance = TurboWorldUtil.Venue.get_current_venue()
        if venue_instance is not None and (TurboWorldUtil.Venue.allows_rolestate_routing(venue_instance) or not TurboWorldUtil.Venue.requires_visitation_rights(venue_instance)):
            return True
    if has_sim_full_permission_role(sim_identifier):
        return True
    return False
