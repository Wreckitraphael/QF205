# -*- coding: utf-8 -*-
"""
Created on Wed Oct 17 18:53:06 2018

@author: Admin
"""

from getstockdata import *
from Summarystats import SummaryStats as ss
from portfoliostats import portfolio_stats as ps
import numpy as np
import itertools as it
import scipy.linalg as linalg 

#Changing product function from itertools to use lists instead of tuple
def product(*args, repeat=1):
    pools = [list(pool) for pool in args] * repeat
    result = [[]]
    for pool in pools:
        result = [x+[y] for x in result for y in pool]
    for prod in result:
        yield list(prod)

# =============================================================================
# Getting portfolio weights using brute force (i.e. iterations)
# =============================================================================
def portfolio_weights_bruteforce():
    #Gettting the list of permissable permutations (i.e. sum of weights is 1)
    permutations = list(product(map(lambda x: x/100,range(0,101,1)), repeat = len(daily_return.keys())))
    allowed_permutations = []
    for j in permutations:
        if sum(j) == 1:
            allowed_permutations.append(j) 
        else:
            pass
    
    #Finding weights combination that give the lowest variance and max sharpe and max return
    test_var = []
    test_sharpe = []
    test_value = []
    for i in allowed_permutations:
        x = ps(i)
        test_var.append(x.portfoliovariance())
        test_sharpe.append(x.sharperatio())
        test_value.append(x.portfoliovalue())
        
    print('--------------------------Min variance strategy----------------------------------')
    print('Min var: ', min(test_var), '\nWeights: ', allowed_permutations[test_var.index(min(test_var))])
    print('--------------------------Max sharpe strategy----------------------------------')
    print('Max sharpe: ', max(test_sharpe), '\nWeights: ', allowed_permutations[test_sharpe.index(max(test_sharpe))])
    print('--------------------------Max return strategy----------------------------------')
    print('Max value: ', max(test_value), '\nWeights: ', allowed_permutations[test_value.index(max(test_value))])
        
# =============================================================================
# Getting portfolio weights using math
# =============================================================================
def minvar_weights():
    covariance_matrix = np.cov(np.array([list(daily_return[i]) for i in daily_return.keys()]))
    covariance_matrix_inverse = np.linalg.inv(covariance_matrix)
    #a_inv * b will give the weights
    a = np.hstack((np.vstack((covariance_matrix,np.ones((1,covariance_matrix.shape[0])))),np.ones((covariance_matrix.shape[0]+1,1))))
    a[a.shape[0]-1,a.shape[0]-1] = 0
    a_inv = np.linalg.inv(a)
    b = np.vstack((np.zeros((covariance_matrix.shape[0],1)),np.ones((1,1))))
    result = np.dot(a_inv,b)
    weights = [round(result[i,0],2) for i in range(result.shape[0]-1)]
    return weights

# =============================================================================
# Min variance weights using dataframe source
# =============================================================================
def minvar_weights2(month,year):
    date_filter = (stock_df.index.month == month) & (stock_df.index.year == year)
    stock = stock_df[date_filter]
    covariance_matrix = np.cov(np.array([stock[i] for i in stock.columns.values]))
    covariance_matrix_inverse = np.linalg.inv(covariance_matrix)
    #a_inv * b will give the weights
    a = np.hstack((np.vstack((covariance_matrix,np.ones((1,covariance_matrix.shape[0])))),np.ones((covariance_matrix.shape[0]+1,1))))
    a[a.shape[0]-1,a.shape[0]-1] = 0
    a_inv = np.linalg.inv(a)
    b = np.vstack((np.zeros((covariance_matrix.shape[0],1)),np.ones((1,1))))
    result = np.dot(a_inv,b)
    weights = [round(result[i,0],2) for i in range(result.shape[0]-1)]
    return weights
    




# =============================================================================
# Testing
# =============================================================================
#x = stockdata(['AAPL', 'TSLA'], dt.datetime(2018,1,1), dt.datetime.now())
#for i in range(1,10,1):
#  print(minvar_weights2(i,2018))

#portfolio_weights_bruteforce()
##minvar_weights()
#minvar_weights2(3,2018)

  


