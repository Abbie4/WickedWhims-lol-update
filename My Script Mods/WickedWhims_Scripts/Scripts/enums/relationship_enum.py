from turbolib.native.enum import TurboEnum


class RelationshipTrackType(TurboEnum):
    __qualname__ = 'RelationshipTrackType'
    FRIENDSHIP = 16650
    ROMANCE = 16651
    MISCHIEF = 26920


class ShortTermRelationshipTrackType(TurboEnum):
    __qualname__ = 'ShortTermRelationshipTrackType'
    AWKWARDNESS = 24098
    FRIENDSHIP = 24099
    FUN = 24100
    INTERROGATION_TABLE_CALM = 103618
    INTERROGATION_TABLE_DEFENSIVE = 103617
    INTERROGATION_TABLE_FRIENDLY = 103613
    INTERROGATION_TABLE_FURIOUS = 103616
    INTERROGATION_TABLE_SHY = 103598
    INTERROGATION_TABLE_SMUG = 103619
    INTERROGATION_TABLE_SUSPICIOUS = 103612
    INTERROGATION_TABLE_TENSE = 103615
    INTERROGATION_TABLE_TERRIFIED = 103614
    INTERROGATION_TABLE_WORRIED = 103620
    RETAIL_PURCHASE_INTEREST = 111598
    ROMANCE = 24101


