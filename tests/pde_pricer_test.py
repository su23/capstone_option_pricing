from pytest import *
import unittest

import sys
sys.path.append('../')

from datetime import date
from yc import YieldCurve
from vol_surface import VolSurface
from payoff import PutPayoff, CallPayoff, DiscountedPayoff
from pde_pricer import *
from shared_constants import test_as_of_date
from shared_constants import test_expiry_date
from payoff_test import MockDiscountedPayoff
from vol_surface_test import MockVolSurface
from yc_test import MockYieldCurve
import math
from scipy.stats import norm

class MockDiscountedPayoffForSpot(IDiscountedPayoff):
    
    def __init__(self, const_payoff: float, for_spot: float):
        self.const_payoff = const_payoff
        self.for_spot = for_spot
    
    def calc_discounted_payoff_yf(self, t: float, spot: float) -> float:
        if (spot == self.for_spot):
            return self.const_payoff
        return 0
    
    def get_as_of_date(self) -> date:
        return date(2014, 1, 20)

class ExceptionHandlingTestCase(unittest.TestCase):
    def pde_pricer_ctor_checks_consistency_of_as_of_dates_payoff_vs_surface(self):
        # arrange
        
        date1 = date(2022, 4, 9)
        date2 = date(2022, 4, 10)
        disc_payoff = MockDiscountedPayoff(42, date1)
        surface = MockVolSurface(0.01, date2)
        grid = PdeGrid(2.0, 10, 2680, 1.5, 10)
        
        # act / assert
        with self.assertRaises(Exception) as context:
            pricer = PdePricer(disc_payoff, surface, grid)
            
            
def pde_pricer_initialises_grid():
    # arrange
    n_time_values = 5
    n_spot_values = 3
        
    as_of_date = date(2022, 4, 11)
    disc_payoff = MockDiscountedPayoff(42, as_of_date)
    surface = MockVolSurface(0.01, as_of_date)
    curve = MockYieldCurve(0.9, 0.01, as_of_date)
    grid = PdeGrid(2, n_time_values, 100, 1.5, n_spot_values)
    
    # act
    pricer = PdePricer(disc_payoff, surface, curve, grid)
    
    # assert
    assert grid.grid is not None
    grid.print_grid()
    
def initialises_expiry_grid_values():
    # arrange
    n_time_values = 5
    n_spot_values = 3
    as_of_date = date(2014, 1, 20)
    spot = 2680
    strike = 3000
    max_spot_mult = 1.5
    expiry_year_fraction = 2
    
    curve = MockYieldCurve(1, 0, as_of_date)
    surface = MockVolSurface(0.05, as_of_date)
    payoff = PutPayoff(strike)
    discounted_payoff = DiscountedPayoff(payoff, curve)
    grid = PdeGrid(expiry_year_fraction, n_time_values, spot, max_spot_mult, n_spot_values)
    
    # act
    pricer = PdePricer(discounted_payoff, surface, curve, grid)
    t_exp_value_s0 = grid.get_pv(0, 4)
    t_exp_value_s1 = grid.get_pv(1, 4)
    t_exp_value_s2 = grid.get_pv(2, 4)
    
    
    # assert
    expected_payoff_s0 = payoff.calc_payoff(grid.get_spot_for_index(0))
    expected_payoff_s1 = payoff.calc_payoff(grid.get_spot_for_index(1))
    expected_payoff_s2 = payoff.calc_payoff(grid.get_spot_for_index(2))
    
    assert t_exp_value_s0 == expected_payoff_s0, f"Expected S0 tExp payoff {expected_payoff_s0}, got {t_exp_value_s0}"
    assert t_exp_value_s1 == expected_payoff_s1, f"Expected S0 tExp payoff {expected_payoff_s1}, got {t_exp_value_s1}"
    assert t_exp_value_s2 == expected_payoff_s2, f"Expected S0 tExp payoff {expected_payoff_s2}, got {t_exp_value_s2}"
    
    

