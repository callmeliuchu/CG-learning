from utils import *
from vector import Vector3f as Color
from vector import Vector3f as Point
from vector import Vector3f
import math
from ray import Ray
from hit_list import HitList
from sphere import Sphere


def write_color(color):
    print(int(255*color.x),int(255*color.y),int(255*color.z))


def ray_color(ray,world,depth):
    if depth <= 0:
        return Color(0,0,0)
    hit_record = world.hit(ray,0,100000)
    if hit_record.is_hit:
        u = hit_record.normal
        return 0.5*Color(u.x+1,u.y+1,u.z+1)
    v = ray.direction.normalize()
    t = 0.5*(v.y + 1.0)
    return (1.0 - t) * Vector3f(1.0, 1.0, 1.0) + t * Vector3f(0.5, 0.7, 1.0)


if __name__ == '__main__':
    #image
    aspect_ratio = 16.0 / 9.0
    width = 400
    height = int(width / aspect_ratio)


    #camera
    orig = Point(0,0,0)
    fov = 90
    h = 2*math.tan(math.radians(fov/2))
    w = h*aspect_ratio
    vertical = Vector3f(0,h,0)
    horizontal = Vector3f(w,0,0)
    front = Vector3f(0,0,1)
    lower_left = orig - vertical*0.5 - horizontal*0.5 - front


    #world
    world = HitList()
    sphere1 = Sphere(Point(0, 0, -3),1)
    sphere2 = Sphere(Point(0,-100,-4),100)
    world.add(sphere1)
    # world.add(sphere2)

    depth = 10


    print("P3")
    print(width,height)
    print(255)
    for i in range(height-1,-1,-1):
        for j in range(width):
            u = j /(width-1)
            v = (1.0*i)/ (height-1)
            target = lower_left + u*horizontal + v*vertical
            a_ray = Ray(orig,(target-orig).normalize())
            color = ray_color(a_ray,world,depth)
            write_color(color)
