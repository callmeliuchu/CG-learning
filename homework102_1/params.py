import math

import numpy as np
import matplotlib.pyplot as plt

pi = np.pi
half_pi = np.pi / 2


# compute the angle between two vector

def unit_form(points):
    m = len(points) - 1
    return [i / m for i in range(len(points))]


def unit_form(points):
    m = len(points) - 1
    return [i / m for i in range(len(points))]


def distance(v1,v2):
    return math.sqrt((v1[0]-v2[0])**2 + (v1[1]-v2[1])**2)

def chordal(points):
    dist = [0]
    for i in range(1,len(points)):
        dist.append(dist[-1] + distance(points[i],points[i-1])**2)
    return [v/dist[-1] for v in dist]



def centripetal(points):
    dist = [0]
    for i in range(1,len(points)):
        dist.append(dist[-1] + distance(points[i],points[i-1]))
    return [v/dist[-1] for v in dist]


def foley(points):
    pass


def generate(arr):
    n = len(arr)
    mat = []
    for t in arr:
        mat.append([np.power(t[0], i) for i in range(n)])
    mat = np.mat(mat)
    mat3 = np.linalg.inv(mat)
    mat2 = [v[1] for v in arr]
    mat2 = np.mat(mat2)
    res = mat3.dot(mat2.transpose())
    params = res
    return params


def func_y(x, n, params):
    arr = [np.power(x, i) for i in range(n)]
    mat1 = np.mat(arr)
    ret = mat1.dot(params)
    return ret.tolist()[0][0]


def fitting(points):
    xt = []
    yt = []
    # ts = unit_form(points)
    ts = centripetal(points)
    for v in zip(ts, points):
        t = v[0]
        x, y = v[1]
        xt.append([t, x])
        yt.append([t, y])
    xt_params = generate(xt)
    yt_params = generate(yt)
    t_seg = [i / 100.0 for i in range(100)]
    xx = [func_y(t, len(points), xt_params) for t in t_seg]
    yy = [func_y(t, len(points), yt_params) for t in t_seg]
    plt.scatter([v[0] for v in points],[v[1] for v in points])
    plt.plot(xx,yy)
    plt.show()


def draw():
    points = [[-3.550000011920929, -0.9100000262260437], [-3.150000035762787, -0.17000001668930054], [-2.649999976158142, 0.22000014781951904], [-1.9500000476837158, 0.48000025749206543], [-1.0800001621246338, 0.6600000858306885], [-0.1100001335144043, 0.3799999952316284], [0.48000001907348633, -0.029999971389770508], [0.7199997901916504, -0.5799999833106995], [0.7999997138977051, -1.559999942779541], [0.5099997520446777, -1.780000001192093], [-0.1700000762939453, -2.050000011920929], [-1.190000057220459, -2.0799999833106995], [-2.2300000190734863, -1.8499999344348907], [-2.4100000858306885, -1.3199999928474426], [-2.3700000047683716, -0.7999999523162842], [-1.3700001239776611, -0.4899998903274536], [-1.1100001335144043, -0.9200000166893005], [-1.2200000286102295, -1.1399999856948853], [-1.5, -1.3100000023841858]]
    fitting(np.array(points[0:11]))

draw()