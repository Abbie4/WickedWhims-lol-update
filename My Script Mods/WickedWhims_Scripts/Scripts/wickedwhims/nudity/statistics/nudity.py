'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from wickedwhims.nudity.outfit_utils import get_sim_outfit_level, OutfitLevel
from wickedwhims.sxex_bridge.statistics import increase_sim_ww_statistic

def increase_sim_nudity_time_statistic(sim_identifier):
    sim_outfit_level = get_sim_outfit_level(sim_identifier)
    if sim_outfit_level == OutfitLevel.NUDE or sim_outfit_level == OutfitLevel.BATHING:
        increase_sim_ww_statistic(sim_identifier, 'time_spent_nude')

