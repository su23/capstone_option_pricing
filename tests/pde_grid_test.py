from pytest import *
import unittest

import sys
sys.path.append('../')

from datetime import date
from pde_grid import *
from shared_constants import test_as_of_date
from shared_constants import test_expiry_date


def test_grid_has_correct_points_for_dates():
    # arrange
    n_spot_values = 3
    n_time_values = 5
    expected_time_points = np.array([0, 0.5, 1, 1.5, 2])
        
    grid = PdeGrid(2, n_time_values, 100, 1.5, n_spot_values)
    
    # act
    grid.build_grid()
    
    # assert

    actual_n_time_points = len(grid.time_points)
    assert actual_n_time_points == n_time_values, f"Expected {n_time_values} rows got {actual_n_time_points}"
    assert np.array_equal(expected_time_points, grid.time_points), f"Expected {expected_time_points} rows got {grid.time_points}"
    

def test_grid_has_correct_points_for_spot():
    # arrange
    n_spot_values = 5
    n_time_values = 3
    spot = 100
    spot_mult = 1.5
    min_spot = spot / spot_mult
    max_spot = spot * spot_mult
    expected_spot_points = np.linspace(min_spot, max_spot, num=n_spot_values)
        
    grid = PdeGrid(2, n_time_values, spot, spot_mult, n_spot_values)
    
    # act
    grid.build_grid()
    
    # assert

    actual_n_spot_points = len(grid.spot_points)
    assert actual_n_spot_points == n_spot_values, f"Expected {n_spot_values} rows got {actual_n_spot_points}"
    assert np.array_equal(expected_spot_points, grid.spot_points), f"Expected {expected_spot_points} rows got {grid.time_points}"
    assert grid.spot_points[0] == min_spot, f"Expected min spot point {min_spot} rows got {grid.spot_points[0]}"
    assert grid.spot_points[-1] == max_spot, f"Expected min spot point {max_spot} rows got {grid.spot_points[-1]}"

    pass

def test_grid_can_go_more_granular_than_day():
    # arrange
    max_t = 1/365.25
    n_spot_values = 3
    n_time_values = 100
        
    grid = PdeGrid(max_t, n_time_values, 100, 1.5, n_spot_values)
    
    # act
    grid.build_grid()
    
    # assert

    actual_n_time_points = len(grid.time_points)
    assert actual_n_time_points == n_time_values, f"Expected {n_time_values} rows got {actual_n_time_points}"

def test_grid_has_correct_number_of_rows_and_columns():
    # arrange
    n_spot_values = 5
    n_time_values = 3
        
    grid = PdeGrid(2, n_time_values, 100, 1.5, n_spot_values)
    
    # act
    grid.build_grid()
    
    # assert

    actual_n_rows, actual_n_cols = grid.grid.shape
    assert actual_n_rows == n_spot_values, f"Expected {n_spot_values} rows got {actual_n_rows}"
    assert actual_n_cols == n_time_values, f"Expected {n_time_values} rows got {actual_n_cols}"
    
def get_t_for_index_works():
    # arrange
    max_t = 4
    n_spot_values = 3
    n_time_values = 9
        
    grid = PdeGrid(max_t, n_time_values, 100, 1.5, n_spot_values)
    grid.build_grid()
    
    # act
    t0 = grid.get_t_for_index(0)
    t1 = grid.get_t_for_index(1)
    t4 = grid.get_t_for_index(4)
    t6 = grid.get_t_for_index(6)
    t7 = grid.get_t_for_index(7)
    t8 = grid.get_t_for_index(8)
    
    # assert
    assert t0 == 0, f"Expected 0, got {t0}"
    assert t1 == 0.5, f"Expected 0.5, got {t1}"
    assert t4 == 2, f"Expected 2, got {t4}"
    assert t6 == 3, f"Expected 3, got {t6}"
    assert t7 == 3.5, f"Expected 3.5, got {t7}"
    assert t8 == 4, f"Expected 4, got {t8}"
    
