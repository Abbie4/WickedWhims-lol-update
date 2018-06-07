import camera
import services
from event_testing.resolver import DoubleSimResolver
from sims4.localization import TunableLocalizedStringFactory
from ui.ui_dialog import UiDialogOk, UiDialogOkCancel, ButtonType
from ui.ui_dialog_generic import UiDialogTextInputOkCancel
from ui.ui_dialog_notification import UiDialogNotification
from ui.ui_dialog_picker import ObjectPickerRow, UiObjectPicker, UiSimPicker, SimPickerRow, OutfitPickerRow, UiOutfitPicker
from turbolib.l18n_util import TurboL18NUtil
from turbolib.manager_util import TurboManagerUtil


class TurboUIUtil:
    __qualname__ = 'TurboUIUtil'

    @staticmethod
    def _get_client_sim():
        client = services.client_manager().get_first_client()
        if client is not None:
            return client.active_sim or next(iter(TurboManagerUtil.Sim.get_all_sim_info_gen(humans=True, pets=False)))

    class Camera:
        __qualname__ = 'TurboUIUtil.Camera'

        @staticmethod
        def move_to_sim(sim_identifier, follow=True):
            sim = TurboManagerUtil.Sim.get_sim_instance(sim_identifier)
            camera.focus_on_sim(sim=sim, follow=follow, client=services.client_manager().get_first_client())

        @staticmethod
        def move_to_position(position):
            camera.focus_on_position(position, services.client_manager().get_first_client())

        @staticmethod
        def shake(duration, frequency=1.0, amplitude=1.0, octaves=1, fade_multiplier=1.0):
            camera.shake_camera(duration, frequency=frequency, amplitude=amplitude, octaves=octaves, fade_multiplier=fade_multiplier)

    class Phone:
        __qualname__ = 'TurboUIUtil.Phone'

        @staticmethod
        def silence():
            services.current_zone().ui_dialog_service._set_is_phone_silenced(True)

        @staticmethod
        def unsilence():
            services.current_zone().ui_dialog_service._set_is_phone_silenced(False)

        @staticmethod
        def is_silenced():
            return services.current_zone().ui_dialog_service.is_phone_silenced

    class OkDialog:
        __qualname__ = 'TurboUIUtil.OkDialog'

        @staticmethod
        def display(text, title, callback=None):
            text = TurboL18NUtil.get_localized_string(text)
            title = TurboL18NUtil.get_localized_string(title)
            ok_dialog = UiDialogOk.TunableFactory().default(TurboUIUtil._get_client_sim(), text=lambda *args, **kwargs: text, title=lambda *args, **kwargs: title)
            if callback is not None:
                ok_dialog.add_listener(callback)
            ok_dialog.show_dialog()

    class OkCancelDialog:
        __qualname__ = 'TurboUIUtil.OkCancelDialog'

        @staticmethod
        def display(text, title, callback=None):
            text = TurboL18NUtil.get_localized_string(text)
            title = TurboL18NUtil.get_localized_string(title)
            ok_dialog = UiDialogOkCancel.TunableFactory().default(TurboUIUtil._get_client_sim(), text=lambda *args, **kwargs: text, title=lambda *args, **kwargs: title)
            if callback is not None:
                ok_dialog.add_listener(callback)
            ok_dialog.show_dialog()

    class DramaDialog:
        __qualname__ = 'TurboUIUtil.DramaDialog'

        @staticmethod
        def display(sim_identifier, target_sim_identifier, text, ok_text, cancel_text, callback=None):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
            target_sim_info = TurboManagerUtil.Sim.get_sim_info(target_sim_identifier)
            text = TurboL18NUtil.get_localized_string(text)
            ok_text = TurboL18NUtil.get_localized_string(ok_text)
            cancel_text = TurboL18NUtil.get_localized_string(cancel_text)
            resolver = DoubleSimResolver(sim_info, target_sim_info)
            drama_dialog = UiDialogOkCancel.TunableFactory().default(sim_info, text=lambda *args, **kwargs: text, text_cancel=lambda *args, **kwargs: cancel_text, text_ok=lambda *args, **kwargs: ok_text, target_sim_id=target_sim_info.id, resolver=resolver)
            if callback is not None:
                drama_dialog.add_listener(callback)
            drama_dialog.show_dialog()

        @staticmethod
        def get_response_result(dialog):
            if dialog.response is not None and dialog.response == ButtonType.DIALOG_RESPONSE_OK:
                return True
            return False

    class TextInputDialog:
        __qualname__ = 'TurboUIUtil.TextInputDialog'

        class CustomUiDialogTextInputOkCancel(UiDialogTextInputOkCancel):
            __qualname__ = 'TurboUIUtil.TextInputDialog.CustomUiDialogTextInputOkCancel'

            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.text_input_responses = dict()

            def on_text_input(self, text_input_name='', text_input=''):
                self.text_input_responses[text_input_name] = text_input
                return False

            def build_msg(self, text_input_overrides=None, additional_tokens=(), **kwargs):
                msg = super().build_msg(additional_tokens=(), **kwargs)
                text_input_msg = msg.text_input.add()
                text_input_msg.text_input_name = 'text_input'
                if additional_tokens and additional_tokens[0] is not None:
                    text_input_msg.initial_value = TurboL18NUtil.get_localized_string(additional_tokens[0])
                return msg

        @staticmethod
        def display(text, title, initial_text=None, callback=None):
            text = TurboL18NUtil.get_localized_string(text)
            title = TurboL18NUtil.get_localized_string(title)
            text_input_dialog = TurboUIUtil.TextInputDialog.CustomUiDialogTextInputOkCancel.TunableFactory().default(TurboUIUtil._get_client_sim(), text=lambda *args, **kwargs: text, title=lambda *args, **kwargs: title)
            if callback is not None:
                text_input_dialog.add_listener(callback)
            if initial_text is not None:
                text_input_dialog.show_dialog(additional_tokens=(initial_text,))
            else:
                text_input_dialog.show_dialog()

        @staticmethod
        def get_response_result(dialog):
            return bool(dialog.accepted)

        @staticmethod
        def get_response_output(dialog):
            return str(dialog.text_input_responses.get('text_input'))

    class SimPickerDialog:
        __qualname__ = 'TurboUIUtil.SimPickerDialog'

        @staticmethod
        def display(text, title, sims_ids, selected_sims_ids=(), min_selectable=1, max_selectable=1, should_show_names=True, hide_row_description=False, sim=None, callback=None):
            text = TurboL18NUtil.get_localized_string(text)
            title = TurboL18NUtil.get_localized_string(title)
            sim_picker_dialog = UiSimPicker.TunableFactory().default(sim or TurboUIUtil._get_client_sim(), text=lambda *args, **kwargs: text, title=lambda *args, **kwargs: title, min_selectable=min_selectable, max_selectable=max_selectable, should_show_names=should_show_names, hide_row_description=hide_row_description)
            for sim_id in sims_ids:
                sim_picker_dialog.add_row(SimPickerRow(sim_id, select_default=sim_id in selected_sims_ids, tag=sim_id))
            if callback is not None:
                sim_picker_dialog.add_listener(callback)
            sim_picker_dialog.show_dialog()

        @staticmethod
        def get_response_result(dialog):
            return bool(dialog.accepted)

        @staticmethod
        def get_tag_result(dialog):
            return dialog.get_result_tags()[-1] or dialog.get_result_tags()[0]

        @staticmethod
        def get_tag_results(dialog):
            return dialog.get_result_tags()

    class ObjectPickerDialog:
        __qualname__ = 'TurboUIUtil.ObjectPickerDialog'

        class ListPickerRow:
            __qualname__ = 'TurboUIUtil.ObjectPickerDialog.ListPickerRow'

            def __init__(self, option_id, name, description, skip_tooltip=False, icon=None, tag=None, tag_itself=False):
                self.option_id = option_id
                self.name = TurboL18NUtil.get_localized_string(name)
                self.description = TurboL18NUtil.get_localized_string(description)
                self.skip_tooltip = skip_tooltip
                self.icon = icon
                self.tag = tag
                self.tag_itself = tag_itself

            def get_option_id(self):
                return self.option_id

            def get_name(self):
                return self.name

            def get_description(self):
                return self.description

            def get_icon(self):
                return self.icon

            def get_tag(self):
                if self.tag is not None:
                    return self.tag
                if self.tag_itself is True:
                    return self
                return self.option_id

            def get_object_picker_row(self):
                return ObjectPickerRow(count=0, option_id=self.get_option_id(), name=self.get_name(), row_description=self.get_description(), row_tooltip=None if self.skip_tooltip else TunableLocalizedStringFactory._Wrapper(self.get_description().hash), icon=self.get_icon(), tag=self.get_tag())

        @staticmethod
        def display(text, title, picker_rows, min_selectable=1, max_selectable=1, sim=None, callback=None):
            picker_list_dialog = UiObjectPicker.TunableFactory().default(sim or TurboUIUtil._get_client_sim(), text=lambda *args, **kwargs: text, title=lambda *args, **kwargs: title, min_selectable=min_selectable, max_selectable=max_selectable)
            for picker_row in picker_rows:
                if picker_row is None:
                    pass
                picker_list_dialog.add_row(picker_row.get_object_picker_row())
            if callback is not None:
                picker_list_dialog.add_listener(callback)
            picker_list_dialog.show_dialog()

        @staticmethod
        def get_response_result(dialog):
            return bool(dialog.accepted)

        @staticmethod
        def get_tag_result(dialog):
            return dialog.get_result_tags()[-1] or dialog.get_result_tags()[0]

        @staticmethod
        def get_tag_results(dialog):
            return dialog.get_result_tags()

    class OutfitPickerDialog:
        __qualname__ = 'TurboUIUtil.OutfitPickerDialog'

        @staticmethod
        def display(text, title, sim_identifier, outfits=(), sim=None, callback=None):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
            text = TurboL18NUtil.get_localized_string(text)
            title = TurboL18NUtil.get_localized_string(title)
            outfit_picker_dialog = UiOutfitPicker.TunableFactory().default(sim or TurboUIUtil._get_client_sim(), text=lambda *args, **kwargs: text, title=lambda *args, **kwargs: title)
            (current_outfit_category, current_outfit_index) = sim_info.get_current_outfit()
            for (outfit_category, outfit_index) in outfits:
                is_enabled = outfit_category == current_outfit_category and outfit_index == current_outfit_index
                outfit_picker_dialog.add_row(OutfitPickerRow(outfit_sim_id=TurboManagerUtil.Sim.get_sim_id(sim_info), outfit_category=outfit_category, outfit_index=outfit_index, is_enable=not is_enabled, tag=(outfit_category, outfit_index)))
            if callback is not None:
                outfit_picker_dialog.add_listener(callback)
            outfit_picker_dialog.show_dialog()

        @staticmethod
        def get_response_result(dialog):
            return bool(dialog.accepted)

        @staticmethod
        def get_tag_result(dialog):
            return dialog.get_result_tags()[-1] or dialog.get_result_tags()[0]

        @staticmethod
        def get_tag_results(dialog):
            return dialog.get_result_tags()

    class Notification:
        __qualname__ = 'TurboUIUtil.Notification'

        class UiDialogNotificationVisualType:
            __qualname__ = 'TurboUIUtil.Notification.UiDialogNotificationVisualType'

            def _get_ui_dialog_notification_visual_type(*args):
                try:
                    return UiDialogNotification.UiDialogNotificationVisualType(args[0])
                except:
                    return

            INFORMATION = _get_ui_dialog_notification_visual_type(0)
            SPEECH = _get_ui_dialog_notification_visual_type(1)
            SPECIAL_MOMENT = _get_ui_dialog_notification_visual_type(2)

        class UiDialogNotificationUrgency:
            __qualname__ = 'TurboUIUtil.Notification.UiDialogNotificationUrgency'

            def _get_ui_dialog_notification_urgency(*args):
                try:
                    return UiDialogNotification.UiDialogNotificationUrgency(args[0])
                except:
                    return

            DEFAULT = _get_ui_dialog_notification_urgency(0)
            URGENT = _get_ui_dialog_notification_urgency(1)

        class UiDialogNotificationLevel:
            __qualname__ = 'TurboUIUtil.Notification.UiDialogNotificationLevel'

            def _get_ui_dialog_notification_level(*args):
                try:
                    return UiDialogNotification.UiDialogNotificationLevel(args[0])
                except:
                    return

            PLAYER = _get_ui_dialog_notification_level(0)
            SIM = _get_ui_dialog_notification_level(1)

        @staticmethod
        def display(text, title, visual_type=None, urgency=None, information_level=None, icons=None):
            text = TurboL18NUtil.get_localized_string(text)
            title = TurboL18NUtil.get_localized_string(title)
            if visual_type is None:
                visual_type = TurboUIUtil.Notification.UiDialogNotificationVisualType.INFORMATION
            if urgency is None:
                urgency = TurboUIUtil.Notification.UiDialogNotificationUrgency.DEFAULT
            if information_level is None:
                information_level = TurboUIUtil.Notification.UiDialogNotificationLevel.SIM
            notification = UiDialogNotification.TunableFactory().default(None, text=lambda *args, **kwargs: text, title=lambda *args, **kwargs: title, visual_type=visual_type, urgency=urgency, information_level=information_level)
            notification.show_dialog(icon_override=icons)

