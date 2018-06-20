'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
import random
from buffs.buff import Buff
from clubs.club_gathering_situation import ClubGatheringSituation
from sims.occult.sim_info_with_occult_tracker import SimInfoWithOccultTracker
from sims.outfits.outfit_change import TunableOutfitChange
from sims.outfits.outfit_tracker import OutfitTrackerMixin
from enums.outfits_enum import SimOutfitChangeReason
from enums.tags_enum import GameTag
from enums.traits_enum import SimTrait
from turbolib.cas_util import TurboCASUtil
from turbolib.injector_util import inject
from turbolib.resource_util import TurboResourceUtil
from turbolib.sim_util import TurboSimUtil
from turbolib.special.custom_exception_watcher import log_custom_exception
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.nudity.nudity_settings import get_nudity_setting, NuditySetting, NudityAutonomyTypeSetting, NudityAutonomyUndressLevelSetting
from wickedwhims.nudity.outfit_utils import get_sim_outfit_level, OutfitLevel
from wickedwhims.nudity.permissions.test import has_sim_permission_for_nudity
from wickedwhims.nudity.skill.skills_utils import convert_sim_nudity_skill, get_sim_nudity_skill_level, is_sim_exhibitionist
from wickedwhims.sxex_bridge.nudity import reset_sim_bathing_outfits
from wickedwhims.utils_cas import copy_outfit_to_special, is_sim_in_special_outfit
BLOCK_OUTFIT_CHANGE_REASONS = (SimOutfitChangeReason.Category_Sleep, SimOutfitChangeReason.Category_Athletic, SimOutfitChangeReason.Category_Swimwear, SimOutfitChangeReason.ExitWorkout, SimOutfitChangeReason.EnterHotTub, SimOutfitChangeReason.Category_Yoga_Enter, SimOutfitChangeReason.Category_Yoga_Exit, SimOutfitChangeReason.ExitNude, SimOutfitChangeReason.ExitShower)
BLOCK_OUTFIT_CHANGE_TAGS = (GameTag.UNIFORM_MASSAGETOWEL,)
UNDRESSING_OCCASION_OUTFIT_CHANGE_REASONS = (SimOutfitChangeReason.Category_Sleep, SimOutfitChangeReason.Category_Athletic, SimOutfitChangeReason.Category_Swimwear, SimOutfitChangeReason.EnterHotTub, SimOutfitChangeReason.Category_Yoga_Enter, SimOutfitChangeReason.Category_Yoga_Exit, SimOutfitChangeReason.ExitShower)
UNDRESSING_OCCASION_OUTFIT_CHANGE_TAGS = (GameTag.UNIFORM_MASSAGETOWEL,)

@inject(OutfitTrackerMixin, 'get_outfit_for_clothing_change')
def _wickedwhims_on_get_outfit_for_clothing_change(original, self, *args, **kwargs):
    try:
        if not get_nudity_setting(NuditySetting.NUDITY_SWITCH_STATE, variable_type=bool) or get_nudity_setting(NuditySetting.INTERACTION_AUTONOMY_UNDRESSING_TYPE, variable_type=int) == NudityAutonomyUndressLevelSetting.DISABLED:
            return original(self, *args, **kwargs)
        sim_info = self.get_sim_info()
        reason = args[1]
        outfit_category_and_index = _on_outfit_change_from_interaction(sim_info, reason=reason)
        if outfit_category_and_index:
            return outfit_category_and_index
    except Exception as ex:
        log_custom_exception("Failed to edit Sim outfit at 'OutfitTrackerMixin.get_outfit_for_clothing_change'.", ex)
    return original(self, *args, **kwargs)


@inject(TunableOutfitChange._OutfitChangeForTags.OutfitTypeSpecial, '__call__')
def _wickedwhims_on_call_on_entry_change(original, self, *args, **kwargs):
    try:
        if not get_nudity_setting(NuditySetting.NUDITY_SWITCH_STATE, variable_type=bool) or get_nudity_setting(NuditySetting.INTERACTION_AUTONOMY_UNDRESSING_TYPE, variable_type=int) == NudityAutonomyUndressLevelSetting.DISABLED:
            return original(self, *args, **kwargs)
        sim_info = args[0]
        outfit_generator = args[1]
        if not outfit_generator.tags:
            return original(self, *args, **kwargs)
        outfit_category_and_index = _on_outfit_change_from_interaction(sim_info, tags=list(outfit_generator.tags))
        if outfit_category_and_index:
            return outfit_category_and_index
    except Exception as ex:
        log_custom_exception("Failed to edit Sim outfit at 'TunableOutfitChange._OutfitChangeForTags.OutfitTypeSpecial.__call__'.", ex)
    return original(self, *args, **kwargs)


