from pytest import *

import sys
sys.path.append('../')

from datetime import date
from shared_constants import test_as_of_date
from payoff import *
from yc_test import MockYieldCurve


class MockPayoff(IPayoff):
    
    def __init__(self, const_payoff: float = 42):
        self.const_payoff = const_payoff
    
    def calc_payoff(self, spot: float) -> float:
        return self.const_payoff
    

class MockDiscountedPayoff(IDiscountedPayoff):
    
    def __init__(self, const_discounted_payoff: float = 42, as_of_date: date = test_as_of_date):
        self.const_payoff = const_discounted_payoff
        self.as_of_date = as_of_date
    
    def calc_discounted_payoff(self, date: date, spot: float) -> float:
        return self.const_payoff
    
    def calc_discounted_payoff_yf(self, year_fraction: float, spot: float) -> float:
        return self.const_payoff

    def get_as_of_date(self) -> date:    
        return self.as_of_date
    


def test_otm_call_payoff():
    # arrange
    s = 10;
    k = 11;
    p = CallPayoff(k)
    
    # act
    payoff = p.calc_payoff(s)
    
    # assert
    assert payoff == 0, f"expected 0 but got {payoff}"
    
def test_atm_call_payoff():
    # arrange
    s = 10;
    k = 10;
    p = CallPayoff(k)
    
    # act
    payoff = p.calc_payoff(s)
    
    # assert
    assert payoff == 0, f"expected 0 but got {payoff}"

def test_itm_call_payoff():
    # arrange
    s = 42;
    k = 10;
    p = CallPayoff(k)
    
    # act
    payoff = p.calc_payoff(s)
    
    # assert
    assert payoff == 32, f"expected 0 but got {payoff}"


def test_otm_put_payoff():
    # arrange
    s = 11;
    k = 10;
    p = PutPayoff(k)
    
    # act
    payoff = p.calc_payoff(s)
    
    # assert
    assert payoff == 0, f"expected 0 but got {payoff}"
    
def test_atm_put_payoff():
    # arrange
    s = 10;
    k = 10;
    p = PutPayoff(k)
    
    # act
    payoff = p.calc_payoff(s)
    
    # assert
    assert payoff == 0, f"expected 0 but got {payoff}"

def test_itm_put_payoff():
    # arrange
    s = 10;
    k = 42;
    p = PutPayoff(k)
    
    # act
    payoff = p.calc_payoff(s)
    
    # assert
    assert payoff == 32, f"expected 0 but got {payoff}"
    
def test_default_mock_payoff():
    # arrange
    payoff = MockPayoff()
    
    # act
    actual_payoff = payoff.calc_payoff(33);
    
    # assert
    assert actual_payoff == 42, f"Expected default payoff of 42, got {actual_payoff}"

def test_custom_mock_payoff():
    # arrange
    payoff = MockPayoff(14)
    
    # act
    actual_payoff = payoff.calc_payoff(33);
    
    # assert
    assert actual_payoff == 14, f"Expected default payoff of 14, got {actual_payoff}"
    
    
def test_discounted_payoff():
    # arrange
    payoff = MockPayoff(11)
    curve = MockYieldCurve(0.42, 0.11)
    
    disc_payoff_obj = DiscountedPayoff(payoff, curve)
    
    a_date = date(2022, 4, 10)
    
    expected_disc_payoff = 11 * 0.42
    
    # act
    disc_payoff = disc_payoff_obj.calc_discounted_payoff(a_date, 1024768)
    
    # assert
    assert disc_payoff == expected_disc_payoff, f"Expected {expected_disc_payoff}, got {disc_payoff}"
    
def test_discounted_payoff_by_year_fraction():
    # arrange
    payoff = MockPayoff(11)
    curve = MockYieldCurve(0.42, 0.11)
    
    disc_payoff_obj = DiscountedPayoff(payoff, curve)
    
    expected_disc_payoff = 11 * 0.42
    
    # act
    disc_payoff = disc_payoff_obj.calc_discounted_payoff_yf(100, 1024768)
    
    # assert
    assert disc_payoff == expected_disc_payoff, f"Expected {expected_disc_payoff}, got {disc_payoff}"

def test_discounted_payoff_by_year_fraction_real_yield_curve():
    # arrange
    year_fraction = 2.07
    payoff = MockPayoff(11)
    curve = YieldCurve(date(2014, 1, 20))
    
    disc_fact = curve.get_disc_fact_yf(year_fraction)
    
    disc_payoff_obj = DiscountedPayoff(payoff, curve)
    
    expected_disc_payoff = 11 * disc_fact
    
    # act
    disc_payoff = disc_payoff_obj.calc_discounted_payoff_yf(year_fraction, 1024768)
    
    # assert
    assert disc_payoff == expected_disc_payoff, f"Expected {expected_disc_payoff}, got {disc_payoff}"

    
def discounted_payoff_returns_curves_as_of_date():
    # arrange
    payoff = MockPayoff(11)
    curve = MockYieldCurve(0.42, 0.11)
    
    disc_payoff_obj = DiscountedPayoff(payoff, curve)
   
    # act
    actual = disc_payoff_obj.get_as_of_date();
    
    # assert
    assert actual == test_as_of_date, f"Expected AsOfDate {test_as_of_date} but got {actual}"
    
def mock_discounted_payoff_returns_parameter_payoff():
    # arrange
    payoff = MockDiscountedPayoff(42)
    a_date = date(2022, 4, 10)
    
    # act
    actual = payoff.calc_discounted_payoff(a_date, 212);
    
    # assert
    assert actual == 42, f"Expected 42 but got {actual}"
    
def mock_discounted_payoff_returns_parameter_payoff_for_year_fraction():
    # arrange
    payoff = MockDiscountedPayoff(42)
    a_date = date(2022, 4, 10)
    
    # act
    actual = payoff.calc_discounted_payoff_yf(2.0, 212);
    
    # assert
    assert actual == 42, f"Expected 42 but got {actual}"

    
def mock_discounted_payoff_returns_test_as_of_date_by_default():
    # arrange
    payoff = MockDiscountedPayoff()
    
    # act
    actual = payoff.get_as_of_date();
    
    # assert
    assert actual == test_as_of_date, f"Expected AsOfDate {test_as_of_date} but got {actual}"
    
def mock_discounted_payoff_returns_custom_as_of_date():
    # arrange
    custom_date = date(2022, 4, 1)
    payoff = MockDiscountedPayoff(42, custom_date)
    
    # act
    actual = payoff.get_as_of_date();
    
    # assert
    assert actual == custom_date, f"Expected AsOfDate {custom_date} but got {actual}"


def all_payoff_tests():
    test_otm_call_payoff()
    test_atm_call_payoff()
    test_itm_call_payoff()
    test_otm_put_payoff()
    test_atm_put_payoff()
    test_itm_put_payoff()
    test_default_mock_payoff()
    test_custom_mock_payoff()
    test_discounted_payoff()
    test_discounted_payoff_by_year_fraction()
    test_discounted_payoff_by_year_fraction_real_yield_curve()
    discounted_payoff_returns_curves_as_of_date()
    mock_discounted_payoff_returns_parameter_payoff()
    mock_discounted_payoff_returns_parameter_payoff_for_year_fraction()
    mock_discounted_payoff_returns_test_as_of_date_by_default()
    mock_discounted_payoff_returns_custom_as_of_date()
    
    
all_payoff_tests()

