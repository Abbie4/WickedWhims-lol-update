'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''import randomfrom enums.traits_enum import LotTraitfrom turbolib.world_util import TurboWorldUtilfrom wickedwhims.main.tick_handler import register_on_game_update_methodfrom wickedwhims.sex.autonomy.location import get_sex_location_style_and_chance, LocationStyleTypefrom wickedwhims.sex.autonomy.triggers_handler import update_sex_autonomy_failure_chance, get_sims_pair_for_sex_autonomy, get_chance_for_random_sex_autonomy, apply_sex_autonomy_location_style_chance_bonus, get_sims_risk_chance_for_sex_autonomy, get_sex_autonomy_location, trigger_sex_autonomy_interactionfrom wickedwhims.sex.settings.sex_settings import get_sex_setting, SexSetting, SexAutonomyLevelSettingfrom wickedwhims.utils_traits import has_current_lot_traitSEX_AUTONOMY_LAST_HOUR_UPDATE = -1
@register_on_game_update_method(interval=5000)
def _trigger_random_sex_autonomy_on_game_update():
    global SEX_AUTONOMY_LAST_HOUR_UPDATE
    if get_sex_setting(SexSetting.AUTONOMY_LEVEL, variable_type=int) == SexAutonomyLevelSetting.DISABLED:
        return
    if not get_sex_setting(SexSetting.AUTONOMY_RANDOM_SEX_STATE, variable_type=bool):
        return
    if SEX_AUTONOMY_LAST_HOUR_UPDATE == -1:
        SEX_AUTONOMY_LAST_HOUR_UPDATE = TurboWorldUtil.Time.get_hour_of_day()
        return
    if SEX_AUTONOMY_LAST_HOUR_UPDATE == TurboWorldUtil.Time.get_hour_of_day():
        return
    SEX_AUTONOMY_LAST_HOUR_UPDATE = TurboWorldUtil.Time.get_hour_of_day()
    result = trigger_random_sex_autonomy()
    if not result:
        update_sex_autonomy_failure_chance(result)

def trigger_random_sex_autonomy(force=False):
    result = False
    is_hypersexual_lot = has_current_lot_trait(LotTrait.WW_LOTTRAIT_HYPERSEXUAL)
    if is_hypersexual_lot is True:
        if get_sex_setting(SexSetting.AUTONOMY_LEVEL, variable_type=int) == SexAutonomyLevelSetting.HIGH:
            triggers_amount = 4
        elif get_sex_setting(SexSetting.AUTONOMY_LEVEL, variable_type=int) == SexAutonomyLevelSetting.NORMAL:
            triggers_amount = 3
        else:
            triggers_amount = 2
        for _ in range(triggers_amount):
            while _trigger_random_sex_autonomy(force=False, only_hypersexual_lot_sims=True):
                result = True
    if _trigger_random_sex_autonomy(force=force):
        result = True
    return result

def _trigger_random_sex_autonomy(force=False, only_hypersexual_lot_sims=False):
    if get_sex_setting(SexSetting.AUTONOMY_LEVEL, variable_type=int) == SexAutonomyLevelSetting.DISABLED:
        return False
    sims_pair = get_sims_pair_for_sex_autonomy(only_on_hypersexual_lot=only_hypersexual_lot_sims)
    if sims_pair is None:
        return False
    if random.uniform(0, 1) <= get_chance_for_random_sex_autonomy(sims_pair, skip_hypersexual_lot_check=only_hypersexual_lot_sims) or force is True:
        location_style_and_chance = get_sex_location_style_and_chance(sims_pair)
        location_style_and_chance = apply_sex_autonomy_location_style_chance_bonus(location_style_and_chance, sims_pair)
        if location_style_and_chance[0] != LocationStyleType.NONE and (random.uniform(0, 1) <= location_style_and_chance[1] or force is True):
            sims_risk = get_sims_risk_chance_for_sex_autonomy(sims_pair, location_style_and_chance[0])
            if random.uniform(0, 1) <= sims_risk or force is True:
                sex_location = get_sex_autonomy_location(sims_pair, location_style=location_style_and_chance[0])
                if sex_location is not None:
                    return trigger_sex_autonomy_interaction(sims_pair, sex_location)
    return False
