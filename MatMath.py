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
    # performs dot product of vectors (given as 2D numpy array)
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
            prod=a*b
            return sum(sum(prod))
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
    return (l,u,p)
            
def LU_solve(a,b):
    # solves a decomposed matrix
    l,u,p=a
    # we have Ax=b and PA=LU => LUx=Pb
    Pb=mmult(p,transpose(b))
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
    x=transpose(x)
    # handle truncation errors
    x=mround(x,epsilon=0.00001)
    return x
        
def m_inv(a):
    # finds inverse of a matrix A using its LU decomposition
    # AA^-1=I, PA=LU
    # PAA^-1=PI => LUA^-1=P
    # rewrite as LU[v1,v2,...,vn]=[i1,i2,...,in] where v1,v2,...,vn are the column vectors of A^-1 and i1,i2,...in are the column vectors of I
    #solve LUvj=ij for i=1,2,...,n to get each vj and we have A^-1
    if np.size(a,0)!=np.size(a,1):
        raise Exception('A not square')
    else:
        # decompose A
        lu_a=LU(a)
        # initialise A^-1 as a zero matrix
        a_inv=np.zeros((np.size(a,0),np.size(a,0)))
        # create I 
        # swapping of rows to get P from I will be done by LU_solve
        rhs=i_mat(np.size(a,0))
        for i in range(np.size(a,0)):
            # get each ij
            col=np.array([rhs[i][j] for j in range(np.size(a,0))],ndmin=2)
            # solve for each vj
            v=LU_solve(lu_a,col)
            a_inv[i]=v
        # vj has been added row-wise to a_inv therefore needs to be transposed
        a_inv=transpose(a_inv)
        return a_inv
    

           
            

