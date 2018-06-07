'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''import osfrom turbolib.hash_util import FNVfrom turbolib.maker.stbl import StblBuilderSTBL_STRINGS = [(1550681791, '--------- Settings ---------', None), (3341159695, 'Relationship Settings', None), (1970181669, 'Change relationship settings.\\n\\nThese settings affect the base game mechanics like age restrictions, gender preferences, incest, polygamy or jealousy).', None), (926615894, 'This option requires restarting the game to take full effect!\\n\\nSave and restart for this setting to work.', None), (3579577312, 'Romance Age Restrictions Settings', None), (689435193, 'Allow/Disallow romance interactions for all ages.\\n\\n(from Teen to Elder)', None), (1972153895, 'Allow All Ages Romance', None), (1840687547, 'Disallow All Ages Romance', None), (2064322478, 'Polyamory Relationships Settings', None), (606279529, 'Allow/Disallow polyamory and polygamy relationships.', None), (3487178965, 'Allow Polyamory/Polygamy Relationships', None), (4221398665, 'Disallow Polyamory/Polygamy Relationships', None), (3857402476, 'Global Jealousy Cheat', None), (4022532503, 'Enable/Disable jealousy of relationships globally.\\n\\nUse the Polyamorous reward trait for individual Sims.', None), (584740058, 'Use the Polyamorous reward trait for individual Sims.\\n\\nReward traits can be found in the Rewards Store for Sims.', None), (1836796321, 'Enable Jealousy', None), (1388686066, 'Disable Jealousy', None), (3799781904, 'Global Incest Cheat', None), (3384770454, 'Enable/Disable incest relationships globally.\\n\\nUse the Incest reward trait for individual Sims.', None), (1417105284, 'Use the Incest reward trait for individual Sims.\\n\\nReward traits can be found in the Rewards Store for Sims.', None), (1836994860, 'Enable Incest Relationships', None), (3076268239, 'Disable Incest Relationships', None), (3375076639, '--------- Interactions ---------', None), (941052129, 'Talk about Fantasies', None), (1457567534, 'Talk about Fantasies with {1.SimFirstName}', None), (3448134335, '--------- Traits ---------', None), (1160291068, 'Polyamorous', None), (3495199535, 'Polyamorous', 'gender_neutral'), (48237703, "These Sims are open to having multiple romantic or sexual committed relationships and don't get jealous about their loved ones having more than one partner.", None), (2914855909, '--------- End ---------', None)]
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
    file_hash = '{}00E8D0AC1B9A96'
    lang_flags = ('00', '02', '03', '04', '05', '06', '07', '08', '0B', '0C', '0D', '0E', '0F', '11', '12', '13', '15')
    for lang_flag in lang_flags:
        file_lang_hash = file_hash.format(lang_flag)
        file_stream = open(os.path.join('D:\\TS4\\WickedWoohoo\\Tuning Files\\Relationships\\STBL', 'S4_220557DA_80000000_' + file_lang_hash + '.stbl'), 'wb')
        file_stream.write(stlb_builder.get_bytes())
        file_stream.close()

def _get_string_hash(string, suffix):
    string = string.replace('\n', '')
    string_hash = 'WickedWhimsTurboDriver' + string + 'Relationship'
    if suffix is not None:
        string_hash += suffix
    string_hash = str(hex(FNV.fnv32(string_hash)))
    string_hash_prefix = string_hash[:2]
    string_hash_suffix = string_hash[2:].upper()
    string_hash_suffix = str('0'*(8 - len(string_hash_suffix))) + string_hash_suffix
    return string_hash_prefix + string_hash_suffix
_save_stbl_files()