from sims.pregnancy.pregnancy_tracker import PregnancyTracker

def set_pregnancy_duration(days):
    if days <= 0:
        days = 1
    PregnancyTracker.PREGNANCY_RATE = round(0.05/days, 6)

