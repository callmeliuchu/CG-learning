import math


def sin(x):
    return math.sin(18000*x)


class Texture:

    def value(self,u,v,p):
        pass


class CheckTexture(Texture):

    def __init__(self,color1,color2):
        self.color1 = color1
        self.color2 = color2

    def value(self,u,v,p):
        sins = sin(p.x)*sin(p.y)*sin(p.z)
        if sins > 0:
            return self.color1
        else:
            return self.color2


class SolidColor(Texture):

    def __init__(self,color):
        self.color = color

    def value(self,u,v,p):
        return self.color
