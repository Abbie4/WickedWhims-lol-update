from turbolib.special.custom_exception_watcher import exception_watch
from turbolib.ui_util import TurboUIUtil
from wickedwhims.main.settings._ts4_menu_utils import get_menu_sim
from wickedwhims.utils_interfaces import get_arrow_icon, display_picker_list_dialog, get_selected_icon, get_unselected_icon, display_text_input_dialog, get_action_icon

class SettingsWindow:
    __qualname__ = 'SettingsWindow'

    def __init__(self, window_id, window_title, window_description, open_callback=None, change_callback=None, cancel_callback=None):
        self.window_id = window_id
        self.window_title = window_title
        self.window_description = window_description
        self.window_picker_rows = list()
        self.window_options = list()
        self.open_callback = open_callback
        self.change_callback = change_callback
        self.cancel_callback = cancel_callback

    def get_window_picker_row(self):
        return TurboUIUtil.ObjectPickerDialog.ListPickerRow(self.window_id, self.window_title, self.window_description, icon=get_arrow_icon(), tag=self.open_window)

    def open_window(self, allow_open_callback=True, allow_change_callback=False):
        display_picker_list_dialog(title=self.window_title, picker_rows=self.window_picker_rows, sim=get_menu_sim(), callback=self._window_callback)
        if allow_open_callback and self.open_callback is not None:
            self.open_callback()
        if allow_change_callback and self.change_callback is not None:
            self.change_callback()

    @exception_watch()
    def _window_callback(self, dialog):
        if not TurboUIUtil.ObjectPickerDialog.get_response_result(dialog):
            if self.cancel_callback is not None:
                self.cancel_callback()
            return
        result = TurboUIUtil.ObjectPickerDialog.get_tag_result(dialog)
        if result is not None:
            selected_option = self.window_options[result]
            selected_option.select_callback()

    def add_settings_option(self, settings_option):
        self.window_picker_rows.append(settings_option.select_picker_row(len(self.window_options)))
        self.window_options.append(settings_option)


class _SettingsOption:
    __qualname__ = '_SettingsOption'

    def __init__(self, option_name, option_description):
        self.option_name = option_name
        self.option_description = option_description

    def select_picker_row(self, picker_row_id):
        raise NotImplementedError

    def select_callback(self):
        raise NotImplementedError


class SettingsBranchOption(_SettingsOption):
    __qualname__ = 'SettingsBranchOption'

    def __init__(self, branch_settings_window_function, allow_open_callback=True):
        self.branch_settings_window_function = branch_settings_window_function
        self.allow_open_callback = allow_open_callback
        branch_settings_window = self.branch_settings_window_function()
        super().__init__(branch_settings_window.window_title, branch_settings_window.window_description)

    def select_picker_row(self, picker_row_id):
        return TurboUIUtil.ObjectPickerDialog.ListPickerRow(picker_row_id, self.option_name, self.option_description, icon=get_arrow_icon())

    def select_callback(self):
        branch_settings_window = self.branch_settings_window_function()
        branch_settings_window.open_window(allow_open_callback=self.allow_open_callback)


class SettingsCallbackOption(_SettingsOption):
    __qualname__ = 'SettingsCallbackOption'

    def __init__(self, option_name, option_description, callback_function):
        super().__init__(option_name, option_description)
        self.callback_function = callback_function

    def select_picker_row(self, picker_row_id):
        return TurboUIUtil.ObjectPickerDialog.ListPickerRow(picker_row_id, self.option_name, self.option_description, icon=get_arrow_icon())

    def select_callback(self):
        self.callback_function()


class SettingsSelectorOption(_SettingsOption):
    __qualname__ = 'SettingsSelectorOption'

    def __init__(self, option_name, option_description, return_settings_window_function, settings_dict, settings_dict_id, target_state, allow_open_callback=False, allow_change_callback=True):
        super().__init__(option_name, option_description)
        self.return_settings_window_function = return_settings_window_function
        self.allow_open_callback = allow_open_callback
        self.allow_change_callback = allow_change_callback
        self.settings_dict = settings_dict
        self.settings_dict_id = settings_dict_id
        self.target_state = target_state

    def select_picker_row(self, picker_row_id):
        return TurboUIUtil.ObjectPickerDialog.ListPickerRow(picker_row_id, self.option_name, self.option_description, icon=get_selected_icon() if self.settings_dict[self.settings_dict_id] == self.target_state else get_unselected_icon())

    def select_callback(self):
        self.settings_dict[self.settings_dict_id] = int(self.target_state)
        return_settings_window = self.return_settings_window_function()
        return_settings_window.open_window(allow_open_callback=self.allow_open_callback, allow_change_callback=self.allow_change_callback)


class SettingsSwitchOption(_SettingsOption):
    __qualname__ = 'SettingsSwitchOption'

    def __init__(self, option_name, option_description, return_settings_window_function, settings_dict, settings_dict_id, allow_open_callback=False, allow_change_callback=True):
        super().__init__(option_name, option_description)
        self.return_settings_window_function = return_settings_window_function
        self.allow_open_callback = allow_open_callback
        self.allow_change_callback = allow_change_callback
        self.settings_dict = settings_dict
        self.settings_dict_id = settings_dict_id

    def select_picker_row(self, picker_row_id):
        return TurboUIUtil.ObjectPickerDialog.ListPickerRow(picker_row_id, self.option_name, self.option_description, icon=get_selected_icon() if self.settings_dict[self.settings_dict_id] else get_unselected_icon())

    def select_callback(self):
        current_state = bool(self.settings_dict[self.settings_dict_id])
        self.settings_dict[self.settings_dict_id] = int(not current_state)
        return_settings_window = self.return_settings_window_function()
        return_settings_window.open_window(allow_open_callback=self.allow_open_callback, allow_change_callback=self.allow_change_callback)


class SettingsInputOption(_SettingsOption):
    __qualname__ = 'SettingsInputOption'

    def __init__(self, option_name, option_description, return_settings_window_function, initial_value, settings_dict, settings_dict_id, min_value=0, max_value=2147483647):
        super().__init__(option_name, option_description)
        self.return_settings_window_function = return_settings_window_function
        self.initial_value = initial_value
        self.min_value = min_value
        self.max_value = max_value
        self.settings_dict = settings_dict
        self.settings_dict_id = settings_dict_id

    def select_picker_row(self, picker_row_id):
        return TurboUIUtil.ObjectPickerDialog.ListPickerRow(picker_row_id, self.option_name, self.option_description, icon=get_action_icon())

    def select_callback(self):

        def _input_callback(dialog):
            if not TurboUIUtil.TextInputDialog.get_response_result(dialog):
                self.return_settings_window_function().open_window()
                return False
            try:
                dialog_output = int(TurboUIUtil.TextInputDialog.get_response_output(dialog))
                dialog_output = max(self.min_value, dialog_output)
                dialog_output = min(self.max_value, dialog_output)
                self.settings_dict[self.settings_dict_id] = dialog_output
            except ValueError:
                pass
            self.return_settings_window_function().open_window()
            return True

        display_text_input_dialog(text=self.option_description, title=self.option_name, initial_text=str(self.initial_value), callback=_input_callback)

