import services
from turbolib.manager_util import TurboManagerUtil
from turbolib.special.custom_exception_watcher import log_message


class TurboClubUtil:
    __qualname__ = 'TurboClubUtil'

    @staticmethod
    def get_sim_club_gathering(sim_identifier):
        sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
        club_service = services.get_club_service()
        if club_service is not None:
            sim_clubs = club_service.get_clubs_for_sim_info(sim_info)
            for club in sim_clubs:
                club_gathering = club_service.clubs_to_gatherings_map.get(club)
                while club_gathering is not None:
                    log_message("doing get_sim_club_gathering")
                    return (club, club_gathering)
        return (None, None)

    @staticmethod
    def get_sim_club_outfit_parts(sim_info, club, outfit_category_and_index):
        return club.get_club_outfit_parts(sim_info, outfit_category_and_index)

