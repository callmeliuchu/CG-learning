from hittable import Hittable
from hitrecord import HitRecord
from aabb import *

class HitList(Hittable):

    def __init__(self):
        self.obj_list = []

    def add(self,obj):
        self.obj_list.append(obj)

    def hit(self,ray,start,end):
        max_end = end
        hit_res = HitRecord()
        for obj in self.obj_list:
            hit_rec = obj.hit(ray,start,max_end)
            if hit_rec.is_hit:
                max_end = hit_rec.dist
                hit_res = hit_rec
        return hit_res

    def bounding_box(self,time0,time1):
        temp = None
        for obj in self.obj_list:
            if not temp:
                temp = obj.bounding_box(time0,time1)
            else:
                temp = surrounding_box(temp,obj.bounding_box(time0,time1))
        return temp
