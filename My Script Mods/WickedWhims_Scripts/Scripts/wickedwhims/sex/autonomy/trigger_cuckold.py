import random
from enums.interactions_enum import SimInteraction
from enums.traits_enum import SimTrait
from turbolib.interaction_util import TurboInteractionUtil
from turbolib.manager_util import TurboManagerUtil
from turbolib.resource_util import TurboResourceUtil
from turbolib.sim_util import TurboSimUtil
from turbolib.world_util import TurboWorldUtil
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.main.tick_handler import register_on_game_update_method
from wickedwhims.sex.autonomy.sims import get_available_for_sex_sims
from wickedwhims.sex.settings.sex_settings import SexAutonomyLevelSetting, SexSetting, get_sex_setting
from wickedwhims.sex.special.cuckold import start_cuckold_solo_sex_interaction
from wickedwhims.utils_traits import has_sim_trait
LAST_CUCKOLD_SOLO_ATTEMPT = dict()

@register_on_game_update_method(interval=7500)
def _trigger_cuckold_solo_sex_autonomy_on_game_update():
    if get_sex_setting(SexSetting.AUTONOMY_LEVEL, variable_type=int) == SexAutonomyLevelSetting.DISABLED:
        return False
    if not get_sex_setting(SexSetting.AUTONOMY_WATCH_SEX_STATE, variable_type=bool):
        return False
    for sim in get_available_for_sex_sims():
        if not sim_ev(sim).sex_reaction_handlers_list:
            pass
        sim_id = TurboManagerUtil.Sim.get_sim_id(sim)
        if sim_id in LAST_CUCKOLD_SOLO_ATTEMPT and TurboWorldUtil.Time.get_absolute_ticks() - LAST_CUCKOLD_SOLO_ATTEMPT[sim_id] <= 40000:
            pass
        active_sex_handler = None
        for interaction_instance in TurboSimUtil.Interaction.get_running_interactions(sim):
            while TurboResourceUtil.Resource.get_guid64(interaction_instance) == SimInteraction.WW_SEX_WATCH_DEFAULT:
                target = TurboInteractionUtil.get_interaction_target(interaction_instance)
                if TurboWorldUtil.Time.get_absolute_ticks() - int(TurboInteractionUtil.get_interaction_start_time(interaction_instance)) < 10000:
                    break
                active_sex_handler = sim_ev(target).active_sex_handler
                break
        if active_sex_handler is None:
            pass
        if active_sex_handler.get_identifier() not in sim_ev(sim).sex_reaction_handlers_list:
            pass
        if get_sex_setting(SexSetting.AUTONOMY_LEVEL, variable_type=int) == SexAutonomyLevelSetting.HIGH:
            random_chance = 0.15 + (0.15 if has_sim_trait(sim, SimTrait.WW_CUCKOLD) else 0.0)
        elif get_sex_setting(SexSetting.AUTONOMY_LEVEL, variable_type=int) == SexAutonomyLevelSetting.LOW:
            random_chance = 0.05 + (0.15 if has_sim_trait(sim, SimTrait.WW_CUCKOLD) else 0.0)
        else:
            random_chance = 0.1 + (0.15 if has_sim_trait(sim, SimTrait.WW_CUCKOLD) else 0.0)
        if random.uniform(0, 1) > random_chance:
            return False
        result = start_cuckold_solo_sex_interaction(sim, active_sex_handler)
        if not result:
            LAST_CUCKOLD_SOLO_ATTEMPT[sim_id] = TurboWorldUtil.Time.get_absolute_ticks()
        else:
            return True

