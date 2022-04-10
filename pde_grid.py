from datetime import date
from payoff import IDiscountedPayoff
from vol_surface import ISurface

import numpy as np


class PdeGrid:
    def __init__(self, max_t: float, n_time_points: int, spot: float, spot_grid_factor: float, n_spot_points: int):
        assert spot_grid_factor > 1
        assert n_spot_points >= 1
        assert n_time_points >= 1
        assert spot_grid_factor < 2
        
        self.min_t = 0
        self.max_t = max_t
        self.n_time_points = n_time_points
        
        
        self.spot = spot
        
        # it might be logical to use min_spot = spot / spot_grid_factor and max_spot = spot * spot_grid_factor
        # but now for simplicity we center a linspace around spot
        # to make i more readable and guarantee spot itself is included
        # this currently forces us to cap spot_grid_factor with 2
        
        self.max_spot = spot * spot_grid_factor
        self.min_spot = spot * (spot_grid_factor - 1)
        self.n_spot_points = n_spot_points
        
        
    def build_grid(self):
        self.grid = np.zeros([self.n_spot_points, self.n_time_points], dtype=float)
#SATODO need to skip weekends here
        self.time_points = np.linspace(self.min_t, self.max_t, num=self.n_time_points)
        self.spot_points = np.linspace(self.min_spot, self.max_spot, num=self.n_spot_points)
        
    def print_grid(self):
        print("Ts (columns): " + str(self.time_points))
        print('\n'.join([' '.join(['{:4}'.format(item) for item in row]) for row in self.grid]))
        print("Ss (rows): " + str(self.spot_points))

#SATODO: tests        
    def get_t_for_index(self, t_index: int):
        assert t_index >= 0
        assert t_index < len(self.time_points)
        return self.time_points[t_index];
        
#SATODO: tests        
    def get_spot_for_index(self, s_index: int):
        assert s_index >= 0
        assert s_index < len(self.spot_points)
        return self.spot_points[s_index];
    
#SATODO: tests
    def set_pv(self, spot_index: int, time_index: int, pv: float):
        self.grid[spot_index, time_index] = pv
        