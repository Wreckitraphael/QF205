# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 14:31:40 2018

@author: Ben
"""

from getstockdata import *
from Summarystats import SummaryStats as ss
import numpy as np

# Getting stock data using getstockdata.py
#x = stockdata()
#stockdata.getstockdata(['TSLA','AAPL','AMZN'], dt.datetime(2018,1,1), dt.datetime.now())

class portfolio_stats:
    def __init__(self, new_weights):
        self.new_weights = new_weights
        self.weights = np.array(new_weights)
    # =============================================================================
    # Calculating portfolio value
    # =============================================================================
    def portfoliovalue(self):
        portfolio_value = round(np.inner(self.weights,list(return_mean.values())),10)
        return portfolio_value
    
    # =============================================================================
    # Calculating portfolio variance
    # =============================================================================
    def portfoliovariance(self):
        covariance_matrix = np.cov(np.array([list(daily_return[i]) for i in daily_return.keys()]))
        portfolio_variance = round(np.dot(np.dot(self.weights, covariance_matrix), self.weights.T),10)
        return portfolio_variance
        return covariance_matrix
    
    def sharperatio(self):
        sharpe_ratio = round((portfolio_stats.portfoliovalue(self) - 0.03)/(portfolio_stats.portfoliovariance(self))**0.5,10)
        return sharpe_ratio
    
    def portfoliostats(self):
        print('\n---Portfolio statistics---')
        print('Portfolio value: ', portfolio_stats.portfoliovalue(self))
        print('Portfolio variance: ', portfolio_stats.portfoliovariance(self))
        print('Sharpe ratio: ', portfolio_stats.sharperatio(self))


