# we are using strike-based vol here without looking at delta/moneyness, 
# haven't even checked which convention is used  in Equities world by default

from daycount import *

class ISurface:
    def get_vol(self, date: date, spot:float) -> float:
        """Returns annualised interpolated vol with as of date = surface's date, for 'date' point in time and 'spot' value of underlying """
        pass
    
    def get_vol_yf(self, year_fraction: float, spot:float) -> float:
        """Returns annualised interpolated vol with as of date = surface's date, for 'date' point matching specified 'year_fraction' and 'spot' value of underlying """
        pass

    def get_as_of_date(self) -> date:
        """Returns base date of the surface"""
        pass

    
class VolSurface(ISurface):
    #TODO: use as_of_date
    def __init__(self, as_of_date: date):
        self.as_of_date = as_of_date
        
    #TODO: implement properly
    def get_vol(self, date: date, spot: float) -> float:
    #TODO: Ideally we should use US trading calendar, not just weekends here
        if date.weekday() > 4:
            return 0
        return 0.15
    
    def get_vol_yf(self, year_fraction: float, spot: float) -> float:
        date = convert_year_fraction_to_date(self.as_of_date, year_fraction)
        return self.get_vol(date, spot)
    
    def get_as_of_date(self) -> date:
        return self.as_of_date
