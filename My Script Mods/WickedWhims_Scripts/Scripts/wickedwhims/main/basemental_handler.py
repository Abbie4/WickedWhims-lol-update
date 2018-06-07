'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''from enums.buffs_enum import SimBufffrom turbolib.manager_util import TurboManagerUtilfrom turbolib.resource_util import TurboResourceUtilfrom wickedwhims.utils_buffs import has_sim_buffIS_BASEMENTAL_DRUGS_INSTALLED = None
def is_basemental_drugs_installed():
    global IS_BASEMENTAL_DRUGS_INSTALLED
    if IS_BASEMENTAL_DRUGS_INSTALLED is not None:
        return IS_BASEMENTAL_DRUGS_INSTALLED
    if TurboResourceUtil.Services.get_instance(TurboResourceUtil.ResourceTypes.ACTION, 18364504526871416666) is not None:
        IS_BASEMENTAL_DRUGS_INSTALLED = True
        return True
    if TurboResourceUtil.Services.get_instance(TurboResourceUtil.ResourceTypes.BUFF, SimBuff.BASEMENTAL_MDMA_HIGH_ON_GOOD_1_QUALITY) is not None:
        IS_BASEMENTAL_DRUGS_INSTALLED = True
        return True
    IS_BASEMENTAL_DRUGS_INSTALLED = False
    return False

def is_sim_on_basemental_drugs(sim_identifier, skip_weed=False, skip_cocaine=False, skip_mdma=False, skip_amphetamine=False):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    if skip_weed is False:
        return has_sim_buff(sim_info, SimBuff.BASEMENTAL_WEED_HIGH_ON_PURPLE_HAZE) or (has_sim_buff(sim_info, SimBuff.BASEMENTAL_WEED_HIGH_ON_OG_KUSH) or (has_sim_buff(sim_info, SimBuff.BASEMENTAL_WEED_HIGH_ON_AK47) or has_sim_buff(sim_info, SimBuff.BASEMENTAL_WEED_SUPER_HIGH_ON_WEED)))
    if skip_cocaine is False:
        return has_sim_buff(sim_info, SimBuff.BASEMENTAL_COCAINE_VERY_HIGH_ON_MEDIUM_QUALITY) or (has_sim_buff(sim_info, SimBuff.BASEMENTAL_COCAINE_VERY_HIGH_ON_HIGH_QUALITY) or (has_sim_buff(sim_info, SimBuff.BASEMENTAL_COCAINE_HIGH_ON_MEDIUM_QUALITY) or has_sim_buff(sim_info, SimBuff.BASEMENTAL_COCAINE_HIGH_ON_HIGH_QUALITY)))
    if skip_mdma is False:
        return has_sim_buff(sim_info, SimBuff.BASEMENTAL_MDMA_HIGH_ON_MEDIUM_QUALITY) or (has_sim_buff(sim_info, SimBuff.BASEMENTAL_MDMA_HIGH_ON_GOOD_1_QUALITY) or (has_sim_buff(sim_info, SimBuff.BASEMENTAL_MDMA_HIGH_ON_GOOD_2_QUALITY) or (has_sim_buff(sim_info, SimBuff.BASEMENTAL_MDMA_HIGH_ON_HIGH_QUALITY) or has_sim_buff(sim_info, SimBuff.BASEMENTAL_MDMA_HIGH_ON_SUPER_QUALITY))))
    if skip_amphetamine is False:
        return has_sim_buff(sim_info, SimBuff.BASEMENTAL_AMPHETAMINE_HIGH_ON_HIGH_QUALITY) or (has_sim_buff(sim_info, SimBuff.BASEMENTAL_AMPHETAMINE_HIGH_ON_POOR_QUALITY) or (has_sim_buff(sim_info, SimBuff.BASEMENTAL_AMPHETAMINE_VERY_HIGH_ON_HIGH_QUALITY) or has_sim_buff(sim_info, SimBuff.BASEMENTAL_AMPHETAMINE_VERY_HIGH_ON_POOR_QUALITY)))
    return False