def get_spot_for_index_works():
    # arrange
    max_t = 4
    n_spot_values = 3
    n_time_values = 9
        
    grid = PdeGrid(max_t, n_time_values, 100, 1.5, n_spot_values)
    grid.build_grid()
    
    # act
    s0 = grid.get_spot_for_index(0)
    s1 = grid.get_spot_for_index(1)
    s2 = grid.get_spot_for_index(2)
    
    # assert
    assert s0 < s1, f"Expected {s0} < {s1}"
    assert s1 < s2, f"Expected {s1} < {s2}"
    
def set_pv_works():
    # arrange
    max_t = 4
    n_spot_values = 3
    n_time_values = 5
        
    grid = PdeGrid(max_t, n_time_values, 100, 1.5, n_spot_values)
    grid.build_grid()
    
    # act
    grid.set_pv(1, 2, 42.2)
    
    # assert
    actual = grid.grid[1,2]
    assert actual  == 42.2, f"Expected 42.2, but got {actual}"

def get_pv_works():
    # arrange
    max_t = 4
    n_spot_values = 3
    n_time_values = 5
        
    grid = PdeGrid(max_t, n_time_values, 100, 1.5, n_spot_values)
    grid.build_grid()
    grid.set_pv(1, 2, 42.2)
    
    # act
    actual = grid.get_pv(1,2)
    
    # assert
    assert actual  == 42.2, f"Expected 42.2, but got {actual}"
    
def interpolate_t0_interpolates():
    # arrange
    max_t = 4
    n_spot_values = 2
    n_time_values = 2
    spot = 100;
        
    grid = PdeGrid(max_t, n_time_values, spot, 1.5, n_spot_values)
    grid.build_grid()
    grid.set_pv(0, 0, 1000)
    grid.set_pv(1, 0, 2000)
    
    spot0 = grid.get_spot_for_index(0)
    spot1 = grid.get_spot_for_index(1)
    
    slope = 1000 / (spot1 - spot0)
    dx = (spot - spot0)
    expected_pv = 1000 + slope * dx
    
    # act
    actual = grid.interpolate_t0()
    
    # assert
    assert actual == expected_pv, f"Expected {expected_pv}, but got {actual}"
    
def delta_spot_is_constant():
    # arrange
    max_t = 4
    n_spot_values = 100
    n_time_values = 2
    spot = 100;
        
    grid = PdeGrid(max_t, n_time_values, spot, 1.5, n_spot_values)
    grid.build_grid()
    
    # act
    delta_spot1 = grid.get_spot_for_index(12)-grid.get_spot_for_index(11)
    delta_spot2 = grid.get_spot_for_index(51)-grid.get_spot_for_index(50)
    delta_spot = grid.get_delta_spot()

    #assert
    assert abs(delta_spot - delta_spot1) < 1e-10, f"Expected {delta_spot}, got {delta_spot1}"
    assert abs(delta_spot1 - delta_spot2) < 1e-10, f"Expected {delta_spot1}, got {delta_spot2}"
    
def delta_time_is_constant():
    # arrange
    max_t = 4
    n_spot_values = 2
    n_time_values = 100
    spot = 100;
        
    grid = PdeGrid(max_t, n_time_values, spot, 1.5, n_spot_values)
    grid.build_grid()
    
    # act
    delta_time1 = grid.get_t_for_index(12)-grid.get_t_for_index(11)
    delta_time2 = grid.get_t_for_index(51)-grid.get_t_for_index(50)
    delta_time = grid.get_delta_t()

    #assert
    assert abs(delta_time - delta_time1) < 1e-10, f"Expected {delta_time}, got {delta_time1}"
    assert abs(delta_time1 - delta_time2) < 1e-10, f"Expected {delta_time1}, got {delta_time2}"
    
    
    
