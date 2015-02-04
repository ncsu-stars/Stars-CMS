import time
import pytz.reference
import datetime

def academic_year(t):
    if isinstance(t, float):
        t = time.localtime(t)
    if isinstance(t, time.struct_time):
        month = t.tm_mon
        year = t.tm_year
    else:
        month = t.month
        year = t.year

    if month > 6:
        return year
    else:
        return year - 1


def get_current_time():
    return datetime.datetime.now(tz=pytz.reference.LocalTimezone())
