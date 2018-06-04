'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from enums.interactions_enum import SimInteraction
from enums.tags_enum import GameTag
from enums.whims_enum import WhimSet
from turbolib.events.core import register_zone_load_event_method, has_game_loaded
from turbolib.object_util import TurboObjectUtil
from turbolib.resources.affordances import AffordanceRegistration, register_affordance_class
from turbolib.resources.whims import WhimRegistration, register_whim_class
from turbolib.sim_util import TurboSimUtil
from turbolib.tunable_util import TurboTunableUtil
from turbolib.types_util import TurboTypesUtil
from wickedwhims.utils_rewards import register_satisfaction_reward

@register_affordance_class()
class SexSimsTerrainAffordanceRegistration(AffordanceRegistration):
    __qualname__ = 'SexSimsTerrainAffordanceRegistration'

    def get_affordance_references(self):
        return (15095161847542473876, 9554172184229158947, 16314198522149046890, 18008904150473882934, 10553537858155665895, 17963971833241456715, 10346555279539941232, 12241619004644128392, 12057396209458507503, 9917000664573370982, 13431173501395474898, 12276100658485032267, 14230666683470868951, 9960878975152193196, 12012720256040397400, 15159097093062328127, 14222403270716049814, 14718415221803545090, 13950721009493965307, 14809392175736143431, 12844991704602693820)

    def is_terrain(self):
        return True

@register_affordance_class()
class SexSimsAffordanceRegistration(AffordanceRegistration):
    __qualname__ = 'SexSimsAffordanceRegistration'

    def get_affordance_references(self):
        return (17954341595687885698, 16659890119786847560, 14129300852073892795, 12310432561821014557, 15148406823298047966, 9246838288378786427, 17729131004035197019, 17631359521993000322, 11129807081087808436, 10252702851088370851, 14069591577128867125, 16099232347801056918, 12237533637515550259, 13160574033297986515, 12629078916217977482, 14874491874589305404, 9352771613755395291, 17526108868849518436, 17499759598812473670, 16268186879956484177, 12284143574410980416, 14395125836771963632, 16929559153213619353, 11749458273093407769, 18217667533188848895, 9635683605225516678, 16131199027336198632, 15166765311294181485, 14593023572004318958, 10639567064125115435, 15754240111089265931, 16134710058322466802, 14082675962621840292, 16224776139584631283, 13515792961838344542, 15302118232999681762, 13825701230762267064, 17752684933312513668, 14782932444961246237, 13256898981663824701, 9689527218741203455, 18284814647767078886, 16889719181311194913, 17216564161072284358, 11309325992773936936, 15583252291121283379, 9736647697107362023, 11775229835539507275, 14249596275579838250, 18351640980564777490, 15594746585680330381, 10067049516964067118, 17672315041119491528, 18303667616776591428, 15327182785484042390, 13239559460358811959, 18281486596505027122, 9832694238985489341, 12353707023674140010, 14350694118135240438, 14331993713869767336, 14536837138734398110)

    def is_script_object(self, script_object):
        return TurboTypesUtil.Sims.is_sim(script_object) and TurboSimUtil.Species.is_human(script_object)

@register_affordance_class()
class SexSimsPhoneAffordanceRegistration(AffordanceRegistration):
    __qualname__ = 'SexSimsPhoneAffordanceRegistration'

    def get_affordance_references(self):
        return (16681719300006683948, 16598097060497753480)

    def is_script_object(self, script_object):
        return TurboTypesUtil.Sims.is_sim(script_object) and TurboSimUtil.Species.is_human(script_object)

    def is_sim_phone(self):
        return True

@register_affordance_class()
class SexObjectsAffordanceRegistration(AffordanceRegistration):
    __qualname__ = 'SexObjectsAffordanceRegistration'

    def get_affordance_references(self):
        return (15095161847542473876, 9554172184229158947, 16314198522149046890, 18008904150473882934, 10553537858155665895, 17963971833241456715, 10346555279539941232, 9649436916593304270, 15588156356683042681, 11188872320060298920, 16245213534999367512, 10410181733362398897, 11292121810552229713, 11799778368907483031, 9226247822342339022, 15017603655298264352, 12241619004644128392, 12057396209458507503, 9917000664573370982, 13431173501395474898, 12276100658485032267, 14230666683470868951, 9960878975152193196, 12012720256040397400, 15159097093062328127, 14222403270716049814, 14718415221803545090, 13950721009493965307, 14809392175736143431, 12844991704602693820, 17426160362286931370, 16756625324408299851)

    def is_script_object(self, script_object):
        return TurboTypesUtil.Objects.is_game_object(script_object)

