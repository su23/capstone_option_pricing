from datetime import datetime

import pandas as pd
import numpy as np


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


class YieldCurve:
    min_yc_days = 30
    min_year = 2014
    df: pd.DataFrame

    def __init__(self):
        self.df = pd.read_csv("yc.csv", parse_dates=["date"]).set_index("date")

    def get_yc_rate(self, base_date: datetime, forward_date: datetime):
        assert base_date < forward_date
        assert base_date.year >= self.min_year
        row = self.__find_yc_row_by_date(base_date)
        delta_days = (forward_date - base_date).days
        print(row.values)
        if delta_days <= BC_DAYS[0]:
            return self.__get_value(row, 0)
        else:
            idx = self.__find_nearest_days_index(delta_days)
            start = BC_DAYS[idx]
            finish = BC_DAYS[idx + 1]
            a = self.__get_value(row, idx)
            b = self.__get_value(row, idx + 1)
            return (b - a) * (delta_days - start) / (finish - start) + a

    def __find_yc_row_by_date(self, base_date: datetime):
        return self.df.iloc[self.df.index.get_indexer([base_date], method="pad")]

    @staticmethod
    def __find_nearest_days_index(value: int):
        array = np.asarray(BC_DAYS)
        return (np.abs(array - value)).argmin()

    @staticmethod
    def __get_value(row, column_id):
        return row[BC_KEY_DAYS[BC_DAYS[column_id]]].values[0]


# testing
# c = YieldCurve()
# print(c.get_yc_rate(datetime(2014, 1, 20), datetime(2014, 1, 25)))
# print(c.get_yc_rate(datetime(2014, 1, 20), datetime(2014, 5, 25)))
# print(c.get_yc_rate(datetime(2014, 1, 20), datetime(2018, 5, 25)))
