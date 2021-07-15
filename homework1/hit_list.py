from hittable import Hittable
from aabb import *


class HitList(Hittable):

    def __init__(self):
        self.obj_list = []

    def add(self, obj):
        self.obj_list.append(obj)

    def hit(self, ray, start, end, hit_record):
        max_end = end
        hit_res = False
        for obj in self.obj_list:
            if obj.hit(ray, start, max_end, hit_record):
                max_end = hit_record.dist
                hit_res = True
        return hit_res

    def bounding_box(self, time0, time1):
        temp = None
        for obj in self.obj_list:
            if not temp:
                temp = obj.bounding_box(time0, time1)
            else:
                temp = surrounding_box(temp, obj.bounding_box(time0, time1))
        return temp