def initialises_max_spot_grid_values():
    # arrange
    n_time_values = 5
    n_spot_values = 3
    as_of_date = date(2014, 1, 20)
    spot = 2680
    strike = 3000
    max_spot_mult = 1.5
    expiry_year_fraction = 2
    expected_max_spot_payoff = 42
    
    curve = MockYieldCurve(1, 0, as_of_date)
    surface = MockVolSurface(0.05, as_of_date)
    grid = PdeGrid(expiry_year_fraction, n_time_values, spot, max_spot_mult, n_spot_values)
    grid.build_grid()
    max_spot_index = grid.n_spot_points - 1
    max_spot = grid.get_spot_for_index(max_spot_index)
    discounted_payoff = MockDiscountedPayoffForSpot(expected_max_spot_payoff, max_spot)

    # act
    pricer = PdePricer(discounted_payoff, surface, curve, grid)
    
    # assert
    for t_index in range(0, n_time_values):
        max_spot_payoff = pricer.grid.get_pv(max_spot_index, t_index)
        assert expected_max_spot_payoff == max_spot_payoff, f"Expected max spot payoff for t {t_index} to be {expected_max_spot_payoff}, got {max_spot_payoff}"

def initialises_min_spot_grid_values():
# arrange
    n_time_values = 5
    n_spot_values = 3
    as_of_date = date(2014, 1, 20)
    spot = 2680
    strike = 3000
    max_spot_mult = 1.5
    expiry_year_fraction = 2
    expected_min_spot_payoff = 42
    
    curve = MockYieldCurve(1, 0, as_of_date)
    surface = MockVolSurface(0.05, as_of_date)
    grid = PdeGrid(expiry_year_fraction, n_time_values, spot, max_spot_mult, n_spot_values)
    grid.build_grid()
    min_spot_index = 0
    min_spot = grid.get_spot_for_index(min_spot_index)
    discounted_payoff = MockDiscountedPayoffForSpot(expected_min_spot_payoff, min_spot)

    # act
    pricer = PdePricer(discounted_payoff, surface, curve, grid)
    
    # assert
    for t_index in range(0, n_time_values):
        min_spot_payoff = pricer.grid.get_pv(min_spot_index, t_index)
        assert expected_min_spot_payoff == min_spot_payoff, f"Expected min spot payoff for t {t_index} to be {expected_min_spot_payoff}, got {min_spot_payoff}"

def realistic_grid_init_test_put():
    # arrange
    n_time_values = 5
    n_spot_values = 10
    as_of_date = date(2014, 1, 20)
    spot = 2680
    strike = 3000
    max_spot_mult = 1.5
    expiry_year_fraction = 1
    
    curve = YieldCurve(as_of_date)
    surface = VolSurface(as_of_date)
    payoff = PutPayoff(strike)
    discounted_payoff = DiscountedPayoff(payoff, curve)
    grid = PdeGrid(expiry_year_fraction, n_time_values, spot, max_spot_mult, n_spot_values)
    pricer = PdePricer(discounted_payoff, surface, curve, grid)
    
    # act
    
    pv = pricer.price()
    print("Put, PV = " + str(pv))
    #grid.print_grid()
    
    # assert is printout above

def realistic_grid_init_test_call():
    # arrange
    n_time_values = 5
    n_spot_values = 10
    as_of_date = date(2014, 1, 20)
    spot = 2680
    strike = 2500
    max_spot_mult = 1.5
    expiry_year_fraction = 1
    
    curve = YieldCurve(as_of_date)
    surface = VolSurface(as_of_date)
    payoff = CallPayoff(strike)
    discounted_payoff = DiscountedPayoff(payoff, curve)
    grid = PdeGrid(expiry_year_fraction, n_time_values, spot, max_spot_mult, n_spot_values)
    pricer = PdePricer(discounted_payoff, surface, curve, grid)
    
    # act
    
    pv = pricer.price()
    print("Call, PV = " + str(pv))
    #grid.print_grid()
    
    # assert is printout above
    
def call_price_has_correct_dynamics():
    # arrange
    n_time_values = 5
    n_spot_values = 10
    as_of_date = date(2014, 1, 20)
    spot = 2680
    strike1 = 2000
    strike2 = 2500
    max_spot_mult = 1.5
    expiry_year_fraction = 1
    
    curve = YieldCurve(as_of_date)
    surface = VolSurface(as_of_date)
    payoff1 = CallPayoff(strike1)
    discounted_payoff1 = DiscountedPayoff(payoff1, curve)
    grid1 = PdeGrid(expiry_year_fraction, n_time_values, spot, max_spot_mult, n_spot_values)
    pricer1 = PdePricer(discounted_payoff1, surface, curve, grid1)
    
    payoff2 = CallPayoff(strike2)
    discounted_payoff2 = DiscountedPayoff(payoff2, curve)
    grid2 = PdeGrid(expiry_year_fraction, n_time_values, spot, max_spot_mult, n_spot_values)
    pricer2 = PdePricer(discounted_payoff2, surface, curve, grid2)

    
    # act
    
    pv1 = pricer1.price()
    pv2 = pricer2.price()
    print(f"PVc(K={strike1}) = {pv1}, PVc(K={strike2}) = {pv2}")
    
    # assert
    assert pv1 > pv2, f"Expected a call with lower strike to be more expensive, but tot {pv1} vs {pv2}"

