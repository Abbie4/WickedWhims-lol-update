'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
import os
from turbolib.hash_util import FNV
from turbolib.maker.stbl import StblBuilder
STBL_STRINGS = [(2450832731, '---------- Settings ----------', None), (351743462, 'Warning! Changing sex settings with running sex interactions can cause issues!\\n\\nEnd running sex interaction first to avoid possible problems.', None), (971624425, 'Sex Settings', None), (165875418, 'Change sex settings.\\n\\nThese settings affect only sex related functions like gender role recognition, positions progression, autonomy, outfit or pregnancy).', None), (2437423776, 'This option requires restarting the game to take full effect!\\n\\nSave and restart for this setting to work.', None), (3942521497, 'Notifications Settings', None), (2390465803, 'Enable/Disable sex related notifications.', None), (3366624962, 'Sex Autonomy Notifications', None), (3419421543, 'Display sex autonomy related notifications.', None), (2850533999, 'Pregnancy Notifications', None), (3244791546, 'Display extra pregnancy related notifications.', None), (772504851, 'Autonomy Settings', None), (355353948, 'Change sex autonomy related settings.', None), (3547420725, 'Autonomy Level Settings', None), (639874934, 'Choose a level of autonomy.\\n\\nAffects autonomy locations, Sims, and frequency.', None), (2812893922, 'Disable Autonomy', None), (4005573132, 'Sims will never have autonomy sex.', None), (1091365348, 'Low Autonomy', None), (1279925819, 'Lower base chance. Less Sims having sex. Sims relationships matter. Less open sex locations.', None), (1843757931, 'Normal Autonomy', None), (2072620352, 'Moderate base chance. Sims relationships matter. Moderate chance for open sex locations.', None), (44141906, 'High Autonomy', None), (2567448436, "High base chance. Sims relationships don't matter. High chance for open sex locations.", None), (1837632671, 'Autonomy Specifics', None), (1237154084, 'Change how autonomy works.', None), (1958432185, 'Relationship Awareness Switch', None), (1853667742, "Enable/Disable if Sims will stay faithful to their partner and not have sex with others.\\n\\nThe 'Polyamorous' and 'Noncommittal' traits on Sims ignore this setting.", None), (2868453401, 'Random Sex Switch', None), (2790533388, 'Enable/Disable if Sims will randomly have sex with each other.', None), (702535409, 'Solo Sex Switch', None), (67063182, 'Enable/Disable if Sims will randomly have fun with themselves.', None), (4290647276, 'Romance Conversation Sex Switch', None), (845223578, 'Enable/Disable if Sims will have sex from romantic conversations.', None), (3379481732, 'Solo Watching Sex Switch', None), (2646001095, 'Enable/Disable if Sims will get off from watching sex.\\n\\n(Requires Amra72 and ooOLaLa World animations.)', None), (1504087796, 'Joining Sex Switch', None), (1846650774, 'Enable/Disable if Sims will try to join to existing sex interactions.', None), (4181149639, 'NPC Pregnancy Awareness Switch', None), (1296624804, 'Enable/Disable if NPC Sims will avoid sex if they have a high chance of getting pregnant.\\n(Only works with Menstrual Cycle Pregnancy Mode enabled.)', None), (2954623901, 'NPC Sex Duration', None), (270337891, 'NPC sex interaction duration in realtime minutes.\\n(Default: 3)', None), (3175007247, 'Player Sims Autonomy', None), (75047863, 'Enable/Disable Player Sims Sex Autonomy.', None), (2850867506, 'Asking for Sex Dialogs Settings', None), (1785597846, 'Change which asking sex dialogs are used.', None), (2452930409, 'Display Player Asking Player Sex Dialog', None), (1667433751, 'Enable/Disable Player Sims asking Player Sims for sex dialogs.', None), (3891041835, 'Display NPC Asking Player Sex Dialog', None), (1254474301, 'Enable/Disable NPC Sims asking Player Sims for sex dialogs.', None), (654398743, 'Display Player Asking NPC Sex Dialog', None), (4097958165, 'Enable/Disable Player Sims asking NPC Sims for sex dialogs.', None), (3877057791, 'Player Sims Joining Sex Autonomy', None), (3708088834, 'Enable/Disable if Player Sims will try and allow joining to existing sex interactions.', None), (679078101, 'Interaction Settings', None), (2235096818, 'Change sex interaction related settings.', None), (2252255568, 'Sex Progression Settings', None), (2366957964, 'Choose a type of how sex positions will progress.', None), (3375283059, 'Disable Sex Progression', None), (1955101260, 'Sex positions will not change on its own.', None), (4196260323, 'Stage Only Sex Progression', None), (1029205692, 'Sex positions will only change within its stages list.', None), (793763770, 'Full Sex Progression', None), (2858531257, 'Sex positions will change within its stages list and then to the next category.', None), (1272575900, 'Random Sex Progression', None), (3811352518, 'Sex positions will always change to the next category.', None), (2304850363, 'Player Sex Duration', None), (2697283065, 'Player Sex Interaction duration type.', None), (3718931206, 'Time Limit Duration', None), (3275682984, 'Sex Interaction Duration', None), (1812879384, 'Sex interaction duration in realtime minutes.\\n(Default: 3)', None), (91570471, 'Climax Finish', None), (406726944, 'Sex interaction ends only after a climax position.', None), (3424533837, 'After Climax Sex Progression', None), (878801550, 'Enable/Disable sex position progression when climax animation is playing.', None), (4282949192, 'Outfit Settings', None), (1311817416, 'Change outfit behavior in sex.', None), (1198907594, 'Sex Undressing Type', None), (20176818, 'Choose a type of how Sims will undress during sex.', None), (2532050121, 'NPC Sex Undressing Type', None), (235100229, 'Choose a type of how NPC Sims will undress during sex.', None), (170791406, 'Disable Undressing', None), (1387510539, 'Sims in sex will not undress automatically.', None), (1669970287, 'Auto Undressing', None), (3534301752, 'Sims in sex will undress automatically.', None), (1122202719, 'Complete Undressing', None), (1550925065, 'Sims in sex will completely undress.', None), (3237215331, 'Auto Dress Up After Sex', None), (1958038349, 'Sims will always dress up after sex.', None), (2301375032, 'Auto Remove Unnecessary Strapon', None), (1690045821, 'Strapon will be automatically undressed when not needed in the current animation.', None), (1255756570, 'Gender Settings', None), (2104076668, 'Change Sims gender recognition.', None), (1788660950, 'Gender Recognition Type', None), (5799974, 'Choose a type of how Sims gender is recognized.', None), (2575413641, 'Sex Identity Based', None), (3674097914, 'Based on biological characteristics of a Sim genitalia.', None), (581623950, 'Gender Identity Based', None), (728075106, 'Based on current characteristics of a Sim genitalia.\\n(Current characteristics are based on the CAS Gender Settings)', None), (656988476, 'Anything Goes', None), (2871758999, 'Gender is not checked at all.', None), (3804026130, 'Recognize Females As Both', None), (1632529084, 'Allow/Disallow female actors roles as both female and male roles (M/M).', None), (1983215653, 'Recognize Males As Both', None), (108985975, 'Allow/Disallow male actors roles as both male and female roles (F/F).', None), (491871453, 'Sim Specific Gender Recognition', None), (4192011344, 'Allow/Disallow deciding about individual Sim gender role.', None), (4283337872, 'Pregnancy Settings', None), (509549869, 'Change pregnancy related settings.', None), (3511666942, 'Pregnancy Mode', None), (47964663, 'Change Sims pregnancy behavior.', None), (1502510716, 'Disabled', None), (438007632, 'Sims will not get pregnant from sex.', None), (1885043084, 'Menstrual Cycle Mode', None), (932412252, 'Sims will follow rules of the menstrual cycle for the pregnancy.', None), (2261619077, 'Simple Mode', None), (4118916902, 'Sims will get pregnant based on the set percentage chance.', None), (556352433, 'Pregnancy Duration', None), (1728685938, 'Pregnancy duration in Sim days.\\n(Default: 3, Minimum: 1)', None), (2645678251, 'Birth Control Mode', None), (2237541236, 'Change birth control behavior.', None), (3625448012, 'Perfect Mode', None), (944923656, 'Every birth control method will prevent pregnancy with 100% success rate.', None), (2936152503, 'Realistic Mode', None), (1099359772, 'Every birth control method has a realistic chance of failing to prevent pregnancy.', None), (3306556634, 'NPC Birth Control Mode', None), (2735186651, 'Change NPC Sims use of birth control behavior.', None), (1445725124, 'Safe Mode', None), (1875877528, 'Most NPC Sims will own and use birth control.', None), (1631987776, 'Moderate Mode', None), (4199709209, 'Some NPC Sims will own and use birth control.', None), (3220390137, 'Unsafe Mode', None), (4218021585, 'NPC Sims will not own birth control unless given.', None), (1288635396, 'Birth Control Automatic Use', None), (3520888385, 'Makes Sims use birth control automatically when needed.\\n\\nCondoms are used during any sex that can cause pregnancy.\\nBirth Control Pills is used once a day.', None), (619151676, 'NPC Pregnancy Switch', None), (3609080218, 'Enable/Disable if NPC Sims can get pregnant on their own.', None), (2235486711, 'Miscarriage Switch', None), (4073427182, 'Enable/Disable if Sims can experience miscarriage.', None), (3329620855, 'Menstrual Cycle Duration', None), (2700070040, 'Choose Sims menstrual cycle duration.', None), (2942546179, 'Automatic', None), (3427448649, 'Uses Sim lifespan set in game settings.', None), (2977040698, 'Very Long', None), (2146497004, 'Life expectancy: Forever (21-30 days per menstrual cycle)', None), (2384666054, 'Long', None), (2690713490, 'Life expectancy: 324 days (18-24 days per menstrual cycle)', None), (3875124511, 'Normal', None), (2803796174, 'Life expectancy: 81 days (8-10 days per menstrual cycle)', None), (3424872466, 'Short', None), (209206419, 'Life expectancy: 42 days (6-7 days per menstrual cycle)', None), (2995617922, 'Player Pregnancy Chance', None), (1003291803, 'Choose pregnancy percentage chance for sex interactions involving player Sims.', None), (713658988, 'NPC Pregnancy Chance', None), (3667660227, 'Choose pregnancy percentage chance for NPC Sims sex interactions.', None), (182912662, 'Pregnancy Chance: {0.String}', None), (2360091807, 'Other Settings', None), (3065078624, 'Change all of the unrelated settings.', None), (307055479, 'Teens Sex Switch', None), (3218540922, 'Enable/Disable if teens can use sex interactions.', None), (2770502675, 'Sex Initiation Settings', None), (1371832521, 'Choose a type of how sex will be initiated.', None), (566493688, 'Talk and Walk', None), (3052811566, 'Sex will start with Sims talking and then walking to the sex location.', None), (2533155814, 'Instant (only with Always Accept enabled)', None), (3856129850, 'Sex will start instantly, teleporting Sims to the sex location.', None), (1338997908, 'Sex Relationship Impact Switch', None), (1149646106, 'Enable/Disable relationship impact from sex.', None), (4288829144, 'Sex Animations Duration Override Settings', None), (21918993, 'Override of sex animations duration in realtime seconds.', None), (3057735727, 'Default Duration', None), (53147723, 'Use animations duration time defined by the author.', None), (1667254996, 'Override Duration', None), (1264078058, 'Animation Override Duration', None), (3491653927, 'Override duration for all sex animations in realtime seconds.\\n\\nAnimations will not play exactly for the set amount out time. They will play for the approximate number of loops for the set time.', None), (3875215528, 'Cum Settings', None), (3025455413, 'Change cum related settings.', None), (342798417, 'Cum Layers Visibility', None), (1797015342, 'Enable/Disable visibility of cum layers.', None), (749165149, 'Cum Layers Visibility with Condom', None), (2755226641, 'Enable/Disable visibility of cum layers when using a condom.', None), (364609057, 'Auto Silence Phone During Sex', None), (1827602266, 'Enable/Disable auto silencing of Sim phone during sex.', None), (3571944160, 'Vanilla Interactions Switch', None), (420791980, 'Enable/Disable if non-sex (vanilla) interactions are available during sex.', None), (142564328, 'Default Woohoo Switch', None), (239190384, 'Enable/Disable default Woohoo and Try for Baby interactions.\\n\\n(Requires to restart the game.)', None), (2605472072, 'Cheats', None), (654545057, 'Change things that you find annoying.', None), (3188897533, 'Always Accept Switch', None), (1973509205, 'Enable/Disable if Sims will always accept sex propositions.', None), (2732646976, 'Global Instant Undressing Switch', None), (176843739, 'Enable/Disable global instant undressing outside sex.', None), (2408622223, 'Manual NPC Sex Switch', None), (2329727648, 'Enable/Disable control over NPC Sims sex.', None), (3057434828, 'Sim Needs Decay Switch', None), (318337624, 'Enable/Disable if Sim needs will decay during sex.', None), (3063236996, 'Sex Privacy Switch', None), (2458180356, 'Enable/Disable if Sims will avoid sex locations.', None), (1413563001, 'Sex Reaction Switch', None), (3687654653, 'Enable/Disable if Sims will react to sex.', None), (634015514, 'Cum Reaction Switch', None), (1608028199, 'Enable/Disable if Sims will react to cum on other Sims.', None), (2657851670, 'Teen Pregnancy Reaction Switch', None), (1137427362, 'Enable/Disable if parent Sims will react to teen Sims pregnancy.', None), (1853900111, 'Animations Disabler', None), (2380367292, 'Animations Disabler\\n{0.String}', None), (115716611, 'Enable/Disable specific animations from being used.', None), (2284702213, 'Autonomy Animations Disabler', None), (3773354670, 'Autonomy Animations Disabler\\n{0.String}', None), (2444846310, 'Enable/Disable specific animations from being used in autonomy sex.', None), (4285227430, 'Select which creator animations you want to disable.', None), (4201638866, 'Toggle All Animations', None), (1537618859, 'Enable/Disable all animations on this list.', None), (2223654951, 'Animations Count: {0.String}', None), (583685786, 'Animations Count: {0.String}\\nAuthor: {1.String}', None), (708866741, 'Locations: {0.String}{1.String}', None), (2011685353, 'Note that using this during any sex interactions may result in problems!\\nIt is recommended to not use this disabler while any sex interactions are playing!', None), (949972304, '---------- General ----------', None), (2764981496, 'Sex', 'General'), (1782200665, 'Teasing', None), (2036049244, 'Handjob', None), (122220731, 'Footjob', None), (1133298919, 'Oraljob', None), (2874903428, 'Vaginal', None), (3553429146, 'Anal', None), (1579105152, 'Climax', None), (1890248379, 'Random', None), (3437399765, '---------- Interface ----------', None), (77458156, 'Teasing Animations', None), (1425559843, 'Handjob Animations', None), (223939754, 'Footjob Animations', None), (2747124438, 'Oraljob Animations', None), (574589211, 'Vaginal Animations', None), (1610085053, 'Anal Animations', None), (3986970407, 'Climax Animations', None), (3494584829, 'Random Animation', None), (2301874612, 'Sex Categories', None), (465151699, "Swap {0.SimFirstName}'s Spot", None), (4149247255, 'Pick a Sim to swap with {0.SimFirstName}.', None), (906772330, 'Pick a partner for sex or yourself for a solo interaction.', None), (747723284, 'Pick partners to invite for group sex.', None), (389626746, 'Pick Sims for sex.', None), (780195446, 'No Sims viable to perform {0.String} Sex at the picked sex location were found around {0.SimFirstName}.', None), (3288282583, 'No Sims viable to perform {0.String} Sex at the picked sex location were found around it.', None), (2721401338, 'No Sims viable to join and perform {0.String} Sex at the current sex location were found around {0.SimFirstName}.', None), (2459296019, 'No animations were found for the picked sex location!', None), (1395546180, 'No animations were found for the current sex location!', None), (2693069513, 'No animations were found for the selected Sims at the current sex location!', None), (443330929, 'No {0.String} were found for more than the current number of Sims in the sex interaction!', None), (3121278879, 'No animations were found for more than the current number of Sims in the sex interaction!', None), (4051936639, 'No compatible Sims to swap with were found in the sex interaction!', None), (3113927949, 'Install Sex Animations!', None), (1066517691, 'Looks like you have not installed any sex animations.\\nCurrently you will only have few default animations that are included with the mod.\\n\\nIf you want more animations, look for them included on the mod page download section.', None), (881372436, 'Author: {0.String}', None), (3166569584, 'Animations Count: {0.String}', 'Interface'), (1298832615, '---------- Interactions ----------', None), (3676092375, 'Outfit', None), (1461289261, 'Undress Top', None), (3447783025, 'Undress Bottom', None), (2894243765, 'Undress Outfit', None), (1558033418, 'Undress Completely', None), (3256159535, 'Undress Hat', None), (133699812, 'Undress Gloves', None), (2488200194, 'Undress Leggings', None), (1416991887, 'Undress Socks', None), (861319970, 'Undress Shoes', None), (3318294418, 'Accessories', None), (1549851454, 'Undress Glasses', None), (2371822416, 'Undress Head', None), (1362721524, 'Undress Left Hand', None), (372117841, 'Undress Right Hand', None), (3715912042, 'Undress Other Accessories', None), (3925581955, 'Change Outfit...', None), (4119196202, 'Change Outfit for {0.SimFirstName}', None), (3099654839, 'Cum', None), (3371620185, 'Face', None), (3278059333, 'Chest', None), (2654708087, 'Back', None), (2370930056, 'Vagina', None), (1398882513, 'Butt', None), (4090662600, 'Feet', None), (3771269126, 'Ask for Sex', None), (3125171884, 'Ask for Sex (Random)', None), (1108932362, 'Be Asked for Sex', None), (1828786758, 'Go to Sex Location', None), (2617168792, 'Wait for Partner', None), (2667173688, 'Sex: {0.String} ({1.String})', None), (4077608115, 'Join In', None), (2031331325, 'Ask to Join In', None), (2783896457, 'Next', None), (145494910, 'Change Sex Location to Here', None), (4149251198, "Swap {1.SimFirstName}'s Spot", None), (1224032036, 'Sim is not ready for climax yet.', None), (1959385898, 'Gender Recognition', None), (2240812365, 'Male', None), (4130350532, 'Female', None), (1208587373, 'Default', None), (3413808683, 'NPC Sex', None), (3165310721, 'Change', 'NPC Sex'), (958248678, 'Invite', 'NPC Sex'), (2338626172, 'Stop', None), (3087413108, 'Go Away', None), (3956250692, 'This interaction is not available while in sex.', None), (3501300246, 'Reacting to Sex', None), (2600043135, 'Watch Sex', None), (1724554353, 'Watching Sex', None), (1282473674, '---------- Autonomy ----------', None), (3606796023, '{0.SimFirstName} is having some fun!', None), (3818025802, 'Sims are having sex!', None), (4154762800, '{0.String} and {1.String} are having sex!', None), (2363440915, '{0.String}, {1.String} and {2.String} are having sex!', None), (81205561, '{0.String}, {1.String}, {2.String} and {3.String} are having sex!', None), (67136532, '{0.String}, {1.String}, {2.String}, {3.String} and {4.String} are having sex!', None), (3768853220, '{0.String}, {1.String}, {2.String}, {3.String}, {4.String} and {5.String} are having sex!', None), (2435035491, '{0.String}, {1.String}, {2.String}, {3.String}, {4.String}, {5.String} and {6.String} are having sex!', None), (1751739389, '{0.String}, {1.String}, {2.String}, {3.String}, {4.String}, {5.String}, {6.String} and {7.String} are having sex!', None), (2414003908, '{0.String}, {1.String}, {2.String}, {3.String}, {4.String}, {5.String}, {6.String}, {7.String} and {8.String} are having sex!', None), (3045675184, '{0.String}, {1.String}, {2.String}, {3.String}, {4.String}, {5.String}, {6.String}, {7.String}, {8.String} and {9.String} are having sex!', None), (2458237828, 'Stop That!', None), (1638454846, 'Do you want to have sex?', None), (3899042444, 'Can I join?', None), (3398494028, 'Accept', None), (3364226930, 'Decline', None), (1839602514, 'Enable for Sex Autonomy', None), (3563659563, 'Disable for Sex Autonomy', None), (3650345964, '---------- Notifications ----------', None), (866800069, '{0.SimFirstName} {0.SimLastName} hates children! No Vaginal or Climax sex without protection!', None), (971885236, 'Miscarriage', 'Notification'), (1234477375, '{0.SimFirstName} {0.SimLastName} just lost a new life that never got a chance to become one.', None), (3709993390, '---------- Skills ----------', None), (2671290095, 'Sex', 'Skill'), (1963749826, 'Acquired the Sex Skill', None), (2089606558, "{0.SimFirstName}'s new Sex skill will allow {M0.him}{F0.her} to satisfy Sims sexual needs better.\\nMore sex, especially with skilled Sims, will make you better at it.", None), (2493315474, 'Reached Sex Level 2', None), (557380405, 'Reached Sex Level 3', None), (4075774676, 'Reached Sex Level 4', None), (3648189949, '{0.SimFirstName} has reached a higher level in Sex Skill!', None), (2407001599, 'Reached Sex Level 5', None), (1086499796, "{0.SimFirstName} has reached max level in Sex Skill! It's almost impossible to have your partners not enjoy your touch.", None), (441817920, 'Have sex with someone.', None), (1082702556, 'The higher the level of your Sex Skill, the higher the satisfaction you and your partners gain after sex.\\nSex with skilled Sims, sex with different partners and, sex in general will increase your Sex Skill.', None), (4249475274, '---------- Buffs ----------', None), (4052013031, '(From Sex Satisfaction)', None), (2908474586, 'Stranger', None), (2411227586, 'Strangers always provide a wildcard to sex, but the touch of Sims unknown has left {0.SimFirstName} satisfied from {M0.his}{F0.her} moment of passion.', None), (3643549842, 'Young Partner', None), (458664978, 'Wow, that was really something. Youth these days sure have a lot of energy and {0.SimFirstName} just loved watching that hot body move.', None), (4261841168, 'Sex in Public', None), (3232071849, "{0.SimFirstName}'s mind is running at superspeed with the idea that they could have been caught whilst in the middle of their dirty deed.", None), (3575312736, 'Caught in the Act', None), (3911209829, "How Exciting! With all eyes on {0.SimFirstName} while they were having sex, {M0.he}{F0.she} couldn't help but feel even more aroused knowing that others were enjoying their show.", None), (339169767, 'Marital Bliss', None), (3357816283, "That was wonderful, there's nothing quite like the familiar touch of a lover's embrace. {0.SimFirstName} is truly glad to have shared a passionate moment with {M0.his}{F0.her} spouse.", None), (11500898, 'Paranormal Intercourse', None), (2775596553, "After what can be described as a strange otherworldly encounter, {0.SimFirstName} can't help but feel full of life whilst being so close to death.", None), (1113045431, 'Group Sex', None), (1569822038, 'Amazing! Sex with several partners was just the sort of fun activity that {0.SimFirstName} needed.', None), (1488861160, 'Satisfied', None), (994202252, 'That was pretty good. {0.SimFirstName} enjoyed their sexual encounter and was able to finish it off satisfied.', None), (870137382, 'Bad Romance', None), (3739408439, 'Seriously? {0.SimFirstName} thought that the sex would be magical but they were left unsatisfied. Did {M0.he}{F0.she} expect too much?', None), (337352833, 'Disqualified!', None), (1909218747, "What even was that!? {0.SimFirstName} wants other Sims to really moan during sex but that was just anticlimactic... Was it because they weren't good enough?", None), (314956249, 'Unsatisfied', None), (4290625297, 'Well that was... something. {0.SimFirstName} was left unsatisfied and uncomfortable from the sex they just had.', None), (2840328936, 'New Sex Partner', None), (1587002602, 'First time sex with a new Sim is always a memorable experience!', None), (1769362881, 'Sex Outdoors', None), (3986856640, "There's nothing like the thrill of sex outside. That was fun!", None), (734577494, 'Wearing a Condom', None), (2542119410, '{0.SimFirstName} is wearing a condom.', None), (1740367557, 'On Birth Control Pills', None), (1369332725, '{0.SimFirstName} is on {M0.his}{F0.her} birth control.', None), (1690070744, 'Sexual Desire', None), (2014725959, 'Such a lust for love... Who? Who do you desire?', None), (3161696242, 'Intense Lust', None), (882194762, 'So much lust makes you uncomfortable! It would be wise to find a way to release this tension.', None), (2404119453, '(From High Desire)', None), (1304494194, 'Cum Whore', None), (3614909518, 'The feel of cum on skin makes you so much more aroused.', None), (472156055, 'Cum Dump', None), (3514555748, 'Having sticky thick fluid on your body is pretty uncomfortable.', None), (1704305853, 'Embarrassing Encounter', None), (2153770005, 'Oh! You didn�t expect to walk in on someone getting hot and heavy.', None), (3929747223, 'Interesting View', None), (2433385000, 'Looking at someone getting it on makes you pretty excited.', None), (2053348550, 'Comical Performance', None), (1818006464, 'It would be a surprise if they considered themselves good at sex.', None), (2782236739, 'Banging Sight', None), (481045908, 'The sight of naked bodies in the act is always enough to turn you on!', None), (4112849859, 'Lost Delight', None), (376756602, 'The sight of past love in a sex act reminds you of all the good that was lost.', None), (842791259, 'Unnecessary View', None), (2368220254, 'Feeling angry after an unpleasant view of someone screwing around without pants.', None), (1186864888, '{M0.Cuckold}{F0.Cuckquean}', None), (3896586053, '{0.SimFirstName} is really turned on by seeing {M0.his}{F0.her} partner have sex with someone else.', None), (1398794256, 'Horrified', None), (2206765891, 'Oh no! I should not have seen that person having sex!', None), (2569326473, 'Discovered Teen Pregnancy', None), (624050181, 'Amidst all the doubtfulness, sadness and confusion, there is anger. Can {0.SimFirstName} cope with having {M0.his}{F0.her} teen child pregnant?', None), (1084339117, 'Pregnancy Termination', None), (3999848715, 'When certain choices leave you with the burden of guilt...', None), (2848064063, 'Hasta La Vista, Baby', None), (2188967402, 'When the stress is gone, the party can go on.', None), (3441893392, '(From Pregnancy Termination)', None), (1509603985, 'Miscarriage', None), (934769185, 'Consequences of not taking care of yourself...', None), (3245985980, '(From Miscarriage)', None), (803366555, '---------- Traits ----------', None), (3515447631, 'Cum Slut', 'Specific'), (3186379380, 'Cum Slut', 'Neutral'), (491947361, 'Cum Sluts love to receive hot loads of cum all over their body.', None), (4208589728, 'Incest', 'Specific'), (3667765805, 'Incest', 'Neutral'), (3002083512, 'These Sims are open to sexual activities with their family members and close relatives.', None), (122688803, 'Sexually Alluring', 'Specific'), (427061256, 'Sexually Alluring', 'Neutral'), (4163229882, 'Sexually Alluring Sims are really successful at convincing other to have sex with them.', None), (1787775829, 'Sexually Abstinent', 'Specific'), (107869422, 'Sexually Abstinent', 'Neutral'), (4040424258, 'Sexually Abstinent Sims have no interest in sexual activities.', None), (2028101360, 'Infertile', 'Specific'), (1181550909, 'Infertile', 'Neutral'), (2229204374, 'Infertile Sims have no chances of having a biological child.', None), (3988093168, '{M0.Cuckold}{F0.Cuckquean}', 'Specific'), (1218796076, 'Cuckold', 'Neutral'), (1643769656, "These Sims desire to see their partner have sex with someone else and don't consider it cheating.", None), (3677499788, '---------- Lot Traits ----------', None), (820333312, 'Hypersexual', None), (1229306406, 'The extreme vibe of sexual desire makes this an especially great place to have sex.', None), (970520582, '---------- Whims ----------', None), (1083979350, 'Have Sex with {2.SimFirstName}', None), (3081865746, 'Click on an object and select Sex from the Wicked category.', None), (2038439524, 'Sex with Someone', None), (2022872058, 'Click on an object and select Sex from the Wicked category. Sims need to have a good relationship to be able to have sex.', 'SexWithSomeone'), (980145852, 'Sex with Someone in Public', None), (2185555824, 'Click on an object and select Sex from the Wicked category. Sims need to have a good relationship to be able to have sex.', 'SexInPublic'), (1212777967, 'Have Sex with Your Date', None), (1298760404, '---------- Messages ----------', None), (2175203501, 'Sex', 'Message'), (2431239863, "An issue with a running sex interaction was detected!\\nAttempting a reset of the active sex interaction...\\n\\n\\nIf you want to force stop all sex interactions:\\n1. Open commands console (CTRL+SHIFT+C).\\n2. Type in 'ww.stop_sex' command.", None), (215847180, "{0.SimFirstName} {0.SimLastName} refused {1.SimFirstName}'s proposition for sex.", None), (2134958105, '---------- Strapon ----------', None), (1851298968, 'Change Sim Strapon', None), (1645033536, 'Set mannequin bottom clothing to strapon you want to use only for the first Everyday Outfit Category.\\nChanging strapon for different outfit categories will have no effect.\\nChanging strapon to other clothing will result in problems.', None), (595241531, 'Strapon', None), (1854539790, 'Allow Strapon', None), (3218185930, 'Disallow Strapon', None), (3478097612, '---------- Birth Control ----------', None), (1873179704, 'Birth Control', None), (2122601819, 'Unpack Box', None), (2855482683, 'Use Condom(s)', None), (727861676, 'Condoms can only be used during sex.', None), (4229281812, 'Allow Condoms Auto Use', None), (791975184, 'Disallow Condoms Auto Use', None), (4082674743, 'Used a condom. (Owned by {0.SimFirstName} {0.SimLastName})', None), (2429963938, 'Used {0.String} condoms. (Owned by {1.SimFirstName} {1.SimLastName})', None), (3990632821, 'Not enough condoms to use for every partner!', None), (3889719519, 'Wicked Condoms Box', None), (407614226, 'Box of 24 strong and thin latex condoms for any size. Exactly what you need to avoid unwanted pregnancy.\\n\\nUnpack the box and get 24 usable condoms.', None), (3331179557, 'Wicked Condom', None), (2920032161, "Exactly what you need to avoid unwanted pregnancy. Keep them around, you never know when you would need one.\\n\\nUse it during sex by clicking on it in Sim inventory, don't wait, it can get too late!", None), (2427313790, 'Take Pill', None), (529767043, '{0.SimFirstName} is already on birth control.', None), (2698055539, 'Allow Birth Control Pills Auto Use', None), (3281245287, 'Disallow Birth Control Pills Auto Use', None), (949418969, '{0.SimFirstName} took a birth control pill.', None), (1635440778, 'Wicked Birth Control Pills Box', None), (4015831811, "Box of 28 birth control pills. Use one every day and don't worry about unwanted pregnancy.\\n\\nUnpack the box and get 28 usable pills.", None), (3125631955, 'Wicked Birth Control Pills', None), (1818011010, 'Helps with periods and unwanted pregnancy. Remember to take one once a day!\\n\\nUse it once a day by clicking on it in Sim inventory. With each missed day, you risk becoming pregnant.', None), (4023694433, '---------- Pregnancy ----------', None), (2364600527, 'Pregnancy', None), (382282328, 'Terminate Pregnancy', None), (3344178125, '{0.SimFirstName} {0.SimLastName} is not pregnant anymore.\\nIt would be cheaper to think about protection before the next time.', None), (1633758340, '{0.SimFirstName} is not able to do this while not pregnant.', None), (2678928905, '{0.SimFirstName} is not able to do this so late in pregnancy.', None), (518027626, 'Fertility Treatment', None), (2518175852, '{0.SimFirstName} {0.SimLastName} received a temporary fertility treatment.\\n{M0.His}{F0.Her} chances of becoming pregnant will now be higher during the next ovulation.\\n\\nAfter the next ovulation ends, treatment will lose its potential.', None), (730377617, '{0.SimFirstName} is not able to do this while pregnant.', None), (332111907, '{0.SimFirstName} {0.SimLastName} might now be pregnant!\\nPerforming a pregnancy test or waiting a day will show the result.\\n\\nAttempting conception sex multiple times a day with the same partner will not yield different results.', None), (567106456, 'Take Fertility Awareness Test', None), (2800719885, 'Fertility Awareness Test', None), (2475884372, "{0.SimFirstName}'s fertility awareness test resulted in {1.String}% chance of becoming pregnant.\\nDays left till ovulation: {2.String}", None), (72538425, "{0.SimFirstName}'s fertility awareness test resulted in {1.String}% chance of becoming pregnant.", None), (3841941810, 'Cramps', None), (2061236478, '(From Premenstrual Syndrome)', None), (801699479, '{0.SimFirstName} is in high discomfort, as if someone was violently squeezing {M0.his}{F0.her} insides...', None), (989570146, 'On Period', None), (3050083018, "The hormone shift inside {0.SimFirstName}'s body is making {M0.him}{F0.her} feel all hot and heavy.", None), (1259827329, '{0.SimFirstName} is feeling just fine today... or is {M0.he}{F0.she}?', None), (1733238395, "{0.SimFirstName} can't concentrate while the uterus is shedding...", None), (2450475522, "{0.SimFirstName} is feeling blue. Wait, no... it's red.", None), (40145217, '{0.SimFirstName} is very stressed from riding the crimson wave.', None), (4291848454, '{0.SimFirstName} is fighting against the flow.', None), (3901690399, "The darkness inside {0.SimFirstName}'s body feels ever stronger. How is this even possible?", None), (2037604436, '---------- Shop ----------', None), (2707883119, 'Purchase Sex Items', None), (2744040171, 'Thanks for ordering! The sex items {0.SimFirstName} purchased will be delivered to {M0.his}{F0.her} mailbox.', None), (4155673645, '----------End----------', None)]

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
    file_hash = '{}0D0E1AB7B23B64'
    lang_flags = ('00', '02', '03', '04', '05', '06', '07', '08', '0B', '0C', '0D', '0E', '0F', '11', '12', '13', '15')
    for lang_flag in lang_flags:
        file_lang_hash = file_hash.format(lang_flag)
        file_stream = open(os.path.join('D:\\TS4\\WickedWoohoo\\Tuning Files\\Sex\\STBL', 'S4_220557DA_80000000_' + file_lang_hash + '.stbl'), 'wb')
        file_stream.write(stlb_builder.get_bytes())
        file_stream.close()


def _get_string_hash(string, suffix):
    string = string.replace('\n', '')
    string_hash = 'WickedWhimsTurboDriver' + string + 'Sex'
    if suffix is not None:
        string_hash += suffix
    string_hash = str(hex(FNV.fnv32(string_hash)))
    string_hash_prefix = string_hash[:2]
    string_hash_suffix = string_hash[2:].upper()
    string_hash_suffix = str('0'*(8 - len(string_hash_suffix))) + string_hash_suffix
    return string_hash_prefix + string_hash_suffix

_save_stbl_files()