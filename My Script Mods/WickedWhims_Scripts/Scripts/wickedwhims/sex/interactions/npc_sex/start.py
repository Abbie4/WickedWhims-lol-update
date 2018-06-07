'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''from turbolib.object_util import TurboObjectUtilfrom turbolib.types_util import TurboTypesUtilfrom turbolib.wrappers.interactions import TurboTerrainImmediateSuperInteraction, TurboInteractionStartMixinfrom wickedwhims.sex._ts4_sex_utils import is_safe_floor_object_positionfrom wickedwhims.sex.animations.animations_cache import get_animation_max_amount_of_actorsfrom wickedwhims.sex.enums.sex_type import SexCategoryTypefrom wickedwhims.sex.settings.sex_settings import SexSetting, get_sex_settingfrom wickedwhims.sex.sex_location_handler import SexInteractionLocationTypefrom wickedwhims.sex.sex_operators.sex_init_operator import start_new_npc_sex_interaction
def _test_for_npc_sex_start(interaction_context, interaction_target, sex_category_types):
    if not get_sex_setting(SexSetting.MANUAL_NPC_SEX_STATE, variable_type=bool):
        return False
    if interaction_target is None:
        return False
    if TurboTypesUtil.Objects.is_game_object(interaction_target):
        interaction_target = TurboObjectUtil.GameObject.get_parent(interaction_target)
    elif not (TurboTypesUtil.Objects.is_terrain(interaction_target) and is_safe_floor_object_position(interaction_target, interaction_context)):
        return False
    object_identifier = SexInteractionLocationType.get_location_identifier(interaction_target)
    for sex_category_type in sex_category_types:
        while get_animation_max_amount_of_actors(sex_category_type, object_identifier[0]) > 0 or get_animation_max_amount_of_actors(sex_category_type, object_identifier[1]) > 0:
            return True
    return False

class StartNPCSexTeasingInteraction(TurboTerrainImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'StartNPCSexTeasingInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _test_for_npc_sex_start(interaction_context, interaction_target, (SexCategoryType.TEASING,))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return start_new_npc_sex_interaction(cls.get_interaction_target(interaction_instance), interaction_context=cls.get_interaction_context(interaction_instance), interaction_type=SexCategoryType.TEASING, is_manual=True)

class StartNPCSexHandjobInteraction(TurboTerrainImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'StartNPCSexHandjobInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _test_for_npc_sex_start(interaction_context, interaction_target, (SexCategoryType.HANDJOB,))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return start_new_npc_sex_interaction(cls.get_interaction_target(interaction_instance), interaction_context=cls.get_interaction_context(interaction_instance), interaction_type=SexCategoryType.HANDJOB, is_manual=True)

class StartNPCSexFootjobInteraction(TurboTerrainImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'StartNPCSexFootjobInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _test_for_npc_sex_start(interaction_context, interaction_target, (SexCategoryType.FOOTJOB,))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return start_new_npc_sex_interaction(cls.get_interaction_target(interaction_instance), interaction_context=cls.get_interaction_context(interaction_instance), interaction_type=SexCategoryType.FOOTJOB, is_manual=True)

class StartNPCSexOraljobInteraction(TurboTerrainImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'StartNPCSexOraljobInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _test_for_npc_sex_start(interaction_context, interaction_target, (SexCategoryType.ORALJOB,))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return start_new_npc_sex_interaction(cls.get_interaction_target(interaction_instance), interaction_context=cls.get_interaction_context(interaction_instance), interaction_type=SexCategoryType.ORALJOB, is_manual=True)

class StartNPCSexVaginalInteraction(TurboTerrainImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'StartNPCSexVaginalInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _test_for_npc_sex_start(interaction_context, interaction_target, (SexCategoryType.VAGINAL,))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return start_new_npc_sex_interaction(cls.get_interaction_target(interaction_instance), interaction_context=cls.get_interaction_context(interaction_instance), interaction_type=SexCategoryType.VAGINAL, is_manual=True)

class StartNPCSexAnalInteraction(TurboTerrainImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'StartNPCSexAnalInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _test_for_npc_sex_start(interaction_context, interaction_target, (SexCategoryType.ANAL,))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return start_new_npc_sex_interaction(cls.get_interaction_target(interaction_instance), interaction_context=cls.get_interaction_context(interaction_instance), interaction_type=SexCategoryType.ANAL, is_manual=True)

class StartNPCSexRandomInteraction(TurboTerrainImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'StartNPCSexRandomInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return _test_for_npc_sex_start(interaction_context, interaction_target, (SexCategoryType.TEASING, SexCategoryType.HANDJOB, SexCategoryType.ORALJOB, SexCategoryType.FOOTJOB, SexCategoryType.VAGINAL, SexCategoryType.ANAL))

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        return start_new_npc_sex_interaction(cls.get_interaction_target(interaction_instance), interaction_context=cls.get_interaction_context(interaction_instance), interaction_type=None, is_manual=True)
