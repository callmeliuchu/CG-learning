from hittable import Hittable
from hitrecord import HitRecord


class HitList(Hittable):

    def __init__(self):
        self.obj_list = []

    def add(self,obj):
        self.obj_list.append(obj)

    def hit(self,ray,start,end):
        max_end = end
        hit_res = HitRecord(False)
        for obj in self.obj_list:
            hit_record = obj.hit(ray,start,max_end)
            if hit_record.is_hit:
                hit_res = hit_record
                max_end = hit_record.closest_far
        return hit_res
