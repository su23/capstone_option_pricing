import numpy as np
from datetime import date
from yc import *

class IPayoff:
    def calc_payoff(self, spot: float) -> float:
        """Return undiscounted payoff for a given underlying value"""
        pass


# Unity notionalnon-discounted Call payoff
class CallPayoff(IPayoff):
    strike = 0
    
    def __init__(self, strike: float):
        self.strike = strike
    
    def calc_payoff(self, spot: float) -> float:
        return max((spot - self.strike), 0)
        


# Unity notionalnon-discounted Call payoff
class PutPayoff(IPayoff):
    strike = 0
    
    def __init__(self, strike: float):
        self.strike = strike
    
    def calc_payoff(self, spot: float) -> float:
        return max((self.strike - spot), 0)
        

class DiscountedPayoff:
    def __init__(self, undiscounted_payoff: IPayoff, yield_curve: ICurve):
        self.inner_payoff = undiscounted_payoff
        self.curve = yield_curve
        
    def calc_discounted_payoff(self, date: date, spot: float) -> float:
        bare_payoff = self.inner_payoff.calc_payoff(spot);
        df = self.curve.get_disc_fact(date);
        return bare_payoff * df;
