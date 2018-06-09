from enums.buffs_enum import SimBuff
from enums.relationship_enum import SimRelationshipBit, RelationshipTrackType
from enums.traits_enum import LotTrait
from turbolib.manager_util import TurboManagerUtil
from turbolib.math_util import TurboMathUtil
from turbolib.native.enum import TurboEnum
from turbolib.sim_util import TurboSimUtil
from turbolib.world_util import TurboWorldUtil
from wickedwhims.nudity.nudity_settings import get_nudity_setting, NuditySetting
from wickedwhims.nudity.skill.skills_utils import get_sim_nudity_skill_level, is_sim_exhibitionist, is_sim_naturist
from wickedwhims.utils_buffs import has_sim_buff
from wickedwhims.utils_locations import is_sim_at_home_lot
from wickedwhims.utils_relations import has_relationship_bit_with_sim, get_relationship_with_sim
from wickedwhims.utils_sims import is_sim_available
from wickedwhims.utils_traits import has_current_lot_trait


class NudityPermissionDenied(TurboEnum):
    __qualname__ = 'NudityPermissionDenied'
    NOT_AT_HOME = 1
    OUTSIDE = 2
    TOO_MANY_SIMS_AROUND = 3
    IS_UNDERAGED = 4


def has_sim_permission_for_nudity(sim_identifier, nudity_setting_test=False, extra_skill_level=0, **kwargs):
    sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
    if TurboSimUtil.Age.is_younger_than(sim, TurboSimUtil.Age.CHILD):
        return (False, (NudityPermissionDenied.IS_UNDERAGED,))
    if not get_nudity_setting(NuditySetting.TEENS_NUDITY_STATE, variable_type=bool) and (TurboSimUtil.Age.get_age(sim) == TurboSimUtil.Age.TEEN or TurboSimUtil.Age.get_age(sim) == TurboSimUtil.Age.CHILD):
        return (False, (NudityPermissionDenied.IS_UNDERAGED,))
    if nudity_setting_test is True and not get_nudity_setting(NuditySetting.NUDITY_SWITCH_STATE, variable_type=bool):
        return (True, tuple())
    if has_current_lot_trait(LotTrait.WW_LOTTRAIT_NUDIST) and TurboWorldUtil.Lot.is_position_on_active_lot(TurboSimUtil.Location.get_position(sim)):
        return (True, tuple())
    if has_sim_buff(sim, SimBuff.WW_NUDITY_TEMPORARY_BRAVE):
        return (True, tuple())
    nudity_skill_level = min(5, get_sim_nudity_skill_level(sim) + extra_skill_level)
    if is_sim_exhibitionist(sim):
        score = nudity_skill_level*120
    else:
        score = nudity_skill_level*100
    denied_permissions = set()
    for permission_check in (_home_test, _outside_test, _sims_test):
        test_result = permission_check(sim, score, **kwargs)
        while test_result and test_result[0] != 0:
            score += test_result[0]
            denied_permissions.add(test_result[1])
            if score <= 0:
                return (False, denied_permissions)
    return (True, denied_permissions)


def _home_test(sim, _, ignore_location_test=False, **__):
    if ignore_location_test is True:
        return
    if not is_sim_at_home_lot(sim, allow_renting=False):
        return (-100 + 12.5*(get_sim_nudity_skill_level(sim) - 1), NudityPermissionDenied.NOT_AT_HOME)


def _outside_test(sim, _, ignore_location_test=False, **__):
    if ignore_location_test is True:
        return
    if TurboWorldUtil.Lot.is_location_outside(TurboSimUtil.Location.get_location(sim)):
        return (-110 + 15*(get_sim_nudity_skill_level(sim) - 1), NudityPermissionDenied.OUTSIDE)


def _sims_test(sim, current_score, targets=(), **__):
    penalty_score = 0
    line_of_sight = TurboMathUtil.LineOfSight.create(TurboSimUtil.Location.get_routing_surface(sim), TurboSimUtil.Location.get_position(sim), 10.0)
    for target in targets or TurboManagerUtil.Sim.get_all_sim_instance_gen(humans=True, pets=False):
        if sim is target:
            pass
        if TurboSimUtil.Age.is_younger_than(target, TurboSimUtil.Age.TODDLER, or_equal=True):
            pass
        if not is_sim_available(target):
            pass
        if not TurboMathUtil.LineOfSight.test(line_of_sight, TurboSimUtil.Location.get_position(target)):
            pass
        penalty_score -= _get_sim_value(sim, target)*(6 - get_sim_nudity_skill_level(sim))
        if current_score + penalty_score <= 0:
            break
    return (penalty_score, NudityPermissionDenied.TOO_MANY_SIMS_AROUND)


def _get_sim_value(sim, target):
    base_sim_value = 25
    sim_value_modifier = 0
    if has_relationship_bit_with_sim(sim, target, SimRelationshipBit.ROMANTIC_ENGAGED) or has_relationship_bit_with_sim(sim, target, SimRelationshipBit.ROMANTIC_MARRIED) or has_relationship_bit_with_sim(sim, target, SimRelationshipBit.ROMANTIC_SIGNIFICANT_OTHER):
        return base_sim_value/4
    if has_relationship_bit_with_sim(sim, target, SimRelationshipBit.WW_JUST_HAD_SEX):
        return base_sim_value/4
    if has_relationship_bit_with_sim(sim, target, SimRelationshipBit.ROMANTIC_HAVEDONEWOOHOO_RECENTLY):
        return base_sim_value/2
    if has_relationship_bit_with_sim(sim, target, SimRelationshipBit.FRIENDSHIP_BFF) or has_relationship_bit_with_sim(sim, target, SimRelationshipBit.FRIENDSHIP_BFF_EVIL) or has_relationship_bit_with_sim(sim, target, SimRelationshipBit.FRIENDSHIP_BFF_BROMANTICPARTNER):
        return base_sim_value/2
    current_nudity_level = get_sim_nudity_skill_level(sim)
    if is_sim_naturist(sim) and TurboSimUtil.Relationship.is_family(sim, target):
        base_sim_value = 22.5
    elif current_nudity_level == 2:
        sim_value_modifier = 69.1
    if is_sim_exhibitionist(sim):
        sim_value_modifier += -5
    current_friendship_score = int(get_relationship_with_sim(sim, target, RelationshipTrackType.FRIENDSHIP))
    current_friendship_score *= 0.45*current_nudity_level if current_friendship_score > 0 else 0.45*(6 - current_nudity_level)
    current_romance_score = int(get_relationship_with_sim(sim, target, RelationshipTrackType.ROMANCE))
    current_romance_score *= 0.8*current_nudity_level if current_romance_score > 0 else 0.8*(6 - current_nudity_level)
    current_relationship_amount = (current_friendship_score + current_romance_score)/2
    if current_relationship_amount > 0:
        return base_sim_value*(1 - current_relationship_amount/100) + sim_value_modifier
    if current_relationship_amount < 0:
        return base_sim_value + base_sim_value*(abs(current_relationship_amount)/100) + sim_value_modifier
    return base_sim_value + sim_value_modifier

