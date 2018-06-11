from enums.buffs_enum import SimBuff
from enums.relationship_enum import SimRelationshipBit
from enums.statistics_enum import SimCommodity
from enums.whims_enum import SimWhim
from turbolib.sim_util import TurboSimUtil
from turbolib.ui_util import TurboUIUtil
from turbolib.world_util import TurboWorldUtil
from wickedwhims.relationships.desire_handler import set_sim_desire_level
from wickedwhims.sex.settings.sex_settings import get_sex_setting, SexSetting
from wickedwhims.sex.sex_handlers.active.utils.outfit import undress_sim
from wickedwhims.sex.sex_handlers.active.utils.strapon import update_stapon
from wickedwhims.sxex_bridge.penis import set_sim_penis_state
from wickedwhims.utils_buffs import remove_sim_buff
from wickedwhims.utils_goals import complete_sim_whim, complete_sim_situation_goal
from wickedwhims.utils_interfaces import display_notification
from wickedwhims.utils_relations import has_relationship_bit_with_sim
from wickedwhims.utils_statistics import set_sim_statistic_value

def apply_before_sex_functions(sex_handler, sims_list, is_fresh_start):
    if is_fresh_start is True:
        if sex_handler.is_autonomy_sex():
            from wickedwhims.sex.autonomy.triggers_handler import update_sex_autonomy_failure_chance
            update_sex_autonomy_failure_chance(True)
        if get_sex_setting(SexSetting.SILENCE_PHONE_STATE, variable_type=bool) and not sex_handler.is_npc_only():
            sex_handler.unsilence_phone_after_sex = True
            TurboUIUtil.Phone.silence()
        if sex_handler.is_autonomy_sex():
            _before_autonomy_sex(sims_list, sex_handler)
        sex_handler.is_at_climax = False
        for (actor_id, sim_info) in sims_list:
            actor_data = sex_handler.get_animation_instance().get_actor(actor_id)
            set_sim_penis_state(sim_info, True, 9999, set_if_nude=True)
            undress_sim(sim_info, actor_data, is_npc_only=sex_handler.is_npc_only())
            update_stapon(sim_info, actor_data=actor_data, is_npc_only=sex_handler.is_npc_only())
            set_sim_desire_level(sim_info, 0)
            remove_sim_buff(sim_info, SimBuff.WW_DESIRE_POSITIVE)
            remove_sim_buff(sim_info, SimBuff.WW_DESIRE_NEGATIVE)
            set_sim_statistic_value(sim_info, 0, SimCommodity.WW_READY_TO_CLIMAX)
            while len(sims_list) >= 2:
                complete_sim_whim(sim_info, SimWhim.WW_SEX_WITH_SIM, target_sim_identifier=sim_info)
                if not TurboWorldUtil.Lot.is_sim_on_home_lot(sim_info):
                    complete_sim_whim(sim_info, SimWhim.WW_SEX_WITH_SIM_IN_PUBLIC, target_sim_identifier=sim_info)
                for (other_actor_id, other_sim_info) in sims_list:
                    complete_sim_whim(sim_info, SimWhim.WW_SEX_WITH_PARTNER, target_sim_identifier=other_sim_info)
                    complete_sim_whim(sim_info, SimWhim.WW_SEX_WITH_NEW_ROMANCE, target_sim_identifier=other_sim_info)
                    while has_relationship_bit_with_sim(sim_info, other_sim_info, SimRelationshipBit.DATE_SITUATION_BIT) and has_relationship_bit_with_sim(sim_info, other_sim_info, SimRelationshipBit.DATE_SITUATION_BIT):
                        complete_sim_situation_goal(sim_info, SimWhim.WW_GOAL_SEX_WITH_DATE, target_sim_identifier=other_sim_info)


def _before_autonomy_sex(sims_list, sex_handler):
    _before_autonomy_sex_notification(sims_list, sex_handler)
    from wickedwhims.sex.autonomy.triggers_handler import set_sex_autonomy_failure_chance
    set_sex_autonomy_failure_chance(0.0)


def _before_autonomy_sex_notification(sims_list, sex_handler):
    if get_sex_setting(SexSetting.AUTONOMY_NOTIFICATIONS_STATE, variable_type=bool):
        if sex_handler.get_actors_amount() == 1:
            display_notification(text=3606796023, text_tokens=(next(iter(sex_handler.get_actors_sim_info_gen())),), title=2175203501, secondary_icon=next(iter(sex_handler.get_actors_sim_info_gen())))
        else:
            if sex_handler.get_actors_amount() == 2:
                text = 4154762800
            elif sex_handler.get_actors_amount() == 3:
                text = 2363440915
            elif sex_handler.get_actors_amount() == 4:
                text = 81205561
            elif sex_handler.get_actors_amount() == 5:
                text = 67136532
            elif sex_handler.get_actors_amount() == 6:
                text = 3768853220
            elif sex_handler.get_actors_amount() == 7:
                text = 2435035491
            elif sex_handler.get_actors_amount() == 8:
                text = 1751739389
            elif sex_handler.get_actors_amount() == 9:
                text = 2414003908
            elif sex_handler.get_actors_amount() == 10:
                text = 3045675184
            else:
                text = 3818025802
            text_tokens = list()
            for (_, sim_info) in sims_list:
                text_tokens.append(' '.join(TurboSimUtil.Name.get_name(sim_info)) if TurboSimUtil.Name.has_name(sim_info) else TurboSimUtil.Name.get_full_name_key(sim_info))
            display_notification(text=text, text_tokens=text_tokens, title=2175203501, secondary_icon=next(iter(sex_handler.get_actors_sim_info_gen())))