class ExceptionHandlingTestCase(unittest.TestCase):
    def get_t_for_index_throws_for_too_small_index(self):
        # arrange
        max_t = 4
        n_spot_values = 3
        n_time_values = 9
        
        grid = PdeGrid(max_t, n_time_values, 100, 1.5, n_spot_values)
        grid.build_grid()
        
        # act / assert
        with self.assertRaises(Exception) as context:
             grid.get_t_for_index(-1)

    def get_t_for_index_throws_for_too_big_index(self):
        # arrange
        max_t = 4
        n_spot_values = 3
        n_time_values = 9
        
        grid = PdeGrid(max_t, n_time_values, 100, 1.5, n_spot_values)
        grid.build_grid()
        
        # act / assert
        with self.assertRaises(Exception) as context:
             grid.get_t_for_index(9)
             
    def get_spot_for_index_throws_for_too_small_index(self):
        # arrange
        max_t = 4
        n_spot_values = 3
        n_time_values = 9
        
        grid = PdeGrid(max_t, n_time_values, 100, 1.5, n_spot_values)
        grid.build_grid()
        
        # act / assert
        with self.assertRaises(Exception) as context:
             grid.get_spot_for_index(-1)

    def get_spot_for_index_throws_for_too_big_index(self):
        # arrange
        max_t = 4
        n_spot_values = 30
        n_time_values = 9
        
        grid = PdeGrid(max_t, n_time_values, 100, 1.5, n_spot_values)
        grid.build_grid()
        
        # act / assert
        with self.assertRaises(Exception) as context:
             grid.get_spot_for_index(30)
             
    def set_pv_throws_for_index_out_of_range(self):
        # arrange
        max_t = 4
        n_spot_values = 3
        n_time_values = 9
        
        grid = PdeGrid(max_t, n_time_values, 100, 1.5, n_spot_values)
        grid.build_grid()
        
        # act / assert
        with self.assertRaises(Exception) as context:
             grid.set_pv(-1, 1, 42)

        with self.assertRaises(Exception) as context:
             grid.set_pv(1, -1, 42)

        with self.assertRaises(Exception) as context:
             grid.set_pv(3, 1, 42)

        with self.assertRaises(Exception) as context:
             grid.set_pv(1, 9, 42)
             
    def get_pv_throws_for_index_out_of_range(self):
        # arrange
        max_t = 4
        n_spot_values = 3
        n_time_values = 9
        
        grid = PdeGrid(max_t, n_time_values, 100, 1.5, n_spot_values)
        grid.build_grid()
        
        # act / assert
        with self.assertRaises(Exception) as context:
             grid.get_pv(-1, 1)

        with self.assertRaises(Exception) as context:
             grid.get_pv(1, -1)

        with self.assertRaises(Exception) as context:
             grid.get_pv(3, 1)

        with self.assertRaises(Exception) as context:
             grid.get_pv(1, 9)
    

def all_pde_grid_tests():
    test_grid_has_correct_points_for_dates()
    test_grid_has_correct_points_for_spot()
    test_grid_can_go_more_granular_than_day()
    test_grid_has_correct_number_of_rows_and_columns()
    get_t_for_index_works()
    get_spot_for_index_works()
    set_pv_works()
    get_pv_works()
    interpolate_t0_interpolates()
    delta_spot_is_constant()
    delta_time_is_constant()
    
    bounds_check_case = ExceptionHandlingTestCase()
    bounds_check_case.get_t_for_index_throws_for_too_small_index()
    bounds_check_case.get_t_for_index_throws_for_too_big_index()
    bounds_check_case.get_spot_for_index_throws_for_too_small_index()
    bounds_check_case.get_spot_for_index_throws_for_too_big_index()
    bounds_check_case.set_pv_throws_for_index_out_of_range()
    bounds_check_case.get_pv_throws_for_index_out_of_range()
    
    
    
all_pde_grid_tests()