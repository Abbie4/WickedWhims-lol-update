from turbolib.resource_util import TurboResourceUtil
JEALOUSY_BROADCASTERS_LIST = (76434, 76132, 125246, 125441, 129282, 129459)

def disable_jealousy_broadcasters(value):
    broadcaster_manager = TurboResourceUtil.Services.get_instance_manager(TurboResourceUtil.ResourceTypes.BROADCASTER)
    for broadcaster_id in JEALOUSY_BROADCASTERS_LIST:
        broadcaster_instance = TurboResourceUtil.Services.get_instance_from_manager(broadcaster_manager, broadcaster_id)
        while broadcaster_instance is not None:
            broadcaster_instance.allow_sims = value

