from enums.situations_enum import SimSituation
from turbolib.manager_util import TurboManagerUtil
from turbolib.math_util import TurboMathUtil
from turbolib.sim_util import TurboSimUtil
from wickedwhims.main.tick_handler import register_on_game_update_method
from wickedwhims.nudity.nudity_settings import NuditySetting, get_nudity_setting
from wickedwhims.nudity.outfit_utils import OutfitLevel, get_sim_outfit_level
from wickedwhims.nudity.skill.skills_utils import is_sim_naturist, is_sim_exhibitionist
from wickedwhims.relationships.desire_handler import get_sim_desire_level, change_sim_desire_level
from wickedwhims.relationships.relationship_utils import get_sim_preferenced_genders
from wickedwhims.sxex_bridge.sex import is_sim_going_to_sex, is_sim_in_sex
from wickedwhims.utils_sims import is_sim_available
from wickedwhims.utils_situations import has_sim_situations

@register_on_game_update_method(interval=2500)
def _trigger_desire_reaction_on_game_update():
    for sim in TurboManagerUtil.Sim.get_all_sim_instance_gen(humans=True, pets=False):
        if TurboSimUtil.Age.is_younger_than(sim, TurboSimUtil.Age.CHILD):
            continue
        if not get_nudity_setting(NuditySetting.TEENS_NUDITY_STATE, variable_type=bool) and (TurboSimUtil.Age.get_age(sim) == TurboSimUtil.Age.TEEN or TurboSimUtil.Age.get_age(sim) == TurboSimUtil.Age.CHILD):
            continue
        if not is_sim_in_sex(sim):
            if is_sim_going_to_sex(sim):
                continue
            if has_sim_situations(sim, (SimSituation.GRIMREAPER, SimSituation.FIRE, SimSituation.BABYBIRTH_HOSPITAL)):
                continue
            if not is_sim_available(sim):
                continue
            line_of_sight = TurboMathUtil.LineOfSight.create(TurboSimUtil.Location.get_routing_surface(sim), TurboSimUtil.Location.get_position(sim), 8.0)
            for target in TurboManagerUtil.Sim.get_all_sim_instance_gen(humans=True, pets=False):
                if sim is target:
                    continue
                if TurboSimUtil.Age.is_younger_than(target, TurboSimUtil.Age.CHILD):
                    continue
                if not _has_reaction_to_nudity(sim, target):
                    continue
                if TurboSimUtil.Gender.get_gender(target) not in get_sim_preferenced_genders(sim):
                    continue
                if not TurboSimUtil.Location.is_visible(target):
                    continue
                if TurboSimUtil.Spawner.is_leaving(target):
                    continue
                (desire_limit, desire_increase) = _get_desire_nudity_value(target)
                if not desire_limit <= 0 and desire_increase > 0:
                    if get_sim_desire_level(sim) > desire_limit:
                        continue
                    if not TurboMathUtil.LineOfSight.test(line_of_sight, TurboSimUtil.Location.get_position(target)):
                        continue
                    change_sim_desire_level(sim, desire_increase)


def _has_reaction_to_nudity(sim, target):
    if TurboSimUtil.Age.get_age(sim) == TurboSimUtil.Age.TEEN or TurboSimUtil.Age.get_age(sim) == TurboSimUtil.Age.CHILD:
        return True
    if is_sim_naturist(sim) and TurboSimUtil.Age.is_older_than(sim, TurboSimUtil.Age.ADULT, or_equal=True) and (TurboSimUtil.Age.get_age(target) == TurboSimUtil.Age.TEEN or TurboSimUtil.Age.get_age(target) == TurboSimUtil.Age.CHILD):
        return True
    if is_sim_exhibitionist(sim):
        return True
    return False


def _get_desire_nudity_value(target):
    target_outfit_level = get_sim_outfit_level(target)
    if target_outfit_level == OutfitLevel.REVEALING:
        desire_limit = 30
        desire_increase = 0.5
    elif target_outfit_level == OutfitLevel.UNDERWEAR:
        desire_limit = 45
        desire_increase = 1.0
    elif target_outfit_level == OutfitLevel.NUDE or target_outfit_level == OutfitLevel.BATHING:
        desire_limit = 80
        desire_increase = 1.25
    else:
        return (0, 0)
    if TurboSimUtil.Age.is_older_than(target, TurboSimUtil.Age.ELDER, or_equal=True):
        desire_limit /= 3
        desire_increase /= 3
    return (desire_limit, desire_increase)

