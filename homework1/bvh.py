from hittable import Hittable
from aabb import surrounding_box
import functools
import random


def compare_x(a,b):
    return compare(a,b,0)


def compare_y(a,b):
    return compare(a,b,1)


def compare_z(a,b):
    return compare(a,b,2)


def compare(a,b,axis):
    a_box = a.bounding_box(0,0)
    b_box = b.bounding_box(0,0)
    return a_box.point_min[axis] - b_box.point_max[axis]


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

    def __init__(self,obj_list,time0,time1):
        axis = random.randint(0,2)
        n = len(obj_list)
        obj_list.sort(key=functools.cmp_to_key(get_cmp(axis)))
        if n == 1:
            self.left = obj_list[0]
            self.right = self.left
        elif n == 2:
            self.left = obj_list[0]
            self.right = obj_list[1]
        else:
            mid = n // 2
            self.left = BVH(obj_list[:mid],time0,time1)
            self.right = BVH(obj_list[mid:],time0,time1)
        box_left = self.left.bounding_box(time0,time1)
        box_right = self.right.bounding_box(time0,time1)
        self.box = surrounding_box(box_left,box_right)

    def bounding_box(self,tim0,time1):
        return self.box

    def hit(self,ray,start,end,hit_record):
        if not self.box.hit(ray,start,end,hit_record):
            return False
        hit_left = self.left.hit(ray,start,end,hit_record)
        hit_right = self.right.hit(ray,start,hit_record.dist if hit_left else end,hit_record)
        return hit_left or hit_right





