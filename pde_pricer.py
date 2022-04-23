from datetime import date
from payoff import IDiscountedPayoff
from vol_surface import ISurface
from yc import ICurve
from pde_grid import PdeGrid

import numpy as np

#TODO: add year_fraction-based methods to YieldCurve and VolSurface and use here
class PdePricer:
    def __init__(self, payoff: IDiscountedPayoff, surface: ISurface, curve: ICurve, grid: PdeGrid):
        self.payoff = payoff
        self.surface = surface
        self.curve = curve
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
        max_s_index = self.grid.n_spot_points - 1
        dS = self.grid.get_delta_spot()
        dT = self.grid.get_delta_t()
        
        #print(f"dS = {dS}, dT = {dT}")
        
        a = np.zeros([max_s_index+1, max_s_index+1])
        b = np.zeros(max_s_index+1)
        
        for t_idx in range(t_index_to_compute, -1, -1):
            t = self.grid.get_t_for_index(t_idx)
            r = self.curve.get_rate_yf(t)
            
            pv_s0 = self.grid.get_pv(0, t_idx)
            pv_s_max = self.grid.get_pv(max_s_index, t_idx)
            a[0, 0]=1
            b[0]=pv_s0
            #print(f"X0={pv_s0}")
            
            for spot_idx in range(1, max_s_index):
                s = self.grid.get_spot_for_index(spot_idx)
                vol = self.surface.get_vol_yf(t, s)
                pv_t_plus_1 = self.grid.get_pv(spot_idx, t_idx+1)
                
                s_minus_1_coeff = (r*s - (vol**2)*(s**2.0)/dS)/(2*dS)
                s_plus_1_coeff = (-r*s - (vol**2)*(s**2)/dS)/(2*dS)
                s_coeff = (1/dT + (vol**2)*(s**2)/(dS**2)+r)
                const = pv_t_plus_1/dT
                #print(f"t={t}, r={r}, s={s}, vol={vol}, pv(T+1,S)={pv_t_plus_1}")
                #print(f"X{spot_idx-1}*{s_minus_1_coeff} + X{spot_idx} * {s_coeff} + X{spot_idx+1}*{s_plus_1_coeff} = {const}")
                a[spot_idx,spot_idx-1]=s_minus_1_coeff
                a[spot_idx,spot_idx]=s_coeff
                a[spot_idx,spot_idx+1]=s_plus_1_coeff
                b[spot_idx]=const
                
            #print(f"X{max_s_index}={pv_s_max}")
            a[max_s_index, max_s_index]=1
            b[max_s_index]=pv_s_max
            
            #print(f"A={a}")
            #print(f"B={b}")
                
            solved_values = np.linalg.solve(a, b)
            #no need to set S0 and Smax - those are const
            for spot_idx in range(1, max_s_index):
                s = self.grid.get_spot_for_index(spot_idx)
                payoff = self.payoff.calc_discounted_payoff_yf(t, s)
                solved = solved_values[spot_idx]
                self.grid.set_pv(spot_idx, t_idx, max(payoff, solved))
                #one can use this to check - should be less than the above 
                #self.grid.set_pv(spot_idx, t_idx, payoff)
            
        return self.grid.interpolate_t0()