class SimRelationshipBit(TurboEnum):
    __qualname__ = 'SimRelationshipBit'
    AUTHORITY_DEFAULT = 161996
    CATOWNED = 148063
    CATOWNER = 148062
    CLUBS_GAMESCOM_SECRETCRUSH = 122859
    COWORKERS = 107373
    CT_NOTPARENT_CAREDEPENDENT = 162483
    CT_NOTPARENT_CAREGIVER = 162482
    DARED = 121352
    DATE_SITUATION_BIT = 37762
    DEBUG_SITUATION_BIT = 37769
    DETECTIVE_FOUNDGUILTY = 116146
    DETECTIVECAREER_ARRESTED = 113055
    DETECTIVECAREER_CRIMINAL = 113060
    DOGOWNED = 148061
    DOGOWNER = 148060
    FAMILY_AUNT_UNCLE = 8829
    FAMILY_BROTHER_SISTER = 8802
    FAMILY_COUSIN = 8826
    FAMILY_GRANDCHILD = 8807
    FAMILY_GRANDPARENT = 8808
    FAMILY_HUSBAND_WIFE = 24490
    FAMILY_NIECE_NEPHEW = 9989
    FAMILY_PARENT = 8809
    FAMILY_SON_DAUGHTER = 8805
    FAMILY_STEPSIBLING = 8824
    FAMILYRELATIONSHIPBITSACQUIRED_CHILD_HIGHREL_HIGHAUTH = 161969
    FAMILYRELATIONSHIPBITSACQUIRED_CHILD_HIGHREL_LOWAUTH = 161971
    FAMILYRELATIONSHIPBITSACQUIRED_CHILD_MAXREL_HIGHAUTH = 161973
    FAMILYRELATIONSHIPBITSACQUIRED_CHILD_MAXREL_LOWAUTH = 161975
    FAMILYRELATIONSHIPBITSACQUIRED_CHILD_NEUTRALREL_HIGHAUTH = 161977
    FAMILYRELATIONSHIPBITSACQUIRED_CHILD_NEUTRALREL_LOWAUTH = 161979
    FAMILYRELATIONSHIPBITSACQUIRED_CHILD_POORREL_HIGHAUTH = 161981
    FAMILYRELATIONSHIPBITSACQUIRED_CHILD_POORREL_LOWAUTH = 161983
    FAMILYRELATIONSHIPBITSACQUIRED_GRANDCHILD_HIGHREL = 161910
    FAMILYRELATIONSHIPBITSACQUIRED_GRANDCHILD_NEUTRALREL = 161922
    FAMILYRELATIONSHIPBITSACQUIRED_GRANDCHILD_POORREL = 161924
    FAMILYRELATIONSHIPBITSACQUIRED_GRANDPARENT_HIGHREL = 161909
    FAMILYRELATIONSHIPBITSACQUIRED_GRANDPARENT_NEUTRALREL = 161911
    FAMILYRELATIONSHIPBITSACQUIRED_GRANDPARENT_POORREL = 161923
    FAMILYRELATIONSHIPBITSACQUIRED_PARENT_HIGHREL_HIGHAUTH = 161968
    FAMILYRELATIONSHIPBITSACQUIRED_PARENT_HIGHREL_LOWAUTH = 161970
    FAMILYRELATIONSHIPBITSACQUIRED_PARENT_MAXREL_HIGHAUTH = 161972
    FAMILYRELATIONSHIPBITSACQUIRED_PARENT_MAXREL_LOWAUTH = 161974
    FAMILYRELATIONSHIPBITSACQUIRED_PARENT_NEUTRALREL_HIGHAUTH = 161976
    FAMILYRELATIONSHIPBITSACQUIRED_PARENT_NEUTRALREL_LOWAUTH = 161978
    FAMILYRELATIONSHIPBITSACQUIRED_PARENT_POORREL_HIGHAUTH = 161980
    FAMILYRELATIONSHIPBITSACQUIRED_PARENT_POORREL_LOWAUTH = 161982
    FAMILYRELATIONSHIPBITSACQUIRED_SIBLING_HIGHREL_HIGHRIVAL = 161931
    FAMILYRELATIONSHIPBITSACQUIRED_SIBLING_HIGHREL_LOWRIVAL = 161930
    FAMILYRELATIONSHIPBITSACQUIRED_SIBLING_NEUTRALREL_HIGHRIVAL = 161932
    FAMILYRELATIONSHIPBITSACQUIRED_SIBLING_NEUTRALREL_LOWRIVAL = 161933
    FAMILYRELATIONSHIPBITSACQUIRED_SIBLING_POORREL_HIGHRIVAL = 161934
    FAMILYRELATIONSHIPBITSACQUIRED_SIBLING_POORREL_LOWRIVAL = 161935
    FRIENDSHIP_ACQUAINTANCES = 15792
    FRIENDSHIP_BFF = 15794
    FRIENDSHIP_BFF_BROMANTICPARTNER = 31211
    FRIENDSHIP_BFF_EVIL = 15795
    FRIENDSHIP_DESPISED = 15796
    FRIENDSHIP_DISLIKED = 15802
    FRIENDSHIP_FRIEND = 15797
    FRIENDSHIP_FRIEND_EVIL = 15798
    FRIENDSHIP_GOOD_FRIENDS = 15799
    FRIENDSHIP_GOOD_FRIENDS_EVIL = 15800
    FRIENDSHIP_NEMESIS = 15801
    HAS_MET = 15803
    HASBEENFRIENDS = 129295
    HAVEBEENROMANTIC = 98756
    INTERROGATIONFINISHED = 109991
    ISCLONE = 109549
    KNOWSISALIEN = 103299
    KNOWSISALIEN_BOTHSIMSAREALIENS = 116465
    LANDLORD = 135305
    LIVING_ROOMMATE = 8812
    LOANRELATIONSHIPBITS_LARGE = 28912
    LOANRELATIONSHIPBITS_SMALL = 28911
    NEIGHBOR = 75294
    PERSONALITYANALYZED = 107716
    PETTOPET_FRIENDLY = 159636
    PETTOPET_HOSTILE = 159635
    PETTOPET_NEUTRAL = 159634
    PLAYDATE_SITUATION_BIT = 117189
    RELATIONSHIPBITS_FRIENDSHIP_NEUTRALBIT = 15809
    RELATIONSHIPBITS_MISCHIEF_NEUTRALBIT = 26922
    RELATIONSHIPBITS_MISCHIEF_PARTNERSINCRIME = 26923
    RELATIONSHIPBITS_ROMANCE_NEUTRALBIT = 15810
    RELBIT_APARTMENTNEIGHBOR_HASKEY = 135106
    RELBIT_PREGNANCY_BIRTHPARENT = 100705
    RELBIT_WRITINGJOURNALISM_ARTICLEINTERVIEW = 33719
    RELBIT_WRITINGJOURNALISM_ARTICLEINTERVIEWNEGATIVE = 33720
    RELBIT_WRITINGJOURNALISM_ARTICLEINTERVIEWPOSITIVE = 33721
    RETAIL_EMPLOYEESWONTTALKTOLOTOWNERS = 117017
    RIVALRY_DEFAULT = 161997
    ROMANTIC_BROKEN_UP = 15811
    ROMANTIC_BROKEN_UP_ENGAGED = 15812
    ROMANTIC_CHEATEDWITH = 37265
    ROMANTIC_DEADSPOUSE = 104161
    ROMANTIC_DESPISED_EX = 15814
    ROMANTIC_DIVORCED = 15815
    ROMANTIC_ENGAGED = 15816
    ROMANTIC_EXCHANGEDNUMBERS = 127076
    ROMANTIC_FIRSTKISS = 10150
    ROMANTIC_FRUSTRATED_EX = 15817
    ROMANTIC_GETTINGMARRIED = 15818
    ROMANTIC_GOTCOLDFEET = 15819
    ROMANTIC_HASBEENUNFAITHFUL = 36957
    ROMANTIC_HAVEDONEWOOHOO = 34619
    ROMANTIC_HAVEDONEWOOHOO_RECENTLY = 97154
    ROMANTIC_LEAVEATTHEALTAR = 39356
    ROMANTIC_LEFTATTHEALTAR = 15821
    ROMANTIC_MARRIED = 15822
    ROMANTIC_PROMISED = 99429
    ROMANTIC_RENEWINGVOWS = 99616
    ROMANTIC_SIGNIFICANT_OTHER = 15825
    ROMANTIC_WIDOW = 102081
    ROMANTIC_WIDOWER = 102911
    ROMANTICCOMBO_ACQUAINTANCES = 77585
    ROMANTICCOMBO_AWKWARDFRIENDS = 15826
    ROMANTICCOMBO_AWKWARDLOVERS = 15827
    ROMANTICCOMBO_BADMATCH = 15828
    ROMANTICCOMBO_BADROMANCE = 15843
    ROMANTICCOMBO_DESPISED = 77648
    ROMANTICCOMBO_DISLIKED = 77647
    ROMANTICCOMBO_ENEMIESWITHBENEFITS = 15830
    ROMANTICCOMBO_FRENEMIES = 15831
    ROMANTICCOMBO_HOTANDCOLD = 15832
    ROMANTICCOMBO_ITSAWKWARD = 15833
    ROMANTICCOMBO_ITSCOMPLICATED = 15834
    ROMANTICCOMBO_ITSVERYAWKWARD = 15835
    ROMANTICCOMBO_ITSVERYCOMPLICATED = 15836
    ROMANTICCOMBO_JUSTFRIENDS = 77633
    ROMANTICCOMBO_JUSTGOODFRIENDS = 77634
    ROMANTICCOMBO_LOVEBIRDS = 15829
    ROMANTICCOMBO_LOVERS = 15837
    ROMANTICCOMBO_ROMANTICINTEREST = 15838
    ROMANTICCOMBO_SOULMATES = 15839
    ROMANTICCOMBO_SWEETHEARTS = 15840
    ROMANTICCOMBO_TERRIBLEMATCH = 15841
    ROMANTICCOMBO_TOTALOPPOSITES = 15842
    SECRETAGENT_DEFEATEDSUPERVILLAIN = 99522
    SECRETAGENT_EXPOSEDASSUPERVILLAIN = 38788
    SECRETAGENT_INVESTIGATED = 37066
    SECRETAGENT_KNOWNSUPERVILLAIN = 38790
    SHORTERMBITS_MINDPOWERS_ALLURINGVISAGE_SOCIALENCOURAGE = 150062
    SHORTTERM_INFIGHTWITH = 15845
    SHORTTERM_INQUARRELWITH = 15846
    SHORTTERM_JUSTBROKEUPORDIVORCED = 97332
    SHORTTERM_JUSTSAIDGOODBYE = 99780
    SHORTTERM_RECENTFIRSTKISS = 77371
    SHORTTERM_RECENTNEGATIVESOCIAL = 99712
    SHORTTERM_SNOOPEDINJOURNAL = 160252
    SHORTTERMBIT_SOCIALMEDIACAREER_REPRESENT = 145918
    SHORTTERMBITS_ARGUMENTS_HADARGUMENT = 162652
    SHORTTERMBITS_CLUBS_NEWMEMBER_GREETED = 130611
    SHORTTERMBITS_KICKEDOUT_INAPPROPRIATEBEHAVIOR = 129869
    SHORTTERMBITS_QUICKSOCIAL_HUG_NOTVISIBLE = 77250
    SHORTTERMBITS_QUICKSOCIAL_KISS_NOTVISIBLE = 77251
    SHORTTERMBITS_QUICKSOCIAL_SHOWFUNNYVIDEO_NOTVISIBLE = 77252
    SHORTTERMBITS_RESTUARANTS_DINING = 132610
    SHORTTERMBITS_TREADMILL_ROCK_CLIMBINGWALL_BEATHIGHSCORE = 167893
    SIMTOPET_00_DESPISED = 159231
    SIMTOPET_01_DISLIKED = 159232
    SIMTOPET_02_ACQUAINTANCE = 159233
    SIMTOPET_03_FRIEND = 159236
    SIMTOPET_04_GOODFRIEND = 159234
    SIMTOPET_05_COMPANION = 159235
    SIMTOPET_INDIFFERENT_NEUTRALBIT = 159230
    SITUATION_BIT_BIRTHDAYGUEST = 38420
    SITUATION_BIT_WEDDINGCOUPLE = 38422
    SITUATION_BIT_WEDDINGGUEST = 38421
    SITUATION_BIT_WELCOMEWAGONGUEST = 120016
    SPECIALBITS_ARCHENEMIES = 26561
    SPECIALBITS_DECLAREDARCHENEMY = 26566
    SPECIALBITS_ENEMY = 26560
    SPECIALBITS_GREETED = 122768
    TENANT = 148657
    TODDLER_CAREDEPENDENTEFFECTIVE = 155923
    TODDLER_CAREGIVEREFFECTIVE = 155918
    TODDLER_NOTPARENT_CAREDEPENDENT = 152851
    TODDLER_NOTPARENT_CAREGIVER = 146488
    TODDLER_STRANGER = 141125
    VAMPIRE_MASTER = 149548
    VAMPIRE_OFFSPRING = 149549
    SOCIALCONTEXT_AWKWARDNESS_AWKWARD = 24089
    SOCIALCONTEXT_AWKWARDNESS_CASUAL = 115902
    SOCIALCONTEXT_AWKWARDNESS_VERYAWKWARD = 24090
    SOCIALCONTEXT_CASUAL = 24032
    SOCIALCONTEXT_FRIENDSHIP_ABHORRENT = 24088
    SOCIALCONTEXT_FRIENDSHIP_DISTASTEFUL = 24086
    SOCIALCONTEXT_FRIENDSHIP_FRIENDLY = 24085
    SOCIALCONTEXT_FRIENDSHIP_OFFENSIVE = 24087
    SOCIALCONTEXT_FUN_BORING = 24081
    SOCIALCONTEXT_FUN_CASUAL = 115903
    SOCIALCONTEXT_FUN_FUNNY = 24077
    SOCIALCONTEXT_FUN_HILARIOUS = 24079
    SOCIALCONTEXT_FUN_INSUFFERABLYTEDIOUS = 24083
    SOCIALCONTEXT_FUN_TEDIOUS = 24082
    SOCIALCONTEXT_INTERROGATIONTABLE_CALM = 103962
    SOCIALCONTEXT_INTERROGATIONTABLE_DEFENSIVE = 103961
    SOCIALCONTEXT_INTERROGATIONTABLE_FRIENDLY = 103960
    SOCIALCONTEXT_INTERROGATIONTABLE_FURIOUS = 103959
    SOCIALCONTEXT_INTERROGATIONTABLE_SHY = 103958
    SOCIALCONTEXT_INTERROGATIONTABLE_SMUG = 104781
    SOCIALCONTEXT_INTERROGATIONTABLE_SUSPICIOUS = 103957
    SOCIALCONTEXT_INTERROGATIONTABLE_TENSE = 103956
    SOCIALCONTEXT_INTERROGATIONTABLE_TENSEDEFAULT = 105228
    SOCIALCONTEXT_INTERROGATIONTABLE_TERRIFIED = 103636
    SOCIALCONTEXT_INTERROGATIONTABLE_VERYWORRIED = 103955
    SOCIALCONTEXT_INTERROGATIONTABLE_WORRIED = 103953
    SOCIALCONTEXT_RETAIL_MILDLYINTERESTED = 111602
    SOCIALCONTEXT_RETAIL_UNINTERESTED = 111600
    SOCIALCONTEXT_RETAIL_VERYINTERESTED = 111601
    SOCIALCONTEXT_ROMANCE_AMOROUS = 24076
    SOCIALCONTEXT_ROMANCE_CASUAL = 115904
    SOCIALCONTEXT_ROMANCE_STEAMY = 24080
    SOCIALCONTEXT_ROMANCE_SUGGESTIVE = 24078
    BASEMENTAL_DEALER_COCAINE_COMPANION = 2554142113
    WW_POTENTIAL_PREGNANCY_PARENT = 3489948750
    WW_KNOWS_ABOUT_TEEN_PREGNANCY = 4092116363
    WW_JUST_HAD_SEX = 297233635
    WW_KNOWS_SEX_FANTASY = 470160556
