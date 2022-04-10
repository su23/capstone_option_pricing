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
    grid = PdeGrid(2, n_time_values, 100, 1.5, n_spot_values)
    
    # act
    pricer = PdePricer(disc_payoff, surface, grid)
    
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
    pricer = PdePricer(discounted_payoff, surface, grid)
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
    #SATODO: check max spot values are initialised with whatever they should be
    pass

def initialises_min_spot_grid_values():
    #SATODO: check max spot values are initialised with whatever they should be
    pass

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
    
    # act
    pricer = PdePricer(discounted_payoff, surface, grid)
    pv = pricer.price()
    print("Put, PV = " + str(pv))
    grid.print_grid()
    
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
    
    # act
    pricer = PdePricer(discounted_payoff, surface, grid)
    pv = pricer.price()
    print("Call, PV = " + str(pv))
    grid.print_grid()
    
    # assert is printout above
    

def all_pde_pricer_tests():
    test_case1 = ExceptionHandlingTestCase()
    test_case1.pde_pricer_ctor_checks_consistency_of_as_of_dates_payoff_vs_surface()
    pde_pricer_initialises_grid()
    initialises_expiry_grid_values()
    initialises_max_spot_grid_values()
    initialises_min_spot_grid_values()
    realistic_grid_init_test_put()
    realistic_grid_init_test_call()
    
    
all_pde_pricer_tests()