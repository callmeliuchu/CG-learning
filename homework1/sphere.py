from hittable import Hittable
from vector import dot_product
import math
from hitrecord import HitRecord



class Sphere(Hittable):

    def __init__(self,center,radius,material):
        self.center = center
        self.radius = radius
        self.material = material

    def hit(self,ray,start,end):
        oc = ray.orig - self.center
        a = dot_product(ray.direction,ray.direction)
        half_b = dot_product(oc,ray.direction)
        c = dot_product(oc,oc) - self.radius*self.radius
        delta = half_b*half_b - a*c
        if delta < 0:
            return HitRecord()
        t = (-half_b-math.sqrt(delta))/a
        if t < start or t > end:
            t = (-half_b+math.sqrt(delta))/a
            if t < start or t > end:
                return HitRecord()
        hit_point = ray.at(t)
        normal = (hit_point - self.center)*(1/self.radius)
        hit_record = HitRecord(hit_point,ray.direction,t,self.material)
        hit_record.set_normal(normal)
        return hit_record