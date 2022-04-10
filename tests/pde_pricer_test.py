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

class ExcptionHandlingTestCase(unittest.TestCase):
    def pde_pricer_ctor_checks_consistency_of_as_of_dates_payoff_vs_surface(self):
        # arrange
        
        date1 = date(2022, 4, 9)
        date2 = date(2022, 4, 10)
        disc_payoff = MockDiscountedPayoff(42, date1)
        surface = MockVolSurface(0.01, date2)
        grid = PdeGrid(date1, test_expiry_date, 10, 2680, 1.5, 10)
        
        # act / assert
        with self.assertRaises(Exception) as context:
            pricer = PdePricer(disc_payoff, surface, grid)
            
            
    def pde_pricer_ctor_checks_consistency_of_as_of_dates_payoff_vs_grid_settings(self):
        # arrange
        
        date1 = date(2022, 4, 9)
        date2 = date(2022, 4, 10)
        disc_payoff = MockDiscountedPayoff(42, date1)
        surface = MockVolSurface(0.01, date1)
        grid = PdeGrid(date2, test_expiry_date, 10, 2680, 1.5, 10)
        
        # act / assert
        with self.assertRaises(Exception) as context:
            pricer = PdePricer(disc_payoff, surface, grid)
    

def pde_pricer_initialises_grid():
    # arrange
        
    as_of_date = date(2022, 4, 11)
    expiry_date = date(2022, 4, 15)
    disc_payoff = MockDiscountedPayoff(42, as_of_date)
    surface = MockVolSurface(0.01, as_of_date)
    grid = PdeGrid(as_of_date, expiry_date, 5, 100, 1.5, 3)
    
    # act
    pricer = PdePricer(disc_payoff, surface, grid)
    
    # assert
    
    assert grid.grid is not None
    grid.print_grid()
    

def all_pde_pricer_tests():
    test_case1 = ExcptionHandlingTestCase()
    test_case1.pde_pricer_ctor_checks_consistency_of_as_of_dates_payoff_vs_surface()
    test_case1.pde_pricer_ctor_checks_consistency_of_as_of_dates_payoff_vs_grid_settings()
    pde_pricer_initialises_grid()
    
    
all_pde_pricer_tests()