def put_price_has_correct_dynamics():
    # arrange
    n_time_values = 10
    n_spot_values = 10
    as_of_date = date(2014, 1, 20)
    spot = 2680
    strike1 = 2500
    strike2 = 3000
    max_spot_mult = 1.5
    expiry_year_fraction = 2
    
    curve = YieldCurve(as_of_date)
    surface = VolSurface(as_of_date)
    payoff1 = PutPayoff(strike1)
    discounted_payoff1 = DiscountedPayoff(payoff1, curve)
    grid1 = PdeGrid(expiry_year_fraction, n_time_values, spot, max_spot_mult, n_spot_values)
    pricer1 = PdePricer(discounted_payoff1, surface, curve, grid1)
    
    payoff2 = PutPayoff(strike2)
    discounted_payoff2 = DiscountedPayoff(payoff2, curve)
    grid2 = PdeGrid(expiry_year_fraction, n_time_values, spot, max_spot_mult, n_spot_values)
    pricer2 = PdePricer(discounted_payoff2, surface, curve, grid2)
    #grid2.print_grid()

    # act
    
    pv1 = pricer1.price()
    pv2 = pricer2.price()
    print(f"PVp(K={strike1}) = {pv1}, PVp(K={strike2}) = {pv2}")
    #grid2.print_grid()
    
    # assert
    assert pv1 < pv2, f"Expected a put with lower strike to be cheaper, but tot {pv1} vs {pv2}"
    
    
def higher_vol_means_more_expensive_option():
    # arrange
    n_time_values = 10
    n_spot_values = 10
    as_of_date = date(2014, 1, 20)
    spot = 2680
    strike = 2700
    max_spot_mult = 1.5
    expiry_year_fraction = 2
    
    curve = YieldCurve(as_of_date)
    surface_lower = MockVolSurface(0.1, as_of_date)
    surface_higher = MockVolSurface(0.11, as_of_date)
    payoff = PutPayoff(strike)
    discounted_payoff = DiscountedPayoff(payoff, curve)
    
    grid_lower = PdeGrid(expiry_year_fraction, n_time_values, spot, max_spot_mult, n_spot_values)
    pricer_lower = PdePricer(discounted_payoff, surface_lower, curve, grid_lower)
    
    grid_higher = PdeGrid(expiry_year_fraction, n_time_values, spot, max_spot_mult, n_spot_values)
    pricer_higher = PdePricer(discounted_payoff, surface_higher, curve, grid_higher)
    #grid_lower.print_grid()

    # act
    
    pv_lower = pricer_lower.price()
    pv_higher = pricer_higher.price()
    print(f"PVlower = {pv_lower}, PVhigher = {pv_higher}")
    #grid_higher.print_grid()
    
    # assert
    assert pv_lower < pv_higher, f"Expected an option with lower vol to be cheaper, but tot {pv_lower} vs {pv_higher}"
    
    
def higher_rates_mean_less_expensive_option():
    # arrange
    n_time_values = 10
    n_spot_values = 10
    as_of_date = date(2014, 1, 20)
    spot = 2680
    strike = 2700
    max_spot_mult = 1.5
    expiry_year_fraction = 2
    
    curve_lower = MockYieldCurve(0.98, 0.01, as_of_date)
    curve_higher = MockYieldCurve(0.96, 0.02, as_of_date)

    surface = VolSurface(as_of_date)
    payoff = PutPayoff(strike)
    discounted_payoff_lower_rates = DiscountedPayoff(payoff, curve_lower)
    discounted_payoff_higher_rates = DiscountedPayoff(payoff, curve_higher)
    
    grid_lower = PdeGrid(expiry_year_fraction, n_time_values, spot, max_spot_mult, n_spot_values)
    pricer_lower_rates = PdePricer(discounted_payoff_lower_rates, surface, curve_lower, grid_lower)
    
    grid_higher = PdeGrid(expiry_year_fraction, n_time_values, spot, max_spot_mult, n_spot_values)
    pricer_higher_rates = PdePricer(discounted_payoff_higher_rates, surface, curve_higher, grid_higher)

    # act
    
    pv_lower_rates = pricer_lower_rates.price()
    pv_higher_rates = pricer_higher_rates.price()
    print(f"PVlower_rates = {pv_lower_rates}, PVhigher_rates = {pv_higher_rates}")
    
    # assert
    assert pv_lower_rates > pv_higher_rates, f"Expected an option with lower rates to be more expensive, but tot {pv_lower_rates} vs {pv_higher_rates}"


