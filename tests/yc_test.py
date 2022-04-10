from pytest import *

import sys
sys.path.append('../')

from datetime import date
from yc import *


def yc_rate_tests():
    # arrange
    c = UnbasedYieldCurve()
    
    # act
    generic_rate1 = c.get_yc_rate(date(2014, 1, 20), date(2014, 1, 25))
    generic_rate2 = c.get_yc_rate(date(2014, 1, 20), date(2014, 5, 25))
    generic_rate3 = c.get_yc_rate(date(2014, 1, 20), date(2018, 5, 25))
    
    exact_curve = YieldCurve(date(2014, 1, 20))
    
    exact_rate1 = exact_curve.get_rate(date(2014, 1, 25))
    exact_rate2 = exact_curve.get_rate(date(2014, 5, 25))
    exact_rate3 = exact_curve.get_rate(date(2018, 5, 25))
    
    
    print(generic_rate1)
    print(generic_rate2)
    print(generic_rate3)
    
    assert generic_rate1==exact_rate1, f"expected {generic_rate1} got {exact_rate1}"
    assert generic_rate2==exact_rate2, f"expected {generic_rate2} got {exact_rate2}"
    assert generic_rate3==exact_rate3, f"expected {generic_rate3} got {exact_rate3}"
    
def yc_disc_fact_tests():
    # arrange
    base_date = date(2014, 1, 20)
    one_year_date = date(2015, 1, 20)
    curve = YieldCurve(base_date)
    rate_one_year = curve.get_rate(one_year_date)
    year_fraction_one_year = calc_year_fraction_from_dates(base_date, one_year_date)
    expected_df_one_year = np.exp(-rate_one_year * year_fraction_one_year)
    
    # act
    df_zero_days = curve.get_disc_fact(date(2014, 1, 20))
    df_one_year = curve.get_disc_fact(date(2015, 1, 20))
    
    # assert
    assert df_zero_days == 1, f"expected {1} got {df_zero_days}"
    assert df_one_year < 1, f"expected less than 1 got {df_one_year}"
    assert df_one_year == expected_df_one_year, f"expected {expected_df_one_year} than 0.8 got {df_one_year}"

    
def all_yc_tests():
    yc_rate_tests()
    yc_disc_fact_tests()
    
    
all_yc_tests()

    
