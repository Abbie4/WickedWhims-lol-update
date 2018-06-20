from turbolib.cas_util import TurboCASUtil
from turbolib.command_util import TurboCommandUtil
from turbolib.events.core import register_zone_load_event_method
from turbolib.manager_util import TurboManagerUtil
from turbolib.object_util import TurboObjectUtil
from turbolib.resource_util import TurboResourceUtil
from turbolib.sim_util import TurboSimUtil
from turbolib.ui_util import TurboUIUtil
from wickedwhims.main.sim_ev_handler import sim_ev
from wickedwhims.sex.strapon.operator import get_sim_strapon_part_id, has_loaded_strapon
from wickedwhims.utils_interfaces import display_notification
STRAPON_MANNEQUIN_IN_USE = False
STRAPON_MANNEQUIN_SIM_ID = -1
STRAPON_MANNEQUIN_OBJECT_ID = -1

def open_strapon_mannequin(sim=None):
    global STRAPON_MANNEQUIN_IN_USE, STRAPON_MANNEQUIN_SIM_ID, STRAPON_MANNEQUIN_OBJECT_ID
    if sim is None:
        sim = TurboManagerUtil.Sim.get_active_sim()
    if not has_loaded_strapon():
        return
    mannequin = TurboObjectUtil.GameObject.create_object(14110242915816833432, location=TurboSimUtil.Location.get_location(sim))
    mannequin_id = TurboResourceUtil.Resource.get_id(mannequin)
    mannequin_component = TurboObjectUtil.Mannequin.get_component(mannequin)
    mannequin_sim_info = TurboObjectUtil.Mannequin.get_mannequin_component_sim_info(mannequin_component)
    TurboObjectUtil.Mannequin.remove_mannequin_protocol_buffer(mannequin)
    for outfit_category in (TurboCASUtil.OutfitCategory.EVERYDAY, TurboCASUtil.OutfitCategory.FORMAL, TurboCASUtil.OutfitCategory.ATHLETIC, TurboCASUtil.OutfitCategory.SLEEP, TurboCASUtil.OutfitCategory.PARTY, TurboCASUtil.OutfitCategory.SWIMWEAR, TurboCASUtil.OutfitCategory.HOTWEATHER, TurboCASUtil.OutfitCategory.COLDWEATHER):
        while TurboSimUtil.CAS.has_outfit(sim, (outfit_category, 0)):
            TurboSimUtil.CAS.set_outfit_parts(mannequin_sim_info, (outfit_category, 0), {TurboCASUtil.BodyType.HAIR: 16045584265534180326, TurboCASUtil.BodyType.HEAD: 16045584265534180326, TurboCASUtil.BodyType.UPPER_BODY: 6540, TurboCASUtil.BodyType.LOWER_BODY: get_sim_strapon_part_id(sim), TurboCASUtil.BodyType.SHOES: 6543})
    TurboObjectUtil.Mannequin.populate_mannequin_protocol_buffer(mannequin_component)
    TurboSimUtil.CAS.set_current_outfit(mannequin_sim_info, TurboSimUtil.CAS.get_current_outfit(sim))
    display_notification(text=1645033536, title=1851298968, information_level=TurboUIUtil.Notification.UiDialogNotificationLevel.PLAYER)
    STRAPON_MANNEQUIN_IN_USE = True
    STRAPON_MANNEQUIN_SIM_ID = TurboManagerUtil.Sim.get_sim_id(sim)
    STRAPON_MANNEQUIN_OBJECT_ID = mannequin_id
    TurboCommandUtil.invoke_command('sims.exit2caswithmannequinid {}'.format(mannequin_id, ''))


@register_zone_load_event_method(unique_id='WickedWhims', priority=50, late=True)
def _wickedwhims_check_for_strapon_mannequin():
    global STRAPON_MANNEQUIN_IN_USE
    if STRAPON_MANNEQUIN_IN_USE is False:
        return
    STRAPON_MANNEQUIN_IN_USE = False
    if STRAPON_MANNEQUIN_SIM_ID == -1 or STRAPON_MANNEQUIN_OBJECT_ID == -1:
        _reset_current_strapon_mannequin_data()
        return
    sim_info = TurboManagerUtil.Sim.get_sim_info(STRAPON_MANNEQUIN_SIM_ID)
    mannequin = TurboObjectUtil.GameObject.get_object_with_id(STRAPON_MANNEQUIN_OBJECT_ID)
    if sim_info is None or mannequin is None:
        _reset_current_strapon_mannequin_data()
        return
    mannequin_component = TurboObjectUtil.Mannequin.get_component(mannequin)
    mannequin_sim_info = TurboObjectUtil.Mannequin.get_mannequin_component_sim_info(mannequin_component)
    body_parts = TurboSimUtil.CAS.get_outfit_parts(mannequin_sim_info, (TurboCASUtil.OutfitCategory.EVERYDAY, 0))
    if TurboCASUtil.BodyType.LOWER_BODY in body_parts:
        sim_ev(sim_info).strapon_part_id = body_parts[TurboCASUtil.BodyType.LOWER_BODY]
    _reset_current_strapon_mannequin_data()
    TurboObjectUtil.GameObject.destroy_object(mannequin, cause='Temporary strapon mannequin.')


def _reset_current_strapon_mannequin_data():
    global STRAPON_MANNEQUIN_IN_USE, STRAPON_MANNEQUIN_SIM_ID, STRAPON_MANNEQUIN_OBJECT_ID
    STRAPON_MANNEQUIN_IN_USE = False
    STRAPON_MANNEQUIN_SIM_ID = -1
    STRAPON_MANNEQUIN_OBJECT_ID = -1

