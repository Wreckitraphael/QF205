# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 15:15:51 2018

@author: Admin
"""

portfolio_names = ['s1','s2','s3','s4']
portfolio_weightage = [0.25,0.25,0.25,0.25]
price_of_stocks_wk0 = [100,100,100,100]
initial_invest=['1000000']
invest_value = [float(i) for i in initial_invest * 4]      
price_of_stocks_wk1 = [200,200,200,200]

def drZ(w,p0,v0):
    num_of_shares=(w*v0)/p0
    return(num_of_shares)

num_of_shares_of_each_stock = []

d = list(zip(portfolio_weightage,price_of_stocks_wk0,invest_value))
for w,p0,v0 in d:
    num_of_shares_of_each_stock.append(drZ(w,p0,v0))

return_of_each_stock = [a*b for a,b in zip(num_of_shares_of_each_stock,price_of_stocks_wk1)]
return_of_portfolio=0
for x in return_of_each_stock:
    return_of_portfolio += x
    
print(return_of_portfolio)
intial_invest = str(return_of_portfolio)

