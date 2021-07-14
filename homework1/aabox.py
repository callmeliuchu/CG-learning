from aarect import *
from hit_list import HitList


class Box(Hittable):

    def __init__(self,p_min,p_max,material):
        self.box = HitList()
        self.xy1 = XYRect(p_min.x, p_max.x, p_min.y, p_max.y, p_min.z, material)
        self.xy2 = XYRect(p_min.x, p_max.x, p_min.y, p_max.y, p_max.z, material)
        self.xz1 = XZRect(p_min.x, p_max.x, p_min.z, p_max.z, p_min.y, material)
        self.xz2 = XZRect(p_min.x, p_max.x, p_min.z, p_max.z, p_max.y, material)
        self.yz1 = YZRect(p_min.y, p_max.y, p_min.z, p_max.z, p_min.x, material)
        self.yz2 = YZRect(p_min.y, p_max.y, p_min.z, p_max.z, p_max.x, material)
        self.box.add(self.xy1)
        self.box.add(self.xy2)
        self.box.add(self.xz1)
        self.box.add(self.xz2)
        self.box.add(self.yz1)
        self.box.add(self.yz2)

    def hit(self,ray,start,end,hit_record):
        return self.box.hit(ray,start,end,hit_record)