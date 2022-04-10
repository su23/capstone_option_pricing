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
        
        for spot_index in range(0, self.grid.n_spot_points):
            spot = self.grid.get_spot_for_index(spot_index)
            pv = self.payoff.calc_discounted_payoff_yf(t_exp, spot)
            self.grid.set_pv(spot_index, t_exp_index, pv)
            print(f"Payoff {t_exp} {spot} = {pv}" )
            
        