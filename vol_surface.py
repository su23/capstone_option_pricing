# we are using strike-based vol here without looking at delta/moneyness, 
# haven't even checked which convention is used  in Equities world by default

from daycount import *
import time
import pandas as pd
import numpy as np
from pandas import DataFrame
from scipy.interpolate import interp2d
from scipy.interpolate import interp1d

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
    
class MockVolSurface(ISurface):
    def __init__(self, const_vol: float, as_of_date: date):
        self.const_vol = const_vol
        self.as_of_date = as_of_date
        
    #TODO: implement properly
    def get_vol(self, date: date, spot:float) -> float:
        return self.const_vol
    
    def get_vol_yf(self, year_fraction: float, spot: float) -> float:
        return self.const_vol
    
    def get_as_of_date(self) -> date:
        return self.as_of_date


    
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


class VolSurfaceBase(ISurface):
    as_of_date: date

    def __init__(self, asset_name: str, as_of_date: date):
        self.as_of_date = as_of_date
        self.load(asset_name)


    def get_vol(self, date: date, spot: float) -> float:
        if date.weekday() > 4:
            return 0

        np_date = np.datetime64(date)
       
        
        result = 0
        
        if (np_date <= self.expiry_days_sorted[0]):
            result = self.interpolators[self.expiry_days_sorted[0]](spot)
            #print(f"Old = {old_result}, new result = {result} (Extrap-)")
            return result
        if (np_date >= self.expiry_days_sorted[-1]):
            result = self.interpolators[self.expiry_days_sorted[-1]](spot)
            #print(f"Old = {old_result}, new result = {result} (Extrap+)")
            return result
        
        
        left_idx = np.searchsorted(self.expiry_days_sorted, np_date)
        
        prev_exp = self.expiry_days_sorted[left_idx-1]
        #print(f"{left_idx} {np_date} {self.expiry_days_sorted[-1]} {self.expiry_days_sorted}")
        next_exp = self.expiry_days_sorted[left_idx]
        
        prev = self.interpolators[prev_exp](spot)
        next = self.interpolators[next_exp](spot)
                
        ratio = (np_date - prev_exp)/(next_exp - prev_exp)
        result = prev + (next - prev) * ratio

        return result

    def get_vol_yf(self, year_fraction: float, spot: float) -> float:
        date = convert_year_fraction_to_date(self.as_of_date, year_fraction)
        return self.get_vol(date, spot)

    def get_as_of_date(self) -> date:
        return self.as_of_date
    
    def create_interpolators(self, vols):
        self.expiry_days_sorted = sorted(vols['Expiration'].unique())
        self.interpolators = {}
        
        for exp in self.expiry_days_sorted:
            per_exp = vols.loc[vols['Expiration'] == exp]
            strikes = per_exp["Strike"]
            implied_vols = per_exp["IV"]
            exp_vol_by_strike_interp = interp1d(strikes, implied_vols, fill_value="extrapolate")
            self.interpolators[exp] = exp_vol_by_strike_interp
        

    def load(self, asset_name: str):
        print(f"Start loading {asset_name}")
        t = time.process_time()
        data = pd.read_csv(f'{asset_name}.csv', sep=",").filter(['Type', 'Expiration','DataDate', 'Strike', 'IV'])
        data['DataDate'] = pd.to_datetime(data['DataDate'])
        data['Expiration'] = pd.to_datetime(data['Expiration'])
        
        all_vols = data[data['DataDate'].dt.date == self.as_of_date]
        put_vols = all_vols[all_vols['Type'] == "put"]
        
        self.create_interpolators(put_vols)
        
        elapsed_time = time.process_time() - t
        

        

