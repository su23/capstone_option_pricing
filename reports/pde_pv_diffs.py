import pandas as pd

import sys
sys.path.append('../')

from datetime import date
from yc import YieldCurve
from vol_surface import VolSurfaceBase

from payoff import PutPayoff, CallPayoff, DiscountedPayoff
from pde_pricer import *
from daycount import *


def price_pde(strike: float, spot: float, as_of_date: date, expiry_date: date, is_call: bool, yield_curve: ICurve, surface: ISurface):
    n_time_values = 366
    n_spot_values = 100
    max_spot_mult = 2
    expiry_year_fraction = calc_year_fraction_from_dates(as_of_date, expiry_date)
   
    if is_call:
        payoff = CallPayoff(strike) 
    else:
        payoff = PutPayoff(strike)
    discounted_payoff = DiscountedPayoff(payoff, yield_curve)
    
    grid = PdeGrid(expiry_year_fraction, n_time_values, spot, max_spot_mult, n_spot_values)
    pricer = PdePricer(discounted_payoff, surface, yield_curve, grid)
    
    return pricer.price()
    

def run_diff(input_data_file, output_data_file):
    as_of_date = date(2020, 1, 21)
    curve = YieldCurve(as_of_date)
    surface = VolSurfaceBase(input_data_file, as_of_date)
    
    
    data = pd.read_csv(f'{input_data_file}.csv', sep=",").filter(['UnderlyingPrice', 'Type', 'Expiration','DataDate', 'Strike', 'Bid', 'Ask'])
    data['DataDate'] = pd.to_datetime(data['DataDate'])
    data['Expiration'] = pd.to_datetime(data['Expiration'])
    
    expiry_date = date(2021,1,15)
    spot = 1482.25
    strike = 1340
    
    result = pd.DataFrame(columns=["Type", "Expiry", "Strike", "PV", "Bid", "Mid", "Ask", "Diff", "BadDiff"])
    
    
    for index, row in data.iterrows():
        expiry_date = row['Expiration'].to_pydatetime().date()
        spot = row['UnderlyingPrice']
        strike = row['Strike']
        type = row['Type']
        is_call = (row['Type']=='call')
        
        bid = row['Bid']
        ask = row['Ask']
        
        pv = price_pde(strike, spot, as_of_date, expiry_date, is_call, curve, surface)
        
        mid = (bid+ask)/2
        diff = abs(mid-pv)
        bad_diff = 0
        if (pv < bid):
            bad_diff = pv - bid
        if (pv > ask):
            bad_diff = pv - ask
            
        new_row = {'Type':type , "Expiry":expiry_date, "Strike":strike, "PV":pv, "Bid":bid, "Mid":mid, "Ask":ask, "Diff":diff, "BadDiff":bad_diff}
        result = result.append(new_row, ignore_index=True)
    
        print(f"{expiry_date}, {strike}, {type}: PV = {pv}, bid={bid}, ask = {ask}, diff={diff}, bad diff: {bad_diff}")
    
    result.to_csv(f"{output_data_file}.csv")


run_diff("../tests/GOOGL_puts", "pde_pv_diffs_put")
run_diff("../tests/GOOGL_calls", "pde_pv_diffs_call")
run_diff("../tests/GOOGL", "pde_pv_diffs_full")
