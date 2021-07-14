from hittable import Hittable
from vector import dot_product,Vector3f
from hitrecord import HitRecord
import math
from aabb import AABB,surrounding_box


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

    def hit(self,ray,start,end,hit_record):
        cen = self.cal_center(ray.tm)
        oc = ray.orig - cen
        a = dot_product(ray.direction,ray.direction)
        half_b = dot_product(oc,ray.direction)
        c = dot_product(oc,oc) - self.radius*self.radius
        delta = half_b*half_b - a*c
        if delta < 0:
            return False
        t = (-half_b-math.sqrt(delta))/a
        if t < start or t > end:
            t = (-half_b+math.sqrt(delta))/a
            if t < start or t > end:
                return False
        hit_point = ray.at(t)
        normal = (hit_point - cen)*(1/self.radius)
        hit_record.set(hit_point,ray.direction,t,self.material)
        hit_record.set_normal(normal)
        hit_record.tm = ray.tm
        u,v = self.get_uv_from(normal)
        hit_record.set_emitted(self.material.emitted(u,v,normal))
        return True

    def bounding_box(self,tim0,time1):
        aabb1 = AABB(self.center0-Vector3f(self.radius,self.radius,self.radius),
                     self.center0+Vector3f(self.radius,self.radius,self.radius))
        aabb2 = AABB(self.center1-Vector3f(self.radius,self.radius,self.radius),
                     self.center1+Vector3f(self.radius,self.radius,self.radius))
        return surrounding_box(aabb1,aabb2)

