# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 04:36:22 2018

@author: mrloo
"""

import numpy as np
import pandas as pd
import MatMath as mm

def max_sharpe(cov_mat,expected_return,rf):
    # implements equation 1.32
    one_vec=np.array([1 for i in range(len(expected_return))],ndmin=2)
    rf_vec=rf*one_vec
    e_r=np.array(expected_return,ndmin=2)
    cov_mat_inv=mm.m_inv(cov_mat)
    # note use of explicit line continuation below
    weights=mm.mmult(cov_mat_inv,mm.transpose(e_r-rf_vec))\
    /float(mm.mmult(mm.mmult(one_vec,cov_mat_inv),mm.transpose(e_r-rf_vec)))
    if sum(weights)!=1.0:
        raise Exception('Weights do not sum to 1')
    return weights

prices=pd.read_csv('C09.SI.csv')
test=prices.loc[:,'Open':'Close']

import Summarystatsv2 as ss

test=SummaryStats(test)
cov=test.cov(output_raw=True)
expr=test.mean(output_raw=True)
r=.05

print(cov)
print(expr)
print(max_sharpe(cov,expr,r))
