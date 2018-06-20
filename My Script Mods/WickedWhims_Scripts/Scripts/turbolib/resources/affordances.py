'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
import services
from objects.script_object import ScriptObject
from services.terrain_service import TerrainService
from sims4.tuning.instance_manager import InstanceManager
from turbolib.events.core import has_game_loaded, register_zone_load_event_method
from turbolib.injector_util import inject
from turbolib.resource_util import TurboResourceUtil
from turbolib.special.custom_exception_watcher import log_custom_exception
AFFORDANCE_REGISTRATION_CLASSES = list()

def register_affordance_class():
    '''
    Use as a decorator on every AffordanceRegistration class to register it.
    '''

    def _wrapper(affordance_class):
        AFFORDANCE_REGISTRATION_CLASSES.append(affordance_class())
        return affordance_class

    return _wrapper


class AffordanceRegistration:
    __qualname__ = 'AffordanceRegistration'

    def __init__(self):
        self.affordences = list()

    def get_affordance_references(self):
        '''
        Should be overridden to return a collection of affordance ids.
        :return: tuple or list or set -> collection of affordance ids that will be injected
        '''
        raise NotImplementedError

    def get_social_mixer_references(self):
        '''
        This references collection is only used when is_social_mixer returns True.
        Should be overridden to return a collection of AffordanceList snippet ids.
        By default returns 'social_Mixers_Special_NonTouching' AffordanceList snippet id.
        :return: tuple -> social mixers that affordences will be injected to
        '''
        return (24513, 163715)

    def _get_affordance_instances(self):
        if self.affordences:
            return tuple(self.affordences)
        affordance_manager = TurboResourceUtil.Services.get_instance_manager(TurboResourceUtil.ResourceTypes.INTERACTION)
        for affordance_id in self.get_affordance_references():
            affordance_instance = TurboResourceUtil.Services.get_instance_from_manager(affordance_manager, affordance_id)
            if affordance_instance is None:
                pass
            self.affordences.append(affordance_instance)
        return tuple(self.affordences)

    def test_for_duplicates(self):
        '''
        Override this function and return if registered affordances should be tested for duplicates to avoid them existing multiple times in one object.
        :return: bool -> if affordances should be tested for duplicates
        '''
        return False

    def is_script_object(self, script_object):
        '''
        Override this function and return if passed script object should have the affordances injected.
        :param script_object: ScriptObject -> native instance of a script object being loaded to the game
        :return: bool -> if passed script objects should have the affordances injected
        '''
        return False

    def is_terrain(self):
        '''
        Override this function and return if affordances should be injected to the terrain object.
        :return: bool -> if affordences should be injected into the terrain object
        '''
        return False

    def is_social_mixer(self):
        '''
        Override this function and return if affordences should be injected as social mixers.
        Social mixers returned by get_social_mixer_references function will be used as targets to inject to.
        :return: bool -> if affordences should be injected as social mixers
        '''
        return False

    def is_sim_phone(self):
        '''
        Override this function and return if affordances should be injected to sim phones.
        Warning - is_script_object function should be only passing Sim instances or injection could fail
        :return: bool -> if affordences should be injected into sim phones
        '''
        return False

    def is_relationship_panel(self):
        '''
        Override this function and return if affordances should be injected to sim relationship panel.
        Warning - is_script_object function should be only passing Sim instances or injection could fail
        :return: bool -> if affordences should be injected into sim relationship panel
        '''
        return False


