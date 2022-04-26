import numpy as np
from datetime import date
from yc import *

class IPayoff:
    def calc_payoff(self, spot: float) -> float:
        """Return undiscounted payoff for a given underlying value"""
        pass
    
    def get_strike(self) -> float:
        """Returns strike"""
        pass

    
class IDiscountedPayoff:
    def calc_discounted_payoff(self, date: date, spot: float) -> float:
        """Return discounted payoff for a given underlying value and date"""
        pass
    
    def calc_discounted_payoff_yf(self, year_fraction: float, spot: float) -> float:
        """Return discounted payoff for a given underlying value and year fraction"""
        pass
    
    def get_as_of_date(self) -> date:
        """Return as of date for discounted payoff (normally taken from curve)"""
        pass
    
    def get_strike(self) -> float:
        """Returns strike"""
        pass
   

# Unity notionalnon-discounted Call payoff
class CallPayoff(IPayoff):
    strike = 0
    
    def __init__(self, strike: float):
        self.strike = strike
    
    def calc_payoff(self, spot: float) -> float:
        return max((spot - self.strike), 0)
    
    def get_strike(self) -> float:
        return self.strike
   
        


# Unity notionalnon-discounted Call payoff
class PutPayoff(IPayoff):
    strike = 0
    
    def __init__(self, strike: float):
        self.strike = strike
    
    def calc_payoff(self, spot: float) -> float:
        return max((self.strike - spot), 0)
 
    def get_strike(self) -> float:
        return self.strike
       


class DiscountedPayoff (IDiscountedPayoff):
    def __init__(self, undiscounted_payoff: IPayoff, yield_curve: ICurve):
        self.inner_payoff = undiscounted_payoff
        self.curve = yield_curve
        
    def calc_discounted_payoff(self, date: date, spot: float) -> float:
        bare_payoff = self.inner_payoff.calc_payoff(spot);
        df = self.curve.get_disc_fact(date);
        return bare_payoff * df;

    def calc_discounted_payoff_yf(self, year_fraction: float, spot: float) -> float:
        bare_payoff = self.inner_payoff.calc_payoff(spot);
        df = self.curve.get_disc_fact_yf(year_fraction);
        return bare_payoff * df;

    
    def get_as_of_date(self) -> date:
        return self.curve.get_as_of_date()

    def get_strike(self) -> float:
        return self.inner_payoff.get_strike()
 