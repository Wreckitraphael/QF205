# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 21:01:09 2018

@author: Raphael Loo
"""
import pandas as pd
import numpy as np
import MatMath as mm

class SummaryStats:
    def __init__(self, data):
        self.data=data
        # data should be a DataFrame with stock tickers as column headers
        if type(self.data)!=pd.DataFrame:
            raise Exception('Wrong datatype')
        self.num_vars=data.shape[1]
        self.datapoints=data.count() #listen here bitch this is a series
        self.headers=list(data.columns)
        
    def mean(self, output_raw=False):
        # arithmetic mean of each stock in data
        # if output_raw==False returns a series, if output_raw==True returns a list
        mu=[sum(self.data.loc[:,i])/self.datapoints[i] for i in self.headers]
        if output_raw==False:
            mu=pd.Series(mu,index=self.headers)
        return mu

    def var(self, sample=False, output_raw=False):
        # variance of each stock in data
        # if sample==False returns the population variance, if sample==True returns the sample variance
        # if output_raw==False returns a series, if output_raw==True returns a list
        mu=self.mean()
        if sample==False:
            variance=[sum([(self.data.loc[j,i]-mu[i])**2 
                     for j in range(self.datapoints[i])])/self.datapoints[i] 
                     for i in self.headers]
        else:
            variance=[sum([(self.data.loc[j,i]-mu[i])**2 
                     for j in range(self.datapoints[i])])/(self.datapoints[i]-1) 
                     for i in self.headers]
        if output_raw==False:
            variance=pd.Series(variance,index=self.headers)
        return variance
    
    def sd(self, sample=False, output_raw=False):
        # standard deviation of each stock in data
        # if sample==False returns the population standard deviation, if sample==True returns the sample standard deviation
        # if output_raw==False returns a series, if output_raw==True returns a list
        variances=self.var(sample, output_raw=True)
        sigma=[i**0.5 for i in variances]
        if output_raw==False:
            sigma=pd.Series(sigma,index=self.headers)  
        return sigma
    
    def cov(self, sample=False, output_raw=False):
        # covariances between each stock in data
        # if sample==False returns the population covariance, if sample==True returns the sample covariance
        # if output_raw==False returns a DataFrame, if output_raw==True returns a ndarray
        mu=self.mean()
        if sample==False:
            cov_mat=[[sum([(self.data.loc[j,i]-mu[i])*(self.data.loc[j,k]-mu[k]) 
                    for j in range(self.datapoints[i])])/self.datapoints[i] 
                    for k in self.headers] 
                    for i in self.headers]
        else:
            cov_mat=[[sum([(self.data.loc[j,i]-mu[i])*(self.data.loc[j,k]-mu[k]) 
                    for j in range(self.datapoints[i])])/(self.datapoints[i]-1) 
                    for k in self.headers] 
                    for i in self.headers]
        if output_raw==True:
            cov_mat=np.array(cov_mat)
        else:
            cov_mat=pd.DataFrame(cov_mat,index=self.headers,columns=self.headers)
        return cov_mat

    def cor(self, output_raw=False):
        # correlations between each stock in data
        # if output_raw==False returns a DataFrame, if output_raw==True returns a ndarray
        cov_mat=self.cov(output_raw=True)
        sigmas=self.sd()
        # create diagonal matrix with 1/sd of each stock in the diagonal
        sd_mat=np.array([[1/sigmas[i] if i==j else 0.0 for j in self.headers] for i in self.headers])
        # transform correlation matrix to covariance matrix => cor_mat = sd_mat*cov_mat*sd_mat
        cor_mat=mm.mmult(mm.mmult(sd_mat,cov_mat),sd_mat)
        if output_raw==False:
            cor_mat=pd.DataFrame(cor_mat,index=self.headers,columns=self.headers)
        return cor_mat
        
        
prices=pd.read_csv('C09.SI.csv')
test=prices.loc[:,'Open':'Close']    
test=SummaryStats(test)
testmean=test.mean()
print(test.var())
print(test.sd())
print(test.cov())
print(test.cor())    
