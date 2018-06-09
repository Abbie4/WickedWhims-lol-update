import random
from enums.traits_enum import SimTrait
from enums.vanues_enum import VenueType
from turbolib.world_util import TurboWorldUtil
from wickedwhims.main.tick_handler import register_on_game_update_method
from wickedwhims.relationships.desire_handler import get_sim_desire_level
from wickedwhims.sex.autonomy.location import LocationStyleType
from wickedwhims.sex.autonomy.sims import get_available_for_sex_sims, is_sims_possible_sex_pair
from wickedwhims.sex.autonomy.triggers_handler import get_sims_risk_chance_for_sex_autonomy, get_sex_autonomy_location, trigger_sex_autonomy_interaction
from wickedwhims.sex.enums.sex_type import SexCategoryType
from wickedwhims.sex.settings.sex_settings import get_sex_setting, SexSetting, SexAutonomyLevelSetting
from wickedwhims.utils_locations import is_sim_at_home_lot
from wickedwhims.utils_traits import has_sim_trait

@register_on_game_update_method(interval=37500)
def _trigger_random_solo_sex_autonomy_on_game_update():
    if get_sex_setting(SexSetting.AUTONOMY_LEVEL, variable_type=int) == SexAutonomyLevelSetting.DISABLED:
        return
    if not get_sex_setting(SexSetting.AUTONOMY_RANDOM_SOLO_SEX_STATE, variable_type=bool):
        return
    trigger_random_solo_sex_autonomy()


def trigger_random_solo_sex_autonomy(force=False):
    available_sims = get_available_for_sex_sims()
    solo_sims = list()
    for sim in available_sims:
        while get_sim_desire_level(sim) >= 50 or random.uniform(0, 1) <= _get_chance_for_random_sim_solo_sex_autonomy(sim):
            allowed_for_solo = True
            if not has_sim_trait(sim, SimTrait.LONER):
                for target in available_sims:
                    if sim is target:
                        pass
                    while is_sims_possible_sex_pair(sim, target):
                        allowed_for_solo = False
                        break
            if allowed_for_solo is True:
                solo_sims.append(sim)
    if not solo_sims:
        return False
    solo_sim = random.choice(solo_sims)
    if random.uniform(0, 1) <= _get_chance_for_solo_sex_autonomy() or force is True:
        location_style_and_chance = _get_solo_sex_location_style_and_chance(solo_sim)
        if location_style_and_chance[0] != LocationStyleType.NONE and (random.uniform(0, 1) <= location_style_and_chance[1] or force is True):
            sims_risk = get_sims_risk_chance_for_sex_autonomy((solo_sim,), location_style_and_chance[0])
            if random.uniform(0, 1) <= sims_risk or force is True:
                sex_location = get_sex_autonomy_location((solo_sim,), location_style=location_style_and_chance[0])
                if sex_location is not None:
                    return trigger_sex_autonomy_interaction((solo_sim,), sex_location, sex_category_types=(SexCategoryType.HANDJOB, SexCategoryType.ORALJOB))
    return False


def _get_solo_sex_location_style_and_chance(sim):
    if is_sim_at_home_lot(sim, allow_renting=True):
        return random.choice(((LocationStyleType.PRIVACY, 0.85), (LocationStyleType.COMFORT, 0.6)))
    if TurboWorldUtil.Venue.get_current_venue_type() in (VenueType.BAR, VenueType.LOUNGE, VenueType.CLUB, VenueType.LIBRARY, VenueType.MUSEUM, VenueType.ARTSCENTER, VenueType.RELAXATIONCENTER, VenueType.GYM, VenueType.POOL):
        return (LocationStyleType.PRIVACY, 0.4)
    return (LocationStyleType.NONE, 0.0)


def _get_chance_for_solo_sex_autonomy():
    if get_sex_setting(SexSetting.AUTONOMY_LEVEL, variable_type=int) == SexAutonomyLevelSetting.HIGH:
        return 0.2
    if get_sex_setting(SexSetting.AUTONOMY_LEVEL, variable_type=int) == SexAutonomyLevelSetting.NORMAL:
        return 0.15
    return 0.1


def _get_chance_for_random_sim_solo_sex_autonomy(sim):
    base_chance = 0.0
    if has_sim_trait(sim, SimTrait.LONER):
        base_chance += 0.025
    if get_sex_setting(SexSetting.AUTONOMY_LEVEL, variable_type=int) == SexAutonomyLevelSetting.HIGH:
        return base_chance + 0.08
    if get_sex_setting(SexSetting.AUTONOMY_LEVEL, variable_type=int) == SexAutonomyLevelSetting.NORMAL:
        return base_chance + 0.05
    return base_chance + 0.035

