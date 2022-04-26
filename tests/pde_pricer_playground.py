from pytest import *
import unittest

import sys
sys.path.append('../')

from datetime import date
from yc import YieldCurve
from vol_surface import VolSurface
from vol_surface import VolSurfaceBase
from payoff import PutPayoff, CallPayoff, DiscountedPayoff
from pde_pricer import *
from shared_constants import test_as_of_date
from shared_constants import test_expiry_date
from payoff_test import MockDiscountedPayoff
from vol_surface_test import MockVolSurface
from yc_test import MockYieldCurve
import math
from scipy.stats import norm


def BlackScholesPut(k: float, r: float, s: float, vol: float, t: float) -> float:
    d1 = (math.log(s/k) + (r + (vol**2)/2)*t)/(vol*t)
    d2 = d1 - vol*math.sqrt(t)
    nd = norm()
    pv = nd.cdf(-d2)*k*math.exp(-r*t)- nd.cdf(-d1) * s 
    return pv

def BlackScholesCall(k: float, r: float, s: float, vol: float, t: float) -> float:
    d1 = (math.log(s/k) + (r + (vol**2)/2)*t)/(vol*t)
    d2 = d1 - vol*math.sqrt(t)
    nd = norm()
    pv = nd.cdf(d1) * s - nd.cdf(d2)*k*math.exp(-r*t)
    return pv

def price_it():
    n_time_values = 100
    n_spot_values = 100
    as_of_date = date(2020, 1, 21)
    spot = 1482.25
    strike = 1340
    max_spot_mult = 2
    expiry_year_fraction = 0.97
    vol = 0.2417
    
    curve = YieldCurve(as_of_date)
    
    surface = VolSurfaceBase("GOOGL", as_of_date)
    payoff = PutPayoff(strike)
    discounted_payoff = DiscountedPayoff(payoff, curve)
    
    grid = PdeGrid(expiry_year_fraction, n_time_values, spot, max_spot_mult, n_spot_values)
    pricer = PdePricer(discounted_payoff, surface, curve, grid)
    
    pv = pricer.price()
    print(f"PV = {pv}")

def price_it_with_bs():
    n_time_values = 100
    n_spot_values = 100
    as_of_date = date(2020, 1, 21)
    spot = 1482.25
    strike = 1340
    max_spot_mult = 2
    expiry_year_fraction = 1
    vol = 0.2417
    
    curve = YieldCurve(as_of_date)
    rate = curve.get_rate_yf(1)
    
    surface = MockVolSurface(vol, as_of_date)
    payoff = PutPayoff(strike)
    discounted_payoff = DiscountedPayoff(payoff, curve)
    
    grid = PdeGrid(expiry_year_fraction, n_time_values, spot, max_spot_mult, n_spot_values)
    pricer = PdePricer(discounted_payoff, surface, curve, grid)
    
    pv = pricer.price()
    bs = BlackScholesPut(strike, 0.01, spot, vol, 1)
    print(f"PV = {pv}, bs={bs}, rate={rate}")
    
    
def rate_test():
    as_of_date1 = date(2014, 1, 21)
    as_of_date2 = date(2020, 1, 21)
    
    
    curve1 = YieldCurve(as_of_date1)
    curve2 = YieldCurve(as_of_date2)
    
    rate1 = curve1.get_rate_yf(1)
    rate2 = curve2.get_rate_yf(1)
    
    print(f"rate1 = {rate1}, rate2={rate2}")
    
#price_it_with_bs()
price_it()
#rate_test()