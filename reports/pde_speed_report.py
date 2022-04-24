from pytest import *
import unittest

import sys
sys.path.append('../')

from datetime import date
from yc import YieldCurve
from vol_surface import VolSurface
from payoff import PutPayoff, CallPayoff, DiscountedPayoff
import pandas as pd
from pde_pricer import *
import time


def put_price_has_correct_dynamics(nTimeValues:int, nSpotValues: int) -> float:
    # arrange
    as_of_date = date(2014, 1, 20)
    spot = 2680
    strike = 2700
    max_spot_mult = 1.5
    expiry_year_fraction = 2
    
    curve = YieldCurve(as_of_date)
    surface = VolSurface(as_of_date)
    payoff = PutPayoff(strike)
    discounted_payoff = DiscountedPayoff(payoff, curve)
    grid = PdeGrid(expiry_year_fraction, nTimeValues, spot, max_spot_mult, nSpotValues)
    pricer = PdePricer(discounted_payoff, surface, curve, grid)
    
   
    pv = pricer.price()
    print(f"PV = {pv}")
    return pv
    
    
def time_grid_dependency_test():
    result = pd.DataFrame()
    for ntv in range(10, 1010, 10):
        start = time.time()
        pv = put_price_has_correct_dynamics(ntv, 50)
        end = time.time()
        result.at['pv',ntv]=pv
        result.at['time',ntv]=end-start
    print(result)
    result.to_csv("pde_speed_report_t.csv")

def spot_grid_dependency_test():
    result = pd.DataFrame()
    for nsv in range(10, 1010, 10):
        start = time.time()
        pv = put_price_has_correct_dynamics(50, nsv)
        end = time.time()
        result.at['pv',nsv]=pv
        result.at['time',nsv]=end-start
    print(result)
    result.to_csv("pde_speed_report_s.csv")
    
def spot_and_time_grids_dependency_test():
    result = pd.DataFrame()
    for nv in range(10, 301):
        start = time.time()
        pv = put_price_has_correct_dynamics(nv, nv)
        end = time.time()
        result.at['pv',nv]=pv
        result.at['time',nv]=end-start
    print(result)
    result.to_csv("pde_speed_report_st.csv")
        
    
#time_grid_dependency_test()
#spot_grid_dependency_test()
spot_and_time_grids_dependency_test()