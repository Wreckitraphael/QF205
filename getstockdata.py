
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
import numpy as np

#Stock price
stock_close = {}

#Stock return
daily_return = {}
return_mean = {}
return_variance = {}
stock_covariance = {}
stock_df = pd.DataFrame()

"""
Data sources:
    Morningstar: unreliable but provides up to date data
    Quandl: reliable but provides only up to 27/3/2018
    IEX: reliable, provides up to date data
"""
class stockdata():
    def __init__(self, syms, start, end):
        for stock_symbol in syms:
            #Downloading the data
            global stock_data, stock_a_open, stock_a_high, stock_a_close, stock_a_dates
            stock_data = web.DataReader(stock_symbol, 'iex', start, end)
            stock_data.to_csv('stockdata.csv')
            stock_data=pd.read_csv('stockdata.csv', parse_dates=True, index_col=0)
            print(stock_symbol, " data loaded")

            #CSV to dictionary
            stock_a_open = list(stock_data['open'])
            stock_a_high = list(stock_data['high'])
            stock_a_close = list(stock_data['close'])
            stock_df[stock_symbol] = list(stock_data['close'])

            #Calculating stock return into list
            a_list=[]
            for i in stock_a_close:
                if stock_a_close.index(i) == 0:
                    a = 0
                    a_list.append(a)
                else:
                    a = (i - stock_a_close[stock_a_close.index(i)-1])/stock_a_close[stock_a_close.index(i)-1]
                    a_list.append(a)
                    daily_return[stock_symbol] = a_list   

            #Calculating stock expected return & variance
            return_variance[stock_symbol] = np.var(daily_return[stock_symbol])
            return_mean[stock_symbol]= np.mean(daily_return[stock_symbol])
        #Adding columns to stock data data frame
        stock_df.index = stock_data.index
#        stock_df['Day'] = list(stock_data.index.day)
#        stock_df['Month'] = list(stock_data.index.month)
#        stock_df['Year'] = list(stock_data.index.year)

        #Calculating stock returns into dataframe
#        compiled_stock_data = pd.DataFrame.from_records(daily_return , index = stock_data.index)
#        return compiled_stock_data

    def printstockdata(self):
            #Printing the data
        for stock_symbol in syms:
            print('Stock symbol: ', stock_symbol)
            print(stock_data.tail(5))
            
            #Today data
            dateindex = end - start
            x = dateindex.days
            print('Date: ', end, 
                  '\nOpen :', stock_a_open[len(stock_a_open)-1],
                  '\nHigh :', stock_a_high[len(stock_a_high)-1],
                  '\nClose :', stock_a_close[len(stock_a_close)-1]
                  )
    #Drawdown and Max Drawdown
    def drawdown(self):
            dd = -max(0, (stock_data['close'].max() - stock_a_close[len(stock_a_close.keys())-1])/stock_data['close'].max())
            mdd = -max(0, (stock_data['close'].max() - stock_data['close'].min()) / stock_data['close'].max())
            print('Drawdown :', dd,
                  '\nMaximum Drawdown', mdd)

#x = stockdata(['AAPL', 'TSLA'], dt.datetime(2018,1,1), dt.datetime.now())
