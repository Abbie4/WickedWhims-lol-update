'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''from event_testing.tests import TestListfrom relationships.relationship_tests import RelationshipTestfrom turbolib.resource_util import TurboResourceUtilfrom turbolib.tunable_util import TurboTunableUtilPOLYGAMY_AFFORDANCE_LIST = ((25913, (15825, 15816, 15818, 15822)), (25914, (15825, 15816, 15818, 15822)), (25915, (15825, 15816, 15818, 15822)), (26165, (15825, 15816, 15818, 15822)), (25871, (15825, 15816, 15818, 15822)), (26164, (15825, 15816, 15818, 15822)), (130878, (15822, 15818, 15816, 15825)), (26130, (99429, 15825, 15818, 15816, 15822)), (26129, (99429, 15825, 15818, 15816, 15822)), (26159, (15825, 15816, 15818, 15822)), (26139, (15822,)), (145628, (15822,)), (99655, (15816, 15822, 99429)), (14091, (15822,)), (14092, (15822,)), (14093, (15822,)), (14094, (15822,)), (14552, (15822,)), (14554, (15822,)), (14553, (15822,)), (14555, (15822,)))HAS_DISABLED_INTERACTIONS_POLYGAMY_TESTS = False
def unlock_polygamy_for_interactions(value):
    global HAS_DISABLED_INTERACTIONS_POLYGAMY_TESTS
    if value is False or HAS_DISABLED_INTERACTIONS_POLYGAMY_TESTS is True:
        return
    affordance_manager = TurboResourceUtil.Services.get_instance_manager(TurboResourceUtil.ResourceTypes.INTERACTION)
    relationship_bits_manager = TurboResourceUtil.Services.get_instance_manager(TurboResourceUtil.ResourceTypes.RELATIONSHIP_BIT)
    for (affordance_id, remove_bits) in POLYGAMY_AFFORDANCE_LIST:
        affordance_instance = TurboResourceUtil.Services.get_instance_from_manager(affordance_manager, affordance_id)
        if affordance_instance is None:
            pass
        tests_list = list()
        for test in affordance_instance.test_globals:
            if isinstance(test, RelationshipTest) and test.prohibited_relationship_bits and len(test.prohibited_relationship_bits.match_any) > 0:
                new_match_any = list()
                for bit in test.prohibited_relationship_bits.match_any:
                    if bit.guid64 in remove_bits:
                        pass
                    new_match_any.append(bit)
                if not new_match_any:
                    pass
                prohibited_relationship_bits_dict = dict()
                for (dict_key, dict_value) in test.prohibited_relationship_bits:
                    prohibited_relationship_bits_dict[dict_key] = dict_value
                prohibited_relationship_bits_dict['match_any'] = frozenset(new_match_any)
                immutable_slots_class = TurboResourceUtil.Collections.get_immutable_slots_class(list(prohibited_relationship_bits_dict.keys()))
                prohibited_relationship_bits_slots = immutable_slots_class(prohibited_relationship_bits_dict)
                test.prohibited_relationship_bits = prohibited_relationship_bits_slots
            tests_list.append(test)
        if affordance_instance.guid64 == 26130 or affordance_instance.guid64 == 26129:
            prohibited_match_any = [TurboResourceUtil.Services.get_instance_from_manager(relationship_bits_manager, 15822), TurboResourceUtil.Services.get_instance_from_manager(relationship_bits_manager, 15825), TurboResourceUtil.Services.get_instance_from_manager(relationship_bits_manager, 15816)]
            tests_list.append(TurboTunableUtil.Tests.Relationship.get_relationship_test(prohibited_relationship_bits=dict(match_all=frozenset(), match_any=frozenset(prohibited_match_any))))
        if affordance_instance.guid64 == 26159:
            prohibited_match_any = [TurboResourceUtil.Services.get_instance_from_manager(relationship_bits_manager, 15825), TurboResourceUtil.Services.get_instance_from_manager(relationship_bits_manager, 15818), TurboResourceUtil.Services.get_instance_from_manager(relationship_bits_manager, 15816), TurboResourceUtil.Services.get_instance_from_manager(relationship_bits_manager, 15822)]
            tests_list.append(TurboTunableUtil.Tests.Relationship.get_relationship_test(prohibited_relationship_bits=dict(match_all=frozenset(), match_any=frozenset(prohibited_match_any))))
        affordance_instance.test_globals = TestList(tests_list)
    HAS_DISABLED_INTERACTIONS_POLYGAMY_TESTS = True
