from pytest import *
import unittest

import sys
sys.path.append('../')

from datetime import date
from pde_grid import *
from shared_constants import test_as_of_date
from shared_constants import test_expiry_date


def test_grid_excludes_weekends():
    # SATODO: test grid excludes weekends
    pass

def test_grid_has_correct_points_for_dates():
    # SATODO: test grid has correct number of points for dates
    pass

def test_grid_has_correct_points_for_spot():
    # SATODO: test grid has correct number of points for spot
    pass

def test_grid_can_go_more_granular_than_day():
    # SATODO: test grid can only go more granular than 1 day
    pass

def all_pde_grid_tests():
    test_grid_excludes_weekends()
    test_grid_has_correct_points_for_dates()
    test_grid_has_correct_points_for_spot()
    test_grid_can_go_more_granular_than_day()
    
    
all_pde_grid_tests()