'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
import os
from turbolib.hash_util import FNV
from turbolib.maker.stbl import StblBuilder
STBL_STRINGS = [(2565953406, '--------------- Debug ---------------', None), (1984280090, 'Debug', None), (2814330362, 'Get Object Data (Debug)', None), (3941214168, 'General Debug Info', None), (458451588, 'Sex Debug Info', None), (3965772007, 'Nudity Debug Info', None), (3681543299, 'Underwear Matrix', None), (1090390374, 'Relationship Debug Info', None), (3305509093, 'Pregnancy Debug Info', None), (432183422, 'Temp Debug Info', None), (315554404, '--------------- End ---------------', None)]

def _save_stbl_files():
    if __name__ != '__main__':
        return
    stlb_builder = StblBuilder()
    for (string_hash, string, suffix) in STBL_STRINGS:
        string_hash = str(hex(string_hash))
        string_hash_prefix = string_hash[:2]
        string_hash_suffix = string_hash[2:].upper()
        string_hash_suffix = str('0'*(8 - len(string_hash_suffix))) + string_hash_suffix
        string_hash = string_hash_prefix + string_hash_suffix
        new_string_hash = _get_string_hash(string, suffix)
        if int(string_hash, 0) != int(new_string_hash, 0):
            print(string_hash + ' -> ' + new_string_hash + ': ' + string)
        stlb_builder.append(string, fnv=int(new_string_hash, 0))
    file_hash = '{}0242B3E0491836'
    lang_flags = ('00', '02', '03', '04', '05', '06', '07', '08', '0B', '0C', '0D', '0E', '0F', '11', '12', '13', '15')
    for lang_flag in lang_flags:
        file_lang_hash = file_hash.format(lang_flag)
        file_stream = open(os.path.join('D:\\\\TS4\\\\WickedWoohoo\\\\Tuning Files\\\\Debug\\\\STBL', 'S4_220557DA_80000000_' + file_lang_hash + '.stbl'), 'wb')
        file_stream.write(stlb_builder.get_bytes())
        file_stream.close()

def _get_string_hash(string, suffix):
    string = string.replace('\
', '')
    string_hash = 'WickedWhimsTurboDriver' + string + 'Debug'
    if suffix is not None:
        string_hash += suffix
    string_hash = str(hex(FNV.fnv32(string_hash)))
    string_hash_prefix = string_hash[:2]
    string_hash_suffix = string_hash[2:].upper()
    string_hash_suffix = str('0'*(8 - len(string_hash_suffix))) + string_hash_suffix
    return string_hash_prefix + string_hash_suffix

_save_stbl_files()
