from pytest import *

import sys
sys.path.append('../')

from datetime import date
from payoff import *
from yc_test import MockYieldCurve


class MockPayoff(IPayoff):
    
    def __init__(self, const_payoff: float = 42):
        self.const_payoff = const_payoff
    
    def calc_payoff(self, spot: float) -> float:
        return self.const_payoff


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
    
    disc_payoff_obj = DiscountedPayoff(payoff, curve )
    
    a_date = date(2022, 4, 10)
    
    expected_disc_payoff = 11 * 0.42
    
    # act
    disc_payoff = disc_payoff_obj.calc_discounted_payoff(a_date, 1024768)
    
    # assert
    assert disc_payoff == expected_disc_payoff, f"Expected {expected_disc_payoff}, got {disc_payoff}"

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
    
    
all_payoff_tests()

