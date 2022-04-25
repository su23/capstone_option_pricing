from pytest import *
import unittest

import sys

sys.path.append('../')

from datetime import date
from yc import YieldCurve
from vol_surface import VolSurface, VolSurfaceBase
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


# class ExceptionHandlingTestCase(unittest.TestCase):
#     def pde_pricer_ctor_checks_consistency_of_as_of_dates_payoff_vs_surface(self):
#         # arrange
#
#         date1 = date(2022, 4, 9)
#         date2 = date(2022, 4, 10)
#         disc_payoff = MockDiscountedPayoff(42, date1)
#         surface = MockVolSurface(0.01, date2)
#         grid = PdeGrid(2.0, 10, 2680, 1.5, 10)
#
#         # act / assert
#         with self.assertRaises(Exception) as context:
#             pricer = PdePricer(disc_payoff, surface, grid)

class GoogleVolSurface(VolSurfaceBase):
    def __init__(self, as_of_date: date = test_as_of_date):
        VolSurfaceBase.__init__(self, "GOOGL", as_of_date)

def realistic_grid_init_test_put():
    # arrange
    as_of_date = date(2020, 1, 21)
    curve = YieldCurve(as_of_date)
    surface = GoogleVolSurface(as_of_date)

    for i in range(10, 50, 5):
        n_time_values = i
        n_spot_values = i
        max_spot_mult = 1.5
        expiry_year_fraction = surface.year_fraction
        spot = surface.spot
        strike = surface.strike

        payoff = PutPayoff(strike)
        discounted_payoff = DiscountedPayoff(payoff, curve)
        grid = PdeGrid(expiry_year_fraction, n_time_values, spot, max_spot_mult, n_spot_values)
        pricer = PdePricer(discounted_payoff, surface, curve, grid)
    # act

        pv = pricer.price()
        print(f"Value: {i}")
        print("Put, PV = " + str(pv))
        print(f"Actual mid = {surface.mid}")
    # grid.print_grid()

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
    # grid.print_grid()

    # assert is printout above


def google_all_pde_pricer_tests():
    # test_case1 = ExceptionHandlingTestCase()
    # test_case1.pde_pricer_ctor_checks_consistency_of_as_of_dates_payoff_vs_surface()
    realistic_grid_init_test_put()
    # realistic_grid_init_test_call()

google_all_pde_pricer_tests()