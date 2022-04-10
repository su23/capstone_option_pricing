from datetime import date
from payoff import IDiscountedPayoff
from vol_surface import ISurface

import numpy as np


class PdeGrid:
    def __init__(self, as_of_date: date, expiry: date, n_date_points: int, spot: float, spot_grid_factor: float, n_spot_points: int):
        self.as_of_date = as_of_date
        self.expiry = expiry
        self.n_date_points = n_date_points
        self.spot = spot
        self.spot_grid_factor = spot_grid_factor
        self.n_spot_points = n_spot_points
        
    def build_grid(self):
        self.grid = np.zeros([self.n_date_points, self.n_spot_points], dtype=float)
        
    def print_grid(self):
        print(self.grid)
        
    def get_as_of_date(self) -> date:
        return self.as_of_date
