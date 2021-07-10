import random

from utils import *
from vector import Vector3f as Color
from vector import Vector3f as Point
from vector import Vector3f
import math
from ray import Ray
from hit_list import HitList
from sphere import Sphere
from camera import Camera
from material import Lambertian,Metal,Dielectric
import sys
from moving_sphere import MovingSphere
from texture import CheckTexture


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
            return attenuation*ray_color(Ray(hit_record.hit_point,hit_record.out_light_dir,ray.tm),world,depth-1)
    v = ray.direction.normalize()
    t = 0.5*(v.y + 1.0)
    return (1.0 - t) * Vector3f(1.0, 1.0, 1.0) + t * Vector3f(0.5, 0.7, 1.0)




def random_scene():
    world = HitList()


    check_texture = CheckTexture(Color(0.2,0.3,0.1),Color(0.9,0.9,0.9))
    ground_material = Lambertian(check_texture)
    world.add(Sphere(Point(0,-1000,0),1000,ground_material))
    for i in range(1,1):
        for j in range(-2,4):
            choose = random.uniform(0,1)
            center = Point(i+0.9*random.uniform(0,1),0.2,j+0.9*random.uniform(0,1))
            if (center - Point(4,0.2,0.2)).length() > 0.9:
                if choose < 0.8:
                    albedo = Color(random.uniform(0.5,1),random.uniform(0.5,1),random.uniform(0.5,1))*\
                    Color(random.uniform(0.5, 1), random.uniform(0.5, 1), random.uniform(0.5, 1))
                    material = Lambertian(albedo)
                    center2 = center + Vector3f(0,random.uniform(0,0.5),0)
                    world.add(MovingSphere(center,center2,0,1,0.2,material))
                elif choose < 0.95:
                    albedo = Color(random.uniform(0.5,1),random.uniform(0.5,1),random.uniform(0.5,1))
                    fuzz = random.uniform(0,0.5)
                    material = Metal(albedo,fuzz)
                    world.add(Sphere(center,0.2,material))
                else:
                    material = Dielectric(1.5)
                    world.add(Sphere(center,0.2,material))
    # material1 = Dielectric(1.5)
    # world.add(Sphere(Point(0,1,0),1.0,material1))
    #
    # material2 = Lambertian(Color(0.4,0.2,0.1))
    # world.add(Sphere(Point(-4,1,0),1.0,material2))
    #
    # material3 = Metal(Color(0.7,0.6,0.5),0.0)
    # world.add(Sphere(Point(4,1,0),1.0,material3))
    return world



if __name__ == '__main__':
    #image
    aspect_ratio = 16.0 / 9.0
    width = 400
    height = int(width / aspect_ratio)


    #camera
    look_from = Point(13,5,3)
    look_at = Point(0,0,0)
    vup = Vector3f(0,1,0)
    dist_to_focus = 10.0
    aperture = 0.1
    cam = Camera(look_from,look_at,vup,aspect_ratio,70,aperture,dist_to_focus)


    #world
    world = random_scene()


    #render
    depth = 20
    sample_per_pix = 10

    print("P3")
    print(width,height)
    print(255)
    for i in range(height-1,-1,-1):
        sys.stderr.write('left {}\n'.format(i))
        sys.stderr.flush()
        for j in range(width):
            color = Color(0,0,0)
            for k in range(sample_per_pix):
                u = (j+random.random())/(width-1)
                v = (i+random.random())/(height-1)
                a_ray = cam.get_ray(u,v,random.uniform(0,1))
                color += ray_color(a_ray,world,depth)
            write_color(color,sample_per_pix)
