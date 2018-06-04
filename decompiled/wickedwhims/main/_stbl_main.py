'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
import os
from turbolib.hash_util import FNV
from turbolib.maker.stbl import StblBuilder
STBL_STRINGS = [(1898650086, '--------------- Main ---------------', None), (4150871865, 'Wicked', 'Main'), (4037785225, 'Congratulations!\\\
WickedWhims {0.String} has been installed!\\\
\\\
If this is not your first time, some data has been set to default. No worries, this is a standard procedure.\\\
\\\
Everything should be working without any problems.', None), (337204630, '--------------- Warnings ---------------', None), (953840858, 'Warning!', None), (3371966942, "Failed to load parts of WickedWhims save data!\\\
\\\
Default data was used instead.\\\
\\\
Saving the game should override incorrect data and fix the issue.\\\
Removing 'WickedWhimsMod' folder from 'saves' folder can help too.", None), (2149295956, 'Failed to load CAS Parts Config File (ww_cas_parts.json).\\\
\\\
Default configuration is used instead.', None), (491667006, "An error has occurred!\\\
An exception file (lastException.txt) has been created!\\\
\\\
Take a deep breath, create a new save, and exit the game.\\\
\\\
The most common reason for errors like these are outdated/broken mods.\\\
Consider reviewing your 'Mods' folder and updating/removing old mods.\\\
\\\
Exception files location: {0.String}\\\
\\\
This message is brought to you by TURBODRIVER.\\\
You can find more information at:\\\
wickedwhimsmod.com/exception", None), (2599945466, '--------------- Settings ---------------', None), (2836913304, 'Settings', None), (137933503, 'WickedWhims Settings', None), (3283606570, 'Headline Effects Settings', None), (3906855187, 'Change headline effects visibility.', None), (366188754, 'Enable Headline Effects', None), (4060605351, 'Visible headline effects and plumbob', None), (2403236729, 'Disable Headline Effects', None), (1479275710, 'Invisible headline effects and plumbob', None), (3921925930, 'More Information', None), (1456337762, 'Information about this modification.', None), (3349884559, 'Do you want to visit WickedWhims website? (https://wickedwhimsmod.com/)\\\
\\\
This will open your web browser!', None), (2009293922, '--------------- Settings Import/Export ---------------', None), (237356084, 'Settings Import/Export', None), (2464205507, 'Import/Export WickedWhims settings and disabled animations.', None), (128859011, 'Export Current Settings', None), (1330537389, 'Save current settings and disabled animations for use in different worlds.', None), (2187363841, 'Enter the name of this save:', None), (3705925691, "Your settings have been saved under the name '{0.String}'.\\\
\\\
They can be loaded using the 'Import Settings' menu.", None), (3126397785, 'Import Settings', None), (543237095, 'Load saved settings and disabled animations.', None), (4228795842, 'You need to export settings first to load them later!', None), (3165307094, 'Settings under the name {0.String} have been loaded.\\\
\\\
Make sure to save and restart the game for the loaded settings to take full effect.', None), (4268061051, 'Delete Settings', None), (645194174, 'Delete saved settings and disabled animations.', None), (294911225, 'You need to export settings first to delete them!', None), (3421488172, 'Settings under the name {0.String} have been deleted.', None), (2878507029, 'Created at: {0.String}', None), (342812316, '--------------- Statistics ---------------', None), (3778116009, 'Global Statistics', None), (2093939627, 'Sex Statistics\\\
   _STAT_: {10.String}\\\
   _STAT_: {11.String}\\\
   _STAT_: {12.String}\\\
   _STAT_: {13.String}\\\
   _STAT_: {14.String}\\\
   _STAT_: {15.String}\\\
   _STAT_: {16.String}\\\
   _STAT_: {17.String}\\\
   _STAT_: {18.String}\\\
   _STAT_: {19.String}\\\
\\\
Exhibitionism Statistics\\\
   _STAT_: {30.String}\\\
   _STAT_: {31.String}\\\
   _STAT_: {32.String}\\\
   _STAT_: {33.String}\\\
   _STAT_: {34.String}\\\
   _STAT_: {35.String}\\\
   _STAT_: {36.String}\\\
   _STAT_: {37.String}\\\
   _STAT_: {38.String}\\\
   _STAT_: {39.String}\\\
\\\
Other Statistics\\\
   _STAT_: {50.String}\\\
   _STAT_: {51.String}\\\
   _STAT_: {52.String}\\\
   _STAT_: {53.String}\\\
   _STAT_: {54.String}\\\
   _STAT_: {55.String}\\\
   _STAT_: {56.String}\\\
   _STAT_: {57.String}\\\
   _STAT_: {58.String}\\\
   _STAT_: {59.String}\\\
', None), (1150191385, 'Sim Statistics', None), (1561155736, '{0.SimFirstName} {0.SimLastName} Statistics', None), (863853338, 'Sex Statistics\\\
  \u2517 Times Had Sex: {10.String}\\\
     \u2517 (Incest: {11.String}%)\\\
  \u2517 Times Masturbated: {12.String}\\\
  \u2517 Has Been Seen In Sex: {13.String}\\\
  \u2517 Reacted To Sex: {14.String}\\\
  \u2517 Asked For Sex: {15.String}\\\
     \u2517 (Accepted: {16.String}%, Rejected: {17.String}%)\\\
  \u2517 Time Spent In Sex: {21.String} hour(s)\\\
    \u2517 (Teasing: {22.String}%, Handjob: {23.String}%,\\\
          Footjob: {24.String}%, Oraljob: {25.String}%,\\\
          Vaginal: {26.String}%, Anal: {27.String}%,\\\
          Climax: {28.String}%)\\\
  \u2517 Unique Sex Partners: {30.String}\\\
     \u2517 (Child: {31.String}%, Teen: {32.String}%,\\\
           Young Adult: {33.String}%, Adult: {34.String}%),\\\
           Elder: {34.String}%\\\
  \u2517 Times Received Cum: {40.String}\\\
     \u2517 (Face: {41.String}%, Chest: {42.String}%, Back: {43.String}%,\\\
           Vagina: {44.String}%, Butt: {45.String}%, Feet: {46.String}%)\\\
\\\
Nudity Statistics\\\
  \u2517 Time Spent Nude: {50.String} hour(s)\\\
  \u2517 Has Been Seen Nude: {51.String}\\\
  \u2517 Reacted To Nudity: {52.String}\\\
  \u2517 Times Talked About Nudity: {53.String}\\\
  \u2517 Flashed Someone: {60.String}\\\
     \u2517 (Top: {61.String}%, Bottom: {62.String}%, Full: {63.String}%)\\\
\\\
Other Statistics\\\
  \u2517 Times Impregnated: {100.String}\\\
  \u2517 Times Got Pregnant: {101.String}\\\
  \u2517 Times Terminated Pregnancy: {102.String}\\\
  \u2517 Times Used Contraception: {103.String}\\\
', None), (438802134, '--------------- Welcome Message ---------------', None), (2433468877, "{0.String}\\\
\\\
You're running version:\\\
{1.String}\\\
\\\
Loaded {2.String} animations by {3.String}.\\\
\\\
WickedWhims by TURBODRIVER.\\\
\\\
Custom Content by Noir.\\\
https://www.patreon.com/noiranddark\\\
\\\
Logo and Custom Content by Luumia.\\\
http://luumiasims.com\\\
\\\
Key Contribution by Mike24, Azmodan22, Denton47, autobanned, PhaseLotA, Wyatt, Redabyss, biondosim and ZoahcX.\\\
https://www.patreon.com/mike24\\\
https://www.patreon.com/azmodan22\\\
https://twitter.com/PhaseLotA\\\
http://wyattssims.tumblr.com\\\
\\\
WickedWhims is provided under the terms of CC BY-NC-ND 4.0 public license.", None), (2039141334, 'Hello!', None), (2218897178, 'Hallo!', None), (4271772397, 'Ol\xe1!', None), (370121153, '\xa1Hola!', None), (586158561, 'Hej!', None), (790896663, 'Aloha!', None), (1213235168, 'Saluto!', None), (4108001505, '\u4eca\u65e5\u306f', None), (2704450329, '\u4f60\u597d', None), (756630283, '\uc548\ub155', None), (3828663345, 'Bonjour!', None), (1988030031, '\u0412\u0456\u0442\u0430\u044e!', None), (3829989166, 'Ahoj!', None), (3162323884, '\u0417\u0434\u0440\u0430\u0432\u0441\u0442\u0432\u0443\u0439\u0442\u0435!', None), (3658047458, 'Ciao!', None), (1430591040, 'Hai!', None), (2867073748, 'Hei!', None), (1349634794, 'Oi!', None), (1800227724, '--------------- End ---------------', None)]

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
    file_hash = '{}5A06555ADD92B1'
    lang_flags = ('00', '02', '03', '04', '05', '06', '07', '08', '0B', '0C', '0D', '0E', '0F', '11', '12', '13', '15')
    for lang_flag in lang_flags:
        file_lang_hash = file_hash.format(lang_flag)
        file_stream = open(os.path.join('D:\\\\TS4\\\\WickedWoohoo\\\\Tuning Files\\\\Main\\\\STBL', 'S4_220557DA_80000000_' + file_lang_hash + '.stbl'), 'wb')
        file_stream.write(stlb_builder.get_bytes())
        file_stream.close()

def _get_string_hash(string, suffix):
    string = string.replace('\
', '')
    string_hash = 'WickedWhimsTurboDriver' + string + 'Main'
    if suffix is not None:
        string_hash += suffix
    string_hash = str(hex(FNV.fnv32(string_hash)))
    string_hash_prefix = string_hash[:2]
    string_hash_suffix = string_hash[2:].upper()
    string_hash_suffix = str('0'*(8 - len(string_hash_suffix))) + string_hash_suffix
    return string_hash_prefix + string_hash_suffix

_save_stbl_files()
