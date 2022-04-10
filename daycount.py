from datetime import date

#super-simple daycount implementation: assuming every year has 365.25 days
#thus for non-leap year year fraction of 1 year is a bit less than one and for leap year - a bit more
#at least year fraction function is monotonous
daycount_convention = 365.25

def calc_year_fraction_from_dates(start: date, end: date):
    assert start <= end
    return (end - start).days / daycount_convention