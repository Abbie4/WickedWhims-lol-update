'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''from turbolib.resource_util import TurboResourceUtil
def get_snippets_with_tag(*tag_names):
    snippet_list = list()
    tuning_snippets = TurboResourceUtil.Services.get_all_instances_from_manager(TurboResourceUtil.Services.get_instance_manager(TurboResourceUtil.ResourceTypes.SNIPPET))
    for (_, snipper_class) in tuning_snippets:
        for tag_name in tag_names:
            while hasattr(snipper_class, tag_name):
                snippet_list.append(snipper_class)
                break
    return tuple(snippet_list)
