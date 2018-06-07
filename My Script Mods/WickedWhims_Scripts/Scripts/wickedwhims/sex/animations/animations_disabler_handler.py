'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''from wickedwhims.utils_saves.save_disabled_animations import update_disabled_animations_save_dataDISABLED_PLAYER_ANIMATIONS_IDS = set()DISABLED_AUTONOMY_ANIMATIONS_IDS = set()
def apply_disabled_sex_animations_from_dict(disabled_animations_dict):
    global DISABLED_PLAYER_ANIMATIONS_IDS, DISABLED_AUTONOMY_ANIMATIONS_IDS
    if 'disabled_animations' in disabled_animations_dict:
        DISABLED_PLAYER_ANIMATIONS_IDS = set(disabled_animations_dict.get('disabled_animations', set()))
    if 'autonomy_disabled_animations' in disabled_animations_dict:
        DISABLED_AUTONOMY_ANIMATIONS_IDS = set(disabled_animations_dict.get('autonomy_disabled_animations', set()))

def update_disabled_sex_animation_data():
    disabled_animations_dict = dict()
    disabled_animations_dict['disabled_animations'] = list(DISABLED_PLAYER_ANIMATIONS_IDS)
    disabled_animations_dict['autonomy_disabled_animations'] = list(DISABLED_AUTONOMY_ANIMATIONS_IDS)
    update_disabled_animations_save_data(disabled_animations_dict)

def get_disabled_sex_animation(autonomy=False):
    if autonomy is True:
        return get_autonomy_disabled_sex_animations()
    return get_player_disabled_sex_animations()

def is_sex_animation_disabled(animation_identifier, autonomy=False):
    if autonomy is True:
        return is_autonomy_sex_animation_disabled(animation_identifier)
    return is_player_sex_animation_disabled(animation_identifier)

def switch_disabled_sex_animation(animation_identifier, autonomy=False):
    if autonomy is True:
        return switch_autonomy_disabled_sex_animation(animation_identifier)
    return switch_player_disabled_sex_animation(animation_identifier)

def get_player_disabled_sex_animations():
    return DISABLED_PLAYER_ANIMATIONS_IDS

def is_player_sex_animation_disabled(animation_identifier):
    return animation_identifier in DISABLED_PLAYER_ANIMATIONS_IDS

def switch_player_disabled_sex_animation(animation_identifier):
    if animation_identifier not in DISABLED_PLAYER_ANIMATIONS_IDS:
        DISABLED_PLAYER_ANIMATIONS_IDS.add(animation_identifier)
    else:
        DISABLED_PLAYER_ANIMATIONS_IDS.remove(animation_identifier)

def get_autonomy_disabled_sex_animations():
    return DISABLED_AUTONOMY_ANIMATIONS_IDS

def is_autonomy_sex_animation_disabled(animation_identifier):
    return animation_identifier in DISABLED_AUTONOMY_ANIMATIONS_IDS

def switch_autonomy_disabled_sex_animation(animation_identifier):
    if animation_identifier not in DISABLED_AUTONOMY_ANIMATIONS_IDS:
        DISABLED_AUTONOMY_ANIMATIONS_IDS.add(animation_identifier)
    else:
        DISABLED_AUTONOMY_ANIMATIONS_IDS.remove(animation_identifier)
