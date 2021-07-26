import random

import numpy as np
import os
import json
import matplotlib.pyplot as plt
import math


arr = [
    [1,1],
    [2,4],
    [3,5],
    [4,4],
    [5,3],
    [6,2],
    [7,2],
    [8,4],
    [8.5,19],
    [9,5],
]



def guass(x,c,b,w):
    return w*math.exp(-(x-c)**2/b)


def f(x,cc,bb,ww):
    return sum(guass(x,c,b,w) for c,b,w in zip(cc,bb,ww))


def loss(xx,yy,cc,bb,ww):
    return sum((f(x,cc,bb,ww)-y)**2 for x,y in zip(xx,yy))


def delta_c(xx,yy,cc,bb,ww,axis):
    ci = cc[axis]
    bi = bb[axis]
    wi = ww[axis]
    return sum(2*(f(x,cc,bb,ww)-y)*guass(x,ci,bi,wi)*2*(x-ci)/bi for x,y in zip(xx,yy))


def delta_b(xx,yy,cc,bb,ww,axis):
    ci = cc[axis]
    bi = bb[axis]
    wi = ww[axis]
    return sum(2*(f(x,cc,bb,ww)-y)*guass(x,ci,bi,wi)*(x-ci)**2/(bi**2) for x,y in zip(xx,yy))


def delta_w(xx,yy,cc,bb,ww,axis):
    ci = cc[axis]
    bi = bb[axis]
    return sum(2*(f(x,cc,bb,ww)-y)*guass(x,ci,bi,1) for x,y in zip(xx,yy))


def main():
    n = 3
    xx = [v[0] for v in arr]
    yy = [v[1] for v in arr]
    min_x = min(xx)
    max_x = max(xx)
    cc = np.array([random.uniform(min_x,max_x) for _ in range(n)])
    bb = np.array([1]*n)
    ww = np.array([1]*n)
    # if os.path.exists('result.json'):
    #     with open('result.json', 'r') as f1:
    #         data = json.load(f1)
    # cc, bb, ww = data
    r = 0.0001
    epoch = 100000000
    for k in range(epoch):
        a_loss = loss(xx,yy,cc,bb,ww)
        delta_ww = np.array([delta_w(xx, yy, cc, bb, ww, i) for i in range(n)])*r
        delta_bb = np.array([delta_b(xx, yy, cc, bb, ww, i) for i in range(n)])*r
        delta_cc = np.array([delta_c(xx, yy, cc, bb, ww, i) for i in range(n)])*r
        ww = ww - delta_ww
        bb = bb - delta_bb
        cc = cc - delta_cc

        if k % 1000 == 0:
            print(ww)
            print(bb)
            print(cc)
            print(k,a_loss)

        if a_loss < 18:
            if k % 10 == 0:
                ret = [cc.tolist(),bb.tolist(),ww.tolist()]
                with open('result.json','w') as f:
                    json.dump(ret,f)



# main()

def draw():
    with open('result.json','r') as f1:
        data = json.load(f1)

    cc,bb,ww = data
    # print(f(8,cc,bb,ww))

    def show_aaaa():
        xx = [v[0] for v in arr]
        yy = [v[1] for v in arr]
        xx1 = [i/10 for i in range(10,90)]
        yy1 = [f(h,cc,bb,ww) for h in xx1]
        print(xx)
        print(yy)
        plt.plot(xx, yy)
        plt.plot(xx1,yy1)
        # plt.show()
        # show(xx1,yy1)
        plt.show()

    show_aaaa()


# main()
draw()

