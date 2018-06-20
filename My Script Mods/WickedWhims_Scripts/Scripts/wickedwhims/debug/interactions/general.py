'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from enums.motives_enum import SimMotive
from enums.situations_enum import SimSituation
from turbolib.cas_util import TurboCASUtil
from turbolib.components_util import TurboComponentUtil
from turbolib.resource_util import TurboResourceUtil
from turbolib.sim_util import TurboSimUtil
from turbolib.wrappers.interactions import TurboImmediateSuperInteraction, TurboInteractionStartMixin
from wickedwhims.debug.debug_controller import is_main_debug_flag_enabled
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.utils_cas import get_modified_outfit, get_previous_modified_outfit
from wickedwhims.utils_interfaces import display_notification
from wickedwhims.utils_motives import get_sim_motive_value

class DebugGeneralInfoInteraction(TurboImmediateSuperInteraction, TurboInteractionStartMixin):
    __qualname__ = 'DebugGeneralInfoInteraction'

    @classmethod
    def on_interaction_test(cls, interaction_context, interaction_target):
        return is_main_debug_flag_enabled()

    @classmethod
    def on_interaction_start(cls, interaction_instance):
        sim = cls.get_interaction_target(interaction_instance)
        basic_debug_info = ''
        sim_position = TurboSimUtil.Location.get_position(sim)
        basic_debug_info += 'X: ' + str(sim_position.x) + '\n'
        basic_debug_info += 'Y: ' + str(sim_position.y) + '\n'
        basic_debug_info += 'Z: ' + str(sim_position.z) + '\n'
        basic_debug_info += '\nMale Gender Pref: ' + str(TurboSimUtil.Gender.get_gender_preference(sim, TurboSimUtil.Gender.MALE)) + '\n'
        basic_debug_info += 'Female Gender Pref: ' + str(TurboSimUtil.Gender.get_gender_preference(sim, TurboSimUtil.Gender.FEMALE)) + '\n'
        basic_debug_info += '\nCurrent Occult: ' + str(TurboSimUtil.Occult.get_current_occult_type(sim).name) + '\n'
        basic_debug_info += 'Occults List: ' + str([str(occult.name) for occult in TurboSimUtil.Occult.get_occult_types(sim)])[1:-1] + '\n'
        if TurboSimUtil.Component.has_component(sim, TurboComponentUtil.ComponentType.BUFF):
            basic_debug_info += '\nActive Buffs: ' + str([str(buff.__class__.__name__) for buff in TurboSimUtil.Buff.get_all_buffs_gen(sim)])[1:-1] + '\n'
        basic_debug_info += '\nTraits: ' + str([str(trait.__name__) for trait in TurboSimUtil.Trait.get_all_traits_gen(sim)])[1:-1] + '\n'
        basic_debug_info += '\nActive Situations: ' + str([str(SimSituation(TurboResourceUtil.Resource.get_guid64(situation)).name) for situation in TurboSimUtil.Situation.get_active_situations(sim)])[1:-1] + '\n'
        basic_debug_info += '\nRunning Interactions: ' + str(TurboSimUtil.Interaction.get_running_interactions_ids(sim))[1:-1] + '\n'
        basic_debug_info += '\nQueued Interactions: ' + str(TurboSimUtil.Interaction.get_queued_interactions_ids(sim))[1:-1] + '\n'
        native_current_outfit = TurboSimUtil.CAS.get_current_outfit(sim)
        modified_current_outfit = get_modified_outfit(sim)
        saved_current_outfit = (sim_ev(sim).current_outfit_category, sim_ev(sim).current_outfit_index)
        saved_previous_outfit = get_previous_modified_outfit(sim)
        basic_debug_info += '\nNative Current Outfit: ' + str(TurboCASUtil.OutfitCategory.get_outfit_category(native_current_outfit[0]).name) + ', ' + str(native_current_outfit[1]) + '\n'
        basic_debug_info += 'Modified Current Outfit: ' + str(TurboCASUtil.OutfitCategory.get_outfit_category(modified_current_outfit[0]).name) + ', ' + str(modified_current_outfit[1]) + '\n'
        basic_debug_info += 'Saved Current Outfit: ' + str(TurboCASUtil.OutfitCategory.get_outfit_category(saved_current_outfit[0]).name) + ', ' + str(saved_current_outfit[1]) + '\n'
        basic_debug_info += 'Saved Previous Outfit: ' + str(TurboCASUtil.OutfitCategory.get_outfit_category(saved_previous_outfit[0]).name) + ', ' + str(saved_previous_outfit[1]) + '\n'
        basic_debug_info += '\nMotives Data:\n'
        basic_debug_info += '  Hunger: ' + str(get_sim_motive_value(sim, SimMotive.HUNGER)) + '\n'
        basic_debug_info += '  Energy: ' + str(get_sim_motive_value(sim, SimMotive.ENERGY)) + '\n'
        basic_debug_info += '  Bladder: ' + str(get_sim_motive_value(sim, SimMotive.BLADDER)) + '\n'
        basic_debug_info += '  Fun: ' + str(get_sim_motive_value(sim, SimMotive.FUN)) + '\n'
        basic_debug_info += '  Hygiene: ' + str(get_sim_motive_value(sim, SimMotive.HYGIENE)) + '\n'
        basic_debug_info += '  Social: ' + str(get_sim_motive_value(sim, SimMotive.SOCIAL)) + '\n'
        basic_debug_info += '  Vampire Power: ' + str(get_sim_motive_value(sim, SimMotive.VAMPIRE_POWER)) + '\n'
        basic_debug_info += '  Vampire Thirst: ' + str(get_sim_motive_value(sim, SimMotive.VAMPIRE_THIRST)) + '\n'
        basic_debug_info += '  PlantSim Water: ' + str(get_sim_motive_value(sim, SimMotive.PLANTSIM_WATER)) + '\n'
        basic_debug_info += 'Is Leaving Lot: ' + str(TurboSimUtil.Spawner.is_leaving(sim)) + '\n'
        display_notification(text=basic_debug_info, title=str(TurboSimUtil.Name.get_name(sim)[0]) + ' ' + str(TurboSimUtil.Name.get_name(sim)[1]) + ' General Debug', secondary_icon=sim)

