from hittable import Hittable
from hitrecord import HitRecord
from vector import Vector3f


class XYRect(Hittable):

    def __init__(self,x0,x1,y0,y1,k,m):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.k = k
        self.m = m

    def hit(self,ray,start,end):
        t = (self.k-ray.orig.z)/(ray.direction.z)
        hit_record = HitRecord()
        if t < start or t > end:
            return hit_record
        p = ray.orig + t*ray.direction
        if p.x < self.x0 or p.x > self.x1 or p.y < self.y0 or p.y > self.y1:
            return hit_record
        normal = Vector3f(0,0,1)
        hit_record.set_normal(normal)
        hit_record.hit_point = p
        u = (p.x-self.x0)/(self.x1-self.x0)
        v = (p.y-self.y0)/(self.y1-self.y0)
        hit_record.uv = (u,v)
        hit_record.material = self.m
        return hit_record