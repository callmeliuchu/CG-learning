points = [[-3.550000011920929, -0.9100000262260437], [-3.150000035762787, -0.17000001668930054],
          [-2.649999976158142, 0.22000014781951904], [-1.9500000476837158, 0.48000025749206543],
          [-1.0800001621246338, 0.6600000858306885], [-0.1100001335144043, 0.3799999952316284],

          [-2.3700000047683716, -0.7999999523162842], [-1.3700001239776611, -0.4899998903274536],
 ]

# arr = [
#     [1,1],
#     [2,4],
#     [3,5],
#     [4,4],
#     [5,3],
#     [6,2],
#     [7,2],
#     [8,4],
#     [9,5]
# ]
#
# points = arr
import numpy as np


def func_yi_iadd1(x,xi,xi_add1,mi,mi_add1,yi,yi_add1):
    # print(x,xi,xi_add1,mi,mi_add1,yi,yi_add1)
    hi = xi_add1 - xi
    return (1/6)*mi_add1/hi*(x-xi)**3+(1/6)*mi/hi*(xi_add1-x)**3 + (yi_add1/hi-1/6*hi*mi_add1)*(x-xi) + \
           (yi/hi-1/6*hi*mi)*(xi_add1-x)


def get_param(points):
    n = len(points)
    mat = [[0]*(n-2) for _ in range(n-2)]
    y_arr = []
    for i in range(1,n-1):
        xi_add1,yi_add1 = points[i+1]
        xi,yi = points[i]
        xi_del1,yi_del1 = points[i-1]
        hi = xi_add1 - xi
        hi_del1 = xi - xi_del1
        if i == 1:
            mat[0][0] = 1/3*(hi+hi_del1)
            mat[0][1] = 1/6*hi
        elif i == n-2:
            mat[i-1][i-1] = 1/3*(hi+hi_del1)
            mat[i-1][i-2] = 1/6*hi_del1
        else:
            hi_del1 = xi - xi_del1
            mat[i-1][i-2] = 1 / 6 * hi_del1
            mat[i-1][i-1] = 1/3*(hi+hi_del1)
            mat[i-1][i] = 1/6*hi
        y_arr.append((yi_add1 - yi) / hi - (yi - yi_del1) / hi_del1)
    mat = np.mat(mat)
    tmp = np.linalg.inv(mat)
    y_arr = np.array(y_arr).transpose()
    res = tmp.dot(y_arr)
    res = res.tolist()[0]
    return res
import matplotlib.pyplot as plt
params = get_param(points)
params = [0] + params + [0]
print(params)
n = len(points)
print(n,len(params))
xx1 = [v[0] for v in points]
yy1 = [v[1] for v in points]
plt.scatter(xx1,yy1)
for i in range(0,n-1):
    xi,yi = points[i]
    xi_add1,yi_add1 = points[i+1]
    mi = params[i]
    mi_add1 = params[i+1]
    dis = xi_add1 - xi
    xx = [k/1000*dis + xi for k in range(1000)]
    yy = [func_yi_iadd1(v,xi,xi_add1,mi,mi_add1,yi,yi_add1) for v in xx]
    print(xx)
    print(yy)

    plt.plot(xx,yy)

plt.show()