def deep_otm_price_is_0():
    # arrange
    n_time_values = 5
    n_spot_values = 10
    as_of_date = date(2014, 1, 20)
    spot = 2680
    strike = 1000
    max_spot_mult = 1.5
    expiry_year_fraction = 1
    
    curve = YieldCurve(as_of_date)
    surface = VolSurface(as_of_date)
    payoff = PutPayoff(strike)
    discounted_payoff = DiscountedPayoff(payoff, curve)
    grid = PdeGrid(expiry_year_fraction, n_time_values, spot, max_spot_mult, n_spot_values)
    pricer = PdePricer(discounted_payoff, surface, curve, grid)
    
    # act
    
    pv = pricer.price()
    print("Deep OTM Put, PV = " + str(pv))
    
    # assert
    assert 0 == pv, f"Expected deep OTM PV to be 0, but got {pv}"
    
    
def deep_itm_put_price_is_k_minus_s():
    # arrange
    n_time_values = 5
    n_spot_values = 10
    as_of_date = date(2014, 1, 20)
    spot = 2680
    strike = 4000
    max_spot_mult = 1.5
    expiry_year_fraction = 1
    
    curve = YieldCurve(as_of_date)
    surface = VolSurface(as_of_date)
    payoff = PutPayoff(strike)
    discounted_payoff = DiscountedPayoff(payoff, curve)
    grid = PdeGrid(expiry_year_fraction, n_time_values, spot, max_spot_mult, n_spot_values)
    pricer = PdePricer(discounted_payoff, surface, curve, grid)
    
    expected_price = strike - spot
    
    # act
    
    pv = pricer.price()
    print("Deep ITM Put, PV = " + str(pv))
    
    # assert
    assert expected_price == pv, f"Expected deep ITM PV to be {expected_price}, but got {pv}"
    
def BlackScholes(k: float, r: float, s: float, vol: float, t: float) -> float:
    d1 = (math.log(s/k) + (r + (vol**2)/2)*t)/(vol*t)
    d2 = d1 - vol*math.sqrt(t)
    nd = norm()
    pv = nd.cdf(d1) * s - nd.cdf(d2)*k*math.exp(-r*t)
    return pv
    
    
def call_with_const_vol_roughly_matches_Black_Scholes():
# arrange
    n_time_values = 100
    n_spot_values = 100
    as_of_date = date(2014, 1, 20)
    spot = 2680
    strike = 2700
    max_spot_mult = 1.5
    expiry_year_fraction = 2
    
    rate = 0.01
    df = math.exp(-rate*expiry_year_fraction)
    curve = MockYieldCurve(df, rate, as_of_date)
    vol = 0.1
    surface = MockVolSurface(vol, as_of_date)
    payoff = CallPayoff(strike)
    discounted_payoff = DiscountedPayoff(payoff, curve)
    
    grid = PdeGrid(expiry_year_fraction, n_time_values, spot, max_spot_mult, n_spot_values)
    pricer = PdePricer(discounted_payoff, surface, curve, grid)
    
    #grid_lower.print_grid()

    # act
    
    pv = pricer.price()
    bs = BlackScholes(strike, rate, spot, vol, expiry_year_fraction)
    
    # assert
    error_pct = abs(bs - pv) / ((bs+pv)/2)
    print(f"PV = {pv}, BS = {bs}, err = {error_pct}")
    assert error_pct  < 0.03, f"Expected call PV {pv} to roughly match BS {bs} with constant vol and rates, error = {error_pct}"



def all_pde_pricer_tests():
    test_case1 = ExceptionHandlingTestCase()
    test_case1.pde_pricer_ctor_checks_consistency_of_as_of_dates_payoff_vs_surface()
    pde_pricer_initialises_grid()
    initialises_expiry_grid_values()
    initialises_max_spot_grid_values()
    initialises_min_spot_grid_values()
    realistic_grid_init_test_put()
    realistic_grid_init_test_call()
    call_price_has_correct_dynamics()
    put_price_has_correct_dynamics()
    higher_vol_means_more_expensive_option()
    higher_rates_mean_less_expensive_option()
    deep_otm_price_is_0()
    deep_itm_put_price_is_k_minus_s()
    call_with_const_vol_roughly_matches_Black_Scholes()
    
    
all_pde_pricer_tests()