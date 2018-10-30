# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 04:36:22 2018

@author: mrloo
"""
import numpy as np
import pandas as pd
import Summarystatsv2 as stats
import MatMath as mat


def min_var(cov_mat):
    cov_mat_dim=np.size(cov_mat, axis=0)
    matrix=[[cov_mat[i][j] if j<cov_mat_dim else 1 for j in range(cov_mat_dim+1)]
           if i<cov_mat_dim else [1 if j<cov_mat_dim else 0 for j in range(cov_mat_dim+1)] 
           for i in range(cov_mat_dim+1)]
    matrix=np.array(matrix)
    lup=mat.LU(matrix)
    b=np.array([0 if i<cov_mat_dim else 1 for i in range(cov_mat_dim+1)],ndmin=2)
    weights=mat.LU_solve(lup,b)[0][:-1]
    return list(weights)

        
def max_sharpe(cov_mat,expected_return,rf):
    # implements equation 1.32
    one_vec=np.array([1 for i in range(len(expected_return))],ndmin=2)
    rf_vec=rf*one_vec
    e_r=np.array(expected_return,ndmin=2)
    cov_mat_inv=mat.m_inv(cov_mat)
    # note use of explicit line continuation below
    weights=mat.mmult(cov_mat_inv,mat.transpose(e_r-rf_vec))\
    /float(mat.mmult(mat.mmult(one_vec,cov_mat_inv),mat.transpose(e_r-rf_vec)))
    if sum(weights)!=1.0:
        raise Exception('Weights do not sum to 1')
    weights=mat.transpose(weights)
    return list(weights[0])

def max_ev(means):
    max_ev=max(means)
    weights=[float(i==max_ev) for i in means]
    return weights

# =============================================================================
# prices=pd.read_csv('C09.SI.csv')
# test=prices.loc[:,'Open':'Close']
# 
# import Summarystatsv2 as ss
# 
# test=SummaryStats(test)
# cov=test.cov(output_raw=True)
# expr=test.mean(output_raw=True)
# r=.05
# 
# print(cov)
# print(expr)
# print(max_sharpe(cov,expr,r))
# print(min_var(cov))
# print(max_ev(expr))
# =============================================================================
