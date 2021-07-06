from hittable import Hittable
from hitrecord import HitRecord


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
