import numpy as np


def sigmoid(x):
    return np.exp(x)/(1+np.exp(x))


def diff_sigmoid(x):
    return np.exp(x)/(1+np.exp(x))/(1+np.exp(x))


class BackPropagation:

    def __init__(self,input_layer,output_layer):
        hidden_layers = [2,2]
        layers = [input_layer] + hidden_layers + [output_layer]
        self.ws = []
        # self.bs = []
        for i in range(1,len(layers)):
            w = np.mat(np.random.rand(layers[i],layers[i-1]))
            # b = np.mat(np.random.rand(layers[i],1))
            # self.bs.append(b)
            self.ws.append(w)

    def p(self,input_vec):
        ret = []
        for w in self.ws:
            h = w.dot(input_vec)
            new_vec = sigmoid(h)
            ret.append((input_vec,w,h,new_vec))
            input_vec = new_vec
        return ret

    def back(self,input_vec,output_vec):
        res = self.p(input_vec)
        wss = []
        bss = []
        diff_out = None
        for i in range(len(res)-1,-1,-1):
            input_v,w,h,out_v = res[i]
            if diff_out is None:
                diff_out = out_v - output_vec
                print(np.sum(np.array(diff_out) ** 2))
            delta_z = np.multiply(diff_out,diff_sigmoid(h))
            delta_w = delta_z * input_v.transpose()
            w = w - delta_w*0.9
            # print(delta_b)
            # b = b - delta_b*0.1
            wss.append(w)
            diff_out = w.transpose().dot(delta_z)
        wss.reverse()
        bss.reverse()
        self.ws = wss
        self.bs = bss


def get_vec(arr):
    return np.mat(arr).transpose()

# [0,0],1
# [0,1],0
# [1,1],1
# [1,0],0
back = BackPropagation(1,1)

# input_vec = np.mat([[0,0],[0,1],[1,1],[1,0]]).transpose()
# output_vec = np.mat([[1],[0],[1],[0]]).transpose()



# print(back.p(np.mat([0,0]).transpose())[-1][-1])
# print(back.p(np.mat([0,1]).transpose())[-1][-1])
# print(back.p(np.mat([1,1]).transpose())[-1][-1])
# print(back.p(np.mat([1,0]).transpose())[-1][-1])

# print(back.p(np.mat([0,0]).transpose())[-1][-1])


# v1 = np.mat([1,5,7,4]).transpose()
# v2 = np.mat([0.1,0.2,0.3,0.4,0.5,0.6,0.7]).transpose()


# print(hh)
# print(np.sum(hh,axis=1))


# for _ in range(10):
#     for v1,v2 in ret:
#         for _ in range(10000):
#             back.back(np.mat(v1).transpose(),np.mat(v2).transpose())
#
# q = back.p(np.mat([0,0]).transpose())[-1][-1]
# print(q)
# q = back.p(np.mat([0,1]).transpose())[-1][-1]
# print(q)
# q = back.p(np.mat([1,0]).transpose())[-1][-1]
# print(q)
# q = back.p(np.mat([1,1]).transpose())[-1][-1]
# print(q)
# print(back.p(np.mat([1,1]).transpose())[-1][-1])
# print(back.p(np.mat([0,1]).transpose())[-1][-1])
# print(back.p(np.mat([1,0]).transpose())[-1][-1])



# import matplotlib as plt
#
#
def load_data():
    x = np.arange(0.0,1.0,0.1)
    y = np.sin(2*np.pi*x)
    # 数据可视化
    return x,y
#进行测试
x,y = load_data()
x = x.reshape(1,10)
y = y.reshape(1,10)


for _ in range(1000000):
    back.back(x,y)