@register_zone_load_event_method(unique_id='WickedWhims', priority=-1, late=True)
def _turbolib_add_affordances_to_terrain():
    if has_game_loaded():
        return
    try:
        terrain_object = TerrainService.TERRAIN_DEFINITION.cls
        affordances_list = list()
        for affordance_registration in AFFORDANCE_REGISTRATION_CLASSES:
            try:
                while affordance_registration.is_terrain():
                    if affordance_registration.test_for_duplicates():
                        existing_affordances = tuple(terrain_object._super_affordances)
                        for affordance_instance in affordance_registration._get_affordance_instances():
                            if affordance_instance in existing_affordances:
                                pass
                            affordances_list.append(affordance_instance)
                    else:
                        affordances_list += affordance_registration._get_affordance_instances()
            except Exception as ex:
                log_custom_exception("[TurboLib] Failed to run 'AffordanceRegistration' class at 'TerrainService.TERRAIN_DEFINITION._super_affordances'.", ex)
        TerrainService.TERRAIN_DEFINITION.set_class(terrain_object)
        services.terrain_service.destroy_terrain_object()
        services.terrain_service.create_terrain_object()
    except Exception as ex:
        log_custom_exception("[TurboLib] Failed to run 'AffordanceRegistration' class at affordances injection to the Terrain object.", ex)


@inject(ScriptObject, 'on_add')
def _turbolib_add_affordances_to_script_objects(original, self, *args, **kwargs):
    result = original(self, *args, **kwargs)
    for affordance_registration in AFFORDANCE_REGISTRATION_CLASSES:
        try:
            if affordance_registration.is_social_mixer():
                continue
            if affordance_registration.is_terrain():
                continue
            if not affordance_registration.is_script_object(self):
                continue
            if affordance_registration.is_sim_phone() and hasattr(self, '_phone_affordances'):
                affordances_list = list()
                if affordance_registration.test_for_duplicates():
                    existing_affordances = tuple(self._phone_affordances)
                    for affordance_instance in affordance_registration._get_affordance_instances():
                        if affordance_instance in existing_affordances:
                            pass
                        affordances_list.append(affordance_instance)
                else:
                    affordances_list += affordance_registration._get_affordance_instances()
            elif affordance_registration.is_relationship_panel() and hasattr(self, '_relation_panel_affordances'):
                affordances_list = list()
                if affordance_registration.test_for_duplicates():
                    existing_affordances = tuple(self._relation_panel_affordances)
                    for affordance_instance in affordance_registration._get_affordance_instances():
                        if affordance_instance in existing_affordances:
                            pass
                        affordances_list.append(affordance_instance)
                else:
                    affordances_list += affordance_registration._get_affordance_instances()
            else:
                while hasattr(self, '_super_affordances'):
                    affordances_list = list()
                    if affordance_registration.test_for_duplicates():
                        existing_affordances = tuple(self._super_affordances)
                        for affordance_instance in affordance_registration._get_affordance_instances():
                            if affordance_instance in existing_affordances:
                                pass
                            affordances_list.append(affordance_instance)
                    else:
                        affordances_list += affordance_registration._get_affordance_instances()
        except Exception as ex:
            log_custom_exception("[TurboLib] Failed to run 'AffordanceRegistration' class at 'ScriptObject.on_add'.", ex)
    return result


@inject(InstanceManager, 'load_data_into_class_instances')
def _turbolib_add_affordances_to_social_mixer_affordance_list_snippets(original, self, *args, **kwargs):
    result = original(self, *args, **kwargs)
    if self.TYPE != TurboResourceUtil.ResourceTypes.SNIPPET:
        return result
    for affordance_registration in AFFORDANCE_REGISTRATION_CLASSES:
        try:
            if not affordance_registration.is_social_mixer():
                continue
            for social_mixer_affordance_list_id in affordance_registration.get_social_mixer_references():
                affordance_list_instance = self._tuned_classes.get(TurboResourceUtil.ResourceTypes.get_resource_key(TurboResourceUtil.ResourceTypes.SNIPPET, social_mixer_affordance_list_id))
                if affordance_list_instance is None:
                    pass
                affordances_list = list()
                if affordance_registration.test_for_duplicates():
                    existing_affordances = tuple(affordance_list_instance.value)
                    for affordance_instance in affordance_registration._get_affordance_instances():
                        if affordance_instance in existing_affordances:
                            pass
                        affordances_list.append(affordance_instance)
                else:
                    affordances_list += affordance_registration._get_affordance_instances()
        except Exception as ex:
            log_custom_exception("[TurboLib] Failed to run 'AffordanceRegistration' class at 'InstanceManager.load_data_into_class_instances'.", ex)
    return result