@register_affordance_class()
class PregnancyFertilityTestObjectAffordanceRegistration(AffordanceRegistration):
    __qualname__ = 'PregnancyFertilityTestObjectAffordanceRegistration'

    def get_affordance_references(self):
        return (10911866778494850481,)

    def is_script_object(self, script_object):
        if not TurboTypesUtil.Objects.is_game_object(script_object):
            return False
        object_tags = TurboObjectUtil.GameObject.get_game_tags(script_object)
        tags_count = 0
        for object_tag in object_tags:
            if object_tag == GameTag.BUYCATPA_TOILET or object_tag == GameTag.FUNC_BLADDER:
                tags_count += 1
            while tags_count >= 2:
                return True
        return False

@register_affordance_class()
class SexComputerObjectAffordanceRegistration(AffordanceRegistration):
    __qualname__ = 'SexComputerObjectAffordanceRegistration'

    def get_affordance_references(self):
        return (15708310791061767036,)

    def is_script_object(self, script_object):
        if not TurboTypesUtil.Objects.is_game_object(script_object):
            return False
        object_tags = TurboObjectUtil.GameObject.get_game_tags(script_object)
        for object_tag in object_tags:
            while object_tag == GameTag.BUYCATEE_COMPUTER or object_tag == GameTag.INTERACTION_COMPUTER or object_tag == GameTag.FUNC_COMPUTER:
                return True
        return False

@register_zone_load_event_method(unique_id='WickedWhims', priority=5, late=True)
def _wickedwhims_add_disabled_sex_interactions_to_phone_tuning():
    if has_game_loaded():
        return
    TurboTunableUtil.Phone.register_disabled_affordances({SimInteraction.WW_ROUTE_TO_SEX_LOCATION, SimInteraction.WW_WAIT_FOR_SEX_PARTNER, SimInteraction.WW_SEX_ANIMATION_DEFAULT})

@register_zone_load_event_method(unique_id='WickedWhims', priority=5, late=True)
def _wickedwhims_add_sex_satisfaction_rewards():
    if has_game_loaded():
        return
    register_satisfaction_reward(3469764812713835673, 1000, TurboTunableUtil.Whims.WhimAwardTypes.TRAIT)
    register_satisfaction_reward(10438028236933481475, 500, TurboTunableUtil.Whims.WhimAwardTypes.TRAIT)
    register_satisfaction_reward(12240898038636396224, 1000, TurboTunableUtil.Whims.WhimAwardTypes.TRAIT)
    register_satisfaction_reward(5499117134932247707, 3000, TurboTunableUtil.Whims.WhimAwardTypes.TRAIT)
    register_satisfaction_reward(10310333123237709450, 500, TurboTunableUtil.Whims.WhimAwardTypes.TRAIT)
    register_satisfaction_reward(9341398068450238656, 500, TurboTunableUtil.Whims.WhimAwardTypes.TRAIT)

@register_whim_class()
class SexPartnerWhimsRegistration(WhimRegistration):
    __qualname__ = 'SexPartnerWhimsRegistration'

    def get_whim_references(self):
        return ((18144792039329369821, 1.0),)

    def get_whim_set_references(self):
        return (WhimSet.PARTNERS,)

@register_whim_class()
class SexNewRomanceWhimsRegistration(WhimRegistration):
    __qualname__ = 'SexNewRomanceWhimsRegistration'

    def get_whim_references(self):
        return ((10262116769238204219, 1.5),)

    def get_whim_set_references(self):
        return (WhimSet.NEWROMANCEPLUS,)

@register_whim_class()
class SexSomeoneWhimsRegistration(WhimRegistration):
    __qualname__ = 'SexSomeoneWhimsRegistration'

    def get_whim_references(self):
        return ((16636620952431474582, 1.0),)

    def get_whim_set_references(self):
        return (WhimSet.EMOTIONFLIRTY, WhimSet.BASEMENTAL_MDMA)

@register_whim_class()
class SexSomeonePublicWhimsRegistration(WhimRegistration):
    __qualname__ = 'SexSomeonePublicWhimsRegistration'

    def get_whim_references(self):
        return ((11561004916990309644, 0.6),)

    def get_whim_set_references(self):
        return (WhimSet.EMOTIONFLIRTY, WhimSet.EMOTIONCONFIDENT, WhimSet.BASEMENTAL_MDMA)

