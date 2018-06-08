from turbolib.manager_util import TurboManagerUtil
from turbolib.sim_util import TurboSimUtil

def get_sim_preferenced_genders(sim_identifier):
    sim_info = TurboManagerUtil.Sim.get_sim_info(sim_identifier)
    male_pref = TurboSimUtil.Gender.get_gender_preference(sim_info, TurboSimUtil.Gender.MALE)
    female_pref = TurboSimUtil.Gender.get_gender_preference(sim_info, TurboSimUtil.Gender.FEMALE)
    if male_pref < 5 and female_pref < 5:
        if TurboSimUtil.Gender.get_gender(sim_info) == TurboSimUtil.Gender.MALE:
            return (TurboSimUtil.Gender.FEMALE,)
        return (TurboSimUtil.Gender.MALE,)
    if abs(male_pref - female_pref) <= 20:
        return (TurboSimUtil.Gender.MALE, TurboSimUtil.Gender.FEMALE)
    if male_pref > female_pref:
        return (TurboSimUtil.Gender.MALE,)
    return (TurboSimUtil.Gender.FEMALE,)

