# s = '34+(67-89)*32'
#
#
#
# def unpack(s):
#
#
#
# def dfs(s):
#
#
#     for i in range(len(s)):
#         if s[i] == '+':
#             return dfs(s[:i]) + dfs(s[i+1:])
#     for i in range(len(s)-1,-1,-1):
#         if s[i] == '-':
#             return dfs(s[:i]) - dfs(s[i+1:])

import numpy as np
import random
mat = np.array([[50.0,2.0,0.0,1.0,0.0,0.0],
                [0.0,0.0,50,0.0,0.0,0.0],
                [0.0,0.0,2.0,0.0,89.0,0.0],
                [7.0,0.0,2.0,0.0,0.0,0.0],
                [0.0,5.0,2.0,0.0,1.0,2.0],
                [2.0,0.0,0.0,0.0,0.0,8.0]])
m,n = mat.shape
k = 6
U = [[random.random()+1 for _ in range(k)] for _ in range(m)] # 3 * 2
V = [[random.random()+1 for _ in range(n)] for _ in range(k)] # 2 * 4
U = np.array(U)
V = np.array(V)


def gradient():
    resu = []
    VT = V.transpose()
    for i in range(len(U)):
        u = U[i]
        t = np.array([0.0]*len(u))
        for j in range(len(VT)):
            v = VT[j]
            t += 2*(v.dot(u.transpose()) - mat[i][j])*v
        resu.append(t)

    resv = []
    for j in range(len(VT)):
        v = VT[j]
        t = np.array([0.0] * len(v))
        for i in range(len(U)):
            u = U[i]
            t += 2*(v.dot(u.transpose()) - mat[i][j])*u
        resv.append(t)
    return np.array(resu), np.array(resv).transpose()

a = 0.0005
b = a
for _ in range(10000):
    grad_u, grad_v = gradient()
    U = U - grad_u*a
    V = V - grad_v*b
    print(U)
    print(V)
    print(mat)
    res = U.dot(V)
    error = res-mat
    ss = error*error
    print(res)
    print(ss.sum())
    print('-'*50)



