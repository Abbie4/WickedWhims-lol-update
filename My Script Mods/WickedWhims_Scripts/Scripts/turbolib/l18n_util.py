from protocolbuffers.Localization_pb2 import LocalizedString
from sims4.localization import LocalizationHelperTuning, _create_localized_string, create_tokens

class TurboL18NUtil:
    __qualname__ = 'TurboL18NUtil'

    @staticmethod
    def get_localized_string_from_text(text):
        return LocalizationHelperTuning.get_raw_text(text)

    @staticmethod
    def get_localized_string_from_stbl_id(text_id, tokens=()):
        return _create_localized_string(text_id, *tokens)

    @staticmethod
    def get_localized_string(object_value, tokens=()):
        if object_value is None:
            return TurboL18NUtil.get_localized_string(0)
        verified_tokens = list()
        for token in tokens:
            verified_tokens.append(TurboL18NUtil.get_localized_string(token))
        if isinstance(object_value, LocalizedString):
            create_tokens(object_value.tokens, verified_tokens)
            return object_value
        if isinstance(object_value, int):
            return TurboL18NUtil.get_localized_string_from_stbl_id(object_value, tokens=verified_tokens)
        if isinstance(object_value, str):
            return TurboL18NUtil.get_localized_string(TurboL18NUtil.get_localized_string_from_text(object_value), tokens=verified_tokens)
        if hasattr(object_value, 'populate_localization_token'):
            return object_value
        return TurboL18NUtil.get_localized_string(str(object_value), tokens=verified_tokens)

    @staticmethod
    def get_localized_string_id(localized_string):
        return localized_string.hash

