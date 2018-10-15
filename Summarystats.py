# -*- coding: utf-8 -*-
"""
Created on Sun Oct  7 22:29:17 2018

@author: Raphael Loo
"""
import numpy as np

class SummaryStats:
    def __init__(self, *args):
# =============================================================================
#         checks that args passed are tuple, list or ndarray
#         if args is an ndarray, only accepts 1 ndarray and self.a is the ndarray
#         if args are tuples or lists, checks that they are of the same length and self.a is a list of args
# =============================================================================
        if len(args)==1:
            if type(args[0]) not in [tuple, list, np.ndarray]:
                raise Exception('wrong datatype, stupid')
            elif type(args[0]) in [np.ndarray]:
                self.a=args[0]
            else:   
                self.a=list(args)
        elif len(args)>1:
            typ=[]
            dim=[] 
            for n in range(len(args)):
                 typ.append(type(args[n]))
                 if type(args[n])!=typ[0]:
                     raise Exception('inconsistent datatypes you idiot')
                     break
                 if type(args[n])==np.ndarray:
                     raise Exception('cannot accept more than one array')
                     break
                 elif type(args[n]) in [tuple, list]:
                     dim.append(len(args[n]))
                     if len(args[n])!=dim[0]:
                         raise Exception('inconsistent dimensions')
                         break
                     else:
                         check=True
                 else:
                    raise Exception('wrong datatype, stupid')
            if check==True:
                self.a=list(args)
        else:
            raise Exception('no data')
    
    def mean(self):
# =============================================================================
#         finds the arithmetic mean
#         if self.a is a single tuple or list, returns the mean as a float
#         else returns the mean as a list [mean(x1), mean(x2), ... ]
# =============================================================================
        if len(self.a)==1:
            mu=sum(self.a[0])/len(self.a[0])
        else:
            mu=[]
            mu=[sum(self.a[n])/len(self.a[n]) for n in range(len(self.a))]
        return mu
    
    def var(self, pop_samp='p'):
# =============================================================================
#         finds the population variance if pop_samp='p' (default), the sample variance if pop_samp='s'
#         if self.a is a single tuple or list, returns the variance as a float
#         else returns the variance as a list [var(x1), var(x2), ... ]
# =============================================================================
        mu=self.mean()
        if len(self.a)==1:    
            sqerr=[]
            sqerr=[(self.a[0][n]-mu)**2 for n in range(len(self.a[0]))]
            if pop_samp=='p':
                return sum(sqerr)/len(sqerr)
            elif pop_samp=='s':
                return sum(sqerr)/(len(sqerr)-1)
        else:
           var=[]
           for n in range(len(self.a)):
               sqerr=0
               for m in range(len(self.a[0])):
                   sqerr=sqerr+(self.a[n][m]-mu[n])**2
               var.append(sqerr/len(self.a[0]))
           return var
        
    def sd(self, pop_samp='p'):
# =============================================================================
#         finds the population standard deviation if pop_samp='p' (default), the sample standard deviation if pop_samp='s'
#         if self.a is a single tuple or list, returns the standard deviation as a float
#         else returns the variance as a list [sd(x1), sd(x2), ... ]
# =============================================================================
        if len(self.a)==1:    
            variance=self.var(pop_samp)
            sig=variance**0.5
            return sig
        else:
            sig=[]
            sig=[self.var(pop_samp)[n]**0.5 for n in range(len(self.var(pop_samp)))]
            return sig
    
    def cov(self, pop_samp='p'):
# =============================================================================
#         finds the population variance if pop_samp='p' (default), the sample variance if pop_samp='s'
# =============================================================================
        if len(self.a)==1 and type(self.a) not in [np.ndarray]:
            raise Exception('only 1 variable')
        elif len(self.a)==2 and type(self.a) not in [np.ndarray]:
            mu=self.mean()
            err=[]
            err=[(self.a[0][n]-mu[0])*(self.a[1][n]-mu[0]) for n in range(len(self.a[0]))]
            if pop_samp=='p':
                return sum(err)/len(err)
            elif pop_samp=='s':
                return sum(err)/(len(err)-1)
        else:
            mu=self.mean()
            if type(self.a)==np.ndarray:
                X=np.empty((np.size(self.a,0),np.size(self.a,0)))
            else:
                X=np.empty((len(self.a),len(self.a)))
            for i in range(np.size(X,0)):
                for j in range(np.size(X,1)):
                    err=0
                    for k in range(len(self.a[0])):
                        err=err+((self.a[i][k]-mu[i])*(self.a[j][k]-mu[j]))
                    if pop_samp=='p':
                        X[i,j]=(err/len(self.a[0]))
                    elif pop_samp=='s':
                        X[i,j]=(err/(len(self.a[0]-1)))
            return X
            
data=np.array([[0,1,2],[2,1,0]])    
test=SummaryStats(data)
#print(test.mean())
#print(test.var())
print(test.cov())
print(np.cov(data,bias=True))
    
