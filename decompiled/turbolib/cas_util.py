'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''
from buffs.appearance_modifier.appearance_modifier import AppearanceModifierType
from cas.cas import get_caspart_bodytype, get_buff_from_part_ids
from protocolbuffers import Outfits_pb2, S4Common_pb2
from sims.outfits.outfit_enums import OutfitCategory, BodyType
from sims.outfits.outfit_utils import get_maximum_outfits_for_category
from turbolib.manager_util import TurboManagerUtil

class TurboCASUtil:
    __qualname__ = 'TurboCASUtil'
    __doc__ = '\
    TurboCASUtil class is used for any CAS related functions outside direct Sim object manipulation or for special CAS related tools.\
    '

    class OutfitCategory:
        __qualname__ = 'TurboCASUtil.OutfitCategory'
        __doc__ = '\
        Direct copy of the original native OutfitCategory enum class.\
        Use this class enum variables to refer to sim outfit category.\
        '

        def _get_outfit_category(*args):
            try:
                return OutfitCategory(args[0])
            except:
                return

        CURRENT_OUTFIT = _get_outfit_category(-1)
        EVERYDAY = _get_outfit_category(0)
        FORMAL = _get_outfit_category(1)
        ATHLETIC = _get_outfit_category(2)
        SLEEP = _get_outfit_category(3)
        PARTY = _get_outfit_category(4)
        BATHING = _get_outfit_category(5)
        CAREER = _get_outfit_category(6)
        SITUATION = _get_outfit_category(7)
        SPECIAL = _get_outfit_category(8)
        SWIMWEAR = _get_outfit_category(9)

        @staticmethod
        def get_outfit_category(outfit_category_id):
            '''
            Returns native OutfitCategory instance.
            :param outfit_category_id: int -> outfit category id
            :return: OutfitCategory -> native OutfitCategory instance of given outfit category id
            '''
            return OutfitCategory(int(outfit_category_id))

        @staticmethod
        def get_maximum_outfits_for_outfit_category(outfit_category):
            '''
            Returns maximum amount of outfits for an outfit category.
            :param outfit_category: OutfitCategory -> outfit category
            :return: int -> maximum number of outfits for the passed outfit category
            '''
            return get_maximum_outfits_for_category(outfit_category)

    class BodyType:
        __qualname__ = 'TurboCASUtil.BodyType'
        __doc__ = '\
        Direct copy of the original native BodyType enum class.\
        Use this class enum variables to refer to sim body types.\
        '

        def _get_body_type(*args):
            try:
                return BodyType(args[0])
            except:
                return BodyType.NONE

        NONE = _get_body_type(0)
        HAT = _get_body_type(1)
        HAIR = _get_body_type(2)
        HEAD = _get_body_type(3)
        TEETH = _get_body_type(4)
        FULL_BODY = _get_body_type(5)
        UPPER_BODY = _get_body_type(6)
        LOWER_BODY = _get_body_type(7)
        SHOES = _get_body_type(8)
        CUMMERBUND = _get_body_type(9)
        EARRINGS = _get_body_type(10)
        GLASSES = _get_body_type(11)
        NECKLACE = _get_body_type(12)
        GLOVES = _get_body_type(13)
        WRIST_LEFT = _get_body_type(14)
        WRIST_RIGHT = _get_body_type(15)
        LIP_RING_LEFT = _get_body_type(16)
        LIP_RING_RIGHT = _get_body_type(17)
        NOSE_RING_LEFT = _get_body_type(18)
        NOSE_RING_RIGHT = _get_body_type(19)
        BROW_RING_LEFT = _get_body_type(20)
        BROW_RING_RIGHT = _get_body_type(21)
        INDEX_FINGER_LEFT = _get_body_type(22)
        INDEX_FINGER_RIGHT = _get_body_type(23)
        RING_FINGER_LEFT = _get_body_type(24)
        RING_FINGER_RIGHT = _get_body_type(25)
        MIDDLE_FINGER_LEFT = _get_body_type(26)
        MIDDLE_FINGER_RIGHT = _get_body_type(27)
        FACIAL_HAIR = _get_body_type(28)
        LIPS_TICK = _get_body_type(29)
        EYE_SHADOW = _get_body_type(30)
        EYE_LINER = _get_body_type(31)
        BLUSH = _get_body_type(32)
        FACEPAINT = _get_body_type(33)
        EYEBROWS = _get_body_type(34)
        EYECOLOR = _get_body_type(35)
        SOCKS = _get_body_type(36)
        MASCARA = _get_body_type(37)
        SKINDETAIL_CREASE_FOREHEAD = _get_body_type(38)
        SKINDETAIL_FRECKLES = _get_body_type(39)
        SKINDETAIL_DIMPLE_LEFT = _get_body_type(40)
        SKINDETAIL_DIMPLE_RIGHT = _get_body_type(41)
        TIGHTS = _get_body_type(42)
        SKINDETAIL_MOLE_LIP_LEFT = _get_body_type(43)
        SKINDETAIL_MOLE_LIP_RIGHT = _get_body_type(44)
        TATTOO_ARM_LOWER_LEFT = _get_body_type(45)
        TATTOO_ARM_UPPER_LEFT = _get_body_type(46)
        TATTOO_ARM_LOWER_RIGHT = _get_body_type(47)
        TATTOO_ARM_UPPER_RIGHT = _get_body_type(48)
        TATTOO_LEG_LEFT = _get_body_type(49)
        TATTOO_LEG_RIGHT = _get_body_type(50)
        TATTOO_TORSO_BACK_LOWER = _get_body_type(51)
        TATTOO_TORSO_BACK_UPPER = _get_body_type(52)
        TATTOO_TORSO_FRONT_LOWER = _get_body_type(53)
        TATTOO_TORSO_FRONT_UPPER = _get_body_type(54)
        SKINDETAIL_MOLE_CHEEK_LEFT = _get_body_type(55)
        SKINDETAIL_MOLE_CHEEK_RIGHT = _get_body_type(56)
        SKINDETAIL_CREASE_MOUTH = _get_body_type(57)
        SKIN_OVERLAY = _get_body_type(58)
        FUR_BODY = _get_body_type(59)
        EARS = _get_body_type(60)
        TAIL = _get_body_type(61)
        FUR_EARS = _get_body_type(62)
        FUR_TAIL = _get_body_type(63)
        OCCULT_BROW = _get_body_type(64)
        OCCULT_EYE_SOCKET = _get_body_type(65)
        OCCULT_EYE_LID = _get_body_type(66)
        OCCULT_MOUTH = _get_body_type(67)
        OCCULT_LEFT_CHEEK = _get_body_type(68)
        OCCULT_RIGHT_CHEEK = _get_body_type(69)
        OCCULT_NECK_SCAR = _get_body_type(70)
        FOREARM_SCAR = _get_body_type(71)
        ACNE = _get_body_type(72)

        @staticmethod
        def get_body_type(body_type_id):
            '''
            Returns native BodyType instance.
            :param body_type_id: int -> outfit body type id
            :return: BodyType -> native BodyType instance of given outfit body type id
            '''
            return BodyType(int(body_type_id))

    class Outfit:
        __qualname__ = 'TurboCASUtil.Outfit'
        __doc__ = '\
        Utilities related to outfit functions.\
        '

        @staticmethod
        def is_cas_part_loaded(cas_part_id):
            '''
            Returns if outfit cas part exists.
            If native get_caspart_bodytype method can't return proper body type for the passed cas part, that cas part doesn't exist.
            :param cas_part_id: int -> outfit cas part id
            :return: bool -> if passed outfit cas part exist
            '''
            return get_caspart_bodytype(int(cas_part_id)) > 0

        @staticmethod
        def get_cas_part_body_type_id(cas_part_id):
            '''
            Returns outfit cas part outfit body type id.
            :param cas_part_id: int -> outfit cas part id
            :return: int -> returns passed outfit cas part body type id
            '''
            return get_caspart_bodytype(cas_part_id)

        @staticmethod
        def get_cas_part_buff_id(cas_part_id):
            '''
            Returns outfit cas part buff id.
            :param cas_part_id: int -> outfit cas part id
            :return: int -> returns passed outfit cas part buff id
            '''
            return get_buff_from_part_ids(cas_part_id)

    class AppearanceModifier:
        __qualname__ = 'TurboCASUtil.AppearanceModifier'
        __doc__ = '\
        Utilities related to appearance modifiers.\
        '

        class AppearanceModifierType:
            __qualname__ = 'TurboCASUtil.AppearanceModifier.AppearanceModifierType'
            __doc__ = '\
            Direct copy of the original native AppearanceModifierType enum class.\
            Use this class enum variables to refer to appearance modifier types.\
            '
            SET_CAS_PART = AppearanceModifierType.SET_CAS_PART
            RANDOMIZE_BODY_TYPE_COLOR = AppearanceModifierType.RANDOMIZE_BODY_TYPE_COLOR
            RANDOMIZE_SKINTONE_FROM_TAGS = AppearanceModifierType.RANDOMIZE_SKINTONE_FROM_TAGS
            GENERATE_OUTFIT = AppearanceModifierType.GENERATE_OUTFIT

        @staticmethod
        def get_sim_appearance_modifiers(sim_identifier, appearance_modifier_type, modifiers_guid=-1):
            '''
            Returns sim appearance modifiers.
            :param sim_identifier: int or SimInfo or Sim -> sim identifier
            :param appearance_modifier_type: AppearanceModifierType -> appearance modifier type to look for
            :param modifiers_guid: int -> guid of appearance modifier info to limit results to
            :return: tuple -> sim active appearance modifiers
            '''
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier, allow_base_wrapper=True)
            if not sim_info:
                return tuple()
            if sim_info.appearance_tracker._active_appearance_modifier_infos is None:
                return tuple()
            if appearance_modifier_type not in sim_info.appearance_tracker._active_appearance_modifier_infos:
                return tuple()
            modifiers = list()
            for appearance_modifier in sim_info.appearance_tracker._active_appearance_modifier_infos[appearance_modifier_type]:
                if modifiers_guid != -1 and appearance_modifier.guid != modifiers_guid:
                    pass
                if not appearance_modifier.should_display:
                    pass
                modifiers.append(appearance_modifier.modifier)
            return tuple(modifiers)

    class Club:
        __qualname__ = 'TurboCASUtil.Club'
        __doc__ = '\
        Utilities related to club outfit functions.\
        '

        @staticmethod
        def remove_sim_apprearance_modifiers(sim_identifier, club_gathering):
            '''
            Removes sim club gathering apprearance modifiers.
            :param sim_identifier: int or SimInfo or Sim -> sim identifier
            :param club_gathering: ClubGatheringSituation -> club gathering situation instance
            :return: bool -> if the attempt to remove apprearance modifiers happened
            '''
            if not club_gathering:
                return False
            sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier, allow_base_wrapper=True)
            if not sim_info:
                return False
            club_gathering._remove_apprearance_modifiers(sim_info)
            return True

    class OutfitEditor:
        __qualname__ = 'TurboCASUtil.OutfitEditor'
        __doc__ = '\
        OutfitEditor class is used to edit sims outfits.\
        '

        def __init__(self, sim_identifier, outfit_category_and_index=None, outfit_body_parts=None):
            '''
            :param sim_identifier: int or SimInfo or Sim -> sim identifier
            :param outfit_category_and_index: tuple(OutfitCategory, int) -> outfit category and outfit index, if None the current outfit of sim is used
            :param outfit_body_parts: dict -> outfit packed as body types paired with outfit cas parts, if None Sim outfit body parts are used
            '''
            self.sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier, allow_base_wrapper=True)
            if not self.sim_info:
                raise RuntimeError('Sim identification is missing.')
            self.outfit_category_and_index = outfit_category_and_index or self.sim_info.get_current_outfit()
            self.outfit_data = self.sim_info.get_outfit(self.outfit_category_and_index[0], self.outfit_category_and_index[1])
            if self.outfit_data is None:
                raise RuntimeError('Sim outfit data is missing.')
            self.outfit_identifier = self._get_outfit_identifier(self.outfit_data.body_types, self.outfit_data.part_ids)
            if outfit_body_parts:
                for (key, value) in outfit_body_parts.items():
                    while not isinstance(key, int) or not isinstance(value, int):
                        raise RuntimeError('outfit_body_parts contains non-integer variables.')
                self.outfit_body_types = list(outfit_body_parts.keys())
                self.outfit_part_ids = list(outfit_body_parts.values())
            else:
                if not self.outfit_data.part_ids or not self.outfit_data.body_types:
                    raise RuntimeError('Sim outfit data is invalid.')
                self.outfit_body_types = list(self.outfit_data.body_types)
                self.outfit_part_ids = list(self.outfit_data.part_ids)
                if len(self.outfit_body_types) != len(self.outfit_part_ids):
                    raise RuntimeError('Sim outfit data is invalid.')

        def _get_outfit_identifier(self, body_types, part_ids):
            return hash(frozenset(TurboCASUtil.Special.pack_outfit(body_types, part_ids).items()))

        def get_outfit_category_and_index(self):
            '''
            :return: tuple(OutfitCategory, int) -> used outfit category and outfit index
            '''
            return self.outfit_category_and_index

        def add_cas_part(self, bodytype, cas_part_id):
            '''
            :param bodytype: int or BodyType -> outfit body type
            :param cas_part_id: int -> cas part id
            :return: bool -> adding cas part success result
            '''
            if bodytype in self.outfit_body_types:
                self.remove_body_type(bodytype)
            self.outfit_body_types.append(bodytype)
            self.outfit_part_ids.append(cas_part_id)
            return True

        def has_body_type(self, bodytype):
            '''
            :param bodytype: int or BodyType -> outfit body type
            :return: bool -> if outfit has the passed body type
            '''
            return bodytype in self.outfit_body_types

        def remove_body_type(self, bodytype):
            '''
            :param bodytype: int or BodyType -> outfit body type
            :return: bool -> if passed body type was removed from the outfit
            '''
            if bodytype not in self.outfit_body_types:
                return False
            for outfit_items_index in range(len(self.outfit_body_types)):
                while self.outfit_body_types[outfit_items_index] == bodytype:
                    del self.outfit_part_ids[outfit_items_index]
                    del self.outfit_body_types[outfit_items_index]
                    return True
            return False

        def get_body_types(self):
            return tuple(self.outfit_body_types)

        def has_cas_part(self, cas_id):
            '''
            :param cas_id: int -> outfit cas part id
            :return: bool -> if outfit has the passed cas part id
            '''
            return cas_id in self.outfit_part_ids

        def remove_cas_part(self, cas_id):
            '''
            :param cas_id: int -> outfit cas part id
            :return: bool -> if passed cas part id was removed from the outfit
            '''
            cas_part_occurrences = self.outfit_part_ids.count(cas_id)
            for _ in range(cas_part_occurrences):
                for outfit_items_index in range(len(self.outfit_body_types)):
                    while self.outfit_part_ids[outfit_items_index] == cas_id:
                        del self.outfit_part_ids[outfit_items_index]
                        del self.outfit_body_types[outfit_items_index]
                        break
            return bool(cas_part_occurrences)

        def get_cas_parts(self):
            return tuple(self.outfit_part_ids)

        def apply(self, apply_to_outfit_category=None, skip_client_update=False):
            '''
            Apply outfit editor current state to sim outfit data.
            :param apply_to_outfit_category: OutfitCategory -> outfit category, if None the passed in init outfit is used
            :param skip_client_update: bool -> skip resending sim outfit data to the client
            '''
            outfits_msg = self.sim_info.save_outfits()
            for outfit in outfits_msg.outfits:
                if apply_to_outfit_category:
                    can_apply = int(outfit.category) == int(apply_to_outfit_category)
                else:
                    can_apply = int(outfit.category) == int(self.outfit_category_and_index[0]) and (outfit.outfit_id == self.outfit_data.outfit_id and self._get_outfit_identifier(outfit.body_types_list.body_types, outfit.parts.ids) == self.outfit_identifier)
                while can_apply:
                    outfit.parts = S4Common_pb2.IdList()
                    outfit.parts.ids.extend(self.outfit_part_ids)
                    outfit.body_types_list = Outfits_pb2.BodyTypesList()
                    outfit.body_types_list.body_types.extend(self.outfit_body_types)
                    if not apply_to_outfit_category:
                        break
            self.sim_info._base.outfits = outfits_msg.SerializeToString()
            if skip_client_update is False:
                self.sim_info.resend_outfits()

    class Special:
        __qualname__ = 'TurboCASUtil.Special'
        __doc__ = '\
        Special utilities related to outfit functions.\
        '

        @staticmethod
        def pack_outfit(body_types, cas_parts):
            '''
            Packs list of body types and list of cas part ids into pairs as a dictionary.
            :param body_types: [int or BodyType] -> list of outfit body types
            :param cas_parts: [int] -> list of outfit cas part ids
            :return: dict -> packed dictionary of body types and cas parts
            '''
            return dict(zip(list(body_types), list(cas_parts)))

        @staticmethod
        def unpack_outfit(body_parts):
            '''
            Look at pack_outfit method for more context.
            :param body_parts: dict -> outfit body types paired with outfit cas parts
            :return: tuple([int], [int]) -> list of outfit body types and list of outfit cas parts
            '''
            body_types = list()
            cas_parts = list()
            for (body_type, cas_part) in body_parts.items():
                body_types.append(body_type)
                cas_parts.append(cas_part)
            return (body_types, cas_parts)

