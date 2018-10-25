# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 16:30:30 2018

@author: Raphael Loo
"""

import numpy as np
import pandas as pd
from pandas_datareader import iex
import MatMath as mm
#import Summarystatsv2 as ss
#import MaxSharpe as ms

class Portfolio():
    def __init__(self, tickers):
        self.tickers=tickers
        
    def get_data(self, tickers=None, start_date=pd.datetime.now().date(), end_date=None, attributes=['open','close']):
        if tickers==None:
            tickers=self.tickers
        if end_date==None:
            tickers=start_date
        data=iex.daily.IEXDailyReader(tickers, start_date, end_date)
        data={i:data.read()[i] for i in attributes}
        return data
        
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
    
class Backtest(Portfolio):
    def __init__(self, *, capital, trade_dates, )    


# =============================================================================
# all_tickers=['APC', 'AMZN','COP','BMY']
# portfolio=Portfolio(all_tickers)
# data=portfolio.get_data(start_date='2017-01-01', end_date='2017-01-31')
# print(data)
# =============================================================================


