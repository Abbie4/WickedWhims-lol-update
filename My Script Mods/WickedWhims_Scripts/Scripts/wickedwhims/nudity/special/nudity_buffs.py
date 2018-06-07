from enums.buffs_enum import SimBuff
from turbolib.events.core import register_zone_load_event_method, is_game_loading
from turbolib.events.sims import register_sim_info_instance_init_event_method
from turbolib.manager_util import TurboManagerUtil
from turbolib.sim_util import TurboSimUtil
from turbolib.special.custom_exception_watcher import exception_watch
from wickedwhims.main.tick_handler import register_on_game_update_method
from wickedwhims.nudity.outfit_utils import OutfitLevel, get_sim_outfit_level
from wickedwhims.nudity.skill.skills_utils import get_sim_nudity_skill_level, is_sim_naturist
from wickedwhims.utils_buffs import has_sim_buff, remove_sim_buff, add_sim_buff

@register_sim_info_instance_init_event_method(unique_id='WickedWhims', priority=1, late=True)
def _wickedwhims_register_nudity_outfit_change_callback_on_new_sim(sim_info):
    if is_game_loading():
        return
    if TurboSimUtil.Species.is_human(sim_info):
        TurboSimUtil.CAS.register_for_outfit_changed_callback(sim_info, _on_sim_outfit_change)


@register_zone_load_event_method(unique_id='WickedWhims', priority=40, late=True)
def _wickedwhims_register_nudity_outfit_change_callback():
    for sim_info in TurboManagerUtil.Sim.get_all_sim_info_gen(humans=True, pets=False):
        TurboSimUtil.CAS.register_for_outfit_changed_callback(sim_info, _on_sim_outfit_change)


@register_on_game_update_method(interval=60000)
def _update_nudity_buffs_on_game_update():
    for sim_info in TurboManagerUtil.Sim.get_all_sim_info_gen(humans=True, pets=False):
        update_naturism_buffs(sim_info, TurboSimUtil.CAS.get_current_outfit(sim_info))


@exception_watch()
def _on_sim_outfit_change(sim_info, category_and_index):
    _update_nudity_buffs(sim_info, category_and_index)
    update_naturism_buffs(sim_info, category_and_index)


def _update_nudity_buffs(sim_info, category_and_index):
    if TurboSimUtil.Age.is_younger_than(sim_info, TurboSimUtil.Age.TEEN):
        return
    if not is_sim_naturist(sim_info) or get_sim_nudity_skill_level(sim_info) < 2:
        return
    has_nudity_buff = has_sim_buff(sim_info, SimBuff.WW_NUDITY_IS_NAKED_HIGH)
    sim_outfit_level = get_sim_outfit_level(sim_info, outfit_category_and_index=category_and_index)
    is_sim_nude = sim_outfit_level == OutfitLevel.NUDE or sim_outfit_level == OutfitLevel.BATHING
    if has_nudity_buff is False and is_sim_nude is True:
        add_sim_buff(sim_info, SimBuff.WW_NUDITY_IS_NAKED_HIGH)
    if has_nudity_buff is True and is_sim_nude is False:
        remove_sim_buff(sim_info, SimBuff.WW_NUDITY_IS_NAKED_HIGH)


def update_naturism_buffs(sim_info, category_and_index):
    if TurboSimUtil.Age.is_younger_than(sim_info, TurboSimUtil.Age.TEEN):
        return
    has_naturist_buff = has_sim_buff(sim_info, SimBuff.WW_NATURISM_SKILL_LEVEL_2) or (has_sim_buff(sim_info, SimBuff.WW_NATURISM_SKILL_LEVEL_3) or (has_sim_buff(sim_info, SimBuff.WW_NATURISM_SKILL_LEVEL_4) or has_sim_buff(sim_info, SimBuff.WW_NATURISM_SKILL_LEVEL_5)))
    sim_outfit_level = get_sim_outfit_level(sim_info, outfit_category_and_index=category_and_index)
    is_sim_allowed_for_buff = (sim_outfit_level == OutfitLevel.NUDE or sim_outfit_level == OutfitLevel.BATHING) and is_sim_naturist(sim_info)
    if has_naturist_buff is False and is_sim_allowed_for_buff is True:
        nudity_skill_level = get_sim_nudity_skill_level(sim_info)
        naturism_buff = None
        if nudity_skill_level <= 1:
            naturism_buff = SimBuff.WW_NATURISM_SKILL_LEVEL_1
        elif nudity_skill_level == 2:
            naturism_buff = SimBuff.WW_NATURISM_SKILL_LEVEL_2
        elif nudity_skill_level == 3:
            naturism_buff = SimBuff.WW_NATURISM_SKILL_LEVEL_3
        elif nudity_skill_level == 4:
            naturism_buff = SimBuff.WW_NATURISM_SKILL_LEVEL_4
        elif nudity_skill_level >= 5:
            naturism_buff = SimBuff.WW_NATURISM_SKILL_LEVEL_5
        if naturism_buff is not None:
            add_sim_buff(sim_info, naturism_buff)
    if has_naturist_buff is True and is_sim_allowed_for_buff is False:
        remove_sim_buff(sim_info, SimBuff.WW_NATURISM_SKILL_LEVEL_2)
        remove_sim_buff(sim_info, SimBuff.WW_NATURISM_SKILL_LEVEL_3)
        remove_sim_buff(sim_info, SimBuff.WW_NATURISM_SKILL_LEVEL_4)
        remove_sim_buff(sim_info, SimBuff.WW_NATURISM_SKILL_LEVEL_5)

