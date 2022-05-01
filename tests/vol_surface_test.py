from pytest import *

import sys
sys.path.append('../')

from datetime import date
from shared_constants import test_as_of_date
from vol_surface import *

    
#TODO: implement properly once VolSurface is properly implemented
def vol_surface_returns_something():
    # arrange
    as_of_date = date(2022, 1, 1)
    a_date = date(2022, 4, 11)
    a_spot = 100500
    surface = VolSurface(as_of_date)
    
    # act
    vol = surface.get_vol(a_date, a_spot)
    
    # assert
    assert vol == 0.15, f"Expected 0.05 but got {vol}"
    
def vol_surface_returns_zero_for_weekends():
    # arrange
    as_of_date = date(2022, 1, 1)
    sat = date(2022, 4, 9)
    sun = date(2022, 4, 10)
    a_spot = 100500
    surface = VolSurface(as_of_date)
    
    # act
    sat_vol = surface.get_vol(sat, a_spot)
    sun_vol = surface.get_vol(sun, a_spot)
    
    # assert
    assert sat_vol == 0, f"Expected Sat vol to be 0 but got {vol}"
    assert sun_vol == 0, f"Expected Sun vol to be 0, but got {vol}"

    
def vol_surface_returns_correct_vol_by_year_fraction():
    # arrange
    as_of_date = date(2022, 1, 1)
    expiry = date(2022, 4, 10)
    a_spot = 100500
    surface = VolSurface(as_of_date)
    year_fraction = calc_year_fraction_from_dates(as_of_date, expiry)
    expected_vol = surface.get_vol(expiry, a_spot);
    
    # act
    vol = surface.get_vol_yf(year_fraction, a_spot)
    
    # assert
    assert vol == expected_vol, f"Expected {expected_vol} but got {vol}"

    
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
    surface = MockVolSurface(const_vol, test_as_of_date)
    
    # act
    vol = surface.get_vol(a_date, a_spot)
    
    # assert
    assert vol == const_vol, f"Expected {const_vol} but got {vol}"
    
def mock_vol_surface_returns_test_as_of_date():
    # arrange
    surface = MockVolSurface(42, test_as_of_date)
    
    # act
    actual = surface.get_as_of_date()
    
    # assert
    assert actual == test_as_of_date, f"Expected AsOfDate {test_as_of_date} but got {actual}"
    
def dump_vol_surface():
    as_of_date = date(2020, 1, 21)
    surface = VolSurfaceBase("GOOGL", as_of_date)
    
    result = pd.DataFrame()

    for d in range(1, 365*2):    
        cur_date = as_of_date + timedelta(days=d)
        for s in range(500, 2000, 10):
            yf = d / 365.25
            vol = surface.get_vol_yf(yf, s)
            result.at[s,d]=vol
    print(result)
    result.to_csv("vol_surface.csv")

        
    
def all_vol_surface_tests():
    vol_surface_returns_something()
    vol_surface_returns_correct_vol_by_year_fraction()
    vol_surface_returns_as_of_date()
    mock_vol_surface_returns_const()
    mock_vol_surface_returns_test_as_of_date()
    dump_vol_surface()
    
    
all_vol_surface_tests()