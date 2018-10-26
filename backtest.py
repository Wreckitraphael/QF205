# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 16:03:59 2018

@author: Admin
"""

from getstockdata import * 
from Summarystats import SummaryStats as ss
from portfoliostats import portfolio_stats as ps
import minvarianceportfolio as minvar
import numpy as np
import pandas as pd

syms = ['AAPL', 'TSLA']
start = dt.datetime(2016,12,1)
end = dt.datetime(2018,1,30)
x = stockdata(syms, start, end)

# =============================================================================
# Generalisation
# =============================================================================
#To get the stocks' price for the start of the month
def price(syms, month, year):
  x = []
  for i in syms:
    date_filter = (stock_df.index.month == month) & (stock_df.index.year == year)
    month_price = stock_df.loc[date_filter, i]
    x.append(month_price.iloc[0])
  return x

#To get the capital for the start of the month; has the recursive function
def capital(month, year):
  if month == periods[1][1] and year == periods[1][0]:
    x = 1000000
    return x
  else:
    x = []
    for i in range(len(syms)):
      y = capital(periods[periods.index((year, month))-1][1], periods[periods.index((year, month))-1][0])*\
          period_weights[periods.index((year, month))-2][i]*\
          period_price[periods.index((year, month))-1][i]/\
          period_price[periods.index((year, month))-2][i]
      x.append(y)
    return sum(x)

#To get the number of stocks to buy at the start of the month
def nstocks(month, year):
  x = []
  for i in range(len(syms)):
    y = period_capital[periods.index((year,month))-1]*\
        period_weights[periods.index((year,month))-1][i]/\
        period_price[periods.index((year,month))-1][i]
    x.append(y)
  return x    

def invest(month, year):
  x = []
  for i in range(len(syms)):
    y = period_capital[periods.index((year,month))-1]*\
        period_weights[periods.index((year,month))-1][i]
    x.append(y)
  return x    

#Summarized backtesting data
periods = sorted(list(set((i.year, i.month) for i in stock_df.index)))
period_weights = [minvar.minvar_weights2(periods[i][1],periods[i][0]) for i in range(len(periods)-1)]
period_price = [price(syms, periods[i+1][1], periods[i+1][0]) for i in range(len(periods)-1)]
period_capital = [capital(j,i) for i,j in periods[1:len(periods)]]
period_nstocks = [nstocks(j,i) for i,j in periods[1:len(periods)]] #Maybe can just do a long list comprehension without defining a new function?
period_invest = [invest(j,i) for i,j in periods[1:len(periods)]]
summary = list(zip(periods[1:len(periods)], period_capital, period_weights, period_price, period_nstocks, period_invest))
summary_df = pd.DataFrame(summary, columns = ('Year, Month', 'Capital', 'Stock weights', 'Stock prices', 'Number stocks to buy', 'Investment amount'))
portfolio_return = (period_capital[len(period_capital)-1] - period_capital[0])/period_capital[0]

# =============================================================================
# Testing code
# =============================================================================
#weights = minvar.minvar_weights2(1,2017)
#price = price(syms, 1, 2017)
#capital = capital(1, 2017)
#number_stocks = nstocks(1,2017)
#month_investment = invest(1, 2017)