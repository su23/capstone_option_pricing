from datetime import date
from pytest import *

import sys
sys.path.append('../')

from daycount import *

def test_year_fractions():

    # arrange
    expected_yf_day = 1/daycount_convention
    
    # act
    yf_year = calc_year_fraction_from_dates(date(2022, 4, 10), date(2023, 4, 10))
    yf_leap_year = calc_year_fraction_from_dates(date(2020, 1, 1), date(2021, 1, 1))
    
    yf_day = calc_year_fraction_from_dates(date(2022, 4, 10), date(2022, 4, 11))
    yf_leap_day = calc_year_fraction_from_dates(date(2020, 1, 1), date(2020, 1, 2))
    
    yf_zero = calc_year_fraction_from_dates(date(2022, 4, 10), date(2022, 4, 10))
    
    
    
    # assert
    assert yf_year == 365/daycount_convention, f"expected {365/daycount_convention} got {yf_year}"
    assert yf_leap_year == 366/daycount_convention, f"expected {366/daycount_convention} got {yf_leap_year}"
    
    assert yf_day == expected_yf_day, f"expected {expected_yf_day} got {yf_day}"
    assert yf_leap_day == expected_yf_day, f"expected {expected_yf_day} got {yf_leap_day}"
    
    assert yf_zero == 0, f"expected {0} got {yf_zero}"
    
    
def all_daycount_tests():
    test_year_fractions();
    
    
all_daycount_tests()

