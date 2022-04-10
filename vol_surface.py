# we are using strike-based vol here without looking at delta/moneyness, 
# haven't even checked which convention is used  in Equities world by default

from datetime import date
from daycount import *

class ISurface:
    def get_vol(self, date: date, spot:float) -> float:
        """Returns annualised interpolated vol with as of date = surface's date, for 'date' point in time and 'spot' value of underlying """
        pass
    
    def get_vol_yf(self, year_fraction: float, spot:float) -> float:
        """Returns annualised interpolated vol with as of date = surface's date, for 'date' point matching specified 'year_fraction' and 'spot' value of underlying """
        pass


    def get_as_of_date() -> date:
        """Returns base date of the surface"""
        pass

    
class VolSurface(ISurface):
    #TODO: use base_date
    def __init__(self, as_of_date: date):
        self.as_of_date = as_of_date
        
    #TODO: implement properly
    def get_vol(self, date: date, spot:float) -> float:
        return 0.05
    
    def get_vol_yf(self, year_fraction: float, spot:float) -> float:
        date = convert_year_fraction_to_date(self.as_of_date, year_fraction)
        return self.get_vol(date, spot)
        pass
    
    def get_as_of_date(self) -> date:
        return self.as_of_date