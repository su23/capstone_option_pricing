from pytest import *
import unittest

import sys
sys.path.append('../')

from datetime import date
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
    n_spot_values = 5
    n_time_values = 3
        
    as_of_date = date(2022, 4, 11)
    disc_payoff = MockDiscountedPayoff(42, as_of_date)
    surface = MockVolSurface(0.01, as_of_date)
    grid = PdeGrid(2, n_spot_values, 100, 1.5, n_time_values)
    
    # act
    pricer = PdePricer(disc_payoff, surface, grid)
    
    # assert
    assert grid.grid is not None
    grid.print_grid()
    
def initialises_expiry_grid_values():
    #SATODO: check expiry values are initialised with tExp payoff
    pass

def initialises_max_spot_values():
    #SATODO: check max spot values are initialised with whatever they should be
    pass

def initialises_min_spot_values():
    #SATODO: check max spot values are initialised with whatever they should be
    pass
    

def all_pde_pricer_tests():
    test_case1 = ExceptionHandlingTestCase()
    test_case1.pde_pricer_ctor_checks_consistency_of_as_of_dates_payoff_vs_surface()
    pde_pricer_initialises_grid()
    initialises_expiry_grid_values()
    initialises_max_spot_values()
    initialises_min_spot_values()
    
    
all_pde_pricer_tests()