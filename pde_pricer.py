from datetime import date
from payoff import IDiscountedPayoff
from vol_surface import ISurface
from pde_grid import PdeGrid

import numpy as np

#TODO: add year_fraction-based methods to YieldCurve and VolSurface and use here
class PdePricer:
    def __init__(self, payoff: IDiscountedPayoff, surface: ISurface, grid: PdeGrid):
        self.payoff = payoff
        self.surface = surface
        self.grid = grid
        
        payoff_as_of_date = payoff.get_as_of_date()
        surface_as_of_date = surface.get_as_of_date()
        
        if (payoff_as_of_date != surface_as_of_date):
            raise f"Inconsistent as of dates: payoff {payoff_as_of_date} vs surface {surface_as_of_date}"
        
        self.as_of_date = payoff_as_of_date
        
        self.grid.build_grid()
        
        t_exp_index = self.grid.n_time_points-1
        
        t_exp = self.grid.get_t_for_index(t_exp_index);
        
        min_spot_index = 0
        max_spot_index = self.grid.n_spot_points - 1
        
        for spot_index in range(0, max_spot_index + 1):
            spot = self.grid.get_spot_for_index(spot_index)
            pv = self.payoff.calc_discounted_payoff_yf(t_exp, spot)
            self.grid.set_pv(spot_index, t_exp_index, pv)
            #print(f"Payoff {t_exp} {spot} = {pv}" )
            
        min_spot = self.grid.get_spot_for_index(min_spot_index)
        max_spot = self.grid.get_spot_for_index(max_spot_index)
            
        # not touching tExp so not using t_exp_index + 1 deliberately
        for t_index in range(0, t_exp_index):
            t = self.grid.get_t_for_index(t_index)
            #we're assuming min and max spot are far enough so that one of values is definitely 0 and the other one is PV(future) i.e. discounted abs(S-K)
            min_spot_payoff = payoff.calc_discounted_payoff_yf(t, min_spot)
            self.grid.set_pv(min_spot_index, t_index, min_spot_payoff)
            
            max_spot_payoff = payoff.calc_discounted_payoff_yf(t, max_spot)
            self.grid.set_pv(max_spot_index, t_index, max_spot_payoff)
            
    def price(self):
        #we've already populated tExp so starting with tExp-1
        t_index_to_compute = self.grid.n_time_points - 2
        min_unknown_s_index = 1
        #we've already populated spot values for first and last spot indices from boundary conditions
        max_unknown_s_index = self.grid.n_spot_points - 2
        
        for t_idx in range(t_index_to_compute, 0, -1):
            print("TODO: interpolate here for T index " + str(t_idx))
            
        return self.grid.interpolate_t0()
            
            
        
        