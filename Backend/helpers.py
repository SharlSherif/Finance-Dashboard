from datetime import timedelta
from datetime import datetime

def get_difference_between_dates(sdate, edate):
    print(sdate, edate)
    dates_between = []
    [s_year, s_month, s_day] = sdate.split('-')
    [e_year, e_month, e_day] = edate.split('-')
    sdate = datetime(int(s_year), int(s_month), int(s_day))   # start date
    edate = datetime(int(e_year), int(e_month), int(e_day))   # end date

    delta = edate - sdate       # as timedelta

    for i in range(delta.days):
        diff_date = sdate + timedelta(days=i)
        dates_between.append(diff_date)
    # remove first dates in the list because it's the starting date
    if len(dates_between) > 0:
        dates_between.pop(0)
    print(f"{len(dates_between)} dates difference")
    return dates_between


def currency_conversion(amount, currency):
    conversion_rate_USD = 15.6
    converted_amount = 0
    if currency == '$':
        converted_amount = round(amount*conversion_rate_USD)
    else:
        converted_amount = amount
    return converted_amount
# ? helpers