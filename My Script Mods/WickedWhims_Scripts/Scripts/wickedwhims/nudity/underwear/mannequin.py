from turbolib.cas_util import TurboCASUtil
from turbolib.command_util import TurboCommandUtil
from turbolib.events.core import register_zone_load_event_method
from turbolib.manager_util import TurboManagerUtil
from turbolib.object_util import TurboObjectUtil
from turbolib.resource_util import TurboResourceUtil
from turbolib.sim_util import TurboSimUtil
from turbolib.ui_util import TurboUIUtil
from turbolib.wrappers.commands import register_game_command, TurboCommandType
from wickedwhims.nudity.underwear.operator import get_sim_underwear_data, set_sim_underwear_data, validate_outfit_underwear
from wickedwhims.sxex_bridge.nudity import get_default_nude_cas_part_id
from wickedwhims.sxex_bridge.outfit import dress_up_outfit
from wickedwhims.utils_interfaces import display_notification
UNDERWEAR_MANNEQUIN_IN_USE = False
UNDERWEAR_MANNEQUIN_SIM_ID = -1
UNDERWEAR_MANNEQUIN_OBJECT_ID = -1

def open_underwear_mannequin(sim=None):
    global UNDERWEAR_MANNEQUIN_IN_USE, UNDERWEAR_MANNEQUIN_SIM_ID, UNDERWEAR_MANNEQUIN_OBJECT_ID
    if sim is None:
        sim = TurboManagerUtil.Sim.get_active_sim()
    if TurboSimUtil.Gender.is_male(sim):
        mannequin = TurboObjectUtil.GameObject.create_object(15785160026562278628, location=TurboSimUtil.Location.get_location(sim))
    else:
        mannequin = TurboObjectUtil.GameObject.create_object(14110242915816833432, location=TurboSimUtil.Location.get_location(sim))
    mannequin_id = TurboResourceUtil.Resource.get_id(mannequin)
    mannequin_component = TurboObjectUtil.Mannequin.get_component(mannequin)
    mannequin_sim_info = TurboObjectUtil.Mannequin.get_mannequin_component_sim_info(mannequin_component)
    TurboObjectUtil.Mannequin.remove_mannequin_protocol_buffer(mannequin)
    for outfit_category in (TurboCASUtil.OutfitCategory.EVERYDAY, TurboCASUtil.OutfitCategory.FORMAL, TurboCASUtil.OutfitCategory.ATHLETIC, TurboCASUtil.OutfitCategory.SLEEP, TurboCASUtil.OutfitCategory.PARTY, TurboCASUtil.OutfitCategory.SWIMWEAR, TurboCASUtil.OutfitCategory.HOTWEATHER, TurboCASUtil.OutfitCategory.COLDWEATHER):
        for outfit_index in range(TurboCASUtil.OutfitCategory.get_maximum_outfits_for_outfit_category(outfit_category)):
            while TurboSimUtil.CAS.has_outfit(sim, (outfit_category, outfit_index)):
                underwear_parts = get_sim_underwear_data(sim, (outfit_category, outfit_index))
                if TurboSimUtil.Gender.is_male(sim):
                    top_body_part = get_default_nude_cas_part_id(sim, TurboCASUtil.BodyType.UPPER_BODY)
                    bottom_body_part = underwear_parts[1] if outfit_category != TurboCASUtil.OutfitCategory.SLEEP and outfit_category != TurboCASUtil.OutfitCategory.SWIMWEAR else get_default_nude_cas_part_id(sim, TurboCASUtil.BodyType.LOWER_BODY)
                    TurboSimUtil.CAS.set_outfit_parts(mannequin_sim_info, (outfit_category, outfit_index), {TurboCASUtil.BodyType.HAIR: 16045584265534180326, TurboCASUtil.BodyType.HEAD: 16045584265534180326, TurboCASUtil.BodyType.UPPER_BODY: top_body_part, TurboCASUtil.BodyType.LOWER_BODY: bottom_body_part, TurboCASUtil.BodyType.SHOES: 6563})
                else:
                    top_body_part = underwear_parts[0] if outfit_category != TurboCASUtil.OutfitCategory.SLEEP and outfit_category != TurboCASUtil.OutfitCategory.SWIMWEAR else get_default_nude_cas_part_id(sim, 6)
                    bottom_body_part = underwear_parts[1] if outfit_category != TurboCASUtil.OutfitCategory.SLEEP and outfit_category != TurboCASUtil.OutfitCategory.SWIMWEAR else get_default_nude_cas_part_id(sim, 7)
                    TurboSimUtil.CAS.set_outfit_parts(mannequin_sim_info, (outfit_category, outfit_index), {TurboCASUtil.BodyType.HAIR: 16045584265534180326, TurboCASUtil.BodyType.HEAD: 16045584265534180326, TurboCASUtil.BodyType.UPPER_BODY: top_body_part, TurboCASUtil.BodyType.LOWER_BODY: bottom_body_part, TurboCASUtil.BodyType.SHOES: 6543})
    TurboObjectUtil.Mannequin.populate_mannequin_protocol_buffer(mannequin_component)
    TurboSimUtil.CAS.set_current_outfit(mannequin_sim_info, TurboSimUtil.CAS.get_current_outfit(sim))
    display_notification(text=2196543455, title=712099301, information_level=TurboUIUtil.Notification.UiDialogNotificationLevel.PLAYER)
    UNDERWEAR_MANNEQUIN_IN_USE = True
    UNDERWEAR_MANNEQUIN_SIM_ID = TurboManagerUtil.Sim.get_sim_id(sim)
    UNDERWEAR_MANNEQUIN_OBJECT_ID = mannequin_id
    dress_up_outfit(sim)
    TurboCommandUtil.invoke_command('sims.exit2caswithmannequinid {}'.format(mannequin_id, ''))


