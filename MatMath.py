# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 14:54:53 2018

@author: Raphael Loo
"""
import numpy as np

def mround(a, epsilon=0):
    # Handles truncation errors
    for i in range(np.size(a,0)):
        for j in range(np.size(a,1)):
            if abs(a[i][j]) < epsilon:
                a[i][j]=0
    return a

def dot(a,b):
    # performs dot product of vectors
    if type(a) and type(b) in [tuple, list]:
        if len(a)!=len(b):
            raise Exception('cannot multiply %i x1 vector with %i x1 vector' % (len(a), len(b)))
        else:
            return sum([a*b for a,b in zip(a,b)])
    elif type(a) and type(b) in [np.ndarray]:
        if np.size(a,0)!=1 or np.size(b,0)!=1:
            raise Exception('arguments are not vectors')
        elif np.size(a,1)!=np.size(b,1):
            raise Exception('cannot multiply %i x1 vector with %i x1 vector' % (len(a), len(b)))
        else:
            total=0
            prod=a*b
            for n in prod[0]:
                total=total+n
            return total
    else:
        raise Exception('wrong datatypes')
            
def transpose(a):
    # transposes a matrix
    a_t=np.empty((np.size(a,1),np.size(a,0)))
    for i in range(np.size(a,0)):
        for j in range(np.size(a,1)):
            a_t[j][i]=a[i][j]
    return a_t
            
def mmult(a,b):
    # performs matrix multiplication
    if np.size(a,1)!=np.size(b,0):
        raise Exception('cannot multiply %ix%i matrix with %ix%i matrix' 
                        % (np.size(a,0), np.size(a,1), np.size(b,0), np.size(b,1)))
    else:
        ab=np.empty((np.size(a,0),np.size(b,1)))
        b_t=transpose(b)
        for i in range(np.size(a,0)):
            for j in range(np.size(b,1)):
                ab[i][j]=dot(np.array(a[i],ndmin=2),np.array(b_t[j],ndmin=2))
        return ab

def i_mat(a):
    # creates identity matrices
    i=np.array([[float(m==n) for m in range(a)] for n in range(a)])
    return i
 
def LU(a):
    # performs LU decomposition of a matrix A using Doolittle algorithm with pivoting
    # returns L,U,P where PA=LU
    l=i_mat(np.size(a,0))
    p=i_mat(np.size(a,0))
    u=a
    # construct permutation matrix P to get best pivot
    for n in range(np.size(a,1)):
        pivot=max(range(min(n,np.size(a,0)),np.size(a,0)), key=lambda i: abs(u[i][n]))
        if n!=pivot:
            row_n=tuple(p[n])
            row_pivot=tuple(p[pivot])
            p[n]=np.array(row_pivot)
            p[pivot]=np.array(row_n)
    # perform pivoting (row swapping) by multiplying U with the permutation matrix P
    u=mmult(p,u)
    # get U into row echelon form (upper triangular matrix) and create L (lower triangular matrix)
    for i in range(np.size(u,0)):
        for k in range(i+1,np.size(u,0)):
            a=u[k][i]/u[i][i]
            u[k]=u[k]-a*u[i]
            l[k][i]=a
    # handle truncation errors
    l=mround(l,epsilon=0.00001)
    u=mround(u,epsilon=0.00001)
    return np.array([l,u,p])
            
def LU_solve(l,u,p,b):
    # solves a decomposed matrix 
    # we have Ax=b and PA=LU => LUx=Pb
    Pb=mmult(p,transpose(b))
    print(Pb)
    # let Y=Ux and solve LY=Pb for Y
    # forward substitution
    Y=[Pb[0]/l[0][0]]
    for i in range(1,np.size(l,0)):
        e=Pb[i]-sum([l[i][j]*Y[j] for j in range(i)])
        Y.append(e)
    # solve Ux=Y for x
    # backward substitution
    n=len(Y)-1
    x=[Y[n]/u[n][n]]
    for i in range(n-1,-1,-1):
        e=Y[i]-sum([u[i][j]*x[n-j] for j in range(i+1,n+1)])
        x.append(e/u[i][i])
    # flip the vector
    x=[x[k] for k in range(len(x)-1,-1,-1)]
    # change list to ndarray
    x=np.array(x,ndmin=2)
    # handle truncation errors
    x=mround(x,epsilon=0.00001)
    return x
        
        
        
           
            

a=np.array([[1,2],[4,5],[7,8]])
b=np.array([[1,0],[0,1]])

# =============================================================================
# print(a)
# print(b)
# print(transpose(b))
# print(mmult(a,b))
# =============================================================================
M=np.array([[1.0,2.0,3.0],[4.0,5.0,6.0],[7.0,8.0,0.0]])
print(LU(M))

from scipy import linalg
p,l,u=linalg.lu(np.array([[1.0,2.0,3.0],[4.0,5.0,6.0],[7.0,8.0,0.0]]))

print(p)
print(l)
print(u)
# =============================================================================
# test=np.empty((np.size(a,1),np.size(a,0)))
# print(test)
# =============================================================================
#print(i_mat(3))
plu=LU(M)
k=np.array([10,11,12],ndmin=2)
print(LU_solve(plu[0],plu[1],plu[2],k))