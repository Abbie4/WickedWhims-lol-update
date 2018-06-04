'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
import struct
from turbolib.hash_util import FNV
from turbolib.resource_util import TurboResourceUtil

def get_clip_resource_key(clip_name):
    return TurboResourceUtil.ResourceTypes.get_resource_key(TurboResourceUtil.ResourceTypes.CLIP, FNV.fnv64(clip_name))

def get_clip_bytes_data(clip_resource_key):
    return TurboResourceUtil.Resource.load_bytes(clip_resource_key)

def get_clip_duration(clip_bytes_data):
    if clip_bytes_data is None:
        return 0
    clip_bytes_data.seek(8)
    duration_float_bytes = clip_bytes_data.read(4)
    return struct.unpack('f', duration_float_bytes)[0]

