'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from turbolib.events.core import has_game_loaded
from turbolib.l18n_util import TurboL18NUtil
from turbolib.manager_util import TurboManagerUtil
from turbolib.resource_util import TurboResourceUtil
from turbolib.ui_util import TurboUIUtil

def display_notification(text=None, text_tokens=(), title=None, title_tokens=(), primary_icon=None, secondary_icon=None, is_safe=False, **kwargs):
    if text is None and title is None:
        return
    if not (is_safe is True and has_game_loaded()):
        return
    localized_text = TurboL18NUtil.get_localized_string(text, text_tokens)
    localized_title = TurboL18NUtil.get_localized_string(title, title_tokens)
    if primary_icon is not None:
        secondary_icon = TurboManagerUtil.Sim.get_sim_info(primary_icon) or primary_icon
    if secondary_icon is not None:
        secondary_icon = TurboManagerUtil.Sim.get_sim_info(secondary_icon) or secondary_icon
    if primary_icon or secondary_icon:
        icon_data = (primary_icon, secondary_icon)
    else:
        icon_data = None
    TurboUIUtil.Notification.display(text=localized_text, title=localized_title, icons=icon_data, **kwargs)


def display_debug(text=None, include_traceback=False, sim_info=None):
    if include_traceback is True and text is not None:
        import traceback
        stacktrace = ''.join(traceback.format_stack())
        text += '\n\n' + stacktrace
    display_notification(text=text, title='Debug', secondary_icon=sim_info, is_safe=True)


def display_ok_dialog(text=None, text_tokens=(), title=None, title_tokens=(), ok_text=3648501874, ok_text_tokens=(), callback=None):
    localized_text = TurboL18NUtil.get_localized_string(text, text_tokens)
    localized_title = TurboL18NUtil.get_localized_string(title, title_tokens)
    localized_ok_text = TurboL18NUtil.get_localized_string(ok_text, ok_text_tokens)
    TurboUIUtil.OkDialog.display(localized_text, localized_title, ok_text=localized_ok_text, callback=callback)


def display_okcancel_dialog(text=None, text_tokens=(), title=None, title_tokens=(), ok_text=3648501874, ok_text_tokens=(), cancel_text=3497542682, cancel_text_tokens=(), callback=None):
    localized_text = TurboL18NUtil.get_localized_string(text, text_tokens)
    localized_title = TurboL18NUtil.get_localized_string(title, title_tokens)
    localized_ok_text = TurboL18NUtil.get_localized_string(ok_text, ok_text_tokens)
    localized_cancel_text = TurboL18NUtil.get_localized_string(cancel_text, cancel_text_tokens)
    TurboUIUtil.OkCancelDialog.display(localized_text, localized_title, ok_text=localized_ok_text, cancel_text=localized_cancel_text, callback=callback)


def display_drama_dialog(sim_identifier, target_sim_identifier, text=None, text_tokens=(), ok_text=None, ok_text_tokens=(), cancel_text=None, cancel_text_tokens=(), callback=None):
    localized_text = TurboL18NUtil.get_localized_string(text, text_tokens)
    localized_ok_text = TurboL18NUtil.get_localized_string(ok_text, ok_text_tokens)
    localized_cancel_text = TurboL18NUtil.get_localized_string(cancel_text, cancel_text_tokens)
    TurboUIUtil.DramaDialog.display(sim_identifier, target_sim_identifier, localized_text, localized_ok_text, localized_cancel_text, callback=callback)


def display_text_input_dialog(text=None, text_tokens=(), title=None, title_tokens=(), initial_text=None, callback=None):
    localized_text = TurboL18NUtil.get_localized_string(text, text_tokens)
    localized_title = TurboL18NUtil.get_localized_string(title, title_tokens)
    TurboUIUtil.TextInputDialog.display(localized_text, localized_title, initial_text=initial_text, callback=callback)


def display_picker_list_dialog(text=None, text_tokens=(), title=None, title_tokens=(), picker_rows=(), sim=None, callback=None):
    localized_text = TurboL18NUtil.get_localized_string(text, text_tokens)
    localized_title = TurboL18NUtil.get_localized_string(title, title_tokens)
    TurboUIUtil.ObjectPickerDialog.display(localized_text, localized_title, picker_rows, sim=TurboManagerUtil.Sim.get_sim_info(sim), callback=callback)


def display_sim_picker_dialog(text=None, text_tokens=(), title=None, title_tokens=(), sims_id_list=(), selected_sims_id_list=(), selectable_amount=1, sim=None, callback=None):
    localized_text = TurboL18NUtil.get_localized_string(text, text_tokens)
    localized_title = TurboL18NUtil.get_localized_string(title, title_tokens)
    TurboUIUtil.SimPickerDialog.display(localized_text, localized_title, sims_id_list, selected_sims_ids=selected_sims_id_list, max_selectable=selectable_amount, sim=TurboManagerUtil.Sim.get_sim_info(sim), callback=callback)


def display_outfit_picker_dialog(text=None, text_tokens=(), title=None, title_tokens=(), outfits=(), sim=None, callback=None):
    localized_text = TurboL18NUtil.get_localized_string(text, text_tokens)
    localized_title = TurboL18NUtil.get_localized_string(title, title_tokens)
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim)
    TurboUIUtil.OutfitPickerDialog.display(localized_text, localized_title, sim_info, outfits=outfits, sim=sim_info, callback=callback)


def get_action_icon():
    return TurboResourceUtil.ResourceTypes.get_resource_key(TurboResourceUtil.ResourceTypes.PNG, 12189911648888101822)


def get_arrow_icon():
    return TurboResourceUtil.ResourceTypes.get_resource_key(TurboResourceUtil.ResourceTypes.PNG, 17339207013735946562)


def get_question_icon():
    return TurboResourceUtil.ResourceTypes.get_resource_key(TurboResourceUtil.ResourceTypes.PNG, 15104483716421527915)


def get_selected_icon():
    return TurboResourceUtil.ResourceTypes.get_resource_key(TurboResourceUtil.ResourceTypes.PNG, 15760333005986945440)


def get_unselected_icon():
    return TurboResourceUtil.ResourceTypes.get_resource_key(TurboResourceUtil.ResourceTypes.PNG, 16229553403167990693)


def get_random_icon():
    return TurboResourceUtil.ResourceTypes.get_resource_key(TurboResourceUtil.ResourceTypes.PNG, 16928883153174250259)

