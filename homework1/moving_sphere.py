from hittable import Hittable
from vector import dot_product
from hitrecord import HitRecord
import math


class MovingSphere(Hittable):

    def __init__(self,center0,center1,tm1,tm2,radius,material):
        self.center0 = center0
        self.center1 = center1
        self.radius = radius
        self.material = material
        self.tm1 = tm1
        self.tm2 = tm2

    def cal_center(self,tm):
        return self.center0 + (self.center1 - self.center0)*((tm-self.tm1)/(self.tm2-self.tm1))

    @staticmethod
    def get_uv_from(point):
        fi = math.atan2(-point.z,point.x) + math.pi
        theta = math.acos(-point.y)
        return fi / (2 * math.pi), theta / math.pi

    def hit(self,ray,start,end):
        cen = self.cal_center(ray.tm)
        oc = ray.orig - cen
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
        normal = (hit_point - cen)*(1/self.radius)
        hit_record = HitRecord(hit_point,ray.direction,t,self.material)
        hit_record.set_normal(normal)
        hit_record.tm = ray.tm
        u,v = self.get_uv_from(normal)
        hit_record.set_emitted(self.material.emitted(u,v,normal))
        return hit_record
