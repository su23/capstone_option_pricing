# we are using strike-based vol here without looking at delta/moneyness, 
# haven't even checked which convention is used  in Equities world by default

from daycount import *
import time
import pandas as pd
from pandas import DataFrame

class ISurface:
    def get_vol(self, date: date, strike:float) -> float:
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
    def get_vol(self, date: date, strike: float) -> float:
    #TODO: Ideally we should use US trading calendar, not just weekends here
        if date.weekday() > 4:
            return 0
        return 0.15
    
    def get_vol_yf(self, year_fraction: float, strike: float) -> float:
        date = convert_year_fraction_to_date(self.as_of_date, year_fraction)
        return self.get_vol(date, strike)
    
    def get_as_of_date(self) -> date:
        return self.as_of_date


class VolSurfaceBase(ISurface):
    # df_call: DataFrame
    df_put: DataFrame
    spot: float
    strike: float
    mid: float
    year_fraction: float
    expiry_date: date
    date_vols: DataFrame

    def __init__(self, asset_name: str, as_of_date: date):
        self.as_of_date = as_of_date
        self.load(asset_name)

    # TODO: implement properly
    def get_vol(self, date: date, strike: float) -> float:
        if date.weekday() > 4:
            return 0

        vols = self.date_vols

        # very rough
        real_strike = vols.iloc[(vols['Strike'] - strike).abs().argsort()[:1]]['Strike'].values[0]
        vols = vols[vols['Strike'] == real_strike]
        vols = vols.iloc[(vols['Expiration'].dt.date - date).abs().argsort()[:1]]
        result = vols

        iv = result["IV"]
        count = iv.count()
        if count == 0:
            return 0

        return iv.values[0]

    def get_vol_yf(self, year_fraction: float, strike: float) -> float:
        date = convert_year_fraction_to_date(self.as_of_date, year_fraction)
        return self.get_vol(date, strike)

    def get_as_of_date(self) -> date:
        return self.as_of_date

    # def get_spot(self) -> float:
    #     return self.spot
    #
    # def get_strike(self) -> float:
    #     return self.strike
    #
    # def get_mid(self) -> float:
    #     return self.mid

    def calculate_initial_values(self):
        self.date_vols = self.df_put[self.df_put['DataDate'].dt.date == self.as_of_date]
        # save file
        # self.date_vols.to_csv(f"GOOGLE2.csv", mode='a', header=True)

        # getting closest DN vol
        result = self.date_vols.iloc[(self.date_vols['Delta'] + 0.5).abs().argsort()[:1]]
        self.spot = result["UnderlyingPrice"].values[0]
        self.strike = result["Strike"].values[0]
        bid = result["Bid"].values[0]
        ask = result["Ask"].values[0]
        self.mid = (bid + ask) / 2
        print(f"Bid = {bid}, Ask = {ask}, Mid = {self.mid}")
        self.year_fraction = result["Days"].values[0] / 365
        self.expiry_date = result["Expiration"].values[0]
        print(f"Year fraction = {self.year_fraction}")

    def load(self, asset_name: str):
        print(f"Start loading {asset_name}")
        t = time.process_time()
        data = pd.read_csv(f'{asset_name}.csv', sep=",").filter(['UnderlyingPrice', 'Type', 'Expiration',
                                                                 'DataDate', 'Strike', 'Last', 'Bid', 'Ask', 'Volume',
                                                                 'OpenInterest', 'IV', 'Delta', 'Gamma',
                                                                 'Theta', 'Vega'])
        data['Expiration'] = pd.to_datetime(data['Expiration'])
        data['DataDate'] = pd.to_datetime(data['DataDate'])
        data['Days'] = (data['Expiration'] - data['DataDate']).astype('timedelta64[D]').astype(int)
        # self.df_call = data.loc[data['Type'] == "call"]
        self.df_put = data.loc[data['Type'] == "put"]
        elapsed_time = time.process_time() - t
        print(f"End loading in {elapsed_time} seconds")
        self.calculate_initial_values()
