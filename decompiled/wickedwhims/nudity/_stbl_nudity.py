'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
import os
from turbolib.hash_util import FNV
from turbolib.maker.stbl import StblBuilder
STBL_STRINGS = [(1747830950, '---------- Settings ----------', None), (3482616025, 'Nudity Settings', None), (1935908617, 'Change nudity settings.\\\
\\\
These settings affect most of nudity/undressing functions.', None), (453629989, 'Naturism and Exhibitionism Switch', None), (3027443619, 'Enable/Disable nudity skills, nudity autonomy, and nudity story progression.', None), (1578351482, 'Underwear Switch', None), (2573526312, 'Enable/Disable if Sims use underwear and are able to undress to underwear.', None), (1926714507, 'Outfit Settings', None), (3432297298, 'Change outfit undressing behavior.', None), (692689912, 'Complete Undressing Type', None), (3042534075, 'Choose a type of how complete undressing should work.', None), (1221347836, 'Default', None), (1256816785, 'Sim bathing outfit with auto fixing will be used for undressing.', None), (2744873298, 'Special', None), (1134862513, 'Sim current outfit will be used as the base for undressing.', None), (2858014063, 'Auto Undress Gloves with Top', None), (119403953, 'Gloves will be undressed with the top part of Sim outfit.', None), (950164393, 'Auto Undress Shoes with Bottom', None), (2917956641, 'Shoes will be undressed with the bottom part of Sim outfit.', None), (2384648499, 'Auto Undress Socks with Shoes', None), (2997894284, 'Socks will be undressed with shoes.', None), (3473641235, 'Auto Undress Leggings with Bottom', None), (2662606901, 'Leggings will be undressed with the bottom part of Sim outfit.', None), (3279709928, 'Notifications Settings', None), (2777387879, 'Enable/Disable nudity related notifications.', None), (1049993247, 'Notifications Visibility Type', None), (3978784152, 'Choose a type of notifications visibility.', None), (674810031, 'Disable Notifications', None), (3883147319, 'No notifications about nudity actions will be displayed.', None), (3818596707, 'Only Autonomy Notifications', None), (4274135008, 'Only notifications about autonomy nudity actions will be displayed.', None), (1487120885, 'Show All Notifications', None), (1289690659, 'All notifications about nudity actions will be displayed.', None), (2284366757, 'Notifications Household Limit Switch', None), (2211369900, 'Enable/Disable if nudity notifications should be displayed only about household Sims.', None), (2952085198, 'Autonomy Settings', None), (4065078282, 'Change nudity autonomy related settings.', None), (273010132, 'Autonomy Level Settings', None), (3506801424, 'Choose a level of autonomy.', None), (10295473, 'Disable Autonomy', None), (3946683557, 'Sims will not attempt autonomy nudity activities.', None), (933284298, 'NPC Only Autonomy', None), (324302165, 'Only NPC Sims will attempt autonomy nudity activities.', None), (3903945432, 'Full Autonomy', None), (4227951371, 'All Sims will attempt autonomy nudity activities.', None), (2601174900, 'Interaction Undressing Autonomy Settings', None), (1342392999, 'Choose a type of interaction undressing autonomy.\\\
\\\
Specific undressing interactions (like changing to sleep or changing for workout) are affected with possibility of undressing to nude.', None), (469378371, 'Disable Interaction Undressing Autonomy', None), (1366608659, 'Sims will not try to get naked for undressing interactions.', None), (2783019522, 'Random Interaction Undressing Autonomy', None), (3623010176, 'Sims will randomly (based on skill level) decide if they want to get naked for undressing interactions.', None), (1795801803, 'Constant Interaction Undressing Autonomy', None), (2851490907, 'Sims will always get naked for undressing interactions.', None), (1581732742, 'Story Progression Settings', None), (1949040668, 'Change nudity story progression related settings.', None), (2988386393, 'Story Progression Switch', None), (787091191, 'Enable/Disable nudity story progression.\\\
\\\
Sims will learn secrets of living without clothes on while they are not around.', None), (3347767978, 'Other Settings', None), (3482441299, 'Change all of the unrelated settings.', None), (4036248285, 'Teens Nudity Switch', None), (1543833768, 'Enable/Disable if teens can use nudity interactions.', None), (1224818283, 'Nudity Assurance Switch', None), (3312839120, 'Enable/Disable nudity body parts assurance system.', None), (1521332630, 'Toilet Undressing Switch', None), (2094981913, 'Enable/Disable if Sims will undress bottom when using a toilet.', None), (3872449146, 'Breast Feeding Undressing Switch', None), (2574151234, 'Enable/Disable if Sims will undress top when breast feeding.', None), (3316653451, 'Cheats', None), (1790619680, 'Change things that you find annoying.', None), (2493503338, 'Nudity Privacy Switch', None), (2379427991, 'Enable/Disable if Sims will respect nudity privacy.', None), (3276318383, 'Nudity Reaction Switch', None), (3542627219, 'Enable/Disable if Sims will react to nudity.', None), (606517051, '---------- Penis Settings ----------', None), (253781263, 'Penis Settings', None), (2898758693, 'Change Sim Soft Penis', None), (1072923186, 'Change Sim Hard Penis', None), (2966523311, 'Change All Sims Soft Penis', None), (4002037116, 'Change All Sims Hard Penis', None), (277158998, 'Sim Soft Penis Selector', None), (1516569631, 'Sim Hard Penis Selector', None), (1952075710, 'Randomize All Sims Penis', None), (1490222904, '(without default penis)', None), (776669783, 'Author: {0.String}', None), (4150646019, '---------- General ----------', None), (3145721892, 'Nudity', 'General'), (4111426025, 'Exhibitionism', 'General'), (3476801842, 'Naturism', 'General'), (1289216189, '---------- Skills ----------', None), (678383997, 'Naturism', 'Skill'), (1629757612, 'Take off your clothes and discover the wonderful world of Naturism!', None), (150937530, 'The thought of nudity is scarier than nudity itself.\\\
\\\
The more you stay naked, the more confidence you gain.\\\
Performing interactions naked lowers the amount of lost hygiene.\\\
\\\
Start by changing into more revealing outfits (sleepwear, swimwear or underwear) or admiring your body in mirrors.', None), (2576418542, 'Acquired the Naturism Skill', None), (3214981689, "{0.SimFirstName}'s new Naturism skill will allow {M0.him}{F0.her} to perform various nudity related activities. As the skill level increases, more will be possible.\\\
Get into your underwear, sleepwear or swimwear outfit and try to get more comfortable around others.", None), (3118202268, 'Reached Naturism Level 2', None), (621368757, "{0.SimFirstName} is now much more comfortable with nudity! Getting naked outside shouldn't be a big problem anymore.", None), (3638291081, 'Reached Naturism Level 3', None), (1705133890, "{0.SimFirstName} is now more confident around others. There is no point to keep this as a secret.\\\
\\\
{0.SimFirstName} can now go a step further and become an exhibitionist. Not hiding anything from anybody.\\\
(Buy the 'Exhibitionist' trait in the Sim Rewards Store)\\\
(Benefits of Naturism will be lost after converting to Exhibitionism)", None), (3298542162, 'Reached Naturism Level 4', None), (2874888352, '{0.SimFirstName} and nature were never closer.', None), (3063200767, 'Reached Naturism Level 5', None), (426384424, 'The feeling of liberation, discovery, and freedom is something that {0.SimFirstName} cannot describe.', None), (936561618, 'Exhibitionism', 'Skill'), (4134248214, 'Take off some clothes and show off your body to others!', None), (1148769968, 'Expose your body to others by undressing, flashing or streaking. You have nothing to hide!', None), (1757191937, 'Acquired the Exhibitionism Skill', None), (3286043213, '{0.SimFirstName} acquired the Exhibitionism skill.', None), (727940737, 'Reached Exhibitionism Level 2', None), (1688494993, '{0.SimFirstName} reached level 2 of Exhibitionism skill.', None), (3646398708, 'Reached Exhibitionism Level 3', None), (1854657662, '{0.SimFirstName} is now much more open to nudity and can flash other Sims! Surprise others with sudden nudity!', None), (2230723639, 'Reached Exhibitionism Level 4', None), (450991505, '{0.SimFirstName} now has no problems with nudity around more Sims.', None), (3400239786, 'Reached Exhibitionism Level 5', None), (2650109385, '{0.SimFirstName} feels complete freedom to show your body off anywhere and anytime. There are no barriers for you anymore!', None), (1706884838, '---------- Traits ----------', None), (2239257939, 'Exhibitionist', 'Trait-Specific'), (2057008568, 'Exhibitionist', 'Trait-Neutral'), (4032773469, 'Turn your naturism into exhibitionism and unlock more nudity related interactions.\\\
\\\
(At least level 3 of Naturism Skill is required to purchase this trait).', None), (2638323095, 'Exhibitionists expose their bodies to gain sexual satisfaction from seeing shocked faces of others.', None), (4155510160, 'No Underwear', 'Trait-Specific'), (357895773, 'No Underwear', 'Trait-Neutral'), (2054347566, 'Sims with no underwear will never be wearing underwear ever again.', None), (3197094815, '---------- Lot Traits ----------', None), (1529541321, 'Nudist', 'Lot Trait'), (2266261289, "The thought of nudity could be scary, but this place pushes anyone's comfort level beyond what is considered appropriate.", None), (1722573033, '---------- Buffs ----------', None), (3044580742, 'Flashed a Sim', None), (466917972, 'Sims that are experienced with Exhibitionism get a lot of joy from flashing others.', None), (2693669807, 'Being Naked', None), (854041355, 'When you shed your clothes you also shed just a few of the burdens of everyday life.', None), (896618533, '---------- Whims ----------', None), (2007397741, 'Flash a Sim', None), (384372, 'Click on a Sim and select any flashing option from the Wicked Exhibitionism category.', None), (87037815, 'Admire Yourself Sexually', None), (2246976066, "Click on a mirror and select 'Admire Your Body'.", None), (3625247786, 'Get Naked', None), (2113244850, 'Click on your Sim and select any outfit undressing option from Wicked Naturism/Exhibitionism category.', None), (1399847452, 'Talk About Nudity', 'Whim'), (370535322, 'Click on a Sim and select any social naturism/exhibitionism option from Wicked Naturism/Exhibitionism category.', None), (1841640354, '---------- Interactions ----------', None), (2640893749, 'Undress Outfit Top', None), (9778775, 'Undress Outfit Bottom', None), (3808026444, 'Undress Outfit Shoes', None), (804165716, 'Undress Outfit', None), (952349486, 'Completely Undress Yourself', None), (302734899, 'Dress Up', None), (3129572812, 'Undress Bra', None), (2698493673, 'Undress Panties', None), (1709726542, 'Undress Underwear', None), (382705438, 'Put On Underwear', None), (2342090050, 'Reacting to Nudity', None), (712099301, 'Change Sim Underwear', None), (2196543455, 'Set mannequin top and bottom (only bottom for males) clothing to the underwear for the chosen outfit category to be used on that outfit.\\\
\\\
Changing underwear for sleepwear and swimwear outfit will have no effect.\\\
\\\
Changing underwear to the same parts as the outfit has will reset the underwear to default for that outfit.', None), (875977016, 'Flash Boobs', None), (3228660125, 'Flash Pussy', None), (3979916530, 'Flash Dick', None), (1134272282, 'Flash Butt', None), (1466639862, 'Flash Everything', None), (191812093, 'Flashing', None), (1897560099, 'Be Flashed by {1.SimFirstName}', None), (4229841253, 'Show Off Flashing', None), (2961626217, 'Compliment Flashing', None), (433831010, 'Disregard Flashing', None), (2086875090, 'Go Streaking!', None), (1094228482, 'Admire Your Body', None), (108564992, 'Compliment Sexy Body', None), (1974344057, '{1.SimFirstName} compliments my body', None), (3044374031, 'Talk About Nudity', None), (1490419223, '{1.SimFirstName} talks about nudity', None), (4066535370, 'Convince to Nudity', None), (2675898656, '{1.SimFirstName} convinces me to nudity', None), (3462563388, 'Ask to Get Naked', None), (1748611052, '{1.SimFirstName} asks me to get naked', None), (2043670257, 'Ask to Dress Up', None), (436096961, '{1.SimFirstName} asks me to dress up', None), (4234981655, '---------- Messages ----------', None), (3743260351, '{0.SimFirstName} {0.SimLastName} stripped from {M0.his}{F0.her} top.', None), (3069021969, '{0.SimFirstName} {0.SimLastName} stripped from {M0.his}{F0.her} bottom.', None), (4281967896, '{0.SimFirstName} {0.SimLastName} stripped from {M0.his}{F0.her} shoes.', None), (2191667249, '{0.SimFirstName} {0.SimLastName} stripped from {M0.his}{F0.her} outfit.', None), (2998371344, '{0.SimFirstName} {0.SimLastName} put {M0.his}{F0.her} outfit back on.\\\
\\\
{0.String}{1.String}{2.String}{3.String}{4.String}{5.String}{6.String}{7.String}{8.String}{9.String}', None), (3224264085, "{0.SimFirstName} {0.SimLastName} doesn't feel like taking off clothes right now is a good idea.\\\
\\\
{0.String}{1.String}{2.String}{3.String}{4.String}{5.String}{6.String}{7.String}{8.String}{9.String}", None), (2434379342, '- The most comfortable place to undress will always be Sim home.\\\
\\\
', None), (14125364, '- Undressing outside requires a lot more courage.\\\
\\\
', None), (902300171, '- Sims around can make it quite embarrassing to undress.\\\
\\\
', None), (1357018163, '{0.SimFirstName} {0.SimLastName} stripped from {M0.his}{F0.her} bra.', None), (3100688268, '{0.SimFirstName} {0.SimLastName} stripped from {M0.his}{F0.her} panties.', None), (3110156917, '{0.SimFirstName} {0.SimLastName} stripped from {M0.his}{F0.her} underwear.', None), (1950586772, '{0.SimFirstName} {0.SimLastName} put {M0.his}{F0.her} underwear back on.\\\
\\\
{0.String}{1.String}{2.String}{3.String}{4.String}{5.String}{6.String}{7.String}{8.String}{9.String}', None), (2447814946, "{0.SimFirstName} {0.SimLastName} doesn't feel like taking off underwear right now is a good idea.\\\
\\\
{0.String}{1.String}{2.String}{3.String}{4.String}{5.String}{6.String}{7.String}{8.String}{9.String}", None), (3499180400, '{0.SimFirstName} {0.SimLastName} flashed her pussy to {1.SimFirstName} {1.SimLastName}.', None), (2396534391, '{0.SimFirstName} {0.SimLastName} flashed her boobs to {1.SimFirstName} {1.SimLastName}.', None), (1399400780, '{0.SimFirstName} {0.SimLastName} flashed his dick to {1.SimFirstName} {1.SimLastName}.', None), (4243459940, '{0.SimFirstName} {0.SimLastName} flashed his butt to {1.SimFirstName} {1.SimLastName}.', None), (3983588816, '{0.SimFirstName} {0.SimLastName} flashed everything to {1.SimFirstName} {1.SimLastName}.', None), (72156750, "{0.SimFirstName} {0.SimLastName} doesn't feel like flashing Sims right now is a good idea.\\\
\\\
{0.String}{1.String}{2.String}{3.String}{4.String}{5.String}{6.String}{7.String}{8.String}{9.String}", None), (267480274, '{0.SimFirstName} {0.SimLastName} lost {M0.his}{F0.her} swimsuit when jumping to water.', None), (1660512188, '----------End----------', None)]

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
    file_hash = '{}160ADBD052187A'
    lang_flags = ('00', '02', '03', '04', '05', '06', '07', '08', '0B', '0C', '0D', '0E', '0F', '11', '12', '13', '15')
    for lang_flag in lang_flags:
        file_lang_hash = file_hash.format(lang_flag)
        file_stream = open(os.path.join('D:\\\\TS4\\\\WickedWoohoo\\\\Tuning Files\\\\Nudity\\\\STBL', 'S4_220557DA_80000000_' + file_lang_hash + '.stbl'), 'wb')
        file_stream.write(stlb_builder.get_bytes())
        file_stream.close()

def _get_string_hash(string, suffix):
    string = string.replace('\
', '')
    string_hash = 'WickedWhimsTurboDriver' + string + 'Nudity'
    if suffix is not None:
        string_hash += suffix
    string_hash = str(hex(FNV.fnv32(string_hash)))
    string_hash_prefix = string_hash[:2]
    string_hash_suffix = string_hash[2:].upper()
    string_hash_suffix = str('0'*(8 - len(string_hash_suffix))) + string_hash_suffix
    return string_hash_prefix + string_hash_suffix

_save_stbl_files()
