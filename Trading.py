# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 16:30:30 2018

@author: Raphael Loo
"""

import numpy as np
import pandas as pd
import MatMath as mm
import Summarystatsv2 as ss
import MaxSharpe as ms

class Portfolio():
    def __init__(self, *, stock_data, trade_intervals, datapoints=10, rf):
        self.data=stock_data
        self.trade_intervals=trade_intervals
        self.datapoints=datapoints
        self.rf=rf
        
    def pos_open(self, start_capital, date, tickers, weights):
        share_price=list(self.data.loc[self.data['Date']==date, tickers].iloc[0,:])
        cap_allocation=list(start_capital*weights)
        num_shares={i:(j/k) for i,j,k in zip(tickers,cap_allocation,share_price)}
        return num_shares
        
    def pos_close(self, num_shares, date):
        tickers=list(num_shares.keys())
        share_price=list(self.data.loc[self.data['Date']==date, tickers].iloc[0,:])
        portfolio_value=sum([i*j for i,j in zip(list(num_shares.values()),share_price)])
        return portfolio_value
    
    





#def trade(capital, strategy, tickers, **kwargs)