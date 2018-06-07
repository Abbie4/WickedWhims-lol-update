'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''from reservation.reservation_mixin import ReservationMixinfrom turbolib.injector_util import inject
@inject(ReservationMixin, 'on_reset_get_interdependent_reset_records')
def _wickedwhims_on_reset_get_interdependent_reset_records_prevent_error(original, self, *args, **kwargs):
    try:
        return original(self, *args, **kwargs)
    except:
        return
