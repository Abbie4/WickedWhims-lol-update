'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
import os
from turbolib.events.core_tick import register_zone_update_event_method, unregister_zone_update_event_method
from wickedwhims.sex.animations.animations_handler import get_available_sex_animations

@register_zone_update_event_method(unique_id='WickedWhims', always_run=True)
def _wickedwhims_create_animations_report_file():
    create_animations_report_file()
    unregister_zone_update_event_method('_wickedwhims_create_animations_report_file', unique_id='WickedWhims')

def create_animations_report_file():
    file_path = _get_animations_report_file_path()
    if os.path.isfile(file_path):
        os.remove(file_path)
    log_file = open(file_path, 'a', buffering=1, encoding='utf-8')
    animations_list = get_available_sex_animations()
    log_file.write('---------------------------------\
')
    log_file.write('Animations Count: ' + str(len(animations_list)) + '\
')
    log_file.write('---------------------------------\
\
\
')
    for animation in animations_list:
        log_file.write('Author: ' + str(animation.get_author()) + '\
')
        log_file.write('Name: ' + str(animation.get_display_name(string_hash=True)) + '\
')
        log_file.write('Stage Name: ' + str(animation.get_stage_name()) + '\
')
        log_file.write('Sex Category: ' + str(animation.get_sex_category().name) + '\
')
        log_file.write('Locations: ' + str(', '.join([str(location) for location in animation.get_locations()])) + '\
')
        log_file.write('Custom Locations: ' + str(', '.join([str(location) for location in animation.get_custom_locations()])) + '\
')
        log_file.write('Duration (loop): ' + str(animation.get_duration()) + ' (' + str(animation.get_single_loop_duration()) + ')' + '\
')
        log_file.write('Actors Count: ' + str(len(animation.get_actors())) + '\
')
        log_file.write('Actors Genders: ' + str('+'.join([str(actor.gender_type.name) for actor in animation.get_actors()])) + '\
')
        log_file.write('\
')
    log_file.flush()

def _get_animations_report_file_path():
    root_dir = ''
    root_file = os.path.normpath(os.path.dirname(os.path.realpath(__file__))).replace(os.sep, '/')
    root_file_split = root_file.split('/')
    exit_index = -1
    for i in range(len(root_file_split)):
        split_part = root_file_split[i]
        while split_part.endswith('.ts4script'):
            exit_index = len(root_file_split) - i
            break
    if exit_index == -1:
        return
    for index in range(0, len(root_file_split) - exit_index):
        root_dir += str(root_file_split[index]) + '/'
    return root_dir + 'WW_Installed_Animations.txt'

