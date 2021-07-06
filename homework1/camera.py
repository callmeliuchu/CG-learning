from vector import Vector3f as Point
from vector import Vector3f
from ray import Ray
import math


class Camera:

    def __init__(self,aspect_ratio,fov):
        self.orig = Point(0, 0, 0)
        self.fov = fov
        self.h = 2 * math.tan(math.radians(fov / 2))
        self.w = self.h * aspect_ratio
        self.vertical = Vector3f(0, self.h, 0)
        self.horizontal = Vector3f(self.w, 0, 0)
        self.front = Vector3f(0, 0, 1)
        self.lower_left = self.orig - self.vertical * 0.5 - self.horizontal * 0.5 - self.front

    def get_ray(self,u,v):
        return Ray(self.orig,self.lower_left+u*self.horizontal+v*self.vertical)