from datetime import date
from payoff import IDiscountedPayoff
from vol_surface import ISurface
from scipy.interpolate import interp1d

import numpy as np


class PdeGrid:
    def __init__(self, max_t: float, n_time_points: int, spot: float, spot_grid_factor: float, n_spot_points: int):
        assert spot_grid_factor > 1
        assert n_spot_points >= 1
        assert n_time_points >= 1
        
        self.min_t = 0
        self.max_t = max_t
        self.n_time_points = n_time_points
        
        self.spot = spot
        
        self.max_spot = spot * spot_grid_factor
        self.min_spot = spot / spot_grid_factor
        self.n_spot_points = n_spot_points
        
        
    def build_grid(self):
        self.grid = np.zeros([self.n_spot_points, self.n_time_points], dtype=float)
        self.time_points = np.linspace(self.min_t, self.max_t, num=self.n_time_points)
        self.spot_points = np.linspace(self.min_spot, self.max_spot, num=self.n_spot_points)
        
    def print_grid(self):
        print("Ts (columns): " + str(self.time_points))
        #print('\n'.join([' '.join(['{:4}'.format(item) for item in row]) for row in self.grid]))
        print(self.grid)
        print("Ss (rows): " + str(self.spot_points))

    def get_t_for_index(self, t_index: int) -> float:
        assert t_index >= 0
        assert t_index < len(self.time_points)
        return self.time_points[t_index];
        
    def get_spot_for_index(self, s_index: int) -> float:
        assert s_index >= 0
        assert s_index < len(self.spot_points)
        return self.spot_points[s_index];
    
    def set_pv(self, s_index: int, t_index: int, pv: float):
        assert t_index >= 0
        assert t_index < len(self.time_points)
        assert s_index >= 0
        assert s_index < len(self.spot_points)

        self.grid[s_index, t_index] = pv
        
    def get_pv(self, s_index: int, t_index: int) -> float:
        assert t_index >= 0
        assert t_index < len(self.time_points)
        assert s_index >= 0
        assert s_index < len(self.spot_points)

        return self.grid[s_index, t_index]

    def interpolate_t0(self) -> float:
        spot_values = self.spot_points
        t0_values = self.grid[:,0]
        interp_f = interp1d(spot_values, t0_values)
        return interp_f(self.spot)