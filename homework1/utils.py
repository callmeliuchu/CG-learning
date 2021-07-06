import random
from vector import Vector3f


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