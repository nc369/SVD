# -*- coding: utf-8 -*-
"""Untitled3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/12zZiBLTH3ts4Zj564wRuNGcMzJugQzN_
"""

import numpy as np

def givens(n,i,j,theta):
    'givens matrix of size n, where i<j'
    mat = np.identity(n)
    mat[i][i] = np.cos(theta)
    mat[i][j] = np.sin(theta)
    mat[j][i] = -np.sin(theta)
    mat[j][j] = np.cos(theta)

    return mat

def find_max(mat):
    'find the coordinates of the greatest modulus element in the upper trinagular region of a square matrix'
    n=mat.shape[0]
    mx=(n-2,n-1)
    for i in range(n-2):
        for j in range(i+1,n):
            if abs(mat[i,j]) > abs(mat[mx[0],mx[1]]):
                mx = [i,j]
    return mx[0],mx[1]

def spectral(mat, epsilon=5,  iterations=250, ):
    """
        approximate spectral decomposition of a real symmetric matrixes using 
        Jacobi method. 
        Returns approximate eigenvalues and eigenvectors ie for A=UDU*, return 
        diagonal of D and U 

        epsilon: non negative integer, defines accuarcy of the decomposition, 
            sets the accuracy to 10 **(-1*epsilon)

        iterations: positive integer, applicable only when kind= 'jacobi'. sets 
        maximum number of multiplication Given's matrix

         fuction uses Givens matrices to find aproximate diagonal entries 
            and corresponding eigenvectors

        
    """

    epsilon = 10**(-1*epsilon)
    n = mat.shape[0]     # size of square matrix
    A = mat      
    P = np.identity(n)

    for i in range(iterations):

        k,l = find_max(A)
        if abs(A[k,l]) < epsilon:
            break
        
        if A[k,k] == A[l,l]:
            tht = np.pi/4
        else:
            u = 2*A[k,l]/(A[l,l] - A[k,k])
            tht = .5 * np.arctan(u)

            Q = givens(n,k,l,tht)
            
            A = (np.transpose(Q) @ A) @ Q
            P = P @ Q
        
    diag = np.copy(np.diag(A))
    
    ind = np.where(diag <0)[0]    
    if len(ind)!=0:                #multiplies eigenvalue and eigenvector with -1 if eigenvalue is negative
        for i in ind:
            diag[i] *= -1
            P[:,i] *= -1

    l = np.argsort(-1*diag)         # orders the eigenvalue and eigenvectors ccording to decreasing order of eiegen values
    P = P[:,[l]].reshape((n,n))
    diag = np.ravel(diag[l])
        
    return diag, P

def svd(A, epsilon=5):
    """
    returns approximate singular value decomposisition of a matrix, 
    U,D,V where A = U * D * transpose(V)

    A: ndarray input

    epsilon: non negative integer, defines accuarcy of the decomposition, 
        sets the accuracy to 10**(-1*epsilon) 
    """

    m,n = A.shape
    trans=0
    if n>m:
        A = np.transpose(A)
        trans = 1
    
    A_t = np.transpose(A)
    D, V = spectral(A_t @ A)
    D = np.sqrt(D)
    U = np.empty(A.shape)

    for i in range(len(D)):
        U[:,i] = (A @ V[:,i]) / D[i]
    
    if trans==1:
        U, V = V ,U

    return D, U, V