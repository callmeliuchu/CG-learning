import math

import numpy as np

from vector import Vector2f
import matplotlib.pyplot as plt




points = [[-3.550000011920929, -0.9100000262260437], [-3.150000035762787, -0.17000001668930054], [-2.649999976158142, 0.22000014781951904], [-1.9500000476837158, 0.48000025749206543], [-1.0800001621246338, 0.6600000858306885], [-0.1100001335144043, 0.3799999952316284], [0.48000001907348633, -0.029999971389770508], [0.7199997901916504, -0.5799999833106995], [0.7999997138977051, -1.559999942779541], [0.5099997520446777, -1.780000001192093], [-0.1700000762939453, -2.050000011920929], [-1.190000057220459, -2.0799999833106995], [-2.2300000190734863, -1.8499999344348907], [-2.4100000858306885, -1.3199999928474426]]




def draw():
    def generate(arr,t):
        if len(arr) == 1:
            return arr[0]
        ret = []
        for i in range(1,len(arr)):
            mid = arr[i-1] + (arr[i] - arr[i-1])*t
            ret.append(mid)
        return generate(ret,t)


    arr = [Vector2f(x,y) for x,y in points]
    xx = []
    yy = []

    for t in range(200):
        p = generate(arr,t/200.0)
        xx.append(p.x)
        yy.append(p.y)


    xx1 = [v[0] for v in points]
    yy1 = [v[1] for v in points]
    plt.plot(xx1,yy1)
    plt.plot(xx, yy)
    plt.show()

def m(n):
    ret = 1
    for k in range(1,n+1):
        ret = ret*k
    return ret

def c_n_i(n,i):
    return m(n)//m(i)//m(n-i)


def bz_func(n,i,t):
    return c_n_i(n,i)*np.power(t,i)*np.power(1-t,n-i)


def f(t,points):
    ret = Vector2f(0,0)
    n = len(points) - 1
    for i,vec in enumerate(points):
        ret += bz_func(n,i,t)*vec
    return ret




arr = [Vector2f(x,y) for x,y in points]
xx = []
yy = []
for i in range(100):
    t = i / 100
    v = f(t,arr)
    xx.append(v.x)
    yy.append(v.y)
xx1 = [v[0] for v in points]
yy1 = [v[1] for v in points]
plt.scatter(xx1,yy1)
plt.plot(xx1,yy1)
plt.plot(xx,yy)
plt.show()






