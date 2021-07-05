from hittable import Hittable
from vector import dot_product,length
from hitrecord import HitRecord
import math



class Sphere(Hittable):

    def __init__(self,center,radius):
        self.center = center
        self.radius = radius

    def hit(self,ray,start,end):
        direct = ray.direction
        orig = ray.orig
        center = self.center
        a = dot_product(direct,direct)
        b = 4*dot_product(orig,direct) - 2*dot_product(direct,center)
        c = 4*dot_product(orig,orig) + dot_product(center,center) \
            - 4*dot_product(orig,center) - self.radius*self.radius
        delta = b*b - 4*a*c
        if delta < 0:
            return HitRecord(False)
        x1 = (-b-math.sqrt(delta))/(2*a)
        t = x1
        if x1 < start or x1 > end:
            x2 = (-b+math.sqrt(delta))/(2*a)
            t = x2
            if x2 < start or x2 > end:
                return HitRecord(False)
        hit_point = ray.at(t)
        normal = hit_point - center
        return HitRecord(True,hit_point,normal.normalize(),t,direct)