from scipy import stats
import numpy as np


class BS_Call_Option(object):
    """ Class for European call options in BS model
    author: WangChun
    Attributes
    ==========
    S0: float/initial stock price
    K: float/strike price
    T: float/maturity 
    r: float/risk free rate
    sigma: float 
    Methods
    =======
    value: float/returns the present value of call option
    vega: float/returns the vega of call option
    imp_vol: float/returns the implied volatility given option quote 
    """

    def __init__(self, S0, K, T, r, sigma):
        self.S0 = float(S0)
        self.k = K
        self.T = T
        self.r = r
        self.sigma = sigma

    def value(self):
        """returns option value."""
        d1 = ((np.log(self.S0 / self.k) + (self.r + 0.5 * self.sigma ** 2) * self.T) / (self.sigma * np.sqrt(self.T)))
        d2 = ((np.log(self.S0 / self.k) + (self.r - 0.5 * self.sigma ** 2) * self.T) / (self.sigma * np.sqrt(self.T)))
        value = (self.S0 * stats.norm.cdf(d1, 0.0, 1.0) - self.k * np.exp(-self.r * self.T) * stats.norm.cdf(d2, 0.0,1.0))
        return value

    def vega(self):
        """ returns vega of option
        """
        d1 = ((np.log(self.S0 / self.k) + (self.r + 0.5 * self.sigma ** 2) * self.T) / (self.sigma * np.sqrt(self.T)))
        vega = self.S0 * stats.norm.pdf(d1, 0.0, 1.0) * np.sqrt(self.T)
        return vega
