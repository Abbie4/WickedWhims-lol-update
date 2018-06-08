import services
from objects import ALL_HIDDEN_REASONS
from sims.sim import Sim
from sims.sim_info import SimInfo
from sims.sim_info_base_wrapper import SimInfoBaseWrapper
from sims.sim_info_types import Species


class TurboManagerUtil:
    __qualname__ = 'TurboManagerUtil'

    class Sim:
        __qualname__ = 'TurboManagerUtil.Sim'
        __doc__ = '\n        Utilities to manage Sims instances.\n        '

        @staticmethod
        def get_sim_id(sim_identifier):
            '''
            Returns passed sim instance id.
            :param sim_identifier: int or SimInfo or Sim -> sim identifier
            :return: int -> sim id or 0 if sim doesn't exist
            '''
            if isinstance(sim_identifier, int):
                return sim_identifier
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier, allow_base_wrapper=True)
            if sim_info is None:
                return 0
            return sim_info.id

        @staticmethod
        def get_sim_info(sim_instance_or_sim_id, allow_base_wrapper=False):
            '''
            Returns SimInfo instance.
            SimInfo instance contains all of the information about a sim.
            :param sim_instance_or_sim_id: int or Sim or SimInfoBaseWrapper** -> sim identifier / **if allow_base_wrapper is True
            :param allow_base_wrapper: bool -> if SimInfoBaseWrapper instance is allowed to be returned
            :return: SimInfo -> native SimInfo instance or None if SimInfo instance can't be found
            '''
            if sim_instance_or_sim_id is None:
                return
            if isinstance(sim_instance_or_sim_id, SimInfo):
                return sim_instance_or_sim_id
            if isinstance(sim_instance_or_sim_id, Sim):
                return sim_instance_or_sim_id.sim_info
            if isinstance(sim_instance_or_sim_id, int):
                return services.sim_info_manager().get(sim_instance_or_sim_id)
            if allow_base_wrapper is True and isinstance(sim_instance_or_sim_id, SimInfoBaseWrapper):
                return sim_instance_or_sim_id

        @staticmethod
        def get_sim_info_with_name(sim_first_name, sim_last_name):
            '''
            Returns SimInfo instance.
            SimInfo instance contains all of the information about a sim.
            :param sim_first_name: string -> sim first name
            :param sim_last_name: string -> sim last name
            :return: SimInfo -> native SimInfo instance or None if sim doesn't exist
            '''
            return services.sim_info_manager().get_sim_info_by_name(sim_first_name, sim_last_name)

        @staticmethod
        def get_all_sim_info_gen(humans=True, pets=True):
            '''
            Returns all SimInfo instances as a generator.
            The reason to use a generator is to avoid users directly using the returned native dict_values of an indexing manager.
            :param humans: bool -> if the returned SimInfo instances are allowed to be human
            :param pets: bool -> if the returned SimInfo instances are allowed to be cats and dogs
            :return: SimInfo* -> generator* of all existing sims SimInfo instances
            '''
            for sim_info in services.sim_info_manager().get_all():
                if sim_info is None:
                    pass
                if humans is False and sim_info.species == Species.HUMAN:
                    pass
                if pets is False and sim_info.species != Species.HUMAN:
                    pass
                yield sim_info

        @staticmethod
        def get_sim_instance(sim_info_or_sim_id):
            '''
            Returns Sim instance.
            Sim instance is an object in the game world that represents a sim.
            Warning - Sim instance object is returned as weakref. Do not keep it in memory for future reference.
            :param sim_info_or_sim_id: int or SimInfo -> sim identifier
            :return: Sim -> native Sim instance or None if Sim instance object doesn't currently exist in the game world
            '''
            if sim_info_or_sim_id is None:
                return
            if isinstance(sim_info_or_sim_id, Sim):
                return sim_info_or_sim_id
            if isinstance(sim_info_or_sim_id, SimInfo):
                return sim_info_or_sim_id.get_sim_instance(allow_hidden_flags=ALL_HIDDEN_REASONS)
            if isinstance(sim_info_or_sim_id, SimInfoBaseWrapper):
                return TurboManagerUtil.Sim.get_sim_instance(sim_info_or_sim_id.id)
            if isinstance(sim_info_or_sim_id, int):
                sim_info = services.sim_info_manager().get(sim_info_or_sim_id)
                if sim_info is not None:
                    return TurboManagerUtil.Sim.get_sim_instance(sim_info)

        @staticmethod
        def get_all_sim_instance_gen(humans=True, pets=True):
            '''
            Returns all Sim instances as a generator.
            SimInfo generator is used to get Sim instances since it's more efficient to get through 100-200 Sims rather than 1000-5000 objects.
            :param humans: bool -> if the returned SimInfo instances are allowed to be human
            :param pets: bool -> if the returned SimInfo instances are allowed to be cats and dogs
            :return: Sim* -> generator* of existing sims Sim instances
            '''
            for sim_info in TurboManagerUtil.Sim.get_all_sim_info_gen(humans=humans, pets=pets):
                sim = TurboManagerUtil.Sim.get_sim_instance(sim_info)
                if sim is None:
                    pass
                yield sim

        @staticmethod
        def get_active_sim():
            '''
            Returns current active Sim instance.
            :return: Sim -> current active Sim instance or None if current game client is invalid
            '''
            client = services.client_manager().get_first_client()
            if client is not None:
                return client.active_sim

        @staticmethod
        def remove_sim_info(sim_identifier, household=None):
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
            sim_info.remove_permanently(household=household)

