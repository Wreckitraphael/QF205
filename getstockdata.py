
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
import numpy as np

start = dt.datetime(2018, 1, 1)
end = dt.datetime.now()
syms = ['AAPL','TSLA','AMZN']
weights = [100/3, 100/3, 100/3]
stock_mean_price = {}
stock_variance = {}
stock_covariance = {}
stock_close = {}
stock_return = {}


"""
Data sources:
    Morningstar: unreliable but provides up to date data
    Quandl: reliable but provides only up to 27/3/2018
    IEX: reliable, provides up to date data
"""
class stockdata():
    def getstockdata():
        for stock_symbol in syms:
            #Downloading the data
            global stock_data, stock_a_open, stock_a_high, stock_a_close
            stock_data = web.DataReader(stock_symbol, 'iex', start, end)
            stock_data.to_csv('AAPL.csv')
            stock_data=pd.read_csv('AAPL.csv', parse_dates=True, index_col=0)
    
            #CSV to dictionary
            stock_a_open = list(stock_data['open'])
            stock_a_high = list(stock_data['high'])
            stock_a_close = list(stock_data['close'])
            stock_close[stock_symbol] = stock_a_close

            #Calculating stock return
            a_list=[]
            for i in stock_a_close:
                a = round((i - stock_a_close[0])/stock_a_close[0],5)
                a_list.append(a)
                stock_return[stock_symbol] = a_list
            
            #Calculating stock stuff
            stock_mean_price[stock_symbol] = stock_data['close'].mean()
            stock_variance[stock_symbol] = stock_data['close'].std()

    getstockdata()                
    
    def printstockdata():
            #Printing the data
            print('Stock symbol: ', stock_symbol)
            print(stock_data.tail(5))
            
            #Today data
            dateindex = end - start
            x = dateindex.days
            print('Date: ', end, 
                  '\nOpen :', stock_a_open[len(stock_a_open.keys())-1],
                  '\nHigh :', stock_a_high[len(stock_a_high.keys())-1],
                  '\nClose :', stock_a_close[len(stock_a_close.keys())-1]
                  )
            #Drawdown and Max Drawdown
            dd = -max(0, (stock_data['close'].max() - stock_a_close[len(stock_a_close.keys())-1])/stock_data['close'].max())
            mdd = -max(0, (stock_data['close'].max() - stock_data['close'].min()) / stock_data['close'].max())
            print('Drawdown :', dd,
                  '\nMaximum Drawdown', mdd)
    
test=stockdata()
test.getstockdata
print('Stock mean price: \n', stock_mean_price)
print('Stock variance: \n', stock_variance)
print(stock_return['AAPL'][0])