@register_zone_load_event_method(unique_id='WickedWhims', priority=50, late=True)
def _wickedwhims_check_for_underwear_mannequin():
    global UNDERWEAR_MANNEQUIN_IN_USE
    if UNDERWEAR_MANNEQUIN_IN_USE is False:
        return
    UNDERWEAR_MANNEQUIN_IN_USE = False
    if UNDERWEAR_MANNEQUIN_SIM_ID == -1 or UNDERWEAR_MANNEQUIN_OBJECT_ID == -1:
        _reset_current_underwear_mannequin_data()
        return
    sim_info = TurboManagerUtil.Sim.get_sim_info(UNDERWEAR_MANNEQUIN_SIM_ID)
    mannequin = TurboObjectUtil.GameObject.get_object_with_id(UNDERWEAR_MANNEQUIN_OBJECT_ID)
    if sim_info is None or mannequin is None:
        _reset_current_underwear_mannequin_data()
        return
    mannequin_component = TurboObjectUtil.Mannequin.get_component(mannequin)
    mannequin_sim_info = TurboObjectUtil.Mannequin.get_mannequin_component_sim_info(mannequin_component)
    for outfit_category in (TurboCASUtil.OutfitCategory.EVERYDAY, TurboCASUtil.OutfitCategory.FORMAL, TurboCASUtil.OutfitCategory.ATHLETIC, TurboCASUtil.OutfitCategory.PARTY, TurboCASUtil.OutfitCategory.HOTWEATHER, TurboCASUtil.OutfitCategory.COLDWEATHER):
        for outfit_index in range(TurboCASUtil.OutfitCategory.get_maximum_outfits_for_outfit_category(outfit_category)):
            while TurboSimUtil.CAS.has_outfit(sim_info, (outfit_category, outfit_index)) and TurboSimUtil.CAS.has_outfit(mannequin_sim_info, (outfit_category, outfit_index)):
                body_parts = TurboSimUtil.CAS.get_outfit_parts(mannequin_sim_info, (outfit_category, outfit_index))
                if TurboSimUtil.Gender.is_male(sim_info):
                    if TurboCASUtil.BodyType.LOWER_BODY in body_parts:
                        set_sim_underwear_data(sim_info, [-1, body_parts[TurboCASUtil.BodyType.LOWER_BODY]], (outfit_category, outfit_index))
                elif TurboCASUtil.BodyType.UPPER_BODY in body_parts and TurboCASUtil.BodyType.LOWER_BODY in body_parts:
                    underwear_data = [-1, -1]
                    underwear_data[0] = body_parts[TurboCASUtil.BodyType.UPPER_BODY]
                    underwear_data[1] = body_parts[TurboCASUtil.BodyType.LOWER_BODY]
                    set_sim_underwear_data(sim_info, underwear_data, (outfit_category, outfit_index))
                validate_outfit_underwear(sim_info, (outfit_category, outfit_index))
    TurboSimUtil.CAS.set_current_outfit(sim_info, TurboSimUtil.CAS.get_current_outfit(sim_info), dirty=True)
    _reset_current_underwear_mannequin_data()
    TurboObjectUtil.GameObject.destroy_object(mannequin, cause='Temporary underwear mannequin.')


def _reset_current_underwear_mannequin_data():
    global UNDERWEAR_MANNEQUIN_IN_USE, UNDERWEAR_MANNEQUIN_SIM_ID, UNDERWEAR_MANNEQUIN_OBJECT_ID
    UNDERWEAR_MANNEQUIN_IN_USE = False
    UNDERWEAR_MANNEQUIN_SIM_ID = -1
    UNDERWEAR_MANNEQUIN_OBJECT_ID = -1


@register_game_command('ww.cleanup_mannequins', command_type=TurboCommandType.LIVE)
def _wickedwhims_command_clean_up_mannequins(output=None):
    male_mannequin = TurboObjectUtil.Definition.get(15785160026562278628)
    female_mannequin = TurboObjectUtil.Definition.get(14110242915816833432)
    for game_object in TurboObjectUtil.GameObject.get_all_gen():
        object_definition = TurboObjectUtil.GameObject.get_object_definition(game_object)
        while object_definition == male_mannequin or object_definition == female_mannequin:
            TurboObjectUtil.GameObject.destroy_object(game_object, cause='Temporary underwear mannequin.')
    output('Cleaned up WickedWhims mannequins.')

