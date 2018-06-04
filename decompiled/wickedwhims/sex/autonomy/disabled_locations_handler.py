'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from wickedwhims.utils_saves.save_disabled_locations import update_disabled_locations_save_data
DISABLED_AUTONOMY_SEX_LOCATIONS_IDS = set()

def apply_disabled_autonomy_sex_locations_from_dict(disabled_locations_dict):
    global DISABLED_AUTONOMY_SEX_LOCATIONS_IDS
    if 'disabled_locations' in disabled_locations_dict:
        DISABLED_AUTONOMY_SEX_LOCATIONS_IDS = set(disabled_locations_dict.get('disabled_locations', set()))

def update_disabled_sex_locations_data():
    disabled_locations_dict = dict()
    disabled_locations_dict['disabled_locations'] = list(DISABLED_AUTONOMY_SEX_LOCATIONS_IDS)
    update_disabled_locations_save_data(disabled_locations_dict)

def get_disabled_autonomy_sex_locations():
    return DISABLED_AUTONOMY_SEX_LOCATIONS_IDS

def is_autonomy_sex_locations_disabled(location_id):
    if location_id == -1:
        return False
    return location_id in DISABLED_AUTONOMY_SEX_LOCATIONS_IDS

def switch_autonomy_sex_disabled_location(location_id):
    if location_id == -1:
        return
    if location_id not in DISABLED_AUTONOMY_SEX_LOCATIONS_IDS:
        DISABLED_AUTONOMY_SEX_LOCATIONS_IDS.add(location_id)
    else:
        DISABLED_AUTONOMY_SEX_LOCATIONS_IDS.remove(location_id)

