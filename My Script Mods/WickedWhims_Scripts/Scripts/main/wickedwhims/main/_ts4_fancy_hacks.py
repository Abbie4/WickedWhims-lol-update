from reservation.reservation_mixin import ReservationMixin
from turbolib.injector_util import inject

@inject(ReservationMixin, 'on_reset_get_interdependent_reset_records')
def _wickedwhims_on_reset_get_interdependent_reset_records_prevent_error(original, self, *args, **kwargs):
    try:
        return original(self, *args, **kwargs)
    except:
        return

