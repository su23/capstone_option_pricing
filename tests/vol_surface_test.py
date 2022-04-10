from pytest import *

import sys
sys.path.append('../')

from datetime import date
from shared_constants import test_as_of_date
from vol_surface import *

class MockVolSurface(ISurface):
    def __init__(self, const_vol: float, as_of_date: date = test_as_of_date):
        self.const_vol = const_vol
        self.as_of_date = as_of_date
        
    #TODO: implement properly
    def get_vol(self, date: date, spot:float) -> float:
        return self.const_vol
    
    def get_as_of_date(self) -> date:
        return self.as_of_date

    
#TODO: implement properly once VolSurface is properly implemented
def vol_surface_returns_something():
    # arrange
    as_of_date = date(2022, 1, 1)
    a_date = date(2022, 4, 10)
    a_spot = 100500
    surface = VolSurface(as_of_date)
    
    # act
    vol = surface.get_vol(a_date, a_spot)
    
    # assert
    assert vol == 0.05, f"Expected 0.05 but got {vol}"
    
def vol_surface_returns_as_of_date():
    # arrange
    as_of_date = date(2022, 1, 1)
    surface = VolSurface(as_of_date)
    
    # act
    actual = surface.get_as_of_date()
    
    # assert
    assert actual == as_of_date, f"Expected AsOfDate {as_of_date} but got {actual}"

    
def mock_vol_surface_returns_const():
    # arrange
    const_vol = 0.01
    a_date = date(2022, 4, 10)
    a_spot = 100500
    surface = MockVolSurface(const_vol)
    
    # act
    vol = surface.get_vol(a_date, a_spot)
    
    # assert
    assert vol == const_vol, f"Expected {const_vol} but got {vol}"
    
def mock_vol_surface_returns_test_as_of_date():
    # arrange
    surface = MockVolSurface(42)
    
    # act
    actual = surface.get_as_of_date()
    
    # assert
    assert actual == test_as_of_date, f"Expected AsOfDate {test_as_of_date} but got {actual}"
        
    
def all_vol_surface_tests():
    vol_surface_returns_something()
    vol_surface_returns_as_of_date()
    mock_vol_surface_returns_const()
    mock_vol_surface_returns_test_as_of_date()
    
    
all_vol_surface_tests()