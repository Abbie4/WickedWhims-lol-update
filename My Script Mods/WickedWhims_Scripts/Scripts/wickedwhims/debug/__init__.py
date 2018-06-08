from turbolib.resources.affordances import AffordanceRegistration, register_affordance_class
from turbolib.sim_util import TurboSimUtil
from turbolib.types_util import TurboTypesUtil

@register_affordance_class()
class DebugSimsAffordanceRegisterClass(AffordanceRegistration):
    __qualname__ = 'DebugSimsAffordanceRegisterClass'

    def get_affordance_references(self):
        return (9733015192887675662, 12611486880284440741, 10589633051635131522, 14815521102511759012, 15938795142154760126, 15525463584674530653, 9509126999778643594)

    def is_script_object(self, script_object):
        return TurboTypesUtil.Sims.is_sim(script_object) and TurboSimUtil.Species.is_human(script_object)


@register_affordance_class()
class DebugObjectsAffordanceRegisterClass(AffordanceRegistration):
    __qualname__ = 'DebugObjectsAffordanceRegisterClass'

    def get_affordance_references(self):
        return (10856314819595805288,)

    def is_script_object(self, script_object):
        return TurboTypesUtil.Objects.is_game_object(script_object)

