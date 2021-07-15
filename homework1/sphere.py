from hittable import Hittable
from vector import dot_product,Vector3f
import math
from aabb import AABB


class Sphere(Hittable):

    def __init__(self,center,radius,material):
        self.center = center
        self.radius = radius
        self.material = material

    @staticmethod
    def get_uv_from(point):
        fi = math.atan2(-point.z,point.x) + math.pi
        theta = math.acos(-point.y)
        return fi / (2 * math.pi), theta / math.pi

    def hit(self,ray,start,end,hit_record):
        oc = ray.orig - self.center
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
        normal = (hit_point - self.center)*(1/self.radius)
        hit_record.set(hit_point,ray.direction,t,self.material)
        hit_record.set_normal(normal)
        u,v = self.get_uv_from(normal)
        hit_record.p = normal
        hit_record.set_emitted(self.material.emitted(u,v,normal))
        return True

    def bounding_box(self,time0,time1):
        aabb = AABB(self.center-Vector3f(self.radius,self.radius,self.radius),
                    self.center+Vector3f(self.radius,self.radius,self.radius))
        return aabb