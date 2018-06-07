'''
This file is part of WickedWhims, licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International public license (CC BY-NC-ND 4.0).
https://creativecommons.org/licenses/by-nc-nd/4.0/
https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

Copyright (c) TURBODRIVER <https://wickedwhimsmod.com/>
'''from sims.pregnancy.pregnancy_tracker import PregnancyTracker
def set_pregnancy_duration(days):
    if days <= 0:
        days = 1
    PregnancyTracker.PREGNANCY_RATE = round(0.05/days, 6)
