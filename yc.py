from datetime import date
from daycount import *

import pandas as pd
import numpy as np

import pathlib
yc_file_name = pathlib.Path(__file__).parent.resolve()

BC_KEY_DAYS = {
    30: "BC_1MONTH",
    90: "BC_3MONTH",
    180: "BC_6MONTH",
    365: "BC_1YEAR",
    730: "BC_2YEAR",
    1095: "BC_3YEAR",
    1825: "BC_5YEAR",
    2555: "BC_7YEAR",
    3650: "BC_10YEAR",
    7300: "BC_20YEAR",
    10950: "BC_30YEAR"
}

BC_DAYS = [
    30,
    90,
    180,
    365,
    730,
    1095,
    1825,
    2555,
    3650,
    7300,
    10950
]


class UnbasedYieldCurve:
    min_yc_days = 30
    min_year = 2014
    df: pd.DataFrame

    def __init__(self):
        self.df = pd.read_csv(str(yc_file_name) + "/yc.csv", parse_dates=["date"]).set_index("date")

    def get_yc_rate(self, base_date: date, forward_date: date):
        assert base_date <= forward_date
        assert base_date.year >= self.min_year
        if base_date == forward_date:
            return 0
        row = self.__find_yc_row_by_date(base_date)
        delta_days = (forward_date - base_date).days
        #print(row.values)
        if delta_days <= BC_DAYS[0]:
            return self.__get_value(row, 0)
        else:
            idx = self.__find_nearest_days_index(delta_days)
            start = BC_DAYS[idx]
            finish = BC_DAYS[idx + 1]
            a = self.__get_value(row, idx)
            b = self.__get_value(row, idx + 1)
            return (b - a) * (delta_days - start) / (finish - start) + a
        
    def __find_yc_row_by_date(self, base_date: date):
        return self.df.iloc[self.df.index.get_indexer([base_date], method="pad")]

    @staticmethod
    def __find_nearest_days_index(value: int):
        array = np.asarray(BC_DAYS)
        return (np.abs(array - value)).argmin()

    @staticmethod
    def __get_value(row, column_id):
        return row[BC_KEY_DAYS[BC_DAYS[column_id]]].values[0]
    
    
class ICurve:
    def get_rate(self, date: date) -> float:
        """Return interest rate with as of date = curve's date, for 'date' point in time"""
        pass

    def get_disc_fact(self, date: date) -> float:
        """Return discount factor with as of date = curve's date, for 'date' point in time"""
        pass
    
    def get_disc_fact_yf(self, year_fraction: float) -> float:
        """Return discount factor with as of date = curve's date, for a given year fraction"""
        pass
    
    def get_as_of_date() -> date:
        """Returns base date of the curve"""
        pass


    
class YieldCurve(ICurve):
    inner_yc = UnbasedYieldCurve()
    
    def __init__(self, as_of_date: date):
        self.as_of_date = as_of_date
      
    def get_rate(self, date: date) -> float:
        return self.inner_yc.get_yc_rate(self.as_of_date, date)
    
    def get_disc_fact(self, date: date) -> float:
        rate = self.get_rate(date)
        year_fraction = calc_year_fraction_from_dates(self.as_of_date, date)
        return np.exp(-rate * year_fraction)
    
    def get_disc_fact_yf(self, year_fraction: float) -> float:
        date = convert_year_fraction_to_date(self.as_of_date, year_fraction)
        rate = self.get_rate(date)
        return np.exp(-rate * year_fraction)
    
    def get_as_of_date(self) -> date:
        return self.as_of_date
        
        
