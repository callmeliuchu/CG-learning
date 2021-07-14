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
        self.material = m

    def hit(self,ray,start,end):
        t = (self.k-ray.orig.z)/(ray.direction.z)
        hit_record = HitRecord()
        if t < start or t > end:
            return hit_record
        p = ray.orig + t*ray.direction
        if p.x < self.x0 or p.x > self.x1 or p.y < self.y0 or p.y > self.y1:
            return hit_record
        hit_record = HitRecord(p, ray.direction, t, self.material)
        normal = Vector3f(0,0,1)
        hit_record.set_normal(normal)
        hit_record.hit_point = p
        u = (p.x-self.x0)/(self.x1-self.x0)
        v = (p.y-self.y0)/(self.y1-self.y0)
        hit_record.uv = (u,v)
        hit_record.material = self.material
        hit_record.set_emitted(self.material.emitted(u,v,normal))
        return hit_record


class XZRect(Hittable):

    def __init__(self,x0,x1,z0,z1,k,m):
        self.x0 = x0
        self.z0 = z0
        self.x1 = x1
        self.z1 = z1
        self.k = k
        self.material = m

    def hit(self,ray,start,end):
        t = (self.k-ray.orig.y)/(ray.direction.y)
        hit_record = HitRecord()
        if t < start or t > end:
            return hit_record
        p = ray.orig + t*ray.direction
        if p.x < self.x0 or p.x > self.x1 or p.z < self.z0 or p.z > self.z1:
            return hit_record
        hit_record = HitRecord(p, ray.direction, t, self.material)
        normal = Vector3f(0,1,0)
        hit_record.set_normal(normal)
        hit_record.hit_point = p
        u = (p.x-self.x0)/(self.x1-self.x0)
        v = (p.z-self.z0)/(self.z1-self.z0)
        hit_record.uv = (u,v)
        hit_record.material = self.material
        hit_record.set_emitted(self.material.emitted(u,v,normal))
        return hit_record


class YZRect(Hittable):

    def __init__(self,y0,y1,z0,z1,k,m):
        self.z0 = z0
        self.y0 = y0
        self.z1 = z1
        self.y1 = y1
        self.k = k
        self.material = m

    def hit(self,ray,start,end):
        t = (self.k-ray.orig.x)/(ray.direction.x)
        hit_record = HitRecord()
        if t < start or t > end:
            return hit_record
        p = ray.orig + t*ray.direction
        if p.y < self.y0 or p.y > self.y1 or p.z < self.z0 or p.z > self.z1:
            return hit_record
        hit_record = HitRecord(p, ray.direction, t, self.material)
        normal = Vector3f(1,0,0)
        hit_record.set_normal(normal)
        hit_record.hit_point = p
        u = (p.y-self.y0)/(self.y1-self.y0)
        v = (p.z-self.z0)/(self.z1-self.z0)
        hit_record.uv = (u,v)
        hit_record.material = self.material
        hit_record.set_emitted(self.material.emitted(u,v,normal))
        return hit_record