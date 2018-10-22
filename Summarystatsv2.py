# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 21:01:09 2018

@author: Raphael Loo
"""
import pandas as pd
import numpy as np

class SummaryStats:
    def __init__(self, data):
        self.data=data
        if type(self.data)!=pd.DataFrame:
            raise Exception('Wrong datatype')
        self.num_vars=data.shape[1]
        self.datapoints=data.count() #listen here bitch this is a series
        self.headers=list(data.columns)
        
    def mean(self, output_raw=False):
        mu=[(sum(self.data.iloc[:,i])/self.data.iloc[:,i].shape[0]) for i in range(self.num_vars)]
        if output_raw==False:
            mu=pd.Series(mu,index=self.headers)
        return mu

    def var(self, sample=False, output_raw=False):
        mu=self.mean()
        if sample==False:
            variance=[sum([(self.data.loc[j,i]-mu[i])**2 for j in range(self.datapoints[i])])/self.datapoints[i] for i in self.headers]
        else:
            variance=[sum([(self.data.loc[j,i]-mu[i])**2 for j in range(self.datapoints[i])])/(self.datapoints[i]-1) for i in self.headers]
        if output_raw==False:
            variance=pd.Series(variance,index=self.headers)
        return variance
    
    def sd(self, sample=False, output_raw=False):
        variances=self.var(sample, output_raw=True)
        sigma=[i**.5 for i in variances]
        if output_raw==False:
            sigma=pd.Series(variances,index=self.headers)  
        return sigma
    
    def cov(self, sample=False, output_raw=False):
        mu=self.mean()
        if sample==False:
            cov_mat=[[sum([(self.data.loc[j,i]-mu[i])*(self.data.loc[j,k]-mu[k]) for j in range(self.datapoints[i])])/self.datapoints[i] for k in self.headers] for i in self.headers]
        else:
            cov_mat=[[sum([(self.data.loc[j,i]-mu[i])*(self.data.loc[j,k]-mu[k]) for j in range(self.datapoints[i])])/(self.datapoints[i]-1) for k in self.headers] for i in self.headers]
        if output_raw==True:
            cov_mat=np.array(cov_mat)
        else:
            cov_mat=pd.DataFrame()
        return cov_mat

prices=pd.read_csv(r"C:\Users\Vincent Loo\Documents\Python Scripts\QF205 Project\QF205\C09.SI.csv")
test=prices.loc[:,'Open':'Close']    
test=SummaryStats(test)
testmean=test.mean()
#print(testmean['Open'])
print(test.var())
print(test.cov())    
