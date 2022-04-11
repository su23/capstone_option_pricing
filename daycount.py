from datetime import date, datetime, timedelta

#super-simple daycount implementation: assuming every year has 365.25 days
#thus for non-leap year year fraction of 1 year is a bit less than one and for leap year - a bit more
#at least year fraction function is monotonous
daycount_convention = 365.25

def calc_year_fraction_from_dates(start: date, end: date) -> float:
    assert start <= end
    return (end - start).days / daycount_convention


def convert_year_fraction_to_date(as_of_date: date, year_fraction: float) -> float:
    assert year_fraction >= 0
    days_to_add = round(year_fraction * daycount_convention)
    return as_of_date + timedelta(days=days_to_add)
    