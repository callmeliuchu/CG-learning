from hittable import Hittable
from aabb import surrounding_box
import functools
import random
from hitrecord import HitRecord


def compare_x(a,b):
    return compare(a,b,0)


def compare_y(a,b):
    return compare(a,b,1)


def compare_z(a,b):
    return compare(a,b,2)


def compare(a,b,axis):
    return a.point_min[axis] - b.point_max[axis]


def get_cmp(axis):
    if axis == 0:
        return compare_x
    elif axis == 1:
        return compare_y
    return compare_z


class BVH(Hittable):
    box = None
    left = None
    right = None

    def __init__(self,obj_list,bg,ed,time0,time1):
        axis = random.randint(0,2)
        obj_list.sorted(key=functools.cmp_to_key(get_cmp(axis)))
        n = len(obj_list)
        if n == 1:
            self.left = obj_list[0]
            self.right = self.left
        elif n == 2:
            self.left = obj_list[0]
            self.right = obj_list[1]
        else:
            mid = n // 2
            self.left = BVH(obj_list,bg,mid,time0,time1)
            self.right = BVH(obj_list,mid+1,ed,time0,time1)
        box_left = self.left.bounding_box(time0,time1)
        box_right = self.right.bounding_box(time0,time1)
        self.box = surrounding_box(box_left,box_right)

    def bounding_box(self,tim0,time1):
        return self.box

    def hit(self,ray,start,end):
        if not self.box.hit(ray,start,end):
            return HitRecord()
        hit_left = self.left.hit(ray,start,end)
        hit_right = self.right.hit(ray,start,hit_left.tm if hit_left.is_hit else end)





