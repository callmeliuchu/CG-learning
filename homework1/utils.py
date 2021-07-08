import math
import random
from vector import Vector3f,dot_product


def random_double():
    return random.uniform(-1,1)




def random_unit_vector():
    return Vector3f(random_double(),random_double(),random_double()).normalize()

def random_in_unit_vector():
    while True:
        v = Vector3f(random_double(),random_double(),random_double())
        if v.length() < 1:
            return v


def reflect(ray_in,normal):
    normal = normal.normalize()
    return ray_in - 2 * ray_in * normal


def refract(ray_in,normal,theta):
    v = -normal.normalize()
    l = dot_product(ray_in,v)
    u = ray_in - l*v
    u = u.normalize()
    cos = dot_product(ray_in.normalize(),v)
    sin = math.sqrt(1-cos*cos)
    sin_t = sin / theta
    cos_t = math.sqrt(1-sin_t*sin_t)
    tan_t = sin_t / cos_t
    return (v + u*tan_t).normalize()

def random_in_unit_disk():
    while True:
        v = Vector3f(random.uniform(-1,1),random.uniform(-1,1),0)
        if v.length() < 1:
            return v