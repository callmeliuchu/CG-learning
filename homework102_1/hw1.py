
arr = [
    [1,1],
    [2,4],
    [3,5],
    [4,4],
    [5,3],
    [6,2],
    [7,2],
    [8,4],
    [9,5]
]

def show(x,y):
    plt.figure(figsize=(10, 10), dpi=100)
    plt.plot(x, y)
    plt.show()


import matplotlib.pyplot as plt
import numpy as np
import math


def generate():
    n = len(arr)
    mat = []
    for t in arr:
        mat.append([np.power(t[0],i) for i in range(n)])
    mat = np.mat(mat)
    print(mat)
    mat3 = np.linalg.inv(mat)
    mat2 = [v[1] for v in arr]
    mat2 = np.mat(mat2)

    res = mat3.dot(mat2.transpose())
    params = res
    # print(params)
    return params



def guss_funci(x,xi):
    a = 1
    return math.exp(-(x-xi)**2/(2*a*a))



def generate_guess():
    mat = []
    for t in arr:
        mat.append([guss_funci(x[0],t[0]) for x in arr])
    mat = np.mat(mat)
    print(mat)
    mat3 = np.linalg.inv(mat)
    mat2 = [v[1] for v in arr]
    mat2 = np.mat(mat2)

    res = mat3.dot(mat2.transpose())
    params = res
    # print(params)
    return params

def guess_y(x,xx,params):
    r = [guss_funci(x,xi) for xi in xx]
    r = np.mat(r)
    ret = r.dot(params)
    return ret.tolist()[0][0]

def show_guess():
    params = generate_guess()
    in_xx = [v[0] for v in arr]
    xx = [i/10.0 for i in range(10,100)]
    yy = [guess_y(h,in_xx,params) for h in xx]
    print(xx)
    print(yy)
    show(xx,yy)



def func_y(x,n,params):
    arr = [np.power(x,i) for i in range(n)]
    mat1 = np.mat(arr)
    ret = mat1.dot(params)
    return ret.tolist()[0][0]


def func1():
    params = generate()
    y = func_y(9,len(arr),params)
    xx = [i/10.0 for i in range(10,90)]
    yy = [func_y(h,len(arr),params) for h in xx]
    print(xx)
    print(yy)
    show(xx,yy)

def lage(x,y):
    pass


def fi(x,xx,i):
    ret = 1
    for k in range(len(xx)):
        xt = xx[k]
        if k != i:
            ret = ret * (x-xt)/(xx[i]-xt)
    return ret


def func(x,xx,yy):
    return sum(fi(x,xx,i)*yy[i] for i in range(len(xx)))


def gen1():

    xx = [v[0] for v in arr]
    yy = [v[1] for v in arr]


    x_input = [i/10.0 for i in range(10,100)]
    y_input = [func(x,xx,yy) for x in x_input]
    print(x_input)
    print(y_input)
    show(x_input,y_input)


def cal_one_item(xx,n):
    return sum(np.power(x,n) for x in xx)

def cal_xy(xx,yy,n):
    return sum(y*np.power(x,n) for x,y in zip(xx,yy))


def cal_params(xx,yy,n,lambdaa=0.2):
    mat = []
    for i in range(n+1):
        mat.append([cal_one_item(xx,i+j) + lambdaa if i == j else cal_one_item(xx,i+j) for j in range(n+1)])
    A = np.mat(mat)
    B = np.mat([cal_xy(xx,yy,i) for i in range(n+1)])
    B = B.transpose()
    params = np.linalg.inv(A).dot(B)
    return params.transpose().tolist()[0]


def cal_result(params,x):
    n = len(params)
    return sum(params[i]*np.power(x,i) for i in range(n))


def show_aaaa():
    xx = [v[0] for v in arr]
    yy = [v[1] for v in arr]
    params = cal_params(xx,yy,5)
    xx1 = [i/10 for i in range(10,90)]
    yy1 = [cal_result(params,h) for h in xx1]
    print(xx)
    print(yy)
    plt.plot(xx, yy)
    plt.plot(xx1,yy1)
    # plt.show()
    # show(xx1,yy1)
    plt.show()



show_aaaa()

def f():
    pass





