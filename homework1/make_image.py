from utils import *
from vector import Vector3f as Color
from vector import Vector3f as Point
from vector import Vector3f
import math
from ray import Ray
from hit_list import HitList
from sphere import Sphere
from camera import Camera
from material import Lambertian,Metal


def clamp(v,bg,ed):
    if v < bg:
        return bg
    if v > ed:
        return ed
    return v


def write_color(color,sample_per_pix):
    r = color.x
    g = color.y
    b = color.z
    scale = 1/sample_per_pix
    r = r*scale
    g = g*scale
    b = b*scale

    r = math.sqrt(r)
    g = math.sqrt(g)
    b = math.sqrt(b)
    print(int(255*clamp(r,0,0.9999)),int(255*clamp(g,0,0.99)),int(255*clamp(b,0,0.999)))


def ray_color(ray,world,depth):
    if depth <= 0:
        return Color(0,0,0)
    hit_record = world.hit(ray,0.001,100000)
    if hit_record.is_hit:
        hit_record.material.scatter(hit_record)
        if hit_record.can_scatter():
            attenuation = hit_record.attenuation
            return attenuation*ray_color(Ray(hit_record.hit_point,hit_record.out_light_dir),world,depth-1)
    v = ray.direction.normalize()
    t = 0.5*(v.y + 1.0)
    return (1.0 - t) * Vector3f(1.0, 1.0, 1.0) + t * Vector3f(0.5, 0.7, 1.0)


if __name__ == '__main__':
    #image
    aspect_ratio = 16.0 / 9.0
    width = 400
    height = int(width / aspect_ratio)


    #camera
    cam = Camera(aspect_ratio,20)


    #world
    world = HitList()
    lamber1 = Lambertian(Color(0.3,0.4,0.4))
    sphere1 = Sphere(Point(0,0,-1), 0.5,lamber1)
    lamber3 = Metal(Color(0.3,0.8,0.4),0.3)
    sphere3 = Sphere(Point(0.5,0,-1), 0.5,lamber3)
    lamber2 = Metal(Color(0.6, 0.5, 0.3),0.2)
    sphere2 = Sphere(Point(0,-100.5,-1), 100,lamber2)
    world.add(sphere1)
    world.add(sphere2)
    world.add(sphere3)

    depth = 20
    sample_per_pix = 10

    print("P3")
    print(width,height)
    print(255)
    for i in range(height-1,-1,-1):
        for j in range(width):
            color = Color(0,0,0)
            for k in range(sample_per_pix):
                u = (j+random.random())/(width-1)
                v = (i+random.random())/(height-1)
                a_ray = cam.get_ray(u,v)
                color += ray_color(a_ray,world,depth)
            write_color(color,sample_per_pix)
