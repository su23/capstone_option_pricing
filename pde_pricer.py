from datetime import date
from payoff import IDiscountedPayoff
from vol_surface import ISurface
from pde_grid import PdeGrid

import numpy as np


class PdePricer:
    def __init__(self, payoff: IDiscountedPayoff, surface: ISurface, grid: PdeGrid):
        self.payoff = payoff
        self.surface = surface
        self.grid = grid
        
        payoff_as_of_date = payoff.get_as_of_date()
        surface_as_of_date = surface.get_as_of_date()
        grid_as_of_date = grid.get_as_of_date()
        
        if (payoff_as_of_date != surface_as_of_date):
            raise f"Inconsistent as of dates: payoff {payoff_as_of_date} vs surface {surface_as_of_date}"
        if (payoff_as_of_date != grid_as_of_date):
            raise f"Inconsistent as of dates: payoff {payoff_as_of_date} vs grid {grid_settings_as_of_date}"
        
        self.as_of_date = payoff_as_of_date
        
        self.grid.build_grid()