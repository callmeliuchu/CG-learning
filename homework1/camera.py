from vector import cross
from ray import Ray
import math
from utils import random_in_unit_disk


class Camera:

    def __init__(self,look_from,look_at,vup,aspect_ratio,fov,aperture,focus_dist):
        self.lens_radius = aperture / 2
        self.look_from = look_from
        self.look_at = look_at
        self.vup = vup
        ww = look_from - look_at
        self.ww = ww.normalize()
        self.uu = cross(vup,self.ww)
        self.vv = cross(self.ww,self.uu)
        self.orig = look_from
        self.fov = fov
        self.h = 2 * math.tan(math.radians(fov / 2))
        self.w = self.h * aspect_ratio
        self.vertical = self.vv*self.h*focus_dist
        self.horizontal = self.uu*self.w*focus_dist
        self.front = self.ww*focus_dist
        self.lower_left = self.orig - self.vertical * 0.5 - self.horizontal * 0.5 - self.front

    def get_ray(self,u,v,tm):
        xx = self.lens_radius * random_in_unit_disk()
        offset = self.uu*xx.x + self.vv*xx.y
        return Ray(self.orig + offset,self.lower_left+u*self.horizontal+v*self.vertical-self.orig - offset,tm)