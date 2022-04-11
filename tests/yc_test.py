from pytest import *

import sys
sys.path.append('../')

from datetime import date
from shared_constants import test_as_of_date
from yc import *

class MockYieldCurve(ICurve):
    def __init__(self, const_disc_fact: float=0.9, const_rate: float=0.01, as_of_date: date = test_as_of_date):
        self.const_disc_fact = const_disc_fact
        self.const_rate = const_rate
        self.as_of_date = as_of_date
      
    def get_rate(self, date: date) -> float:
        return self.const_rate;
    
    def get_rate_yf(self, year_fraction: float) -> float:
        return self.const_rate;
    
    def get_disc_fact(self, date: date) -> float:
        return self.const_disc_fact;
    
    def get_disc_fact_yf(self, year_fraction: float) -> float:
        return self.const_disc_fact;
    
    def get_as_of_date(self) -> date:
        return self.as_of_date



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
    as_of_date = date(2014, 1, 20)
    one_year_date = date(2015, 1, 20)
    curve = YieldCurve(as_of_date)
    rate_one_year = curve.get_rate(one_year_date)
    year_fraction_one_year = calc_year_fraction_from_dates(as_of_date, one_year_date)
    expected_df_one_year = np.exp(-rate_one_year * year_fraction_one_year)
    
    # act
    df_zero_days = curve.get_disc_fact(date(2014, 1, 20))
    df_one_year = curve.get_disc_fact(date(2015, 1, 20))
    
    # assert
    assert df_zero_days == 1, f"expected {1} got {df_zero_days}"
    assert df_one_year < 1, f"expected less than 1 got {df_one_year}"
    assert df_one_year == expected_df_one_year, f"expected {expected_df_one_year} than 0.8 got {df_one_year}"
    
def yc_disc_fact_tests_year_fraction():
    # arrange
    as_of_date = date(2014, 1, 20)
    
    curve = YieldCurve(as_of_date)
    
    one_day_date = date(2014, 1, 21)
    rate_one_day = curve.get_rate(one_day_date)
    year_fraction_one_day = calc_year_fraction_from_dates(as_of_date, one_day_date)
    expected_df_one_day = np.exp(-rate_one_day * year_fraction_one_day)
    
    one_year_date = date(2015, 1, 20)
    rate_one_year = curve.get_rate(one_year_date)
    year_fraction_one_year = calc_year_fraction_from_dates(as_of_date, one_year_date)
    expected_df_one_year = np.exp(-rate_one_year * year_fraction_one_year)
    
    # act
    df_zero_days = curve.get_disc_fact_yf(0)
    df_one_day = curve.get_disc_fact_yf(year_fraction_one_day)
    df_one_year = curve.get_disc_fact_yf(year_fraction_one_year)
    
    # assert
    assert df_zero_days == 1, f"expected {1} got {df_zero_days}"
    
    assert df_one_day < 1, f"expected less than 1 got {df_one_year}"
    assert df_one_day == expected_df_one_day, f"expected {expected_df_one_year} than 0.8 got {df_one_year}"

    
    assert df_one_year < 1, f"expected less than 1 got {df_one_year}"
    assert df_one_year == expected_df_one_year, f"expected {expected_df_one_year} than 0.8 got {df_one_year}"

    
def yc_returns_as_of_date():
    # arrange
    as_of_date = date(2022, 1, 1)
    curve = YieldCurve(as_of_date)
    
    # act
    actual = curve.get_as_of_date()
    
    # assert
    assert actual == as_of_date, f"Expected AsOfDate {as_of_date} but got {actual}"

    
def yc_default_mock_tests():
    # arrange
    
    a_date = date(2022, 4, 10)
    mock = MockYieldCurve()
    
    # act
    df = mock.get_disc_fact(a_date)
    rate = mock.get_rate(a_date)
    
    # assert
    assert df == 0.9, f"Expected default DF of 0.9, got {df}"
    assert rate == 0.01, f"Expected default rate of 0.01, got {rate}"
    
def yc_semi_default_mock_tests():
    # arrange
    
    a_date = date(2022, 4, 10)
    mock = MockYieldCurve(0.42)
    
    # act
    df = mock.get_disc_fact(a_date)
    rate = mock.get_rate(a_date)
    
    # assert
    assert df == 0.42, f"Expected DF of 0.42, got {df}"
    assert rate == 0.01, f"Expected default rate of 0.01, got {rate}"    
    
def yc_custom_mock_tests():
    # arrange
    
    a_date = date(2022, 4, 10)
    mock = MockYieldCurve(0.42, 0.11)
    
    # act
    df = mock.get_disc_fact(a_date)
    rate = mock.get_rate(a_date)
    
    # assert
    assert df == 0.42, f"Expected DF of 0.42, got {df}"
    assert rate == 0.11, f"Expected rate of 0.11, got {rate}"
    
def yc_default_mock_tests_year_fraction():
    # arrange
    
    a_date = date(2022, 4, 10)
    mock = MockYieldCurve()
    
    # act
    df = mock.get_disc_fact_yf(100)
    
    # assert
    assert df == 0.9, f"Expected default DF of 0.9, got {df}"

    
def mock_curve_returns_test_as_of_date():
    # arrange
    curve = MockYieldCurve()
    
    # act
    actual = curve.get_as_of_date()
    
    # assert
    assert actual == test_as_of_date, f"Expected AsOfDate {test_as_of_date} but got {actual}"

def all_yc_tests():
    yc_rate_tests()
    yc_disc_fact_tests()
    yc_returns_as_of_date()
    yc_disc_fact_tests_year_fraction()
    yc_default_mock_tests()
    yc_semi_default_mock_tests()
    yc_custom_mock_tests()
    yc_default_mock_tests_year_fraction()
    mock_curve_returns_test_as_of_date()
    
    
all_yc_tests()

    