def _on_outfit_change_from_interaction(sim_info, reason=None, tags=None):
    if reason is not None and reason not in BLOCK_OUTFIT_CHANGE_REASONS:
        return
    if tags and not any(i in tags for i in BLOCK_OUTFIT_CHANGE_TAGS):
        return
    sim_outfit_level = get_sim_outfit_level(sim_info)
    if sim_outfit_level == OutfitLevel.NUDE:
        return (TurboCASUtil.OutfitCategory.SPECIAL, 0)
    if sim_outfit_level == OutfitLevel.BATHING:
        return (TurboCASUtil.OutfitCategory.BATHING, 0)
    if (tags and any(i in tags for i in UNDRESSING_OCCASION_OUTFIT_CHANGE_TAGS) or reason is not None) and reason in UNDRESSING_OCCASION_OUTFIT_CHANGE_REASONS and _has_chance_for_random_undressing(sim_info):
        reset_sim_bathing_outfits(sim_info)
        copy_outfit_to_special(sim_info, set_special_outfit=False, outfit_category_and_index=(TurboCASUtil.OutfitCategory.BATHING, 0))
        return (TurboCASUtil.OutfitCategory.SPECIAL, 0)


def _has_chance_for_random_undressing(sim_info):
    if not get_nudity_setting(NuditySetting.NUDITY_SWITCH_STATE, variable_type=bool):
        return False
    if get_nudity_setting(NuditySetting.INTERACTION_AUTONOMY_UNDRESSING_TYPE, variable_type=int) == NudityAutonomyUndressLevelSetting.DISABLED:
        return False
    if get_nudity_setting(NuditySetting.AUTONOMY_TYPE, variable_type=int) == NudityAutonomyTypeSetting.DISABLED or get_nudity_setting(NuditySetting.AUTONOMY_TYPE, variable_type=int) == NudityAutonomyTypeSetting.NPC_ONLY and TurboSimUtil.Sim.is_player(sim_info):
        return False
    if not has_sim_permission_for_nudity(sim_info)[0]:
        return False
    if get_nudity_setting(NuditySetting.INTERACTION_AUTONOMY_UNDRESSING_TYPE, variable_type=int) == NudityAutonomyUndressLevelSetting.ALWAYS:
        return True
    if get_nudity_setting(NuditySetting.INTERACTION_AUTONOMY_UNDRESSING_TYPE, variable_type=int) == NudityAutonomyUndressLevelSetting.RANDOM:
        base_chance = 0.0
        base_chance += 0.08*get_sim_nudity_skill_level(sim_info)
        if is_sim_exhibitionist(sim_info):
            base_chance += 0.1
        if random.uniform(0, 1) <= base_chance:
            return True
    return False


@inject(Buff, '_on_sim_outfit_changed')
def _wickedwhims_on_outfit_changed_buff(original, self, *args, **kwargs):
    try:
        sim_info = args[0]
        while sim_ev(sim_info).is_ready() and sim_ev(sim_info).is_outfit_update_locked is True:
            return
    except Exception as ex:
        log_custom_exception("Failed to prevent Sim outfit update at 'Buff._on_sim_outfit_changed'.", ex)
    return original(self, *args, **kwargs)


@inject(ClubGatheringSituation, '_on_outfit_changed')
def _wickedwhims_on_outfit_changed_club(original, self, *args, **kwargs):
    try:
        sim_info = args[0]
        if is_sim_in_special_outfit(sim_info):
            return
    except Exception as ex:
        log_custom_exception("Failed to prevent Sim outfit update at 'ClubGatheringSituation._on_outfit_changed'.", ex)
    return original(self, *args, **kwargs)


@inject(SimInfoWithOccultTracker, 'add_trait')
def _wickedwhims_on_exhibitionist_trait_add(original, self, *args, **kwargs):
    result = original(self, *args, **kwargs)
    try:
        trait = args[0]
        while trait is not None and TurboResourceUtil.Resource.get_guid64(trait) == SimTrait.WW_EXHIBITIONIST:
            convert_sim_nudity_skill(self)
    except Exception as ex:
        log_custom_exception("Failed to run 'convert_sim_nudity_skill' at 'SimInfoWithOccultTracker.add_trait'.", ex)
    return result

